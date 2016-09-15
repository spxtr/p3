[![Test Status](https://travis-ci.org/spxtr/p3.svg)](https://travis-ci.org/spxtr/p3)

# Super Smash Bros. Melee CPU

Run with `python -m p3` before opening Dolphin. Stop with ^C.

Requires Python 3. You'll need to configure the pipe input in Dolphin for player 3. See `example_gc_config.ini` for an example Dolphin profile. Turn on the "Netplay Community Settings" Gecko code before booting the game.

Test with `python -m unittest discover -p "*_test.py"`.

## Write your own Melee AI

Feel free to use this code in your own AI. At the very least you'll want to use `memory_watcher` to listen to Dolphin's output and `pad` to send Dolphin controller inputs. I recommend also using `state_manager`.

`p3` is lisenced under GPL version 3.
