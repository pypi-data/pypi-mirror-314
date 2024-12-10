
from typing import Callable
from typing import Dict
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from dataclasses import dataclass
from dataclasses import field

from os import path as osPath

from enum import Enum

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType
from wx import ClientDC

from pyutmodelv2.PyutLink import PyutLink

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglInterface2 import OglInterface2
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglObject import OglObject
from ogl.OglPosition import OglPositions
from ogl.OglUseCase import OglUseCase
from ogl.OglActor import OglActor

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

HybridLinks = Union[OglLink, OglInterface2]

OglClasses  = NewType('OglClasses',  List[OglClass])
OglLinks    = NewType('OglLinks',    List[HybridLinks])
OglNotes    = NewType('OglNotes',    List[OglNote])
OglTexts    = NewType('OglTexts',    List[OglText])
OglActors   = NewType('OglActors',   List[OglActor])
OglUseCases = NewType('OglUseCases', List[OglUseCase])

OglSDInstances = NewType('OglSDInstances', Dict[int, OglSDInstance])
OglSDMessages  = NewType('OglSDMessages',  Dict[int, OglSDMessage])

OglObjectType = Union[OglClass, OglLink, OglNote, OglText, OglActor, OglUseCase, OglInterface2, OglSDMessage, OglSDInstance, OglUseCase, OglActor]

OglObjects = NewType('OglObjects',  List[OglObjectType])
PyutLinks  = NewType('PyutLinks',   List[PyutLink])

SelectedOglObjectsCallback = Callable[[OglObjects], None]        # Todo: Figure out appropriate type for callback


def createOglObjectsFactory() -> OglObjects:
    """
    Factory method to create  the OglClasses data structure;

    Returns:  A new data structure
    """
    return OglObjects([])


@dataclass
class FrameSize:
    """
    The strategy is to provide minimal information to the pyutplugins
    we do not want them to not abuse it.
    """
    width:  int = -1
    height: int = -1


def createFrameSizeFactory() -> FrameSize:
    """
    Factory method to create  the OglClasses data structure;

    Returns:  A new data structure
    """
    return FrameSize()


@dataclass
class FrameInformation:
    """
    The document title is the name of the frame
    """
    frameActive:        bool       = False
    selectedOglObjects: OglObjects = field(default_factory=createOglObjectsFactory)
    diagramTitle:       str         = ''
    diagramType:        str        = ''
    frameSize:          FrameSize  = field(default_factory=createFrameSizeFactory)
    clientDC:           ClientDC   = cast(ClientDC, None)


FrameInformationCallback = Callable[[FrameInformation], None]
FrameSizeCallback        = Callable[[FrameSize], None]

NO_INTEGER: int = cast(int, None)


@dataclass
class ObjectBoundaries:
    minX: int = NO_INTEGER
    minY: int = NO_INTEGER
    maxX: int = NO_INTEGER
    maxY: int = NO_INTEGER


ObjectBoundaryCallback = Callable[[ObjectBoundaries], None]

InterfaceName          = NewType('InterfaceName', str)
AssociationName        = NewType('AssociationName', str)
SourceCardinality      = NewType('SourceCardinality', str)
DestinationCardinality = NewType('DestinationCardinality', str)


def createOglPositionsFactory() -> OglPositions:
    return OglPositions([])


@dataclass
class LinkInformation:
    """
    The field interfaceName is only valid when linkType is PyutLinkType.INTERFACE
    The fields
        associationName
        sourceCardinality
        destinationCardinality
    are valid only when linkType is  one of
        PyutLinkType.ASSOCIATION
        PyutLinkType.COMPOSITION
        PyutLinkType.AGGREGATION
    """
    linkType:               PyutLinkType            = cast(PyutLinkType, None)
    path:                   OglPositions            = field(default_factory=createOglPositionsFactory)
    sourceShape:            OglObject               = cast(OglObject, None)
    destinationShape:       OglObject               = cast(OglObject, None)
    interfaceName:          InterfaceName           = cast(InterfaceName, None)
    associationName:        AssociationName         = cast(AssociationName, None)
    sourceCardinality:      SourceCardinality       = cast(SourceCardinality, None)
    destinationCardinality: DestinationCardinality  = cast(DestinationCardinality, None)


