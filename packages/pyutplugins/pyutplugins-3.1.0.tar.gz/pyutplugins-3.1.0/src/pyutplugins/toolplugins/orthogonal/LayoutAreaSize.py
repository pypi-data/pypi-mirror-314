
from typing import List

from dataclasses import dataclass


@dataclass
class LayoutAreaSize:

    width:  int = 0
    height: int = 0

    @classmethod
    def deSerialize(cls, value: str) -> 'LayoutAreaSize':

        layoutAreaSize: LayoutAreaSize = LayoutAreaSize()

        widthHeight: List[str] = value.split(sep=',')

        assert len(widthHeight) == 2, 'Incorrectly formatted dimensions'
        assert value.replace(',', '', 1).isdigit(), 'String must be numeric'

        layoutAreaSize.width  = int(widthHeight[0])
        layoutAreaSize.height = int(widthHeight[1])

        return layoutAreaSize

    def __str__(self):
        return f'{self.width},{self.height}'

    def __repr__(self):
        return self.__str__()
