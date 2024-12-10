from typing import Dict
from typing import List
from typing import NewType
from typing import cast

from dataclasses import dataclass
from dataclasses import field

NO_INTEGER = cast(int, None)


@dataclass
class Size:
    width:  int = NO_INTEGER
    height: int = NO_INTEGER


@dataclass
class Position:
    x: int = NO_INTEGER
    y: int = NO_INTEGER


def positionFactory() -> Position:
    return Position()


def sizeFactory() -> Size:
    return Size()


OglName = NewType('OglName', str)


@dataclass
class Layout:
    name:     OglName  = cast(OglName, None)
    position: Position = field(default_factory=positionFactory)
    size:     Size     = field(default_factory=sizeFactory)


Layouts = NewType('Layouts', Dict[OglName, Layout])


def layoutsFactory() -> Layouts:
    return Layouts({})


@dataclass
class LayoutInformation:
    layouts: Layouts = field(default_factory=layoutsFactory)
