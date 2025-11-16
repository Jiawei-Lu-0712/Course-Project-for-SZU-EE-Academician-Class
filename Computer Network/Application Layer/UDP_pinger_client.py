import socket
import datetime

def udp_ping(host, port, num_pings=10):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)  # 设置超时时间为1秒

    for i in range(num_pings):
        send_time = datetime.datetime.now()
        message = f"ping {i+1} {send_time}"
        client_socket.sendto(message.encode(), (host, port))

        try:
            data, _ = client_socket.recvfrom(1024)
            receive_time = datetime.datetime.now()
            rtt = (receive_time - send_time).total_seconds()
            print(f"响应：{data.decode()}，RTT：{rtt:.6f}秒")
        except socket.timeout:
            print("请求超时")

    client_socket.close()

# 调用函数，这里假设服务器地址为'localhost'，端口为25000
udp_ping('172.24.219.249', 12340)
