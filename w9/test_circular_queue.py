"""CircularQueue 单元测试：FIFO、绕回、满/空边界。"""

import unittest

from circular_queue import CircularQueue


class TestCircularQueue(unittest.TestCase):
    def test_fifo(self):
        q = CircularQueue(4)
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)

    def test_full_ignores_enqueue(self):
        """满时入队直接返回，不覆盖也不报错。"""
        q = CircularQueue(2)
        q.enqueue("a")
        q.enqueue("b")
        q.enqueue("c")
        self.assertEqual(q.items, ["a", "b"])
        self.assertEqual(q.count, 2)

    def test_empty_dequeue_returns_none(self):
        self.assertIsNone(CircularQueue(2).dequeue())

    def test_wrap_around(self):
        q = CircularQueue(4)
        for v in (1, 2, 3, 4):
            q.enqueue(v)
        self.assertEqual(q.rear, 0)                  # rear 绕回
        q.dequeue()
        q.enqueue(5)
        self.assertEqual(q.items, [5, 2, 3, 4])
        self.assertEqual((q.front, q.rear, q.count), (1, 1, 4))

    def test_capacity_one(self):
        """capacity=1 也能存一个，证明没牺牲空位。"""
        q = CircularQueue(1)
        q.enqueue("x")
        self.assertEqual(q.count, 1)
        self.assertEqual(q.dequeue(), "x")


if __name__ == "__main__":
    unittest.main(verbosity=2)
