from heapq import heappush, heappop

from time import monotonic


class TimeQueue:
    def __init__(self):
        self.near = []

    def push(self, item, expires=0):
        now = monotonic()
        when = now + expires
        heappush(self.near, (when, item))

    def qsize(self):
        return len(self.near)

    def deadline(self):
        if self.near:
            return self.near[0][0] - monotonic()

    def pop(self):
        return heappop(self.near)
