from heapq import nlargest
from threading import Lock
import time


class Congestion:
    def __init__(self):
        self.timeline = []
        self.timeline_lock = Lock()

    def add_timeline(self):
        with self.timeline_lock:
            self.timeline.append(time.time())

    def clear(self):
        with self.timeline_lock:
            self.timeline.clear()

    def find_largest(self, n):
        with self.timeline_lock:
            if len(self.timeline) < n:
                return self.timeline
            else:
                return nlargest(n, self.timeline)

    def congestion_control(self, t, n):
        largest_n = self.find_largest(n)
        current_time = time.time()  # 获取当前时间戳
        within_minutes = [ts for ts in largest_n if current_time - ts <= t]
        return within_minutes
