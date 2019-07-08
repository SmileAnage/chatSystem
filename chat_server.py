"""
chat room
env: python3.6
socket udp & fork
"""

from socket import *
import os, sys

"""
全局变量: 很多封装模块都要用或者有一定的固定含义
"""
# 服务器地址
ADDR = ('0.0.0.0', 9856)

# 存储用户 {name:address}
user = {}


# 登录
def do_login(socket_, name_, addr_):
    if name_ in user or '管理员' in name_:
        socket_.sendto('该用户存在'.encode(), addr_)
        return
    socket_.sendto(b'OK', addr_)  # 可以进入聊天室

    # 通知其他人
    msg = "\n欢迎'{}'进入聊天室".format(name_)
    for i in user:
        socket_.sendto(msg.encode(), user[i])
    user[name_] = addr_  # 插入字典


# 聊天
def do_chat(socket_, name_, text):
    msg = "\n{}: {}".format(name_, text)
    for i in user:
        # 刨除其本人
        if i != name_:
            socket_.sendto(msg.encode(), user[i])


# 退出
def do_quit(socket_, name_):
    msg = "\n{}退出聊天室".format(name_)
    for i in user:
        if i != name_:  # 其他人
            socket_.sendto(msg.encode(), user[i])
        else:
            socket_.sendto(b'EXIT', user[i])
    del user[name_]  # 删除用户


# 　处理请求
def do_request(socket_):
    while True:
        data, addr = socket_.recvfrom(1024)
        tmp = data.decode().split(' ')  # 拆分请求
        # 根据不同的请求类型具体执行不同的事情
        # L 进入　　C 聊天　　Q 退出
        if tmp[0] == 'L':
            do_login(socket_, tmp[1], addr)  # 执行具体工作
        elif tmp[0] == 'C':
            text = ' '.join(tmp[2:])
            do_chat(socket_, tmp[1], text)
        elif tmp[0] == 'Q':
            do_quit(socket_, tmp[1])


# 搭建网络
def main():
    # udp服务端
    socket_ = socket(AF_INET, SOCK_DGRAM)
    socket_.bind(ADDR)

    pid = os.fork()
    if pid == 0:  # 子进程处理管理员消息
        while True:
            msg = input("管理员消息：")
            msg = "C 管理员 " + msg
            socket_.sendto(msg.encode(), ADDR)
    else:
        # 　请求处理函数
        do_request(socket_)


main()
