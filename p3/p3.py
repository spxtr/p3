import os.path
import time

import p3.fox
import p3.memory_watcher
import p3.menu_manager
import p3.pad
import p3.state
import p3.state_manager

# TODO This should really be written to be tested.
class P3:
    def __init__(self):
        # TODO This might not always be accurate.
        dolphin_dir = os.path.expanduser('~/.dolphin-emu')

        self.state = p3.state.State()
        self.sm = p3.state_manager.StateManager(self.state)
        self.write_locations(dolphin_dir)

        self.fox = p3.fox.Fox()
        self.mm = p3.menu_manager.MenuManager()

        try:
            print('Creating MemoryWatcher.')
            self.mw = p3.memory_watcher.MemoryWatcher(dolphin_dir + '/MemoryWatcher/MemoryWatcher')
            print('Creating Pad. Open dolphin now.')
            self.pad = p3.pad.Pad(dolphin_dir + '/Pipes/p3')
            self.initialized = True
        except KeyboardInterrupt:
            self.initialized = False

        self.init_stats()

    def run(self):
        if not self.initialized:
            return
        print('Starting run loop.')
        try:
            while True:
                self.advance_frame()
        except KeyboardInterrupt:
            self.print_stats()

    def init_stats(self):
        self.total_frames = 0
        self.skip_frames = 0
        self.thinking_time = 0

    def print_stats(self):
        frac_skipped = self.skip_frames / self.total_frames
        frac_thinking = self.thinking_time * 1000 / self.total_frames
        print('Total Frames:', self.total_frames)
        print('Fraction Skipped: {:.6f}'.format(frac_skipped))
        print('Average Thinking Time (ms): {:.6f}'.format(frac_thinking))

    def write_locations(self, dolphin_dir):
        path = dolphin_dir + '/MemoryWatcher/Locations.txt'
        print('Writing locations to:', path)
        with open(path, 'w') as f:
            f.write('\n'.join(self.sm.locations()))

    def advance_frame(self):
        last_frame = self.state.frame
        self.update_state()
        if self.state.frame > last_frame:
            if self.state.frame != last_frame + 1:
                self.skip_frames += 1
            self.total_frames += self.state.frame - last_frame
            last_frame = self.state.frame
            start = time.time()
            self.make_action()
            self.thinking_time += time.time() - start

    def update_state(self):
        res = next(self.mw)
        if res is not None:
            self.sm.handle(*res)

    def make_action(self):
        if self.state.menu == p3.state.Menu.Game:
            self.fox.advance(self.state, self.pad)
        elif self.state.menu == p3.state.Menu.Characters:
            self.mm.pick_fox(self.state, self.pad)
        elif self.state.menu == p3.state.Menu.Stages:
            # Handle this once we know where the cursor position is in memory.
            self.pad.tilt_stick(p3.pad.Stick.C, 0.5, 0.5)
        elif self.state.menu == p3.state.Menu.PostGame:
            self.mm.press_start_lots(self.state, self.pad)
