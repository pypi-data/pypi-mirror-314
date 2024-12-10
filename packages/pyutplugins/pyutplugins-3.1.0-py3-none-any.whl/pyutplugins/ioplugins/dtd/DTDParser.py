
from typing import cast
from typing import Dict
from typing import Tuple
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from xml.parsers.expat import ParserCreate
from pyexpat import XMLParserType

from pyutmodelv2.PyutType import PyutType
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutField import PyutField

from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink

from pyutplugins.common.ElementTreeData import ElementTreeData
from pyutplugins.common.LinkMakerMixin import LinkMakerMixin
from pyutplugins.common.PluginTypes import ClassPair
from pyutplugins.common.PluginTypes import ClassTree

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglLinks

from pyutplugins.ioplugins.dtd.DTDAttribute import DTDAttribute
from pyutplugins.ioplugins.dtd.DTDElementTypes import DTDElementTypes

DTDElements   = NewType('DTDElements',   Dict[str, Tuple])
DTDAttributes = NewType('DTDAttributes', List[DTDAttribute])


class DTDParser(LinkMakerMixin):

    MODEL_CHILD_ELEMENT_TYPE_INDEX:                int = 0
    MODEL_CHILD_ELEMENT_NAME_INDEX:                int = 2
    MODEL_CHILD_ELEMENT_ADDITIONAL_ELEMENTS_INDEX: int = 3

    MODEL_CHILDREN_INDEX:           int = 3

    def __init__(self):
        """
        Also, I use the pycharm noinspection pragma because I cannot get the correct
        type imported for the parser; I think because the code is 'generated' with
        some kind of C language binder;

        """
        super().__init__()
        self.logger:    Logger                = getLogger(__name__)

        self._elementTypes:   DTDElements    = DTDElements({})
        self._attributes:     DTDAttributes  = DTDAttributes([])
        self._classTree:      ClassTree      = ClassTree({})
        self._links:          OglLinks       = OglLinks([])
        self._oglClasses:     OglClasses     = OglClasses([])

        # noinspection SpellCheckingInspection
        """
        Due to limitations in the Expat library used by pyexpat, the xmlparser instance returned can
        only be used to parse a single XML document.Call ParserCreate for each document to provide unique
        parser instances.
        """
        self._dtdParser: XMLParserType = ParserCreate()

        # noinspection SpellCheckingInspection
        self._dtdParser.StartDoctypeDeclHandler = self.startDocumentTypeHandler
        # noinspection SpellCheckingInspection
        self._dtdParser.ElementDeclHandler      = self.elementHandler
        # noinspection SpellCheckingInspection
        self._dtdParser.AttlistDeclHandler      = self.attributeListHandler
        # noinspection SpellCheckingInspection
        self._dtdParser.EndDoctypeDeclHandler   = self.endDocumentTypeHandler

    def open(self, filename: str) -> bool:
        """

        Args:
            filename:

        Returns:  'True' if opened and parsed correctly else 'False'

        """
        self.logger.info(f'filename: {filename}')

        with open(filename, "r") as dataFile:
            dtdData: str = dataFile.read()
            self._dtdParser.Parse(dtdData)

        return True

    @property
    def classTree(self) -> ClassTree:
        assert len(self._classTree) != 0, 'You should call open first'
        return self._classTree

    @property
    def oglClasses(self) -> OglClasses:
        if len(self._oglClasses) == 0:
            classTree: ClassTree = self.classTree
            for className in classTree.keys():
                elementTreeData: ElementTreeData = classTree[className]
                self._oglClasses.append(elementTreeData.oglClass)

        return self._oglClasses

    @property
    def links(self) -> OglLinks:
        assert len(self._classTree) != 0, 'You should call open first'  # Maybe does not have any links
        return self._links

    def startDocumentTypeHandler(self, docTypeName, sysId, pubId, hasInternalSubset):

        dbgStr: str = f'startDocTypeHandler - {docTypeName=} {sysId=} {pubId=} {hasInternalSubset=}'
        self.logger.info(dbgStr)

    def elementHandler(self, elementName: str, model):
        # noinspection SpellCheckingInspection
        """

        Args:
            elementName:   Element name
            model:  The element content model in (sep,cont,mod) format, where cont is a list of (name,mod) and (sep,cont,mod) tuples.
            ANY content models are represented as None, and EMPTYs as ("",[],"").

            (name , descr , (attribute | attribute-group-ref)*)
        """
        currentLineNumber: int = self._dtdParser.CurrentLineNumber
        self.logger.debug(f'elementHandler - {currentLineNumber:{2}} name: {elementName:{12}} model: {model}')

        self._elementTypes[elementName] = model

    def attributeListHandler(self, eltName, attrName, attrType, attrValue, valType: int):

        dtdAttribute: DTDAttribute = DTDAttribute()

        dtdAttribute.elementName    = eltName
        dtdAttribute.attributeName  = attrName
        dtdAttribute.attributeType  = attrType
        dtdAttribute.attributeValue = attrValue
        dtdAttribute.valueType      = valType

        self.logger.debug(dtdAttribute)

        self._attributes.append(dtdAttribute)

    def endDocumentTypeHandler(self):

        self._classTree = self._createClassTree()
        self.logger.debug(f'elementsTree: {self._classTree}')
        self._addAttributesToClasses()
        self._addLinks()

        self.logger.info(f'attributes: {self._attributes}')

    def _createClassTree(self) -> ClassTree:

        elementsTree: ClassTree = ClassTree({})
        x: int = 50
        y: int = 50

        for eltName in list(self._elementTypes.keys()):

            classPair: ClassPair = self._createClassPair(name=eltName, x=x, y=y)
            pyutClass: PyutClass = classPair.pyutClass
            oglClass:  OglClass  = classPair.oglClass

            elementTreeData: ElementTreeData = ElementTreeData(pyutClass=pyutClass, oglClass=oglClass)

            model = self._elementTypes[eltName]
            # noinspection SpellCheckingInspection
            chillunNames: List[str] = self._getChildElementNames(eltName=eltName, model=model)
            elementTreeData.childElementNames = chillunNames

            elementsTree[eltName] = elementTreeData

            # Carefully, update the graphics layout
            if x < 800:
                x += 80
            else:
                x = 80
                y += 80

        return elementsTree

    def _addLinks(self):

        for className in list(self._classTree.keys()):

            eltTreeData: ElementTreeData = self._classTree[className]

            for associatedClassName in eltTreeData.childElementNames:

                self.logger.info(f'{className} associated with {associatedClassName}')

                parent:      OglClass = eltTreeData.oglClass
                dstTreeData: ElementTreeData = self._classTree[associatedClassName]
                child:       OglClass = dstTreeData.oglClass

                link: OglLink = self.createLink(parent, child, PyutLinkType.AGGREGATION)

                self._links.append(link)

    def _addAttributesToClasses(self):

        for classAttr in self._attributes:
            typedAttr: DTDAttribute   = cast(DTDAttribute, classAttr)
            className: str            = typedAttr.elementName
            treeData: ElementTreeData = self._classTree[className]
            attrName: str             = typedAttr.attributeName
            attrType: str             = typedAttr.attributeType
            attrValue: str            = typedAttr.attributeValue

            pyutField: PyutField = PyutField(name=attrName,
                                             type=PyutType(value=attrType),
                                             defaultValue=attrValue,
                                             visibility=PyutVisibility.PUBLIC)

            self.logger.info(f'pyutField: {pyutField}')
            pyutClass: PyutClass = treeData.pyutClass
            pyutClass.addField(pyutField)

    def _getChildElementNames(self, eltName, model) -> List[str]:

        self.logger.debug(f'_getChildElementNames - {eltName=}\n {model[0]=}\n {model[1]=}\n {model[2]=}\n {model[3]=}')

        children = model[DTDParser.MODEL_CHILDREN_INDEX]
        self.logger.info(f'children {children}')
        # noinspection SpellCheckingInspection
        chillunNames: List[str] = []
        for child in children:

            self.logger.info(f'eltName: {eltName} - child Length {len(child)}')

            dtdElementType: DTDElementTypes = DTDElementTypes(child[DTDParser.MODEL_CHILD_ELEMENT_TYPE_INDEX])
            childName = child[DTDParser.MODEL_CHILD_ELEMENT_NAME_INDEX]
            self.logger.info(f'eltName: {eltName} child: `{child}` eltType: `{dtdElementType.__repr__()}` childName: `{childName}`')
            additionalElements = child[DTDParser.MODEL_CHILD_ELEMENT_ADDITIONAL_ELEMENTS_INDEX]
            if len(additionalElements) != 0:
                for additionChildren in additionalElements:
                    additionalChildName = additionChildren[DTDParser.MODEL_CHILD_ELEMENT_NAME_INDEX]
                    chillunNames.append(additionalChildName)
            else:
                chillunNames.append(childName)

        self.logger.info(f'Children names: {chillunNames}')
        return chillunNames

    def _createClassPair(self, name: str, x: int, y: int) -> ClassPair:
        """
        Create a pair of classes (pyutClass and oglClass)

        TODO:  This method may belong in a common place for plugin development.

        Args:
            name: Class Name

            x:  x-coordinate on the uml frame  oglClass
            y:  y coordinate on the uml frame  oglClass

        Returns: The class pair
        """
        pyutClass: PyutClass = PyutClass()
        pyutClass.name = name

        oglClass: OglClass = OglClass(pyutClass, 50, 50)
        # To make this code capable of being debugged
        oglClass.SetPosition(x=x, y=y)
        # self.addShape(oglClass, x, y)     # TODO:  adding to UML frame does not belong here

        classPair: ClassPair = ClassPair(pyutClass=pyutClass, oglClass=oglClass)

        return classPair
