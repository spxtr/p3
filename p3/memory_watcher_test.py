import os
import socket
import unittest

import p3.memory_watcher

class MemoryWatcherTest(unittest.TestCase):
    def setUp(self):
        self.sock_path = os.getcwd() + '/sock'
        self.mw = p3.memory_watcher.MemoryWatcher(self.sock_path)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    def test_memory_watcher_recv(self):
        self.sock.sendto(b'DEAD BEEF\n15\0', self.sock_path)
        self.assertEqual(next(self.mw), ('DEAD BEEF', b'\x00\x00\x00\x15'))

    def test_memory_watcher_iter(self):
        self.sock.sendto(b'0123\n12000000\0', self.sock_path)
        self.sock.sendto(b'4567\n34000000\0', self.sock_path)
        self.sock.sendto(b'89AB\n56000000\0', self.sock_path)

        expecteds = [
            ('0123', b'\x12\x00\x00\x00'),
            ('4567', b'\x34\x00\x00\x00'),
            ('89AB', b'\x56\x00\x00\x00'),
            ]

        for actual, expected in zip(self.mw, expecteds):
            self.assertEqual(actual, expected)

    def test_memory_watcher_timeout(self):
        self.assertIsNone(next(self.mw))

    def tearDown(self):
        self.sock.close()
        del self.mw
        os.unlink(self.sock_path)

if __name__ == '__main__':
    unittest.main()
