
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglClass import OglClass
from ogl.OglInterface import OglInterface
from ogl.OglLink import OglLink
from ogl.OglLinkFactory import OglLinkFactory

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType


class LinkMakerMixin:
    """
    Used to aid the pyutplugins when they need to create a link;  Usually not used
    directly by the plugin but by the supplementary classes used by the pyutplugins

    """
    def __init__(self):

        self.logger: Logger = getLogger('LinkMakerMixin')

        self._oglLinkFactory: OglLinkFactory  = OglLinkFactory()

    def createLink(self, src: OglClass, dst: OglClass, linkType: PyutLinkType = PyutLinkType.INHERITANCE) -> OglLink:
        """
        Add a paternity link between child and father.

        Args:
            src:  subclass
            dst: Base Class
            linkType:   The type of link

        Returns: an OglLink

        """
        sourceClass:      PyutClass = cast(PyutClass, src.pyutObject)
        destinationClass: PyutClass = cast(PyutClass, dst.pyutObject)

        pyutLink: PyutLink = PyutLink("", linkType=linkType, source=sourceClass, destination=destinationClass)

        oglLink = self._oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)

        src.addLink(oglLink)
        dst.addLink(oglLink)

        pyutClass: PyutClass = cast(PyutClass, src.pyutObject)
        pyutClass.addLink(pyutLink)

        return oglLink

    def createInterfaceLink(self, src: OglClass, dst: OglClass) -> OglInterface:
        """
        Adds an OglInterface link between src and dst.

        Args:
            src:    source of the link
            dst:    destination of the link

        Returns: the created OglInterface link
        """
        sourceClass:      PyutClass = cast(PyutClass, src.pyutObject)
        destinationClass: PyutClass = cast(PyutClass, dst.pyutObject)

        pyutLink:     PyutLink     = PyutLink(linkType=PyutLinkType.INTERFACE, source=sourceClass, destination=destinationClass)
        oglInterface: OglInterface = OglInterface(srcShape=src, pyutLink=pyutLink, dstShape=dst)

        src.addLink(oglInterface)
        dst.addLink(oglInterface)

        return oglInterface
