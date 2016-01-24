import enum
import math
import unittest

from p3.state import State
from p3.state import PlayerType
from p3.state import Character
from p3.state_manager import StateManager
from p3.state_manager import int_handler
from p3.state_manager import float_handler
from p3.state_manager import add_address

class IntHandlerTest(unittest.TestCase):
    def setUp(self):
        self.state = State()

    def test_int_handler_basic(self):
        with self.assertRaises(AttributeError):
            self.state.attribute
        handler = int_handler(self.state, 'attribute')
        self.assertEqual(self.state.attribute, 0)
        handler(b'\x00\x00\x00\x01')
        self.assertEqual(self.state.attribute, 1)

    def test_int_handler_mask(self):
        handler = int_handler(self.state, 'attribute', mask=0xFF00)
        handler(b'\x00\x00\xFF\xFF')
        self.assertEqual(self.state.attribute, 0xFF00)

    def test_int_handler_shift(self):
        handler = int_handler(self.state, 'attribute', shift=8)
        handler(b'\xF0\xFF\xFF\x0F')
        self.assertEqual(self.state.attribute, 0xF0FFFF)

    def test_int_handler_wrapper(self):
        wrapper = lambda x: x*x
        handler = int_handler(self.state, 'attribute', wrapper=wrapper)
        handler(b'\x00\x00\x00\x04')
        self.assertEqual(self.state.attribute, 0x10)

    def test_int_handler_default(self):
        handler = int_handler(self.state, 'attribute', default=7)
        self.assertEqual(self.state.attribute, 7)
        handler(b'\x00\x00\x00\x08')
        self.assertEqual(self.state.attribute, 8)

    def test_int_handler_enum(self):
        class TestWrapper(enum.Enum):
            ValOne = 1
            ValTwo = 2
        handler = int_handler(self.state, 'attribute', wrapper=TestWrapper)
        handler(b'\x00\x00\x00\x02')
        self.assertEqual(self.state.attribute, TestWrapper.ValTwo)

class FloatHandlerTest(unittest.TestCase):
    def setUp(self):
        self.state = State()

    def test_float_handler_basic(self):
        with self.assertRaises(AttributeError):
            self.state.attribute
        handler = float_handler(self.state, 'attribute')
        self.assertEqual(self.state.attribute, 0.0)
        handler(b'@I\x0f\xdb')
        self.assertAlmostEqual(self.state.attribute, math.pi, places=5)

    def test_float_handler_wrapper(self):
        handler = float_handler(self.state, 'attribute', lambda x: x*x)
        handler(b'@I\x0f\xdb')
        self.assertAlmostEqual(self.state.attribute, math.pi*math.pi, places=5)

    def test_float_handler_default(self):
        handler = float_handler(self.state, 'attribute', default=7.0)
        self.assertEqual(self.state.attribute, 7.0)

    def test_float_handler_wrapper_default(self):
        handler = float_handler(self.state, 'attribute', lambda x: x > 0, True)
        self.assertTrue(self.state.attribute)
        handler(b'\xc2(\x00\x00')
        self.assertFalse(self.state.attribute)
        handler(b'B(\x00\x00')
        self.assertTrue(self.state.attribute)

class AddAddressTest(unittest.TestCase):
    def test_add_address(self):
        self.assertEqual(add_address('0', 0), '00000000')
        self.assertEqual(add_address('0', 1), '00000001')
        self.assertEqual(add_address('1', 0), '00000001')
        self.assertEqual(add_address('1', 1), '00000002')
        self.assertEqual(add_address('804530E0', 0xE90), '80453F70')

class StateManagerTest(unittest.TestCase):
    def setUp(self):
        self.state = State()
        self.state_manager = StateManager(self.state)

    def test_state_manager_basic(self):
        self.assertEqual(self.state.frame, 0)
        self.state_manager.handle('80479D60', b'\x00\x00\x00\x01')
        self.assertEqual(self.state.frame, 1)

    def test_state_manager_player(self):
        self.assertEqual(self.state.players[0].character, Character.Unselected)
        self.assertEqual(self.state.players[0].type, PlayerType.Unselected)
        self.state_manager.handle('803F0E08', b'\x00\x00\x0A\x00')
        self.assertEqual(self.state.players[0].character, Character.Fox)
        self.assertEqual(self.state.players[0].type, PlayerType.Human)

    def test_state_manager_asserts(self):
        with self.assertRaises(AssertionError):
            self.state_manager.handle('missing', 12345)

if __name__ == '__main__':
    unittest.main()
