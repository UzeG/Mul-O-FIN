from threading import Lock


class Sockets:
    def __init__(self):
        self.socket_map = {}  # 创建一个空字典来存储 ID 和 socket 的映射关系
        self.socket_lock = Lock()
        self.start_flag = True

    def add(self, socket_id, socket_obj):
        with self.socket_lock:
            self.socket_map[socket_id] = socket_obj

    def delete(self, socket_id):
        with self.socket_lock:
            if socket_id in self.socket_map:
                del self.socket_map[socket_id]

    def has_device(self, device_id):
        with self.socket_lock:
            return device_id in self.socket_map

    def get_socket(self, device_id):
        with self.socket_lock:
            return self.socket_map.get(device_id, None)

    def get_start_flag(self):
        with self.socket_lock:
            return self.start_flag

    def change_start_flag(self):
        with self.socket_lock:
            self.start_flag = False


sockets = Sockets()
