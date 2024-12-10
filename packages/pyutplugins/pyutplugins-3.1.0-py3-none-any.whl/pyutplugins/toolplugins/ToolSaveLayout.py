
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import asdict

from json import dumps as jsonDumps

from ogl.OglObject import OglObject

from pyutmodelv2.PyutObject import PyutObject

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension

from pyutplugins.plugintypes.PluginDataTypes import PluginName

from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse
from pyutplugins.toolplugins.savelayout.Layout import Layout
from pyutplugins.toolplugins.savelayout.Layout import LayoutInformation
from pyutplugins.toolplugins.savelayout.Layout import Layouts
from pyutplugins.toolplugins.savelayout.Layout import OglName
from pyutplugins.toolplugins.savelayout.Layout import Position
from pyutplugins.toolplugins.savelayout.Layout import Size
from pyutplugins.toolplugins.savelayout.Layout import layoutsFactory

DEFAULT_FILE_NAME: str = 'DiagramLayout'     # TODO make a plugin option

FORMAT_NAME:        FormatName        = FormatName('Layout File')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('json')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Save Diagram Layout')


class ToolSaveLayout(ToolPluginInterface):

    # noinspection SpellCheckingInspection
    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Save Layout')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '2.0'

        self._menuTitle = 'Save Layout'

        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._outputFileName: str = ''

    def setOptions(self) -> bool:
        """

        Returns:   True when user selects an output filename
        """

        response: SingleFileRequestResponse = self.askForFileToExport(defaultFileName=DEFAULT_FILE_NAME)

        if response.cancelled is True:
            return False
        else:
            self._outputFileName = response.fileName
            return True

    def doAction(self):
        self._pluginAdapter.selectAllOglObjects()
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, oglObjects: OglObjects):

        layouts: Layouts = layoutsFactory()

        oglObject: OglObject = cast(OglObject, None)
        for el in oglObjects:
            if isinstance(el, OglObject):
                try:
                    oglObject = cast(OglObject, el)
                    pyutObject: PyutObject = oglObject.pyutObject

                    if pyutObject.name is None:
                        name: OglName = OglName(f'id: {pyutObject.id}')
                    else:
                        name = OglName(pyutObject.name)
                    x, y = oglObject.GetPosition()
                    w, h = oglObject.GetSize()
                    position: Position = Position(x=x, y=y)
                    size:     Size     = Size(width=w, height=h)
                    layout: Layout = Layout(name=name, position=position, size=size)

                    layouts[name] = layout

                except (AttributeError, TypeError) as e:
                    self.logger.error(f'{e} - {oglObject=}')

        layoutInformation: LayoutInformation = LayoutInformation(layouts=layouts)

        with open(self._outputFileName, 'w') as fd:
            jsonStr: str = jsonDumps(asdict(layoutInformation), indent=4)
            fd.write(jsonStr)

        self._pluginAdapter.deselectAllOglObjects()
