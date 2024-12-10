
from logging import Logger
from logging import getLogger

from json import load as jsonLoad
from typing import cast

from ogl.OglObject import OglObject
from pyutmodelv2.PyutObject import PyutObject

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse

from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginName

from pyutplugins.toolplugins.savelayout.Layout import Layout
from pyutplugins.toolplugins.savelayout.Layout import LayoutInformation
from pyutplugins.toolplugins.savelayout.Layout import Layouts
from pyutplugins.toolplugins.savelayout.Layout import OglName
from pyutplugins.toolplugins.savelayout.Layout import Position
from pyutplugins.toolplugins.savelayout.Layout import Size


FORMAT_NAME:        FormatName        = FormatName('Layout File')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('json')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Load Diagram Layout')


class ToolLoadLayout(ToolPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Save Layout')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '2.0'
        self._menuTitle = 'Load Layout'

        self._inputFormat = InputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._inputFileName: str = ''

    def setOptions(self) -> bool:

        proceed: bool = False
        response: SingleFileRequestResponse = self.askForFileToImport(startDirectory=self._pluginAdapter.currentDirectory)
        if response.cancelled is False:
            proceed = True
            self._inputFileName = response.fileName

        return proceed

    def doAction(self):
        self._pluginAdapter.selectAllOglObjects()
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, oglObjects: OglObjects):

        layoutInformation: LayoutInformation = self._loadLayoutInformation()
        layouts:           Layouts           = layoutInformation.layouts
        keys = layouts.keys()
        for o in oglObjects:
            if isinstance(o, OglObject):

                oglObject:  OglObject  = cast(OglObject, o)
                pyutObject: PyutObject = oglObject.pyutObject
                name:       OglName    = OglName(pyutObject.name)

                if name in keys:
                    layout:   Layout   = layouts[name]
                    size:     Size     = layout.size
                    position: Position = layout.position

                    oglObject.SetSize(width=size.width, height=size.height)
                    oglObject.SetPosition(x=position.x, y=position.y)

        self._pluginAdapter.deselectAllOglObjects()
        self._pluginAdapter.refreshFrame()

    def _loadLayoutInformation(self) -> LayoutInformation:

        with open(self._inputFileName, 'r') as fd:
            layoutsDict = jsonLoad(fp=fd)

        layoutInformation: LayoutInformation = LayoutInformation()

        self.logger.info(f'{layoutsDict=}')
        layoutsDict = layoutsDict['layouts']

        for layoutDict in layoutsDict.values():

            self.logger.info(f'{layoutDict=}')

            layout: Layout = self._toLayout(layoutDict=layoutDict)
            layoutInformation.layouts[layout.name] = layout

        self.logger.info(f'dataclass={layoutInformation}')

        return layoutInformation

    def _toLayout(self, layoutDict) -> Layout:

        positionDict = layoutDict['position']
        sizeDict     = layoutDict['size']

        name: OglName = layoutDict['name']

        x: int = int(positionDict['x'])
        y: int = int(positionDict['y'])

        width:  int = int(sizeDict['width'])
        height: int = int(sizeDict['height'])

        position: Position = Position(x=x, y=y)
        size:     Size     = Size(width=width, height=height)

        layout: Layout = Layout(name=name, position=position, size=size)

        return layout
