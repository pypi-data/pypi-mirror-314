
from typing import cast

from logging import Logger
from logging import getLogger

from time import localtime
from time import strftime

from pyumldiagrams.BaseDiagram import BaseDiagram
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import DisplayMethodParameters
from pyumldiagrams.Definitions import UmlLineDefinitions
from pyumldiagrams.Definitions import UmlLollipopDefinitions
from pyumldiagrams.Definitions import UmlNoteDefinitions
from pyumldiagrams.image.ImageDiagram import ImageDiagram
from pyumldiagrams.pdf.PdfDiagram import PdfDiagram
from wx import Yield as wxYield


from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface

from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse

from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension

from pyutplugins.ioplugins.pdf.ImageFormat import ImageFormat
from pyutplugins.ioplugins.pdf.ImageOptions import ImageOptions
from pyutplugins.ioplugins.pdf.PyUmlDefinitionAdapter import PyUmlDefinitionAdapter

FORMAT_NAME:        FormatName        = FormatName('PDF')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('pdf')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('A simple PDF for UML diagrams')

PLUGIN_VERSION: str = '1.4'


class IOPdf(IOPluginInterface):
    """
    Set up for PDF generation;  However, with a simple refactor to
    move definition generation and a new subclass we can generate
    png images;  Waiting on pyumldiagrams to be images to support
    Notes and lollipop interfaces
    """
    def __init__(self, pluginAdapter: IPluginAdapter):
        """

        Args:
            pluginAdapter:   A class that implements IMediator
        """
        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name    = PluginName('Output PDF')
        self._author  = "Humberto A. Sanchez II"
        self._version = PLUGIN_VERSION

        self._exportResponse: SingleFileRequestResponse = cast(SingleFileRequestResponse, None)

        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._imageOptions: ImageOptions = ImageOptions()

        self._imageOptions.imageFormat = ImageFormat.PDF

        self._autoSelectAll = True     # we are taking a picture of the entire diagram

    def setImportOptions(self) -> bool:
        return False

    def setExportOptions(self) -> bool:
        """
        Prepare the export.

        Returns:
            if False, the export is cancelled.
        """
        self._exportResponse = self.askForFileToExport(defaultFileName=self._pluginPreferences.pdfExportFileName)

        if self._exportResponse.cancelled is True:
            return False
        else:
            self._imageOptions.outputFileName = self._exportResponse.fileName
            return True

    def read(self) -> bool:
        return False

    def write(self, oglObjects: OglObjects):
        """
        Write data to a file;  Presumably, the file was specified on the call
        to setExportOptions

         Args:
            oglObjects:  list of exported objects

        """
        self.logger.info(f'export file name: {self._imageOptions.outputFileName}')
        wxYield()

        oglToPdf: PyUmlDefinitionAdapter = PyUmlDefinitionAdapter()

        oglToPdf.toDefinitions(oglObjects=oglObjects)

        self._createTheImage(oglToPdf)

    def _createTheImage(self, oglToPdf: PyUmlDefinitionAdapter):
        """
        Loop through the definitions to create the UML Diagram

        Args:
            oglToPdf: The UML definitions
        """

        diagram: BaseDiagram = self._getCorrectDiagramGenerator()

        umlClassDefinitions: ClassDefinitions = oglToPdf.umlClassDefinitions
        for classDefinition in umlClassDefinitions:
            diagram.drawClass(classDefinition=classDefinition)

        umlLineDefinitions: UmlLineDefinitions = oglToPdf.umlLineDefinitions
        for lineDefinition in umlLineDefinitions:
            diagram.drawUmlLine(lineDefinition=lineDefinition)

        lollipopDefinitions: UmlLollipopDefinitions = oglToPdf.umlLollipopDefinitions
        for lollipopDefinition in lollipopDefinitions:
            diagram.drawUmlLollipop(umlLollipopDefinition=lollipopDefinition)

        umlNoteDefinitions: UmlNoteDefinitions = oglToPdf.umlNoteDefinitions
        for umlNoteDefinition in umlNoteDefinitions:
            diagram.drawNote(umlNoteDefinition)

        diagram.write()

    def _getCorrectDiagramGenerator(self) -> BaseDiagram:

        dpi:   int = self._pluginAdapter.screenMetrics.dpiX
        today: str = strftime("%d %b %Y %H:%M:%S", localtime())

        headerText: str = f'Pyut Version {self._pluginAdapter.pyutVersion} Plugin Version {self.version} - {today}'
        imageOptions = self._imageOptions

        fqFileName:  str         = imageOptions.outputFileName
        imageFormat: ImageFormat = imageOptions.imageFormat
        #
        # TODO use plugin preferences
        #
        # imageLibShowParameters: DisplayMethodParameters = self.__toImageLibraryEnum(self._prefs.showParameters)
        imageLibShowParameters: DisplayMethodParameters = self._toImageLibraryEnum(True)
        if imageFormat == ImageFormat.PDF:
            diagram: BaseDiagram = PdfDiagram(fileName=fqFileName, dpi=dpi, headerText=headerText, docDisplayMethodParameters=imageLibShowParameters)
        else:
            diagram = ImageDiagram(fileName=fqFileName, headerText=headerText)   # TODO use image size from new method signature)

        return diagram

    def _toImageLibraryEnum(self, showParameters: bool) -> DisplayMethodParameters:

        if showParameters is True:
            return DisplayMethodParameters.DISPLAY
        else:
            return DisplayMethodParameters.DO_NOT_DISPLAY
