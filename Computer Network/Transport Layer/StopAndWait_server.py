import socket
import random

# 设置server
HOST = "172.24.219.249"  # ip
PORT = 12340  # 端口
LOSS_RATE = 0.5  # 预设丢包率

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            data, addr = server_socket.recvfrom(1024)
            if not data:
                break

            packet_number = int(data.decode())
            print(f"Received packet #{packet_number} from {addr}")

            # 模拟丢包
            if random.random() < LOSS_RATE:
                print(f"Packet #{packet_number} lost.")
                continue

            # 发送ack
            ack = f"ACK {packet_number}"
            server_socket.sendto(ack.encode(), addr)
            print(f"Sent: {ack}")

if __name__ == "__main__":
    server()
