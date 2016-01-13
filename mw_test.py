import os
import mw
import socket
import unittest

class MemoryWatcherTest(unittest.TestCase):
    def setUp(self):
        self.sock_path = os.getcwd() + '/sock'
        self.mw = mw.MemoryWatcher(self.sock_path)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    def test_recv(self):
        self.sock.sendto(b'DEAD BEEF\n15\0', self.sock_path)
        self.assertEqual(next(self.mw), ('DEAD BEEF', b'\x00\x00\x00\x15'))

    def test_iter(self):
        self.sock.sendto(b'0123\n12000000\0', self.sock_path)
        self.sock.sendto(b'4567\n34000000\0', self.sock_path)
        self.sock.sendto(b'89AB\n56000000\0', self.sock_path)
        # It blocks if we try to read past the end, so limit to three
        gen = ((addr, value) for _, (addr, value) in zip(range(3), self.mw))
        self.assertEqual(next(gen), ('0123', b'\x12\x00\x00\x00'))
        self.assertEqual(next(gen), ('4567', b'\x34\x00\x00\x00'))
        self.assertEqual(next(gen), ('89AB', b'\x56\x00\x00\x00'))

    def tearDown(self):
        self.sock.close()
        del self.mw
        os.unlink(self.sock_path)

if __name__ == '__main__':
    unittest.main()
