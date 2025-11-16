import socket

TCP_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

TCP_client.connect(('172.24.219.249',12340))

while 1:
    file_request=input('请输入查询文件：')
    TCP_client.send(file_request.encode('utf-8'))
    back_info=TCP_client.recv(1024).decode('utf-8')
    print(back_info)