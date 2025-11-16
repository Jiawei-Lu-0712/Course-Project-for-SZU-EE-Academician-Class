import socket
import random


def udp_server(host, port, packet_loss_probability=0.1):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"服务器正在监听 {host}:{port}...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"从 {addr} 收到消息：{message}")

        # 模拟丢包，以packet_loss_probability的概率忽略消息
        if random.random() > packet_loss_probability:
            response = f"pong {message}"
            server_socket.sendto(response.encode(), addr)
        else:
            print(f"模拟丢包：忽略来自 {addr} 的消息 {message}")


# 调用函数，这里假设服务器地址为 'localhost'，端口为12345，丢包概率为10%
udp_server('172.24.219.249', 12340, 0.1)
