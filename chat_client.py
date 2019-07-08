"""
chat room  客户端
发送请求，展示结果
"""
from socket import *
import os, sys

# 服务器地址
ADDR = ('127.0.0.1', 9856)


# 发送消息
def send_msg(socket_, name_):
    while True:
        try:
            text = input("Speak:")
        except KeyboardInterrupt:
            text = 'quit'
        if text.strip() == 'quit':
            msg = "Q " + name_
            socket_.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = 'C {} {}'.format(name_, text)
        socket_.sendto(msg.encode(), ADDR)


# 接收消息
def recv_msg(socket_):
    while True:
        try:
            data, addr = socket_.recvfrom(4096)
        except KeyboardInterrupt:
            sys.exit()
        # 从服务器收到EXIT退出
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode() + '\nSpeak:', end='')


# 客户端启动函数
def main():
    socket_ = socket(AF_INET, SOCK_DGRAM)

    # 进入聊天室
    while True:
        name_ = input("请输入姓名:")
        msg = 'L ' + name_
        socket_.sendto(msg.encode(), ADDR)
        # 　接收反馈
        data, addr = socket_.recvfrom(128)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())
    # 已经进入聊天室
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(socket_, name_)  # 子进程负责消息发送
    else:
        recv_msg(socket_)  # 父进程负责消息接收


main()
