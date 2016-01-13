import os
import unittest

import p3.pad as pad

class PadTest(unittest.TestCase):
    def setUp(self):
        # Create a fifo for testing. We'll remove it in tearDown.
        self.fifo_path = os.getcwd() + '/fifo'
        os.mkfifo(self.fifo_path)

        self.pipe = os.open(self.fifo_path, os.O_RDONLY | os.O_NONBLOCK)
        self.pad = pad.Pad(self.fifo_path)

    # Returns whatever is pending in the fifo
    def read_pipe(self):
        return os.read(self.pipe, 256)

    def test_buttons_basic(self):
        self.pad.press_button(pad.Button.A)
        self.assertEqual(self.read_pipe(), b'PRESS A\n')

    def test_buttons_multi(self):
        self.pad.press_button(pad.Button.L)
        self.pad.press_button(pad.Button.R)
        self.assertEqual(self.read_pipe(), b'PRESS L\nPRESS R\n')

    def test_buttons_release(self):
        self.pad.release_button(pad.Button.A)
        self.assertEqual(self.read_pipe(), b'RELEASE A\n')

    def test_buttons_assert(self):
        with self.assertRaises(AssertionError):
            self.pad.press_button('Not a button')
        with self.assertRaises(AssertionError):
            self.pad.press_button(pad.Trigger.L)

    def test_triggers_basic(self):
        self.pad.press_trigger(pad.Trigger.L, 0)
        self.pad.press_trigger(pad.Trigger.R, 1.0)
        self.assertEqual(self.read_pipe(), b'SET L 0.00\nSET R 1.00\n')

    def test_triggers_round(self):
        self.pad.press_trigger(pad.Trigger.L, 0.124)
        self.pad.press_trigger(pad.Trigger.R, 0.126)
        self.assertEqual(self.read_pipe(), b'SET L 0.12\nSET R 0.13\n')

    def test_triggers_assert(self):
        with self.assertRaises(AssertionError):
            self.pad.press_trigger(pad.Button.L, 0.5)
        with self.assertRaises(AssertionError):
            self.pad.press_trigger(pad.Trigger.R, 1.2)
        with self.assertRaises(AssertionError):
            self.pad.press_trigger(pad.Trigger.R, -0.3)

    def test_sticks_basic(self):
        self.pad.tilt_stick(pad.Stick.MAIN, 0, 0)
        self.assertEqual(self.read_pipe(), b'SET MAIN 0.00 0.00\n')
        self.pad.tilt_stick(pad.Stick.C, 1, 0)
        self.assertEqual(self.read_pipe(), b'SET C 1.00 0.00\n')
        self.pad.tilt_stick(pad.Stick.MAIN, 0.05, 0.55)
        self.assertEqual(self.read_pipe(), b'SET MAIN 0.05 0.55\n')

    def test_sticks_round(self):
        self.pad.tilt_stick(pad.Stick.MAIN, 0.054, 0)
        self.assertEqual(self.read_pipe(), b'SET MAIN 0.05 0.00\n')
        self.pad.tilt_stick(pad.Stick.MAIN, 0.056, 0)
        self.assertEqual(self.read_pipe(), b'SET MAIN 0.06 0.00\n')

    def test_sticks_assert(self):
        with self.assertRaises(AssertionError):
            self.pad.tilt_stick('Not a stick', 0.5, 0.5)
        with self.assertRaises(AssertionError):
            self.pad.tilt_stick(pad.Stick.MAIN, -0.5, 0.5)
        with self.assertRaises(AssertionError):
            self.pad.tilt_stick(pad.Stick.C, 0.5, 1.5)

    def tearDown(self):
        del self.pad
        os.close(self.pipe)
        os.unlink(self.fifo_path)

if __name__ == '__main__':
    unittest.main()
