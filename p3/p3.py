import os.path
import time

import p3.fox
import p3.memory_watcher
import p3.menu_manager
import p3.pad
import p3.state
import p3.state_manager
import p3.stats

def find_dolphin_dir():
    """Attempts to find the dolphin user directory. None on failure."""
    candidates = ['~/.dolphin-emu', '~/.local/share/.dolphin-emu']
    for candidate in candidates:
        path = os.path.expanduser(candidate)
        if os.path.isdir(path):
            return path
    return None

def write_locations(dolphin_dir, locations):
    """Writes out the locations list to the appropriate place under dolphin_dir."""
    path = dolphin_dir + '/MemoryWatcher/Locations.txt'
    with open(path, 'w') as f:
        f.write('\n'.join(locations))

class P3:
    def __init__(self):
        dolphin_dir = find_dolphin_dir()
        if dolphin_dir is None:
            print('Could not detect dolphin directory.')
            return

        self.state = p3.state.State()
        self.sm = p3.state_manager.StateManager(self.state)
        write_locations(dolphin_dir, self.sm.locations())

        self.fox = p3.fox.Fox()
        self.mm = p3.menu_manager.MenuManager()
        self.stats = p3.stats.Stats()

        try:
            print('Start dolphin now. Press ^C to stop p3.')
            self.mw = p3.memory_watcher.MemoryWatcher(dolphin_dir + '/MemoryWatcher/MemoryWatcher')
            self.pad = p3.pad.Pad(dolphin_dir + '/Pipes/p3')
            self.run()
        except KeyboardInterrupt:
            print('Stopped')
            print(self.stats)

    def run(self):
        while True:
            last_frame = self.state.frame
            res = next(self.mw)
            if res is not None:
                self.sm.handle(*res)
            if self.state.frame > last_frame:
                self.stats.add_frames(self.state.frame - last_frame)
                self.make_action()

    def make_action(self):
        start = time.time()
        if self.state.menu == p3.state.Menu.Game:
            self.fox.advance(self.state, self.pad)
        elif self.state.menu == p3.state.Menu.Characters:
            self.mm.pick_fox(self.state, self.pad)
        elif self.state.menu == p3.state.Menu.Stages:
            # Handle this once we know where the cursor position is in memory.
            self.pad.tilt_stick(p3.pad.Stick.C, 0.5, 0.5)
        elif self.state.menu == p3.state.Menu.PostGame:
            self.mm.press_start_lots(self.state, self.pad)
        self.stats.add_thinking_time(time.time() - start)
