import struct

from p3.state import State
from p3.state import PlayerType
from p3.state import Character
from p3.state import Menu
from p3.state import Stage
from p3.state import ActionState
from p3.state import BodyState

def int_handler(obj, name, shift=0, mask=0xFFFFFFFF, wrapper=None, default=0):
    """Returns a handler that sets an attribute for a given object.

    obj is the object that will have its attribute set. Probably a State.
    name is the attribute name to be set.
    shift will be applied before mask.
    Finally, wrapper will be called on the value if it is not None. If wrapper
    raises ValueError, sets attribute to default.

    This sets the attribute to default when called. Note that the actual final
    value doesn't need to be an int. The wrapper can convert int to whatever.
    This is particularly useful for enums.
    """
    def handle(value):
        transformed = (struct.unpack('>i', value)[0] >> shift) & mask
        setattr(obj, name, generic_wrapper(transformed, wrapper, default))
    setattr(obj, name, default)
    return handle

def float_handler(obj, name, wrapper=None, default=0.0):
    """Returns a handler that sets an attribute for a given object.

    Similar to int_handler, but no mask or shift.
    """
    def handle(value):
        as_float = struct.unpack('>f', value)[0]
        setattr(obj, name, generic_wrapper(as_float, wrapper, default))
    setattr(obj, name, default)
    return handle

def generic_wrapper(value, wrapper, default):
    if wrapper is not None:
        try:
            value = wrapper(value)
        except ValueError:
            value = default
    return value

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

        self.addresses['804D7420'] = int_handler(self.state, 'frame')
        self.addresses['80479D30'] = int_handler(self.state, 'menu', 0, 0xFF, Menu, Menu.Characters)
        self.addresses['804D6CAC'] = int_handler(self.state, 'stage', 8, 0xFF, Stage, Stage.Unselected)

        self.state.players = []
        for player_id in range(4):
            player = State()
            self.state.players.append(player)
            data_pointer = add_address('80453130', 0xE90 * player_id)

            cursor_x_address = add_address('81118DEC', -0xB80 * player_id)
            cursor_y_address = add_address('81118DF0', -0xB80 * player_id)
            self.addresses[cursor_x_address] = float_handler(player, 'cursor_x')
            self.addresses[cursor_y_address] = float_handler(player, 'cursor_y')

            type_address = add_address('803F0E08', 0x24 * player_id)
            type_handler = int_handler(player, 'type', 24, 0xFF, PlayerType, PlayerType.Unselected)
            character_handler = int_handler(player, 'character', 8, 0xFF, Character, Character.Unselected)
            self.addresses[type_address] = [type_handler, character_handler]

            self.addresses[data_pointer + ' 70'] = int_handler(player, 'action_state', 0, 0xFFFF, ActionState, ActionState.Unselected)
            self.addresses[data_pointer + ' 8C'] = float_handler(player, 'facing')
            self.addresses[data_pointer + ' E0'] = float_handler(player, 'self_air_vel_x')
            self.addresses[data_pointer + ' E4'] = float_handler(player, 'self_air_vel_y')
            self.addresses[data_pointer + ' EC'] = float_handler(player, 'attack_vel_x')
            self.addresses[data_pointer + ' F0'] = float_handler(player, 'attack_vel_y')
            self.addresses[data_pointer + ' 110'] = float_handler(player, 'pos_x')
            self.addresses[data_pointer + ' 114'] = float_handler(player, 'pos_y')
            self.addresses[data_pointer + ' 140'] = int_handler(player, 'on_ground', 0, 0xFFFF, lambda x: x == 0, True)
            self.addresses[data_pointer + ' 8F4'] = float_handler(player, 'action_frame')
            self.addresses[data_pointer + ' 1890'] = float_handler(player, 'percent')
            self.addresses[data_pointer + ' 19BC'] = float_handler(player, 'hitlag')
            self.addresses[data_pointer + ' 19C8'] = int_handler(player, 'jumps_used', 0, 0xFF)
            self.addresses[data_pointer + ' 19EC'] = int_handler(player, 'body_state', 0, 0xFF, BodyState, BodyState.Normal)


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
