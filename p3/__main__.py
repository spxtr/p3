import os.path

import p3.fox
import p3.memory_watcher
import p3.menu_manager
import p3.pad
import p3.state
import p3.state_manager

# Assume dolphin config is in ~/.dolphin-emu.
dolphin_dir = os.path.expanduser('~/.dolphin-emu')

try:
    state = p3.state.State()
    sm = p3.state_manager.StateManager(state)
    with open(dolphin_dir + '/MemoryWatcher/Locations.txt', 'w') as loc:
        loc.write('\n'.join(sm.locations()))

    mw = p3.memory_watcher.MemoryWatcher(dolphin_dir + '/MemoryWatcher/MemoryWatcher')
    pad = p3.pad.Pad(dolphin_dir + '/Pipes/p3')
    menu_manager = p3.menu_manager.MenuManager()

    fox = p3.fox.Fox()

    while True:
        frame = state.frame
        res = next(mw)
        if res is not None:
            sm.handle(*res)
        if state.frame > frame:
            frame = state.frame
            if state.menu == p3.state.Menu.Game:
                fox.advance(state, pad)
            elif state.menu == p3.state.Menu.Characters:
                menu_manager.pick_fox(state, pad)
            elif state.menu == p3.state.Menu.Stages:
                # Handle this once we know where the cursor position is in memory.
                pad.tilt_stick(p3.pad.Stick.C, 0.5, 0.5)
            elif state.menu == p3.state.Menu.PostGame:
                menu_manager.press_start_lots(state, pad)
except KeyboardInterrupt:
    pass
