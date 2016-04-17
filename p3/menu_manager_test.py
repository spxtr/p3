import unittest
import unittest.mock

import p3.menu_manager
import p3.pad
import p3.state

class MenuManagerTest(unittest.TestCase):
    def setUp(self):
        self.mm = p3.menu_manager.MenuManager()
        self.pad = unittest.mock.MagicMock()
        self.state = p3.state.State()
        self.state.players = []
        for _ in range(4):
            self.state.players.append(p3.state.State())

    def test_menu_manager_press_start_even(self):
        self.state.frame = 0
        self.mm.press_start_lots(self.state, self.pad)
        self.pad.press_button.assert_called_with(p3.pad.Button.START)

    def test_menu_manager_press_start_odd(self):
        self.state.frame = 1
        self.mm.press_start_lots(self.state, self.pad)
        self.pad.release_button.assert_called_with(p3.pad.Button.START)

    def test_menu_manager_pick_fox_presses(self):
        self.state.players[2].cursor_x = -23.5
        self.state.players[2].cursor_y = 11.5
        self.mm.pick_fox(self.state, self.pad)
        self.pad.press_button.assert_called_with(p3.pad.Button.A)
        self.assertTrue(self.pad.selected_fox)

    def test_menu_manager_pick_fox_tilts(self):
        # Make sure we point the cursor in the right direction.
        self.state.players[2].cursor_x = 0
        self.state.players[2].cursor_y = 0
        self.mm.pick_fox(self.state, self.pad)
        args = self.pad.tilt_stick.call_args
        self.assertIsNotNone(args)
        (stick, x, y), _ = args
        self.assertEqual(stick, p3.pad.Stick.MAIN)
        self.assertLess(x, 0.5)
        self.assertGreater(x, 0.0)
        self.assertLess(y, 1.0)
        self.assertGreater(y, 0.5)

    def test_menu_manager_pick_fox_plays(self):
        # This doesn't need to be too strict.
        self.mm.selected_fox = True
        self.state.frame = 0
        self.mm.pick_fox(self.state, self.pad)
        self.assertTrue(self.pad.release_button.called)
        self.assertTrue(self.pad.tilt_stick.called)
