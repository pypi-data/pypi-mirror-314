
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from pyutmodelv2.PyutClass import PyutClass

from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutNote import PyutNote

from pyutmodelv2.enumerations.PyutDisplayParameters import PyutDisplayParameters
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglAssociation import OglAssociation
from ogl.OglInterface2 import OglInterface2
from ogl.OglNote import OglNote

from pyumldiagrams.Definitions import AttachmentSide
from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import Contents
from pyumldiagrams.Definitions import NoteDefinition
from pyumldiagrams.Definitions import UmlLollipopDefinition
from pyumldiagrams.Definitions import UmlLollipopDefinitions
from pyumldiagrams.Definitions import UmlNoteDefinitions
from pyumldiagrams.Definitions import VisibilityType
from pyumldiagrams.Definitions import DisplayMethodParameters
from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Parameters
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import UmlLineDefinitions
from pyumldiagrams.Definitions import LineType

from pyutplugins.ExternalTypes import OglObjects


NamedAssociations: List[LineType] = [LineType.Association, LineType.Aggregation, LineType.Composition]


class PyUmlDefinitionAdapter:
    """
    This class turns Ogl objects into PyUmlDiagram definitions.  This is
    necessary so that we can call PyUmlDiagram to generated pdf or images
    of Pyut diagrams
    """

    INHERITANCE_DESTINATION_POSITION_NUDGE_FACTOR: int = 1

    # https://www.codetable.net/hex/a
    END_OF_LINE_MARKER: str = '&#xA;'

    def __init__(self):
        """

        """

        self.logger:                  Logger                 = getLogger(__name__)
        self._umlClassDefinitions:    ClassDefinitions       = ClassDefinitions([])
        self._umlLineDefinitions:     UmlLineDefinitions     = UmlLineDefinitions([])
        self._umlLollipopDefinitions: UmlLollipopDefinitions = UmlLollipopDefinitions([])
        self._umlNoteDefinitions:      UmlNoteDefinitions    = UmlNoteDefinitions([])

    @property
    def umlClassDefinitions(self) -> ClassDefinitions:
        return self._umlClassDefinitions

    @property
    def umlLineDefinitions(self) -> UmlLineDefinitions:
        return self._umlLineDefinitions

    @property
    def umlLollipopDefinitions(self) -> UmlLollipopDefinitions:
        return self._umlLollipopDefinitions

    @property
    def umlNoteDefinitions(self) -> UmlNoteDefinitions:
        return self._umlNoteDefinitions

    def toDefinitions(self, oglObjects: OglObjects):

        self._toClassDefinitions(oglObjects=oglObjects)
        self._toLineDefinitions(oglObjects=oglObjects)
        self._toLollipopDefinitions(oglObjects=oglObjects)
        self._toNoteDefinitions(oglObjects=oglObjects)

    def _toClassDefinitions(self, oglObjects: OglObjects):
        """
        We will create class definitions

        Args:
            oglObjects:  All objects
        """
        classDefinitions: ClassDefinitions = ClassDefinitions([])
        for oglObject in oglObjects:

            if not isinstance(oglObject, OglClass):
                continue

            umlObject: OglClass = cast(OglClass, oglObject)
            pyutClass: PyutClass = cast(PyutClass, umlObject.pyutObject)

            x, y = umlObject.GetPosition()
            w, h = umlObject.GetSize()
            position: Position = Position(x=x, y=y)
            size: Size = Size(width=int(w), height=int(h))

            classDefinition: ClassDefinition = ClassDefinition(name=pyutClass.name, position=position, size=size)

            if pyutClass.displayParameters is PyutDisplayParameters.WITH_PARAMETERS:
                classDefinition.displayMethodParameters = DisplayMethodParameters.DISPLAY
            else:
                classDefinition.displayMethodParameters = DisplayMethodParameters.DO_NOT_DISPLAY

            classDefinition = self.__addClassDiagramDisplayPreferences(pyutClass=pyutClass, classDefinition=classDefinition)

            self._addMethods(classDefinition=classDefinition, pyutClass=pyutClass)

            classDefinitions.append(classDefinition)
        self._umlClassDefinitions = classDefinitions

    def _toLineDefinitions(self, oglObjects: OglObjects):

        umlLineDefinitions: UmlLineDefinitions = UmlLineDefinitions([])

        for umlObject in oglObjects:

            if not isinstance(umlObject, OglLink):
                continue
            oglLink: OglLink = cast(OglLink, umlObject)

            pyutLink:    PyutLink     = oglLink.pyutObject
            umlLinkType: PyutLinkType = pyutLink.linkType
            lineType:    LineType     = self._toPyUmlLineType(umlLinkType)

            linePositions: LinePositions  = self._toPyUmlPositions(oglLink, umlLinkType)
            self.logger.debug(f'{lineType=} {linePositions=}')

            line: UmlLineDefinition = UmlLineDefinition(lineType=lineType, linePositions=linePositions)

            if lineType in NamedAssociations:
                oglAssociation: OglAssociation = cast(OglAssociation, oglLink)

                line.name = pyutLink.name
                x, y = oglAssociation.centerLabel.GetRelativePosition()
                line.namePosition = Position(x=x, y=y)

                line.cardinalitySource = pyutLink.sourceCardinality
                x, y = oglAssociation.sourceCardinality.GetRelativePosition()
                line.sourceCardinalityPosition = Position(x=x, y=y)

                line.cardinalityDestination = pyutLink.destinationCardinality
                x, y = oglAssociation.destinationCardinality.GetRelativePosition()
                line.destinationCardinalityPosition = Position(x=x, y=y)

            umlLineDefinitions.append(line)
        self._umlLineDefinitions = umlLineDefinitions

    def _toLollipopDefinitions(self, oglObjects: OglObjects):

        lollipopDefinitions: UmlLollipopDefinitions = UmlLollipopDefinitions([])
        for oglObject in oglObjects:

            if not isinstance(oglObject, OglInterface2):
                continue
            oglInterface2:         OglInterface2         = cast(OglInterface2, oglObject)
            umlLollipopDefinition: UmlLollipopDefinition = UmlLollipopDefinition()
            pyutInterface: PyutInterface = oglInterface2.pyutInterface

            name: str = pyutInterface.name

            destinationAnchor: SelectAnchorPoint = oglInterface2.destinationAnchor
            attachmentPoint = destinationAnchor.attachmentPoint
            x, y = destinationAnchor.GetPosition()

            umlLollipopDefinition.name = name
            umlLollipopDefinition.position = Position(x=x, y=y)
            umlLollipopDefinition.attachmentSide = AttachmentSide.toEnum(attachmentPoint.name)

            lollipopDefinitions.append(umlLollipopDefinition)
        self._umlLollipopDefinitions = lollipopDefinitions

    def _toNoteDefinitions(self, oglObjects: OglObjects):

        noteDefinitions: UmlNoteDefinitions = UmlNoteDefinitions([])
        for oglObject in oglObjects:

            if not isinstance(oglObject, OglNote):
                continue
            oglNote:  OglNote  = cast(OglNote, oglObject)
            pyutNote: PyutNote = oglNote.pyutObject

            umlNoteDefinition: NoteDefinition = NoteDefinition(pyutNote.name)

            x, y = oglNote.GetPosition()
            width, height = oglNote.GetSize()

            umlNoteDefinition.position = Position(x=x, y=y)
            umlNoteDefinition.size     = Size(width=width, height=height)

            rawContent:   str      = pyutNote.content
            cleanContent: str      = rawContent.replace(PyUmlDefinitionAdapter.END_OF_LINE_MARKER, osLineSep)
            lineList:     Contents = cast(Contents, cleanContent.split(osLineSep))  # I am coercive

            umlNoteDefinition.content = Contents(lineList)

            noteDefinitions.append(umlNoteDefinition)
        self._umlNoteDefinitions = noteDefinitions

    def _toPyUmlLineType(self, umlLinkType) -> LineType:

        if umlLinkType == PyutLinkType.INHERITANCE:
            lineType: LineType = LineType.Inheritance
        elif umlLinkType == PyutLinkType.COMPOSITION:
            lineType = LineType.Composition
        elif umlLinkType == PyutLinkType.AGGREGATION:
            lineType = LineType.Aggregation
        elif umlLinkType == PyutLinkType.NOTELINK:
            lineType = LineType.NoteLink
        elif umlLinkType == PyutLinkType.ASSOCIATION:
            lineType = LineType.Association
        elif umlLinkType == PyutLinkType.INTERFACE:
            lineType = LineType.Interface
        else:
            assert False, f'Unknown umlLinkType: {umlLinkType}'

        return lineType

    def _toPyUmlPositions(self, oglLink, pyutLinkType: PyutLinkType) -> LinePositions:

        if pyutLinkType == PyutLinkType.INHERITANCE:
            srcAnchor:  AnchorPoint = oglLink.sourceAnchor
            destAnchor: AnchorPoint = oglLink.destinationAnchor
        else:
            srcAnchor  = oglLink.sourceAnchor
            destAnchor = oglLink.destinationAnchor

        srcX,  srcY  = srcAnchor.GetPosition()
        destX, destY = destAnchor.GetPosition()

        sourcePosition:      Position = Position(x=srcX, y=srcY)
        destinationPosition: Position = Position(x=destX, y=destY)

        bends: List[ControlPoint] = oglLink.GetControlPoints()
        if bends is None or len(bends) == 0:
            linePositions: LinePositions = LinePositions([sourcePosition, destinationPosition])
        else:
            linePositions = LinePositions([sourcePosition])
            for cp in bends:
                bend: ControlPoint = cast(ControlPoint, cp)
                self.logger.debug(f'{bend:}')

                bendX, bendY = bend.GetPosition()
                bendPosition: Position = Position(x=bendX, y=bendY)
                linePositions.append(bendPosition)

            linePositions.append(destinationPosition)

        return linePositions

    def _addMethods(self, classDefinition: ClassDefinition, pyutClass: PyutClass) -> ClassDefinition:

        methods: Methods = Methods([])
        for method in pyutClass.methods:

            pyutMethod: PyutMethod = cast(PyutMethod, method)

            methodDef: MethodDefinition = MethodDefinition(name=pyutMethod.name)

            methodDef.visibility = self.__toVisibilityType(pyutMethod.visibility)
            methodDef.returnType = pyutMethod.returnType.value

            self.__addParameters(methodDefinition=methodDef, pyutMethod=pyutMethod)
            methods.append(methodDef)

        classDefinition.methods = methods
        return classDefinition

    def __addParameters(self, methodDefinition: MethodDefinition, pyutMethod: PyutMethod) -> MethodDefinition:

        parameters: Parameters = Parameters([])
        for parameter in pyutMethod.parameters:

            paramDef: ParameterDefinition = ParameterDefinition(name=parameter.name)
            paramDef.parameterType = parameter.type.value
            paramDef.defaultValue  = parameter.defaultValue

            parameters.append(paramDef)

        methodDefinition.parameters = parameters
        self.logger.debug(f'{methodDefinition.name=}  {parameters=}')
        return methodDefinition

    def __toVisibilityType(self, visibility: PyutVisibility) -> VisibilityType:

        if visibility == PyutVisibility.PUBLIC:
            return VisibilityType.Public
        elif visibility == PyutVisibility.PRIVATE:
            return VisibilityType.Private
        elif visibility == PyutVisibility.PROTECTED:
            return VisibilityType.Protected
        else:
            assert False, 'Unknown UML Visibility type.  Probably developer error'

    def __addClassDiagramDisplayPreferences(self, pyutClass: PyutClass, classDefinition: ClassDefinition) -> ClassDefinition:

        classDefinition.displayMethods    = pyutClass.showMethods
        classDefinition.displayFields     = pyutClass.showFields

        return classDefinition
