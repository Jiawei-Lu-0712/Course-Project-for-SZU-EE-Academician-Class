import datetime
import json
import os
import threading
import time
import tkinter as tk
import warnings
from datetime import datetime
from tkinter import messagebox, ttk
from tkinter.ttk import Progressbar
import mnemonic as m
import qrcode
from Crypto.PublicKey import RSA
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus import SimpleDocTemplate, Table
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound
import base64
from Crypto.Cipher import AES

warnings.filterwarnings("default")


class BlockchainWallet:
    """
    钱包主界面
    """

    def __init__(self, master):
        """
        登录以太坊账户界面初始化
        :param master:
        """
        with open('./script/config.json', 'r') as config_file:
            self.config = json.load(config_file)
        self.web3 = Web3(HTTPProvider(self.config['web3ProviderUrl']))
        self.master = master
        self.master.title("以太坊钱包")
        image = Image.open("./assets/Wallet1.PNG")
        photo = ImageTk.PhotoImage(image)
        window_width = 1250
        window_height = 900
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))
        self.master.minsize(window_width, window_height)
        self.master.maxsize(window_width, window_height)
        self.outputimage = tk.Label(self.master)
        self.outputimage.place(x=0, y=0)
        self.outputimage.configure(image=photo)
        self.outputimage.image = photo
        # 添加控件
        self.label_title = tk.Label(self.master)
        self.label_title.grid(row=0, column=1, columnspan=2, padx=0, pady=0)
        self.label_title.configure(bg="white")

        self.label_PriKey = tk.Label(self.master, text="私钥或短密码：", font=("黑体", 20))
        self.label_PriKey.grid(row=2, column=0, sticky="e", padx=50, pady=150)
        self.label_PriKey.configure(bg="white")
        self.entry_PriKey = tk.Entry(self.master, width=50, show="*", font=("黑体", 20), highlightthickness=1,
                                     highlightbackground="black")
        self.entry_PriKey.grid(row=2, column=1, sticky="", padx=0, pady=20)

        self.button_enter = tk.Button(self.master, text="进入钱包", font=("黑体", 20), command=self.goto_Wallet,
                                      bg='#F8EFEF', width=20, height=1)
        self.button_enter.grid(row=6, column=1, sticky="", padx=60, pady=30)

        self.button_create = tk.Button(self.master, text="没有账户？创建账户", font=("黑体", 20),
                                       command=self.goto_CreatWallet, bg='#F8EFEF', width=20, height=1)
        self.button_create.grid(row=7, column=1, sticky="", padx=200, pady=30)

        self.button_exit = tk.Button(self.master, text="退出钱包", font=("黑体", 20),
                                       command=self.exit_app, bg='#F8EFEF', width=20, height=1)
        self.button_exit.grid(row=8, column=1, sticky="", padx=60, pady=30)

    def goto_CreatWallet(self):
        """
        进入以太坊账户创建界面
        """
        self.master.withdraw()  # 隐藏主页窗口
        page1 = tk.Toplevel()  # 进入以太坊账户创建界面
        CreateWalletWindow(page1)


    # def goto_Wallet(self):
    #     """
    #     以太坊账户登录界面
    #     """
    #     if not self.web3.is_connected():  # 判断网络是否连接正常
    #         messagebox.showerror("网络异常", "网络连接异常，请检查网络连接!")
    #         return None
    #
    #     try:
    #         # 从用户输入的私钥中获得以太坊账户，包括公钥和账户地址
    #         account = self.web3.eth.account.from_key(self.entry_PriKey.get())
    #         """
    #         判断用户输入的账户地址格式是否正确，以及用户输入的账户地址和私钥是否匹配
    #         """
    #         if self.web3.to_checksum_address(account.address) == self.web3.to_checksum_address(
    #                 self.entry_address.get()):
    #             # 验证成功，进入账户详细界面
    #             key = self.entry_PriKey.get()
    #             addr = self.entry_address.get()
    #             # addr = self.web3.eth.account.from_key(self.entry_PriKey).address
    #             self.master.withdraw()  # 隐藏主页窗口
    #             page2 = tk.Toplevel()  # 创建账户详细窗口
    #             TransactionWindow(page2, addr, key)  # 将用户输入的账户地址和私钥参数传递给账户详细界面
    #
    #         else:
    #             # 验证失败，错误提示
    #             messagebox.showerror("错误", "账户或私钥错误，请重新输入！")
    #     except:
    #         messagebox.showerror("错误", "账户或私钥错误，请重新输入！")

    def goto_Wallet(self):
        key = self.entry_PriKey.get()
        if len(key) >= 64:
            private_key = key
            accountAddress = self.web3.eth.account.from_key(private_key).address
        else:
            if os.path.exists('./script/encrypted_key.txt'):
                with open('./script/encrypted_key.txt', 'r', encoding='utf-8') as key_file:
                    aes_key = key_file.read()
                    pad_key = pad(key)
                    if aes_ECB_Decrypt(aes_key, pad_key):
                        private_key = aes_ECB_Decrypt(aes_key, pad_key)
                        accountAddress = self.web3.eth.account.from_key(private_key).address
                    else:
                        messagebox.showerror("密码错误", "密码输入错误，请重新输入")
            else:
                messagebox.showerror("找不到文件", "本地未存储！")

        """
        以太坊账户登录界面
        """
        if not self.web3.is_connected():  # 判断网络是否连接正常
            messagebox.showerror("网络异常", "网络连接异常，请检查网络连接!")
            return None

        try:
            """
            判断用户输入的账户地址格式是否正确，以及用户输入的账户地址和私钥是否匹配
            """
            if self.web3.is_address(accountAddress):
                # 验证成功，进入账户详细界面
                key = self.entry_PriKey.get()
                if len(key) >= 64:
                    private_key = key
                else:
                    pad_key = pad(key)
                    private_key = aes_ECB_Decrypt(aes_key, pad_key)
                addr = accountAddress
                self.entry_PriKey.delete(0, tk.END)
                self.master.withdraw()  # 隐藏主页窗口
                page2 = tk.Toplevel()  # 创建账户详细窗口
                TransactionWindow(page2, addr, private_key, key)  # 将用户输入的账户地址和私钥参数传递给账户详细界面
                print('true')


            else:
                # 验证失败，错误提示
                print("错误", "密码或私钥错误，请重新输入！")

        except:
            print("错误", "密码或私钥错误，请重新输入！")



    def exit_app(self):
        """
        退出钱包应用界面
        """
        result = messagebox.askyesno("退出", "确定要退出钱包应用吗？")  # 弹窗提示，确认用户是否确定退出钱包应用
        if result:
            self.master.destroy()  # 销毁界面


