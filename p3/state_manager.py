import struct

from p3.state import State
from p3.state import PlayerType
from p3.state import Character
from p3.state import Menu
from p3.state import Stage

def int_handler(obj, name, mask=0xFFFFFFFF, shift=0, wrapper=None, default=0):
    """Returns a handler that sets an attribute for a given object.

    obj is the object that will have its attribute set. Probably a State.
    name is the attribute name to be set.
    mask will be applied *before* shifting to the right by shift.
    Finally, wrapper will be called on the value if it is not None.

    This sets the attribute to default when called. Note that the actual final
    value doesn't need to be an int. The wrapper can convert int to whatever.
    This is particularly useful for enums.
    """
    def handle(value):
        transformed = (struct.unpack('>i', value)[0] & mask) >> shift
        wrapped = transformed if wrapper is None else wrapper(transformed)
        setattr(obj, name, wrapped)
    setattr(obj, name, default)
    return handle

def float_handler(obj, name, wrapper=None, default=0.0):
    """Returns a handler that sets an attribute for a given object.

    Similar to int_handler, but no mask or shift.
    """
    def handle(value):
        as_float = struct.unpack('>f', value)[0]
        setattr(obj, name, as_float if wrapper is None else wrapper(as_float))
    setattr(obj, name, default)
    return handle

def add_address(x, y):
    """Returns a string representation of the sum of the two parameters.

    x is a hex string address that can be converted to an int.
    y is an int.
    """
    return "{0:08X}".format(int(x, 16) + y)

class StateManager:
    """Converts raw memory changes into attributes in a State object."""
    def __init__(self, state):
        """Pass in a State object. It will have its attributes zeroed."""
        self.state = state
        self.addresses = {}

        self.addresses['80479D60'] = int_handler(self.state, 'frame')
        self.addresses['80479d30'] = int_handler(self.state, 'menu', 0xFF, 0, Menu, Menu.Characters)
        self.addresses['804D6CAC'] = int_handler(self.state, 'stage', 0xFF00, 8, Stage, Stage.Unselected)

        self.state.players = []
        for player_id in range(4):
            player = State()
            self.state.players.append(player)

            type_address = add_address('803F0E08', 0x24 * player_id)
            type_handler = int_handler(player, 'type', 0xFF000000, 24, PlayerType, PlayerType.Unselected)
            character_handler = int_handler(player, 'character', 0xFF00, 8, Character, Character.Unselected)
            self.addresses[type_address] = [type_handler, character_handler]

    def handle(self, address, value):
        """Convert the raw address and value into changes in the State."""
        assert address in self.addresses
        handlers = self.addresses[address]
        if isinstance(handlers, list):
            for handler in handlers:
                handler(value)
        else:
            handlers(value)

    def locations(self):
        """Returns a list of addresses for exporting to Locations.txt."""
        return self.addresses.keys()
