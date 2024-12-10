
from enum import Enum


class MermaidDirection(str, Enum):

    diagramValue: str
    userValue:    str

    def __new__(cls, title: str, diagramValue: str) -> 'MermaidDirection':
        obj = str.__new__(cls, title)
        obj._value_ = title

        obj.diagramValue = diagramValue

        return obj

    RightToLeft = ('Right To Left', 'direction RL')
    LeftToRight = ('Left To Right', 'direction LR')

    @classmethod
    def toEnum(cls, enumStr: str) -> 'MermaidDirection':

        assert (enumStr is not None) and (enumStr != ''), 'I need a real string dude'
        match enumStr:
            case MermaidDirection.RightToLeft.value:
                retEnum: MermaidDirection = MermaidDirection.RightToLeft
            case MermaidDirection.LeftToRight.value:
                retEnum = MermaidDirection.LeftToRight
            case _:
                print(f'Unknown enumeration string {enumStr}')
                retEnum = MermaidDirection.LeftToRight

        return retEnum