class CreateWalletWindow:
    """
    以太坊账户创建界面
    """

    def __init__(self, master):
        """
        界面初始化
        :param master:
        """
        self.label_title = None
        with open('./script/config.json', 'r') as config_file:
            self.config = json.load(config_file)
        self.web3 = Web3(HTTPProvider(self.config['web3ProviderUrl']))
        self.master = master
        self.master.title("以太坊钱包")
        window_width = 1250
        window_height = 900
        image = Image.open("./assets/Wallet2.PNG")
        photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.master, image=photo)
        self.label.place(x=0, y=0)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))
        self.master.minsize(window_width, window_height)
        self.master.maxsize(window_width, window_height)
        self.label_address = tk.Label(self.master, text="账户地址：", font=("黑体", 20))
        self.label_address.grid(row=1, column=0, sticky="", padx=20, pady=20)
        self.label_address.configure(bg='white')
        self.entry_address = tk.Entry(self.master, width=45, font=("黑体", 20), highlightthickness=1,
                                      highlightbackground="black")
        self.entry_address.grid(row=1, column=1, sticky="", padx=20, pady=20)

        self.button_create = tk.Button(self.master, text="创建账户", font=("黑体", 20), command=self.qr_generate,
                                       bg='#F8EFEF')
        self.button_create.grid(row=2, column=0, sticky="W", padx=20, pady=20)
        self.qr_output = tk.Label(self.master)
        self.qr_output.grid(row=3, column=0, columnspan=2)
        self.qr_output.configure(bg="white")
        self.button_exit = tk.Button(self.master, text="返回", font=("黑体", 20), command=self.goto_main,
                                       bg='#F8EFEF')
        self.button_exit.place(x=1160, y=825)
        root.mainloop()

    def goto_main(self):
        """
        退出创建以太坊账户界面
        :return:None
        """
        result = messagebox.askyesno("退出", "确定要退出账户创建吗？")  # 确认用户是否退出账户创建
        if result:
            self.master.destroy()  # 销毁账户创建界面
            main_page.master.deiconify()  # 恢复显示主页窗口


    def qr_generate(self):
        """
        生成账户地址私钥和助记词函数，并将私钥和助记词写入到二维码中
        :return:None
        """

        new_account = self.web3.eth.account.create()  # 创建一个以太坊账户，包含公私钥对
        new_address = new_account.address  # 获取账户地址
        new_private_key = new_account._private_key  # 获取私钥
        mnemonic = m.Mnemonic('english', ).to_mnemonic(new_private_key)  # 通过私钥生成助记词
        self.entry_address.insert(0, new_address)

        data = "地址：" + new_address + '\n' + "私钥:" + new_private_key.hex()[2:] + '\n' + "助记词：" + mnemonic  # 编码的信息
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
        qr.add_data(data)  # 将编码的私钥和助记词写入到二维码中
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")  # 生成二维码图片
        tk_image = ImageTk.PhotoImage(img)
        # 在组件中输出二维码图片
        self.qr_output.configure(image=tk_image)
        self.qr_output.image = tk_image
        self.label_title = tk.Label(self.master,
                                    text="账户创建成功!请扫描二维码获取账户地址、私钥和助记词！",
                                    font=("黑体", 28))
        self.label_title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        self.label_title.configure(bg="white")
        self.button_create = tk.Button(self.master, text="再次创建账户", font=("黑体", 20), command=self.qr_generate,
                                       bg='#F8EFEF')
        self.button_create.grid(row=2, column=0, sticky="W", padx=20, pady=20)