CreatedLinkCallback = Callable[[OglLink], None]


def createPluginClassesFactory() -> OglClasses:
    """
    Factory method to create  the OglClasses data structure;

    Returns:  A new data structure
    """
    return OglClasses([])


def createPluginLinksFactory() -> OglLinks:
    """
    Factory method to create  the OglLinks data structure;

    Returns:  A new data structure
    """
    return OglLinks([])


def createPluginNotesFactory() -> OglNotes:
    return OglNotes([])


def createOglTextsFactory() -> OglTexts:
    return OglTexts([])


def createPluginActorsFactory() -> OglActors:
    return OglActors([])


def createPluginUseCasesFactory() -> OglUseCases:
    return OglUseCases([])


def createPluginSDInstances() -> OglSDInstances:
    return OglSDInstances({})


def createPluginSDMessages() -> OglSDMessages:
    return OglSDMessages({})


PluginDocumentTitle = NewType('PluginDocumentTitle', str)


class PluginDocumentType(Enum):

    CLASS_DIAGRAM    = 'CLASS_DIAGRAM'
    SEQUENCE_DIAGRAM = 'SEQUENCE_DIAGRAM'
    USECASE_DIAGRAM  = 'USECASE_DIAGRAM'
    UNKNOWN_DIAGRAM  = 'UNKNOWN_DIAGRAM'

    @classmethod
    def toEnum(cls, enumStr: str) -> 'PluginDocumentType':

        assert (enumStr is not None) and (enumStr != ''), 'I need a real string dude'
        # TODO use switch statement when we get to 3.10.x
        if enumStr == 'CLASS_DIAGRAM':
            retEnum: PluginDocumentType = PluginDocumentType.CLASS_DIAGRAM
        elif enumStr == 'SEQUENCE_DIAGRAM':
            retEnum = PluginDocumentType.SEQUENCE_DIAGRAM
        elif enumStr == 'USECASE_DIAGRAM':
            retEnum = PluginDocumentType.USECASE_DIAGRAM
        else:
            assert False, 'Unknown diagram type'

        return retEnum

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


@dataclass
class PluginDocument:
    """
    This is a plugin's version of a document
    """
    documentType:    PluginDocumentType  = PluginDocumentType.UNKNOWN_DIAGRAM
    documentTitle:   PluginDocumentTitle = PluginDocumentTitle('')
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses:      OglClasses     = field(default_factory=createPluginClassesFactory)
    oglLinks:        OglLinks       = field(default_factory=createPluginLinksFactory)
    oglNotes:        OglNotes       = field(default_factory=createPluginNotesFactory)
    oglTexts:        OglTexts       = field(default_factory=createOglTextsFactory)
    oglActors:       OglActors      = field(default_factory=createPluginActorsFactory)
    oglUseCases:     OglUseCases    = field(default_factory=createPluginUseCasesFactory)
    oglSDInstances:  OglSDInstances = field(default_factory=createPluginSDInstances)
    oglSDMessages:   OglSDMessages  = field(default_factory=createPluginSDMessages)


PluginDocuments     = NewType('PluginDocuments', dict[PluginDocumentTitle, PluginDocument])


def createPluginDocumentsFactory() -> PluginDocuments:
    return PluginDocuments({})


@dataclass
class PluginProject:
    """
    This is a plugin's version of a project
    """
    fileName:        str             = cast(str, None)
    projectName:     str             = cast(str, None)
    version:         str             = cast(str, None)
    codePath:        str             = cast(str, None)
    pluginDocuments: PluginDocuments = field(default_factory=createPluginDocumentsFactory)

    @classmethod
    def toProjectName(cls, fqFilename):
        """
        Return just the file name portion of the fully qualified path

        Args:
            fqFilename:  file name to display

        Returns:
            A project name
        """
        regularFileName: str = osPath.split(fqFilename)[1]
        projectName:     str  = osPath.splitext(regularFileName)[0]

        return projectName


CurrentProjectCallback     = Callable[[PluginProject], None]
