from threading import Lock

sockets = []


class Sockets:
    def __init__(self):
        self.socket_map = {}  # 创建一个空字典来存储 ID 和 socket 的映射关系
        self.socket_lock = Lock()
