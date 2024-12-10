
from typing import cast

from pathlib import Path

from logging import Logger
from logging import getLogger

from wx import ICON_ERROR
from wx import MessageDialog
from wx import OK
from wx import Yield as wxYield

from pyutplugins.ExternalTypes import FrameInformation
from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.ioplugins.mermaid.MermaidWriter import MermaidWriter

from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface
from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse


FORMAT_NAME:        FormatName        = FormatName('Mermaid Markdown')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('md')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Export Ogl to Mermaid Markdown')


class IOMermaid(IOPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._requireSelection = False      # Override base class
        self._autoSelectAll    = True
        # from super class
        self._name    = PluginName('Mermaid Writer')
        self._author  = 'Humberto A. Sanchez II'
        self._version = MermaidWriter.VERSION
        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportResponse: SingleFileRequestResponse = cast(SingleFileRequestResponse, None)
        self._oglObjects:     OglObjects                = cast(OglObjects, None)

    def setImportOptions(self) -> bool:
        return False

    def setExportOptions(self) -> bool:

        self._exportResponse = self.askForFileToExport()

        if self._exportResponse.cancelled is True:
            return False
        else:
            return True

    def read(self) -> bool:
        return False

    def write(self, oglObjects: OglObjects):

        self._oglObjects = oglObjects

        self._pluginAdapter.getFrameInformation(callback=self._frameInformationCallback)
        wxYield()

    def _frameInformationCallback(self, frameInformation: FrameInformation):

        if frameInformation.diagramType == 'CLASS_DIAGRAM':
            fqFileName: str = self._exportResponse.fileName
            self.logger.info(f'Export to {fqFileName=}')

            mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=True)
            mermaidWriter.translate(oglObjects=self._oglObjects)
        else:
            booBoo: MessageDialog = MessageDialog(parent=None, message='Currently Only Class Diagrams export is supported',
                                                  caption='Try Again!', style=OK | ICON_ERROR)
            booBoo.ShowModal()
