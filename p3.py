#!/usr/bin/env python3

import mw
import pad
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home')
    home = sys.argv[1]

    pad = pad.Pad(home + '/Pipes/p3')
    mw = mw.MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')

    # Just print out addresses and values for now
    for address, value in mw:
        print(address, value)