class TransactionWindow:
    """
    以太坊账户地址详细界面
    """

    def __init__(self, master, addr, private_key, key):
        """
        账户界面初始化
        :param master:
        :param addr: 账户地址
        :param private_key: 私钥
        :key：输入的私钥或者短密码
        """

        self.verify_key_entry = None
        self.re_input_key_entry = None
        self.input_key_entry = None
        self.progress_window = None
        with open('./script/config.json', 'r') as config_file:
            self.config = json.load(config_file)
        self.web3 = Web3(HTTPProvider(self.config['web3ProviderUrl']))
        self.master = master
        self.address = addr
        self.privateKey = private_key
        self.key = key
        self.balance_var = tk.StringVar()
        self.master.title("账户信息")
        window_width = 1250
        window_height = 900
        image = Image.open("./assets/Wallet3.PNG")
        photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.master, image=photo)
        self.label.place(x=0, y=0)
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()

        x_pos = int((self.screen_width - window_width) / 2)
        y_pos = int((self.screen_height - window_height) / 2)
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))
        self.master.minsize(window_width, window_height)
        self.master.maxsize(window_width, window_height)
        self.progress_bar = Progressbar(self.master, mode='indeterminate')
        self.label_address = tk.Label(self.master, text="地址：" + str(self.address), font=("黑体", 20))
        self.label_address.grid(row=0, column=1, sticky="W", padx=20, pady=20)
        self.label_address.configure(bg='white')
        self.label_balance = tk.Label(self.master, text="余额：" + str(self.get_balance(self.address)) + " ether",
                                      font=("黑体", 20))
        self.label_balance.grid(row=1, column=1, sticky="W", padx=20, pady=20)
        self.label_balance.configure(bg='white')
        self.label_network = tk.Label(self.master, text="网络：Ganache私链", font=("黑体", 20))
        self.label_network.grid(row=2, column=1, sticky="W", padx=20, pady=20)
        self.label_network.configure(bg='white')

        self.label_receiveAddr = tk.Label(self.master, text="To", font=("黑体", 18))
        self.label_receiveAddr.grid(row=3, column=1, sticky="W", padx=20, pady=18)
        self.label_receiveAddr.configure(bg='white')
        self.entry_receiveAddr = tk.Entry(self.master, width=30, font=("黑体", 18), highlightthickness=1,
                                          highlightbackground="black")
        self.entry_receiveAddr.grid(row=3, column=1, sticky="", padx=20, pady=18)
        self.label_amount = tk.Label(self.master, text="金额(ETH)", font=("黑体", 18))
        self.label_amount.grid(row=4, column=1, sticky="W", padx=20, pady=18)
        self.label_amount.configure(bg='white')
        self.entry_amount = tk.Entry(self.master, width=30, font=("黑体", 18), highlightthickness=1,
                                     highlightbackground="black")
        self.entry_amount.grid(row=4, column=1, sticky="", padx=20, pady=18)

        self.label_data = tk.Label(self.master, text="Data", font=("黑体", 18))
        self.label_data.grid(row=5, column=1, sticky="W", padx=20, pady=18)
        self.label_data.configure(bg='white')
        self.entry_data = tk.Entry(self.master, width=30, font=("黑体", 18), highlightthickness=1,
                                   highlightbackground="black")
        self.entry_data.grid(row=5, column=1, sticky="", padx=20, pady=18)
        self.button_tranfer = tk.Button(self.master, text="转账", font=("黑体", 20),
                                        command=self.send_transaction,
                                        bg='#F8EFEF')
        self.button_tranfer.grid(row=6, column=1, sticky="", padx=20, pady=20)
        self.button_setKey = tk.Button(self.master, text="设置短密码", font=("黑体", 20),
                                       command=self.set_shortKey,
                                       bg='#F8EFEF')
        self.button_setKey.grid(row=6, column=0, sticky="", padx=20, pady=20)
        self.transation_text = tk.Text(self.master, font=("黑体", 18), width=100, height=50)
        self.transation_text.tag_configure("green", foreground="green")
        self.transation_text.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

        # 创建垂直滚动条
        self.scrollbar = tk.Scrollbar(self.master, command=self.transation_text.yview)
        self.scrollbar.grid(row=7, column=2, sticky="ns")

        # 将滚动条与文本框关联
        self.transation_text.config(yscrollcommand=self.scrollbar.set)

        # 设置文本框的网格行和列的拉伸权重
        self.master.grid_rowconfigure(7, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # 设置网格行和列的伸缩性
        self.master.rowconfigure(7, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.button_back = tk.Button(self.master, text="退出", font=("黑体", 20), command=self.goto_main, bg='#F8EFEF')
        self.button_back.grid(row=7, column=1, sticky="SE", padx=20, pady=20)
        self.button_export = tk.Button(self.master, text="导出交易", font=("黑体", 20), command=self.export_receipt,
                                       bg='#F8EFEF')
        self.button_export.grid(row=7, column=0, sticky="SW", padx=20, pady=20)
        self.button_clear_export = tk.Button(self.master, text="清除交易数据", font=("黑体", 20),
                                             command=self.clear_receipt,
                                             bg='#F8EFEF')
        self.button_clear_export.grid(row=7, column=1, sticky="SW", padx=20, pady=20)
        root.mainloop()

    def goto_main(self):
        """
        返回钱包主界面
        :return:
        """
        # result = messagebox.askyesno("退出", "确定要退出您的钱包账户吗？")  # 确认用户是否要退出账户界面，返回钱包主界面
        # if result:
        self.master.destroy()  # 销毁账户界面
        main_page.master.deiconify()  # 显示钱包主界面窗口

    def send_transaction_thread(self):
        """
        生成并发送交易
        :return:
        """
        global privateKey
        result = messagebox.askyesno("交易确认",
                                     "确定要给 " + self.entry_receiveAddr.get() + " 账户转帐 "
                                     + self.entry_amount.get() + "ether吗?")  # 确认用户是否要发送交易

        if result:
            # 发送交易
            try:
                self.show_progress_bar()
                if len(self.privateKey) == 66:
                    privateKey = self.privateKey[2:66]
                # 获取发送方私钥，并将十六进制私钥转换为字节串
                sender_private_key = bytes.fromhex(privateKey)
                # web3.to_checksum_address()会将输入的地址进行大小写混合，并将其转换为以"0x"开头的42个字符的字符串。
                # 其中包含了大小写的混合以及校验和相关的字符。如果输入的地址不是一个有效的以太坊地址，该函数将会抛出异常。
                sender_address = self.web3.to_checksum_address(self.address)  # 获取发送方账户地址，同时会校验和验证账户地址格式是否正确，
                receiver_address = self.web3.to_checksum_address(self.entry_receiveAddr.get())  # 从用户输入框获得交易接收方地址
                data = self.entry_data.get()  # 从用户输入框获取交易中附加的data数据，默认data字段为空
                amount = self.entry_amount.get()  # 从用户输入框获取交易金额，单位为ETH
                nonce = self.web3.eth.get_transaction_count(sender_address)  # 获取当前交易的nonce值
                gas_price = self.web3.eth.gas_price * 3  # 获取gas费，这里为了提高交易被打包上链的速度，将gas费提高了200%
                # 估计这笔交易所需要的汽油单位个数
                gas = self.web3.eth.estimate_gas({
                    'from': sender_address,
                    'to': receiver_address,
                    'value': self.web3.to_wei(amount, 'ether'),
                    'data': data.encode().hex()
                })
                gas *= 1.2  # 为防止汽油单位估计不准确，导致实际交易给的汽油单位不足，交易失败，设置缓冲，将给的汽油单位提高20%
                # 创建一个交易对象，包含交易的所有必要细节，如接收地址、要发送的ETH,gas数量,gas价格，以及要包含在交易中的数据（如果有）
                transaction = {
                    'nonce': nonce,
                    'from': sender_address,
                    'to': receiver_address,
                    'value': self.web3.to_wei(amount, 'ether'),
                    'gas': int(gas),
                    'gasPrice': int(gas_price),
                    'data': data.encode().hex()
                }
                # 对这笔交易用交易发送方的私钥签名，得到已签名的交易对象 signed_tx
                signed_tx = self.web3.eth.account.sign_transaction(transaction, sender_private_key)
                timestamp = time.time()
                # 将时间戳格式化为日期和时间字符串，获取发起交易时的时间戳
                submit_transaction_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

                # signed_tx.rawTransaction是获取已签名的交易的二进制编码，
                # send_raw_transaction()代表将已签名的交易广播到区块链网络中

                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                # 自定义的交易头信息
                transaction_info = "=====================Initiate transaction time:" + submit_transaction_time + \
                                   "=====================" + '\n'

            except Exception as e:
                self.hide_progress_bar()
                # 交易对象创建失败，弹出交易异常提示框
                messagebox.showerror("交易异常", "交易异常，请重新发起交易！" + "异常信息：" + str(e))

                return None
            # 调用update_receipt函数，不断在区块链网络上查询这笔交易是否已经上链，上链则返回交易收据
            receipt = self.update_receipt(tx_hash)
            block_number = receipt['blockNumber']  # 获取交易上链后，交易所在的区块高度
            timestamp = self.web3.eth.get_block(block_number)['timestamp']  # 获取交易被打包上链时的时间戳
            gas_used = receipt['gasUsed']  # 获取交易的gas消耗量
            gas_price = self.web3.eth.get_transaction(tx_hash).gasPrice  # 获取这笔交易实际的gas价格
            percentage_used = "{:.2%}".format(gas_used / gas)  # 计算gas消耗百分比
            transaction_fee = gas_used * gas_price  # 交易费=gas消耗量*单位gas价格
            # 将时间戳从UTC时间转化为北京时间
            timestamp_common = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            # 下面是交易信息汇总
            transaction_info += "Transaction Hash: " + str(
                tx_hash.hex()) + '\n' + "Status: success" + '\n' + "Block number: " \
                                + str(block_number) + '\n' + "Timestamp: " + str(timestamp_common) + '\n' + "From: " + \
                                self.address + '\n' + "To: " + str(self.entry_receiveAddr.get()) + '\n' + "Value: " \
                                + str(self.entry_amount.get()) + '\n' + "Transaction Fee: " + str(
                self.web3.from_wei(transaction_fee, 'ether')) + " ETH" + '\n' + \
                                "Gas Price: " + str(self.web3.from_wei(gas_price, 'gwei')) + " Gwei" + '\n' \
                                + "Gas Limit & Usage by Txn: " + str(int(gas)) + " | " \
                                + str(gas_used) + "(" + str(percentage_used) + ")" + '\n' \
                                + "Nonce:" + str(int(nonce)) +'\n'\
                                +"Input Data: "+ str(self.entry_data.get().encode().hex()) + '\n\n'
            self.hide_progress_bar_txSuccess()
            self.transation_text.insert(tk.END, transaction_info)

        self.label_balance = tk.Label(self.master, text="余额：" + str(self.get_balance(self.address)) + " ether",
                                      font=("黑体", 20))  # 更新交易成功后的账户余额
        self.label_balance.grid(row=1, column=1, sticky="W", padx=20, pady=20)
        self.label_balance.configure(bg='white')

    def show_progress_bar(self):
        self.progress_window = ProgressTransactionWindow(self.master)
        self.progress_window.grab_set()
        self.progress_window.progress_bar.start()

    def hide_progress_bar(self):
        if self.progress_window:
            self.progress_window.progress_bar.stop()
            self.progress_window.destroy()
            self.progress_window = None

    def hide_progress_bar_txSuccess(self):
        if self.progress_window:
            self.progress_window.progress_bar.stop()
            self.progress_window.destroy()
            self.progress_window = None
            messagebox.showinfo("提示", "交易成功！")

    def send_transaction(self):
        send_thread = threading.Thread(target=self.send_transaction_thread)
        send_thread.start()

    def set_shortKey(self):
        """
        设置短密码
        :return:encrypted_key.txt
        """
        if os.path.exists('./script/encrypted_key.txt'):
            shortKey_window = tk.Toplevel(self.master)
            shortKey_window.title("设置短密码")
            window_width = 500
            window_height = 200
            screen_width = shortKey_window.winfo_screenwidth()
            screen_height = shortKey_window.winfo_screenheight()
            x_pos = (screen_width - window_width) // 2
            y_pos = (screen_height - window_height) // 2
            shortKey_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
            label = tk.Label(shortKey_window, text="本地已设置常用账户短密码，是否为本账户？", font=("黑体", 15))
            label.pack(pady=10)
            change_key_button = tk.Button(shortKey_window, text="是，我要修改账户密码", font=("黑体", 13),
                                          command=self.verify_shortKey)
            change_key_button.pack(pady=20)
            reset_key_button = tk.Button(shortKey_window, text="否，我要更换常用账户", font=("黑体", 13),
                                         command=self.set_newKey_button)
            reset_key_button.pack(pady=10)
        else:
            no_shortKey_window = tk.Toplevel(self.master)
            no_shortKey_window.title("设置短密码")
            window_width = 500
            window_height = 130
            screen_width = no_shortKey_window.winfo_screenwidth()
            screen_height = no_shortKey_window.winfo_screenheight()
            x_pos = (screen_width - window_width) // 2
            y_pos = (screen_height - window_height) // 2
            no_shortKey_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
            label = tk.Label(no_shortKey_window, text="本地未设置常用账户，是否将本账户设置为常用账户？",
                             font=("黑体", 15))
            label.grid(row=1, column=0, padx=10, pady=20)
            close_button = tk.Button(no_shortKey_window, text="确定", font=("黑体", 15), command=self.set_newKey_button)
            close_button.grid(row=2, column=0, padx=10, pady=10)

    def verify_shortKey(self):
        verify_shortKey_window = tk.Toplevel(self.master)
        verify_shortKey_window.title("验证短密码")
        window_width = 600
        window_height = 100
        screen_width = verify_shortKey_window.winfo_screenwidth()
        screen_height = verify_shortKey_window.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        verify_shortKey_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        label_verify = tk.Label(verify_shortKey_window, text="请输入本账户短密码：",
                                font=("黑体", 15))
        label_verify.grid(row=1, column=0, padx=10, pady=10)
        self.verify_key_entry = tk.Entry(verify_shortKey_window, width=20, show="*", font=("黑体", 15),
                                         highlightthickness=1,
                                         highlightbackground="black")
        self.verify_key_entry.grid(row=1, column=1, padx=10, pady=10)
        verify_button = tk.Button(verify_shortKey_window, text="确认", font=("黑体", 15),
                                  command=self.verify_key_button)
        verify_button.grid(row=1, column=3, padx=10, pady=10, sticky="")

    def verify_key_button(self):
        verify_key = self.verify_key_entry.get()
        if verify_key == "":
            messagebox.showerror("输入错误", "密码为空，请重新输入！")
        else:
            with open('./script/encrypted_key.txt', 'r', encoding='utf-8') as key_file:
                aes_key = key_file.read()
                pad_verify_key = pad(verify_key)
                if aes_ECB_Decrypt(aes_key, pad_verify_key):
                    self.set_newKey_button()
                else:
                    messagebox.showerror("密码错误", "密码输入错误，请重新输入!")
                    self.verify_key_entry.delete(0, tk.END)

    def set_newKey_button(self):
        set_newKey_window = tk.Toplevel(self.master)
        set_newKey_window.title("设置短密码")
        window_width = 500
        window_height = 150
        screen_width = set_newKey_window.winfo_screenwidth()
        screen_height = set_newKey_window.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        set_newKey_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        label1 = tk.Label(set_newKey_window, text="请输入短密码：",
                          font=("黑体", 15))
        label1.grid(row=1, column=0, padx=10, pady=10)
        self.input_key_entry = tk.Entry(set_newKey_window, width=30, show="*", font=("黑体", 15), highlightthickness=1,
                                        highlightbackground="black")
        self.input_key_entry.grid(row=1, column=1, padx=10, pady=10)
        label2 = tk.Label(set_newKey_window, text="请再次输入：", font=("黑体", 15))
        label2.grid(row=2, column=0, padx=10, pady=10)
        self.re_input_key_entry = tk.Entry(set_newKey_window, width=30, show="*", font=("黑体", 15),
                                           highlightthickness=1,
                                           highlightbackground="black")
        self.re_input_key_entry.grid(row=2, column=1, padx=10, pady=10)
        set_button = tk.Button(set_newKey_window, text="确认修改", font=("黑体", 15), command=self.set_newKey)
        set_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

    def set_newKey(self):
        input_key = self.input_key_entry.get()
        re_input_key = self.re_input_key_entry.get()
        if input_key == "" or re_input_key == "":
            messagebox.showerror("输入错误", "密码为空，请重新输入！")
        else:
            if input_key == re_input_key:
                pad_input_key = pad(input_key)
                cache_key = aes_ECB_Encrypt(self.priviateKey, pad_input_key)
                with open('./script/encrypted_key.txt', 'w', encoding='utf-8') as key_file:
                    key_file.write(cache_key)
                messagebox.showinfo(title="更改成功", message="设置成功！请重新登录！", command=self.goto_main())
            else:
                messagebox.showerror("输入错误", "两次密码不一致，请重新输入！")
                self.input_key_entry.delete(0, tk.END)
                self.re_input_key_entry.delete(0, tk.END)

    def get_balance(self, address):
        """
        获取以太坊账户余额
        :param address: 账户地址
        :return:余额
        """
        balance_wei = self.web3.eth.get_balance(address)
        balance = self.web3.from_wei(balance_wei, 'ether')
        return balance

    def export_receipt(self):
        """
        导出交易收据,每次最多能导出4笔交易
        :return:None
        """

        result = messagebox.askyesno("导出交易", "确定要导出您当前的交易记录吗？")
        if result:
            try:
                timestamp = time.time()
                receipt_info = self.transation_text.get("1.0", tk.END)
                file_name = str(datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d-%H-%M-%S")) + "receipt.pdf"
                folder_path = "transaction_history"
                file_path = os.path.join(folder_path, file_name)
                # 确保文件夹路径存在，并具有写入权限
                if not os.path.exists(folder_path):  # 没有这个文件夹则自动创建，用于保存交易历史收据
                    os.makedirs(folder_path)
                receipt_pdf = SimpleDocTemplate(file_path, pagesize=A4, topMargin=20)
                elements = []
                title_style = ParagraphStyle(
                    "Title",
                    fontSize=20,
                    leading=10,
                    alignment=1,  # 居中对齐
                    fontName="Times-Bold",
                )
                title = Paragraph("transaction history", title_style)
                elements.append(title)
                elements.append(Spacer(1, 30))
                elements.append(
                    Table([[receipt_info]], colWidths=receipt_pdf.width, rowHeights=[None]))
                receipt_pdf.build(elements)
            except Exception as e:
                # 导出异常，弹出异常提示框
                messagebox.showerror("失败", "交易导出失败，请重试！" + " 异常信息:" + str(e))
                return None
            messagebox.showinfo("导出成功", "交易导出成功！交易已导入到 " + file_path + " 文件中！")  # 导出成功

    def clear_receipt(self):
        self.transation_text.delete(1.0, tk.END)

    def update_receipt(self, tx_hash, interval=3):
        """
        更新交易收据，直到交易上链为止
        :param tx_hash: 交易哈希
        :param interval: 查询时间间隔，默认为3秒
        :return: 交易收据
        """

        receipt = None

        while receipt is None:
            try:
                # 通过交易哈希去区块链网络上查询交易是否上链，
                # 如果上链则返回交易收据receipt
                receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                if receipt is not None and receipt['status']:  # receipt不为空且'status'为1表示交易成功上链
                    return receipt  # 返回交易收据
            except TransactionNotFound:

                pass
            time.sleep(interval)


class ProgressTransactionWindow(tk.Toplevel):
    """
    交易等待处理中界面
    """

    def __init__(self, master):
        super().__init__(master)
        self.title("交易处理")
        self.resizable(False, False)  # 固定界面大小
        # 设置固定的界面的大小
        self.geometry("400x100")
        # 界面居中于屏幕
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2)
        self.geometry("+{}+{}".format(position_right, position_down))
        self.protocol("WM_DELETE_WINDOW", self.do_nothing)  # 禁止强行关闭进度条
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)

        self.label = tk.Label(self, text="交易正在处理，请稍后...", font=("黑体", 16))
        self.label.pack(pady=10)

    def do_nothing(self):
        pass


def pad(data):
    text = data + chr(16 - len(data) % 16) * (16 - len(data) % 16)
    return text


def unpad(s):
    last_num = s[-1]
    text = s[:-last_num]
    return text


def aes_ECB_Encrypt(data, key):  # ECB模式的加密函数，data为明文，key为16字节密钥
    key = key.encode('utf-8')
    data = pad(data)  # 补位
    data = data.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_ECB)  # 创建加密对象
    # encrypt AES加密  B64encode为base64转二进制编码
    result = base64.b64encode(aes.encrypt(data))
    return str(result, 'utf-8')  # 以字符串的形式返回


def aes_ECB_Decrypt(data, key):  # ECB模式的解密函数，data为密文，key为16字节密钥
    key = key.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_ECB)  # 创建解密对象
    # decrypt AES解密  B64decode为base64 转码
    result = aes.decrypt(base64.b64decode(data))  # 对密文数据进行预处理，过滤掉或替换掉无效的字节
    result = unpad(result)  # 除去补16字节的多余字符
    try:
        return str(result, 'utf-8')  # 以字符串的形式返回
    except ValueError as e:
        print("Decryption failed:", e)


if __name__ == "__main__":
    root = tk.Tk()
    main_page = BlockchainWallet(root)
    root.mainloop()
