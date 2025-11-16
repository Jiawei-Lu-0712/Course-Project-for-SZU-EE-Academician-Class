import socket

TCP_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 创建文件目录
file_content=['Chinese','Math','English','Music']

# 建立连接
TCP_server.bind(('172.24.219.249',12340)) # 不同设备运行时要换IP和端口号

# 设置监听
TCP_server.listen(5)

#设置阻塞
info,addr=TCP_server.accept()

while 1:
    file_request=info.recv(1024)

    print('收到客户请求文件：' + file_request.decode('utf-8'))

    if file_request.decode('utf-8') in file_content:
        info.send(file_request)
        print('exsist')
    else:
        info.send('error'.encode('utf-8'))
        print('error')