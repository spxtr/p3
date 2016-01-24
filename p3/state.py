import enum

@enum.unique
class PlayerType(enum.Enum):
    Human      = 0
    CPU        = 1
    Demo       = 2
    Unselected = 3

@enum.unique
class Character(enum.Enum):
    Doc        = 0
    Mario      = 1
    Luigi      = 2
    Bowser     = 3
    Peach      = 4
    Yoshi      = 5
    DK         = 6
    Falcon     = 7
    Ganon      = 8
    Falco      = 9
    Fox        = 10
    Ness       = 11
    Icies      = 12
    Kirby      = 13
    Samus      = 14
    Zelda      = 15
    Link       = 16
    YoungLink  = 17
    Pichu      = 18
    Pikachu    = 19
    Jiggs      = 20
    Mewtwo     = 21
    GnW        = 22
    Marth      = 23
    Roy        = 24
    Unselected = 25

@enum.unique
class Stage(enum.Enum):
    PeachCastle = 0
    Rainbow     = 1
    Kongo       = 2
    Japes       = 3
    GreatBay    = 4
    Temple      = 5
    Story       = 6
    Island      = 7
    FoD         = 8
    Greens      = 9
    Corneria    = 10
    Venom       = 11
    Brinstar    = 12
    Depths      = 13
    Onett       = 14
    Fourside    = 15
    Mute        = 16
    BigBlue     = 17
    Pokemon     = 18
    Floats      = 19
    Kingdom     = 20
    Kingdom2    = 21
    Icicle      = 22
    FlatZone    = 23
    Battlefield = 24
    Final       = 25
    DreamLand   = 26
    Island64    = 27
    Kongo64     = 28
    Random      = 29
    Unselected  = 30

@enum.unique
class Menu(enum.Enum):
    Characters = 0
    Stages     = 1
    Game       = 2
    PostGame   = 4

class State:
    """Databag that is handled by StateManager."""
    pass
