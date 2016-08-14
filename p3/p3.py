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

        dolphin_dir = find_dolphin_dir()
        if dolphin_dir is None:
            print('Could not detect dolphin directory.')
            return

def run(state, sm, mw, pad, stats):
    fox = p3.fox.Fox()
    mm = p3.menu_manager.MenuManager()
    while True:
        last_frame = state.frame
        res = next(mw)
        if res is not None:
            sm.handle(*res)
        if state.frame > last_frame:
            stats.add_frames(state.frame - last_frame)
            start = time.time()
            make_action(state, pad, mm, fox)
            stats.add_thinking_time(time.time() - start)

def make_action(state, pad, mm, fox):
    if state.menu == p3.state.Menu.Game:
        fox.advance(state, pad)
    elif state.menu == p3.state.Menu.Characters:
        mm.pick_fox(state, pad)
    elif state.menu == p3.state.Menu.Stages:
        # Handle this once we know where the cursor position is in memory.
        pad.tilt_stick(p3.pad.Stick.C, 0.5, 0.5)
    elif state.menu == p3.state.Menu.PostGame:
        mm.press_start_lots(state, pad)

def main():
    dolphin_dir = find_dolphin_dir()
    if dolphin_dir is None:
        print('Could not find dolphin config dir.')
        return

    state = p3.state.State()
    sm = p3.state_manager.StateManager(state)
    write_locations(dolphin_dir, sm.locations())

    stats = p3.stats.Stats()

    try:
        print('Start dolphin now. Press ^C to stop p3.')
        mw = p3.memory_watcher.MemoryWatcher(dolphin_dir + '/MemoryWatcher/MemoryWatcher')
        pad = p3.pad.Pad(dolphin_dir + '/Pipes/p3')
        run(state, sm, mw, pad, stats)
    except KeyboardInterrupt:
        print('Stopped')
        print(stats)

if __name__ == '__main__':
    main()
