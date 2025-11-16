import socket
import time
from datetime import datetime

# 设置client
HOST = "172.24.219.249"
PORT = 12340
TIMEOUT = 1  # 超时
NUM_PACKETS = 100  # 设置总packet数

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(TIMEOUT)

        total_sent_packets = 0  # 初始化总发包数，用于计算丢包率，每发一次包就加1（包括丢包的那次发包）
        lost_packets = 0  # 初始化总丢包数，用于计算丢包率，后续for循环中每丢包一次，lost_packets加1
        total_rtt = []  # 储存rtt值到数组

        start_time = time.time()  # 传输的初始时间

        for packet_number in range(1, NUM_PACKETS + 1):
            message = str(packet_number).encode()
            ack_received = False  # 检查是否收到ack

            while not ack_received:
                try:
                    send_time = datetime.now()  # 记录发送时间
                    client_socket.sendto(message, (HOST, PORT))  # 发包
                    total_sent_packets += 1
                    print(f"Sent packet #{packet_number} (Attempt {total_sent_packets})")

                    # 等待ack
                    ack, _ = client_socket.recvfrom(1024)  # 接收ack
                    recv_time = datetime.now()  # 记录接收时间
                    print(f"Received: {ack.decode()}")

                    # 计算rtt
                    rtt = (recv_time - send_time).total_seconds()
                    total_rtt.append(rtt)

                    # 标记此包为已确认
                    ack_received = True

                except socket.timeout:
                    # 发生超时丢包数加1
                    lost_packets += 1
                    print(f"Timeout on packet #{packet_number}, resending...")

        end_time = time.time()  # 传输的结束时间

        # 计算
        total_time = end_time - start_time  # 计算总传输时间
        avg_rtt = sum(total_rtt) / len(total_rtt) if total_rtt else 0  # 计算平均rtt
        packet_loss_rate = lost_packets / total_sent_packets  # 计算丢包率

        # 打印数据
        print("\nStatistics:")
        print(f"  Unique packets to send: {NUM_PACKETS}")
        print(f"  Total packets sent (including retransmissions): {total_sent_packets}")
        print(f"  Packets retransmitted (lost): {lost_packets}")
        print(f"  Packet loss rate: {packet_loss_rate:.2%}")
        print(f"  Total time: {total_time:.2f} seconds")
        print(f"  Average RTT: {avg_rtt:.4f} seconds")

if __name__ == "__main__":
    client()
