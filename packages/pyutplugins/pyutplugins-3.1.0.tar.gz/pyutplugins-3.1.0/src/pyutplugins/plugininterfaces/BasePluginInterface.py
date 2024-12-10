
from typing import Optional

from wx import DD_NEW_DIR_BUTTON
from wx import FD_OPEN
from wx import FD_MULTIPLE
from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE
from wx import ICON_ERROR
from wx import ID_CANCEL
from wx import OK

from wx import DirDialog
from wx import FileDialog
from wx import FileSelector
from wx import MessageDialog
from wx import Yield as wxYield

from pyutplugins.preferences.PluginPreferences import PluginPreferences

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglLinks
from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.ExportDirectoryResponse import ExportDirectoryResponse
from pyutplugins.plugintypes.ImportDirectoryResponse import ImportDirectoryResponse
from pyutplugins.plugintypes.MultipleFileRequestResponse import MultipleFileRequestResponse
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse

from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginName

UNSPECIFIED_NAME:        FormatName        = FormatName('Unspecified Plugin Name')
UNSPECIFIED_EXTENSION:   PluginExtension   = PluginExtension('*')
UNSPECIFIED_DESCRIPTION: PluginDescription = PluginDescription('Unspecified Plugin Description')


class BasePluginInterface:
    """
    This is meant to provide base properties and methods for the Input/Output
    pyutplugins and the Tool Plugins

    Implementations set the protected variables during class construction

    There should be no implementations of this interface
    """

    def __init__(self, pluginAdapter: IPluginAdapter):
        """
        Menu handlers may instantiate a plugin merely to get plugin information.  In that case,
        the input parameter will be None

        Args:
            pluginAdapter:   A class that implements ICommunicator

        """
        self._pluginAdapter:     IPluginAdapter    = pluginAdapter
        self._pluginPreferences: PluginPreferences = PluginPreferences()

        #
        # To be set by implementor constructor and read by property
        self._name:         PluginName = PluginName('Implementor must provide the plugin name')
        self._author:       str = 'Implementor must provide the plugin author'
        self._version:      str = 'Implementor must provide the version'
        self._inputFormat:  InputFormat  = InputFormat(formatName=UNSPECIFIED_NAME, extension=UNSPECIFIED_EXTENSION, description=UNSPECIFIED_DESCRIPTION)
        self._outputFormat: OutputFormat = OutputFormat(formatName=UNSPECIFIED_NAME, extension=UNSPECIFIED_EXTENSION, description=UNSPECIFIED_DESCRIPTION)

    @property
    def name(self) -> PluginName:
        """
        Implementations set the protected variable at class construction

        Returns:  The plugin name
        """
        return self._name

    @property
    def author(self) -> str:
        """
        Implementations set the protected variable at class construction

        Returns:  The author's name
        """
        return self._author

    @property
    def version(self) -> str:
        """
        Implementations set the protected variable at class construction

        Returns: The plugin version string
        """
        return self._version

    @property
    def inputFormat(self) -> InputFormat:
        """
        Implementations set the protected variable at class construction

        Returns: The input format type; Plugins should return `None` if they do
        not support input operations
        """
        return self._inputFormat

    @property
    def outputFormat(self) -> OutputFormat:
        """
        Implementations set the protected variable at class construction

        Returns: The output format type;  Plugins should return `None` if they do
        not support output operations
        """
        return self._outputFormat

    @classmethod
    def displayNoUmlFrame(cls):
        booBoo: MessageDialog = MessageDialog(parent=None, message='No UML frame', caption='Try Again!', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    @classmethod
    def displayNoSelectedOglObjects(cls):
        booBoo: MessageDialog = MessageDialog(parent=None, message='No selected UML objects', caption='Try Again!', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def askForFileToImport(self, startDirectory: str | None) -> SingleFileRequestResponse:
        """
        Called by plugin to ask for a file to import

        Args:
            startDirectory: The directory to display

        Returns:  The request response
        """
        defaultDir:  Optional[str] = startDirectory

        if defaultDir is None:
            defaultDir = self._pluginAdapter.currentDirectory
        file = FileSelector(
            "Choose a file to import",
            # wildcard=inputFormat.name + " (*." + inputFormat.extension + ")|*." + inputFormat.description,
            default_path=defaultDir,
            wildcard=self.__composeWildCardSpecification(),
            flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR
        )
        response: SingleFileRequestResponse = SingleFileRequestResponse()
        if file == '':
            response.cancelled = True
            response.fileName  = ''
        else:
            response.cancelled = False
            response.fileName = file

        return response

    def askToImportMultipleFiles(self, startDirectory: str | None) -> MultipleFileRequestResponse:
        """
        This method determines how to filter the input files via the Plugin Input
        format specification.
        Args:
            startDirectory:   The initial directory to display

        Returns:  The request response
        """
        defaultDir:  Optional[str] = startDirectory

        if defaultDir is None:
            defaultDir = self._pluginAdapter.currentDirectory

        dlg: FileDialog = FileDialog(
            None,
            "Choose files to import",
            wildcard=self.__composeWildCardSpecification(),
            defaultDir=defaultDir,
            style=FD_OPEN | FD_FILE_MUST_EXIST | FD_MULTIPLE | FD_CHANGE_DIR
        )
        dlg.ShowModal()
        response: MultipleFileRequestResponse = MultipleFileRequestResponse()
        if dlg.GetReturnCode() == ID_CANCEL:
            response.directoryName = ''
            response.fileList      = []
            response.cancelled     = True
        else:
            response.directoryName = dlg.GetDirectory()
            response.fileList      = dlg.GetFilenames()
            response.cancelled     = False

        return response

    def askForFileToExport(self, defaultFileName: str = '') -> SingleFileRequestResponse:
        """
        Called by a plugin to ask for the export filename

        Returns: The appropriate response object
        """
        wxYield()

        outputFormat: OutputFormat = self.outputFormat

        wildCard:    str = f'{outputFormat.formatName} (*.{outputFormat.extension}) |*.{outputFormat.extension}'
        fileName:    str = FileSelector("Choose export file name",
                                        default_filename=defaultFileName,
                                        wildcard=wildCard,
                                        flags=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR)

        response: SingleFileRequestResponse = SingleFileRequestResponse(cancelled=False)
        if fileName == '':
            response.fileName  = ''
            response.cancelled = True
        else:
            response.fileName = fileName

        return response

    def askForImportDirectoryName(self) -> ImportDirectoryResponse:
        """
        Called by plugin to ask which directory must be imported

        Returns:  The appropriate response object;  The directory name is valid only if
        response.cancelled is True
        """
        dirDialog: DirDialog = DirDialog(None,
                                         "Choose a directory to import",
                                         defaultPath=self._pluginAdapter.currentDirectory,
                                         style=DD_NEW_DIR_BUTTON)

        response: ImportDirectoryResponse = ImportDirectoryResponse()
        if dirDialog.ShowModal() == ID_CANCEL:
            response.cancelled     = True
            response.directoryName = ''
        else:
            response.directoryName = dirDialog.GetPath()
            response.cancelled     = False
            # self._pluginAdapter.currentDirectory = response.directoryName    # TODO: Should plugin be doing this?  No

        dirDialog.Destroy()

        return response

    def askForExportDirectoryName(self, preferredDefaultPath: str | None) -> ExportDirectoryResponse:
        """
        Called by plugin to ask for an output directory
        Args:
            preferredDefaultPath:

        Returns:  The appropriate response object;  The directory name is valid only if
        response.cancelled is True
        """
        if preferredDefaultPath is None:
            defaultPath: str = self._pluginAdapter.currentDirectory
        else:
            defaultPath = preferredDefaultPath

        dirDialog: DirDialog = DirDialog(None, "Choose a destination directory", defaultPath=defaultPath)

        response: ExportDirectoryResponse = ExportDirectoryResponse(cancelled=False)
        if dirDialog.ShowModal() == ID_CANCEL:
            dirDialog.Destroy()
            response.directoryName = ''
            response.cancelled     = True
        else:
            directory = dirDialog.GetPath()
            # self._pluginAdapter.currentDirectory = directory     # TODO  Should a plugin do this;  No
            dirDialog.Destroy()
            response.directoryName = directory

        return response

    def _layoutUmlClasses(self, oglClasses: OglClasses):
        """
        Organize by vertical descending sizes

        Args:
            oglClasses
        """
        # Sort by descending height
        # noinspection PyProtectedMember
        sortedOglClasses = sorted(oglClasses, key=lambda oglClassToSort: oglClassToSort._height, reverse=True)

        x: int = 20
        y: int = 20

        incY: int = 0
        for oglClass in sortedOglClasses:
            incX, sy = oglClass.GetSize()
            incX += 20
            sy += 20
            incY = max(incY, int(sy))
            # find good coordinates
            if x + incX >= 3000:
                x = 20
                y += incY
                incY = int(sy)
            oglClass.SetPosition(x, y)
            x += incX
            self._pluginAdapter.addShape(shape=oglClass)
        self._pluginAdapter.refreshFrame()

    def _layoutLinks(self, oglLinks: OglLinks):

        # umlDiagram = umlFrame.GetDiagram()

        for oglLink in oglLinks:
            self._pluginAdapter.addShape(oglLink)

            # umlDiagram.AddShape(oglLink.sourceAnchor)
            # umlDiagram.AddShape(oglLink.destinationAnchor)

        self._pluginAdapter.refreshFrame()

    def __composeWildCardSpecification(self) -> str:

        inputFormat: InputFormat = self.inputFormat

        # wildcard: str = inputFormat.name + " (*." + inputFormat.extension + ")|*." + inputFormat.description
        wildcard: str = (
            f'{inputFormat.formatName} '
            f' (*, {inputFormat.extension}) '
            f'|*.{inputFormat.extension}'
        )
        return wildcard
