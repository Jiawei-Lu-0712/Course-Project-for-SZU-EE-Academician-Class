import cryptography
import base64
from Crypto.Cipher import AES


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

print("请输入短密码：")
short_key = input("")
short_pad_key = pad(short_key)
print(short_pad_key)
private_key = "0x631cfc6ba0604a03d6cfcf1ffa3c6bb9c20ad593469d38fe9f4b7bf26943185f"
aes_key= aes_ECB_Encrypt(private_key, short_pad_key)
print(aes_key)
KEY = aes_ECB_Decrypt(aes_key, short_pad_key)
print(KEY)
# 是否修改密码
print("是否修改密码?")
change = input("")
while change == "Y":
    print("请输入之前的短密码")
    re_key=input("")
    re_pad_key = pad(re_key)
    if aes_ECB_Decrypt(aes_key, re_pad_key):
        while aes_ECB_Decrypt(aes_key,re_pad_key) == private_key:
            print("请输入新的短密码：")
            new_key = input("")
            print("请再次输入：")
            new_key_again = input("")
            if new_key_again == new_key:
                short_key = pad(new_key)
                ase_key = aes_ECB_Encrypt(private_key,short_key)
                print("修改成功！")
                break
            else:
                print("两次密码不一致，请重新输入：")
                continue
        break
    else:
        print("密码错误，请重新输入：")
        continue



# private_key = "0x631cfc6ba0604a03d6cfcf1ffa3c6bb9c20ad593469d38fe9f4b7bf26943185f"
# short_key = "123"
# short_pad_key = pad(short_key)
# KEY = aes_ECB_Encrypt(private_key, short_pad_key)
# print(KEY)
# err_key = "456"
# err_pad_key = pad(err_key)
# if aes_ECB_Decrypt(KEY, err_pad_key):
#     print('密码正确')
# else:
#     print("错误！")
