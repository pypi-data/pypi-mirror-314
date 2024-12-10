
from logging import Logger
from logging import getLogger
from typing import Tuple

from ogl.OglClass import OglClass

from pyforcedirectedlayout.LayoutTypes import DrawingContext
from pyforcedirectedlayout.Node import Node
from pyforcedirectedlayout.Point import Point
from pyforcedirectedlayout.Size import Size

OglPositionTuple = Tuple[int, int]


class OglNode(Node):

    def __init__(self, oglClass: OglClass):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._oglClass: OglClass = oglClass

        oglPosition: OglPositionTuple = self._oglClass.GetPosition()

        self._location = Point(x=oglPosition[0], y=oglPosition[1])

    @property
    def size(self) -> Size:
        width, height = self._oglClass.GetSize()

        return Size(width=width, height=height)

    @property
    def location(self) -> Point:
        """
        Override base implementation for OglNode
        """
        return self._location

    @location.setter
    def location(self, point: Point):
        oglPosition: OglPositionTuple = point.x, point.y
        self._oglClass.SetPosition(oglPosition[0], oglPosition[1])

        self._location = point

    def drawNode(self, dc: DrawingContext):
        pass
