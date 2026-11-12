# 项目 A · 循环队列实现与状态追踪

第九周研讨课二 · 二选一（本组选 A）

## 一、背景

用固定大小数组实现队列时，队尾指针到达数组末尾会导致"假溢出"：前面明明有空位，却无法再入队。循环队列用取模运算让指针绕回数组开头，把这些空位重新利用起来。

## 二、选择说明（一句话）

选 A：取模绕回是数组实现里最容易出错、又最容易用 `front/rear/count` 逐步验证的细节，比 B 更多依赖标准库的堆操作更能体现"自己实现"的部分。

## 三、反思（1–2 句）

绕回让我理解了空间复用：数组物理上是连成一圈的，"队尾"只是 `(rear + 1) % capacity` 算出来的下一个写入位置，出队腾出的格子会被下一次入队立刻重用，所以定长缓冲区不用搬移任何元素就能持续工作。这也解释了"假溢出"的成因——不是没空间，而是指针不敢回头。

## 四、文件结构

```
w9/
├── circular_queue.py        # 核心代码（20 行）+ 状态追踪打印
├── test_circular_queue.py   # 单元测试（5 个用例）
└── README.md                # 本文件
```

## 五、核心代码（题面第 1 题）

```python
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
```

三个要点：

1. **判满用 `count == capacity`**，不是 `front == rear`——队满时两个指针也会重合，光看指针分不出满和空；
2. **`rear` 和 `front` 各自独立绕回**，入队只动 rear、出队只动 front，永远不搬移元素；
3. **出队后把槽位置 `None`**，否则被出队的对象仍被 `items` 引用着，程序长跑会泄漏内存。

## 六、状态追踪（题面第 2 题）

`capacity=4`，依次执行 `enqueue(1)`、`enqueue(2)`、`dequeue()`、`enqueue(3)`、`enqueue(4)`、`enqueue(5)`、`enqueue(6)`：

| 操作 | front | rear | count | 数组内容 / 结果 |
|---|---|---|---|---|
| 初始 | 0 | 0 | 0 | `[None, None, None, None]` |
| enqueue(1) | 0 | 1 | 1 | `[1, None, None, None]` |
| enqueue(2) | 0 | 2 | 2 | `[1, 2, None, None]` |
| dequeue() | 1 | 2 | 1 | `[None, 2, None, None]` |
| enqueue(3) | 1 | 3 | 2 | `[None, 2, 3, None]` |
| enqueue(4) | 1 | **0** | 3 | `[None, 2, 3, 4]` |
| enqueue(5) | 1 | 1 | 4 | `[5, 2, 3, 4]` |
| enqueue(6)（验证） | 1 | 1 | 4 | 拒绝入队（`count == capacity`），状态不变 |

两个关键观察：

- **`enqueue(4)` 时 rear 从 3 绕回 0**，假溢出被消除，空出来的 0 号格立刻被复用；
- **最后 `front == rear == 1` 但队列是满的**（count=4）——这正说明为什么必须靠 count 区分，只看指针会误判成空队列。

## 七、判空/判满方案对比（题面第 3 题）

| 对比项 | 用 `count` 计数（本实现） | 牺牲一个位置 |
|---|---|---|
| 判空 | `count == 0` | `front == rear` |
| 判满 | `count == capacity` | `(rear + 1) % capacity == front` |
| 可用容量 | **capacity（100%）** | capacity − 1 |
| 状态量 | 多维护一个整数 | 只需 front / rear |
| 极端情况 | `capacity=1` 也能存 1 个 | `capacity=1` 时完全不可用 |

**各有优劣**：

- **count 方案**的优势是容量一点不浪费，`capacity` 很小的场景优势明显；判空判满都是简单比较，不容易写错。代价是多一个状态量，入队出队都得维护，漏改就和指针不一致，序列化或多线程共享时它也得一起同步。
- **牺牲一位方案**的优势是状态最少，满/空都能用指针关系式直接表达，适合容量大、状态越少越好的场合（嵌入式、硬件环形缓冲区）；代价是永久少用一个格子，容量 1 直接不可用，判满式子也更容易写错。

一句话：**count 用"一个整数"换"一格空间"，牺牲位用"一格空间"换"一个变量"**；容量越小、越在乎利用率，越该用 count。

## 八、运行方式

```powershell
cd w9
chcp 65001                               # Windows 控制台切 UTF-8，否则中文乱码
python circular_queue.py                 # 打印题面第 2 题的 7 步状态表
python -m unittest test_circular_queue -v
```

## 九、测试覆盖

| 用例 | 验证内容 |
|---|---|
| `test_fifo` | 先进先出 |
| `test_full_ignores_enqueue` | 满时入队不覆盖、不报错，count 保持 capacity |
| `test_empty_dequeue_returns_none` | 空时出队返回 `None` |
| `test_wrap_around` | rear 绕回 0 后仍能正确写入，front/rear/count 同步 |
| `test_capacity_one` | `capacity=1` 可用，证明没牺牲空位 |

运行结果：`Ran 5 tests in 0.000s — OK`

## 十、一点说明

为了和课件保持一致，队满/队空用 `return` / `return None` 表示，而不是抛异常——代码短，但"满"和"元素恰好是 None"在调用方看来无法区分。工程实现里通常会改成抛 `OverflowError` / `IndexError`，或者额外返回一个成功标志。这里优先照顾可读性和与课件的一致性。
