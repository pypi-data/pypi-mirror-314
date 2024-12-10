
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CENTRE
from wx import ICON_QUESTION
from wx import YES
from wx import YES_NO

from wx import MessageBox

from wx import Yield as wxYield

from oglio.Reader import Reader
from oglio.Writer import Writer
from oglio.Types import OglProject
from oglio.Types import OglDocument
from oglio.Types import OglDocuments
from oglio.Types import OglDocumentTitle

from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface

from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglLinks
from pyutplugins.ExternalTypes import OglSDInstances
from pyutplugins.ExternalTypes import OglSDMessages
from pyutplugins.ExternalTypes import OglTexts
from pyutplugins.ExternalTypes import OglActors
from pyutplugins.ExternalTypes import OglNotes
from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.ExternalTypes import OglUseCases
from pyutplugins.ExternalTypes import PluginDocument
from pyutplugins.ExternalTypes import PluginDocumentType
from pyutplugins.ExternalTypes import PluginDocumentTitle
from pyutplugins.ExternalTypes import PluginProject

FORMAT_NAME:        FormatName        = FormatName("XML")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('xml')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Pyut XML File')


class IOXml(IOPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        self.logger: Logger = getLogger(__name__)

        super().__init__(pluginAdapter=pluginAdapter)

        # from super class
        self._name    = PluginName('IOXml')
        # noinspection SpellCheckingInspection
        self._author  = "Humberto A. Sanchez II"
        self._version = '2.0'
        self._inputFormat  = InputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._prettyPrint:  bool = True
        self._fileToExport: str  = ''
        self._fileToImport: str  = ''

        self._requireActiveFrame = False
        self._requireSelection   = False

    def setImportOptions(self) -> bool:
        """
        We do need to ask for the input file names

        Returns:  'True', we support import
        """
        response: SingleFileRequestResponse = self.askForFileToImport(startDirectory=None)
        if response.cancelled is True:
            return False
        else:
            self._fileToImport   = response.fileName

        return True

    def setExportOptions(self) -> bool:
        """
        Prepare the export.

        Returns:
        """
        prettPrintAnswer: int = MessageBox("Do you want pretty xml ?", "Export option", style=YES_NO | CANCEL | CENTRE | ICON_QUESTION)

        if prettPrintAnswer is YES:
            self._prettyPrint = True
        else:
            self._prettyPrint = False

        response: SingleFileRequestResponse = self.askForFileToExport()
        if response.cancelled is True:
            exportAnswer: bool = False
        else:
            self._fileToExport = response.fileName
            exportAnswer = True

        return exportAnswer

    def read(self) -> bool:
        reader: Reader = Reader()

        oglProject: OglProject = reader.readXmlFile(fqFileName=self._fileToImport)

        pluginProject: PluginProject = PluginProject()

        pluginProject.fileName    = self._fileToImport
        pluginProject.projectName = PluginProject.toProjectName(fqFilename=self._fileToImport)
        pluginProject.version     = oglProject.version
        pluginProject.codePath    = oglProject.codePath

        oglDocuments: OglDocuments = oglProject.oglDocuments
        for oglDocument in oglDocuments.values():
            pluginDocument: PluginDocument = PluginDocument()
            pluginDocument.documentType    = PluginDocumentType.toEnum(oglDocument.documentType)
            pluginDocument.documentTitle   = PluginDocumentTitle(oglDocument.documentTitle)
            pluginDocument.scrollPositionX = oglDocument.scrollPositionX
            pluginDocument.scrollPositionY = oglDocument.scrollPositionY
            pluginDocument.pixelsPerUnitX  = oglDocument.pixelsPerUnitX
            pluginDocument.pixelsPerUnitY  = oglDocument.pixelsPerUnitY
            pluginDocument.oglClasses      = cast(OglClasses,     oglDocument.oglClasses)
            pluginDocument.oglLinks        = cast(OglLinks,       oglDocument.oglLinks)
            pluginDocument.oglNotes        = cast(OglNotes,       oglDocument.oglNotes)
            pluginDocument.oglTexts        = cast(OglTexts,       oglDocument.oglTexts)
            pluginDocument.oglActors       = cast(OglActors,      oglDocument.oglActors)
            pluginDocument.oglUseCases     = cast(OglUseCases,    oglDocument.oglUseCases)
            pluginDocument.oglSDInstances  = cast(OglSDInstances, oglDocument.oglSDInstances)
            pluginDocument.oglSDMessages   = cast(OglSDMessages,  oglDocument.oglSDMessages)

            pluginProject.pluginDocuments[pluginDocument.documentTitle] = pluginDocument

        self._pluginAdapter.loadProject(pluginProject=pluginProject)
        wxYield()
        self._pluginAdapter.indicatePluginModifiedProject()
        return True

    def write(self, oglObjects: OglObjects):
        """
        Ignoring the input objects since they are from a single frame
        Args:
            oglObjects:
        """

        self._pluginAdapter.requestCurrentProject(callback=self._currentProjectCallback)

    def _currentProjectCallback(self, pluginProject: PluginProject):

        import oglio
        assert isinstance(pluginProject, PluginProject)

        oglProject: OglProject = OglProject()

        oglProject.version  = pluginProject.version
        oglProject.codePath = pluginProject.codePath
        oglProject.fileName = pluginProject.fileName

        for document in pluginProject.pluginDocuments.values():
            pluginDocument: PluginDocument = cast(PluginDocument, document)
            oglDocument:    OglDocument    = OglDocument()

            oglDocument.scrollPositionX = pluginDocument.scrollPositionX
            oglDocument.scrollPositionY = pluginDocument.scrollPositionY
            oglDocument.pixelsPerUnitX  = pluginDocument.pixelsPerUnitX
            oglDocument.pixelsPerUnitY  = pluginDocument.pixelsPerUnitY
            oglDocument.documentTitle   = OglDocumentTitle(pluginDocument.documentTitle)
            oglDocument.documentType    = pluginDocument.documentType.value
            oglDocument.oglClasses      = cast(oglio.Types.OglClasses, pluginDocument.oglClasses)
            oglDocument.oglLinks        = cast(oglio.Types.OglLinks, pluginDocument.oglLinks)
            oglDocument.oglNotes        = cast(oglio.Types.OglNotes, pluginDocument.oglNotes)
            oglDocument.oglTexts        = cast(oglio.Types.OglTexts, pluginDocument.oglTexts)
            oglDocument.oglActors       = cast(oglio.Types.OglActors, pluginDocument.oglActors)
            oglDocument.oglUseCases     = cast(oglio.Types.OglUseCases, pluginDocument.oglUseCases)
            oglDocument.oglSDMessages   = cast(oglio.Types.OglSDMessages, pluginDocument.oglSDMessages)
            oglDocument.oglSDInstances  = cast(oglio.Types.OglSDInstances, pluginDocument.oglSDInstances)

            self.logger.debug(f'{oglDocument=}')

            oglProject.oglDocuments[oglDocument.documentTitle] = oglDocument

        writer:     Writer = Writer()

        writer.writeXmlFile(oglProject=oglProject, fqFileName=self._fileToExport, prettyXml=self._prettyPrint)
