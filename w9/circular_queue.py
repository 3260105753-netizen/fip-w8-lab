"""项目 A · 循环队列核心代码（与课件骨架一致）

用定长数组 + 取模把队列"弯"成环，用 count 区分空和满。
"""


class CircularQueue:
    def __init__(self, capacity=5):
        self.items = [None] * capacity
        self.capacity = capacity
        self.front = self.rear = 0
        self.count = 0

    def enqueue(self, x):
        if self.count == self.capacity:
            return                          # 满
        self.items[self.rear] = x
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None                     # 空
        x = self.items[self.front]
        self.items[self.front] = None       # 断开引用
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return x


def show_trace(capacity=4):
    """题面第 2 题：打印每一步的 front / rear / count 和数组内容。"""
    q = CircularQueue(capacity)
    log = []

    def snap(op):
        log.append(f"| {op} | {q.front} | {q.rear} | {q.count} | {q.items} |")

    snap("初始")
    q.enqueue(1); snap("enqueue(1)")
    q.enqueue(2); snap("enqueue(2)")
    q.dequeue();  snap("dequeue()")
    q.enqueue(3); snap("enqueue(3)")
    q.enqueue(4); snap("enqueue(4)")
    q.enqueue(5); snap("enqueue(5)")
    q.enqueue(6); snap("enqueue(6) 拒绝")

    print("| 操作 | front | rear | count | 数组内容 |")
    print("|---|---|---|---|---|")
    print("\n".join(log))


if __name__ == "__main__":
    show_trace()
