/*
* @作者：周志贤
* @日期：2024/04/28
* @修改：2024/10/18
* @修改：2024/11/14
*/

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// 导入ERC721.sol文件。
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract MyNFT is ERC721 {
    // tokenId计数器
    uint public tokenIdCounter;

    // 合约拥有者，immutable：只允许在constructor中被更改一次。
    address public immutable owner;

    // 若authorized[address]=true，则说明该地址为被授权地址。
    mapping(address => bool) public authorized;

    // 记录已铸造的所有NFT的tokenId列表
    uint[] public tokenIdList;

    // 记录正在拍卖的NFT的列表
    uint[] public auctionNFTList;

    // 储存NFT对应的tokenId和拥有者
    struct FromTokenIdGetNFTData {
        // NFT的tokenId
        uint tokenId;
        // 该NFT的拥有者。
        address Owner;
    }
    // 通过NFT的tokenId来记录或查询NFT的数据
    mapping(uint => FromTokenIdGetNFTData) public fromTokenIdGetNFTData;

    // 记录或查询对应地址下的所有tokenId
    mapping(address => uint[]) public tokenIdListOfAccount;

    // NFT对应的拍卖信息
    struct NFTAuctionInfo {
        // 拍卖受益人
        address payable beneficiary;
        // 竞价者列表
        address[] bidder;
        // 拍卖结束时间
        uint auctionEndTime;
        // 起拍价
        uint bottomPrice;
        // 最高出价者
        address highestBidder;
        // 最高出价
        uint highestBid;
        // 每个地址的待退款金额
        mapping(address => uint) pendingReturns;
        // 是否正在拍卖
        bool isAuction;
        // 拍卖是否结束
        bool ended;
    }
    // 通过NFT的tokenId来记录或查询NFT的拍卖数据
    mapping(uint => NFTAuctionInfo) public nftAuctionInfo;


    // NFT转移事件
    event TransferNFT(address _from, address _to, uint _tokenId);

    // NFT拍卖开始事件
    event AuctionStart(uint _token, uint _bottomPrice, uint _auctionEndTime);

    // 最高出价更新事件
    event HighestBidRefresh(uint _tokenId, uint _highestBid, address _highestBidder);

    // 撤回出价事件
    event BidWithdraw(uint _tokenId, address _bidder, uint _bidAmount);

    // 拍卖结束事件
    event AuctionEnded(uint256 _tokenId, address _winner, uint256 _highestBid);


    // 修饰函数，仅管理员
    modifier onlyAdmin() {
        require(authorized[msg.sender] == true, "Only Admin can call this function");
        _;
    }

    // 修饰函数，仅普通用户
    modifier onlyRegularUser() {
        require(msg.sender != owner && authorized[msg.sender] == false, "Only regular user can all this function");
        _;
    }


    // 部署合约时触发的构造函数
    constructor(string memory _name, string memory _symbol) ERC721(_name, _symbol) {
        // 将部署智能合约的以太坊地址置为智能合约的拥有者
        owner = msg.sender;

        // 设置管理员权限
        authorized[owner] = true;

        // 初始化tokenId
        tokenIdCounter = 1;
    }


    /*
     * @功能：铸造 ERC-721 代币（NFT），仅管理员可调用该函数
     * @参数（_to）：NFT 接收者的以太坊地址
     * @事件：TransferNFT
     */
    function mintERC721Token(address _to) public onlyAdmin {
        // 新的NFT的tokenId
        uint256 newTokenId = tokenIdCounter;

        // 调用ERC721.sol中的_mint函数，铸造NFT。
        _mint(_to, newTokenId);

        // 更新tokenIdCounter的值，为铸造下一个NFT做准备。
        tokenIdCounter ++;

        // 更新结构体FromTokenIdGetNFTData中对应的NFT的数据。
        fromTokenIdGetNFTData[newTokenId].tokenId = newTokenId;
        fromTokenIdGetNFTData[newTokenId].Owner = msg.sender;

        // 将新铸造的NFT的tokenId加入到该地址下的tokenIdListOfAccount中。
        tokenIdListOfAccount[_to].push(newTokenId);

        // 将该NFT的tokenId加入到tokenIdList中。
        tokenIdList.push(newTokenId);

        // 发送NFT铸造事件
        emit TransferNFT(address(0), _to, newTokenId);
    }

    /*
    * @功能：转移ERC-721代币，仅管理员可调用该函数
    * @参数（_to）：接收者地址
    * @参数（_tokenId）：要转移的NFT的tokenId
    * @事件：TransferNFT
    */
    function transferERC721Token(address _to, uint _tokenId) public onlyAdmin {
        // 转移NFT的前提是需要拥有该NFT。
        require(msg.sender == ownerOf(_tokenId), "Caller is not the owner of the NFT!");

        // 调用ERC721.sol中的 _transfer函数，转移NFT。
        _transfer(msg.sender, _to, _tokenId);

        // 将该NFT的tokenId从发送者的tokenIdListOfAccount中删除。
        removeItemFromTokenIdListOfAccount(_tokenId, msg.sender);

        // 将该NFT的tokenId从可用于拍卖的NFT列表中删除。
        removeItemFromAuctionNFTList(_tokenId);

        // 将该NFT的tokenId添加到接收者的tokenIdListOfAccount中。
        tokenIdListOfAccount[_to].push(_tokenId);

        // 更新该NFT的拍卖信息。
        nftAuctionInfo[_tokenId].isAuction = false;
        nftAuctionInfo[_tokenId].ended = true;

        // 发送NFT转移事件
        emit TransferNFT(msg.sender, _to, _tokenId);
    }

    /*
    * @功能：转移ETH
    * @参数（recipient）：接收者的以太坊地址
    * @参数（amount）：代币数量
    */
    function transferETH(address payable recipient, uint amount) public {
        recipient.transfer(amount);
    }

    /*
    * @功能：开始NFT拍卖
    * @参数（_tokenId）：用于拍卖的NFT的ID
    * @参数（_biddingDuration）：拍卖持续时间
    * @参数（_beneficiary）：受益人
    * @参数（_bottomPrice）：底价
    * @事件：AuctionStart
    */
    function startAuction(
        uint _tokenId,
        uint _biddingDuration,
        address payable _beneficiary,
        uint _bottomPrice
    ) public onlyAdmin {
        // 开始拍卖之前，对应NFT的拍卖结束时间必须为0
        require(nftAuctionInfo[_tokenId].auctionEndTime == 0, "Auction for this NFT is already in progress");

        // 写入拍卖信息
        nftAuctionInfo[_tokenId].auctionEndTime = block.timestamp + _biddingDuration;
        nftAuctionInfo[_tokenId].beneficiary = _beneficiary;
        nftAuctionInfo[_tokenId].bottomPrice = _bottomPrice;
        nftAuctionInfo[_tokenId].isAuction = true;
        nftAuctionInfo[_tokenId].ended = false;
        auctionNFTList.push(_tokenId);

        // 发送拍卖开始事件
        emit AuctionStart(_tokenId, _bottomPrice, nftAuctionInfo[_tokenId].auctionEndTime);
    }

    /*
    * @功能：出价
    * @参数（_tokenId）：出价对应的NFT的ID
    * @事件：HighestBidRefresh
    */
    function bid(uint _tokenId) public payable onlyRegularUser {
        // 出价时，当前的时间必须小于拍卖结束时间
        require(block.timestamp <= nftAuctionInfo[_tokenId].auctionEndTime, "Auction already ended.");

        // 出价时，对应的NFT需要处于正在拍卖状态
        require(nftAuctionInfo[_tokenId].isAuction == true, "The auction for this NFT has not started yet.");
        require(nftAuctionInfo[_tokenId].ended == false, "The auction for this NFT has ended.");

        // 获取最高出价者的信息
        address highestBidder = nftAuctionInfo[_tokenId].highestBidder;
        uint highestBid = nftAuctionInfo[_tokenId].highestBid;

        // 出价者不能为当前的最高出价者
        require(msg.sender != highestBidder, "You are the highest bidder!");

        // 更新上一个最高出价者的待退款金额
        nftAuctionInfo[_tokenId].pendingReturns[highestBidder] = highestBid;

        // 将当前的出价者添加到竞价者名单内
        if(nftAuctionInfo[_tokenId].pendingReturns[msg.sender] == 0) {
            nftAuctionInfo[_tokenId].bidder.push(msg.sender);
        }

        // 更新当前最高出价
        nftAuctionInfo[_tokenId].highestBid = msg.value + nftAuctionInfo[_tokenId].pendingReturns[msg.sender];

        // 将当前最高出价者的待退款金额置为0
        nftAuctionInfo[_tokenId].pendingReturns[msg.sender] = 0;

        // 更新当前的最高出价者
        nftAuctionInfo[_tokenId].highestBidder = msg.sender;

        // 发送最高出价更新事件
        emit HighestBidRefresh(_tokenId, nftAuctionInfo[_tokenId].highestBid, msg.sender);
    }

    /*
    * @功能：撤回出价
    * @参数（_tokenId）：出价对应的NFT的Token ID
    * @事件：BidWithdraw
    */
    function withdraw(uint _tokenId) public onlyRegularUser returns(bool) {
        // 撤回出价的用户不能为最高出价者
        require(msg.sender != nftAuctionInfo[_tokenId].highestBidder, "You are the highest bidder and can't withdraw your bid.");

        // 获取待退款金额
        uint refundAmount = nftAuctionInfo[_tokenId].pendingReturns[msg.sender];

        if (refundAmount > 0) {
            // 调用transferETH()将待退款金额返还给用户
            transferETH(payable(msg.sender), refundAmount);

            // 将该用户的待退款金额置为0
            nftAuctionInfo[_tokenId].pendingReturns[msg.sender] = 0;

            // 发送撤回出价事件
            emit BidWithdraw(_tokenId, msg.sender, refundAmount);
        }
        return true;
    }

    /*
    * @功能：结束拍卖
    * @参数（_tokenId）：对应的NFT的ID
    * @事件：AuctionEnded、BidWithdraw
    */
    function endAuction(uint _tokenId) public onlyAdmin {
        // 结束拍卖时，当前时间大于拍卖结束时间
        require(block.timestamp >= nftAuctionInfo[_tokenId].auctionEndTime, "This auction has not yet ended.");
        require(nftAuctionInfo[_tokenId].auctionEndTime != 0, "The auction has not started yet.");
        require(nftAuctionInfo[_tokenId].ended == false, "This auction is already been ended.");
        require(nftAuctionInfo[_tokenId].isAuction == true, "This auction is already been ended.");

        // 调用该函数的用户需要拥有该NFT
        require(ownerOf(_tokenId) == msg.sender, "Only the owner of the NFT can end the auction.");

        // 发送拍卖结束事件
        emit AuctionEnded(_tokenId, nftAuctionInfo[_tokenId].highestBidder, nftAuctionInfo[_tokenId].highestBid);

        // 将待退款金额退还给用户
        for (uint i = 0; i < nftAuctionInfo[_tokenId].bidder.length; i++) {
            if (nftAuctionInfo[_tokenId].bidder[i] != nftAuctionInfo[_tokenId].highestBidder) {
                address payable bidder = payable(nftAuctionInfo[_tokenId].bidder[i]);
                uint refundAmount = nftAuctionInfo[_tokenId].pendingReturns[bidder];

                if (refundAmount > 0) {
                    transferETH(bidder, refundAmount);
                    nftAuctionInfo[_tokenId].pendingReturns[bidder] = 0;

                    // 发送撤回出价事件
                    emit BidWithdraw(_tokenId, bidder, refundAmount);
                }
            }
        }

        // 若最高出价者的地址不为0地址。
        if (nftAuctionInfo[_tokenId].highestBidder != address(0)) {
            // 若最高出价大于0
            if (nftAuctionInfo[_tokenId].highestBid > 0) {
                // 将最高出价对应的金额发送给受益人
                transferETH(nftAuctionInfo[_tokenId].beneficiary, nftAuctionInfo[_tokenId].highestBid);
                // 将对应的NFT发送给最高出价者
                transferERC721Token(nftAuctionInfo[_tokenId].highestBidder, _tokenId);
            }
        }
        // 若最高出价者地址为0地址，即无人出价。
        else {
            removeItemFromAuctionNFTList(_tokenId);

            nftAuctionInfo[_tokenId].ended = false;
            nftAuctionInfo[_tokenId].isAuction = false;
        }

        // 重置该NFT的拍卖信息
        nftAuctionInfo[_tokenId].highestBidder = address(0);
        nftAuctionInfo[_tokenId].beneficiary = payable(address(0));
        nftAuctionInfo[_tokenId].highestBid = 0;
        nftAuctionInfo[_tokenId].auctionEndTime = 0;
        nftAuctionInfo[_tokenId].bottomPrice = 0;
    }

    /*
    * @功能：查询正在拍卖的NFT的tokenId
    * @返回：正在拍卖的NFT的tokenId
    */
    function getAuctionNFTList() public view returns(uint[] memory) {
        return auctionNFTList;
    }

    /*
    * @功能：查询竞价者列表
    * @返回：对应的NFT的竞价者列表
    */
    function getBidderList(uint _tokenId) public view returns(address[] memory) {
        return nftAuctionInfo[_tokenId].bidder;
    }

    /*
    * @功能：查询待退款金额
    * @返回：对应的待退款金额
    */
    function getPendingReturns(uint _tokenId, address _address) public view returns(uint) {
        return nftAuctionInfo[_tokenId].pendingReturns[_address];
    }
    
    /*
    * @功能：查询NFT的拥有者
    * @参数（_tokenId）：要查询的NFT的tokenId
    * @返回：NFT拥有者的以太坊地址
    */
    function ownerOfNFT(uint _tokenId) public view returns(address) {
        // 调用ERC721.sol中的 ownerOf函数，查询NFT的拥有者。
        return ownerOf(_tokenId);
    }

    /*
    * @功能：查询以太坊地址下的所有NFT的tokenId
    * @参数（_address）：要查询的以太坊地址
    * @返回：该地址下所拥有的NFT的tokenId
    */
    function getAccountNFTInfo(address _address) public view returns(uint[] memory) {
        return tokenIdListOfAccount[_address];
    }

    /*
    * @功能：删除数组中的指定元素
    * @参数（_value）：需要删除的元素
    * @参数（_address）：以太坊地址
    */
    function removeItemFromTokenIdListOfAccount(uint _value, address _address) public {
        for (uint i = 0; i < tokenIdListOfAccount[_address].length; i++) {
            if (tokenIdListOfAccount[_address][i] == _value) {
                for (uint j = i; j < tokenIdListOfAccount[_address].length - 1; j++) {
                    tokenIdListOfAccount[_address][j] = tokenIdListOfAccount[_address][j + 1];
                }
                tokenIdListOfAccount[_address].pop();
            }
        }
    }

    /*
    * @功能：删除数组中的指定元素
    * @参数（_value）：需要删除的元素
    */
    function removeItemFromAuctionNFTList(uint _value) public {
        for (uint i = 0; i < auctionNFTList.length; i++) {
            if (auctionNFTList[i] == _value) {
                for (uint j = i; j < auctionNFTList.length - 1; j++) {
                    auctionNFTList[j] = auctionNFTList[j + 1];
                }
                auctionNFTList.pop();
            }
        }
    }
}