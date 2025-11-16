from web3 import Web3,  HTTPProvider
import json

with open('./script/config.json', 'r') as config_file:
    config = json.load(config_file)

web3 = Web3(HTTPProvider(config['web3ProviderUrl']))

address = '0x090cb34CC4B2d804EE23669dbB172f9008cb37D9'

# privateKey = '0xf7d20e5d3493a60406cda99533ea80095799be190c679363184b987de7fdd162'

print('是否连接到以太坊网络：', web3.is_connected())

# print(web3.to_checksum_address(address))
#
# print(bytes.fromhex(privateKey))

print('账户余额：', web3.eth.get_balance(address) / (10 ** 18))
