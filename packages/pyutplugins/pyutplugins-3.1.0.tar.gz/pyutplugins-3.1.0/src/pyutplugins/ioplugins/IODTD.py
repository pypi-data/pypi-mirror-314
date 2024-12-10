
from typing import cast

from wx import Yield as wxYield

from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglLinks
from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface

from pyutplugins.ioplugins.dtd.DTDParser import DTDParser

FORMAT_NAME:        FormatName        = FormatName("DTD")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('dtd')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('W3C DTD 1.0 file format')


class IODTD(IOPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):
        super().__init__(pluginAdapter)

        # from super class
        self._name    = PluginName('IoDTD')
        self._author  = "C.Dutoit <dutoitc@hotmail.com>"
        self._version = '1.0'
        self._inputFormat  = InputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = cast(OutputFormat, None)

        self._fileToImport: str = ''

    def setImportOptions(self) -> bool:
        """
        We do need to ask for the input file name

        Returns:  'True', we support import
        """
        response: SingleFileRequestResponse = self.askForFileToImport(startDirectory=None)
        if response.cancelled is True:
            return False
        else:
            self._fileToImport = response.fileName

        return True

    def setExportOptions(self) -> bool:
        return False

    def read(self) -> bool:
        """

        Returns:  True if import succeeded, False if error or cancelled
        """
        filename: str = self._fileToImport

        dtdParser: DTDParser = DTDParser()

        dtdParser.open(filename=filename)

        oglClasses: OglClasses = dtdParser.oglClasses
        for oglClass in oglClasses:
            self._pluginAdapter.addShape(oglClass)

        oglLinks: OglLinks = dtdParser.links
        for oglLink in oglLinks:
            self._pluginAdapter.addShape(oglLink)

        self._pluginAdapter.refreshFrame()
        wxYield()
        self._pluginAdapter.indicatePluginModifiedProject()

        return True

    def write(self, oglObjects: OglObjects):
        """

        Args:
            oglObjects:

        Returns:  False, write not supported

        """
        return False
