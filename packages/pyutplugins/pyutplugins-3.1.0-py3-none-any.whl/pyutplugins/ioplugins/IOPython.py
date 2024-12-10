
from typing import cast
from typing import Dict
from typing import List

from logging import Logger
from logging import getLogger

from os import sep as osSep

from wx import ICON_ERROR
from wx import OK
from wx import PD_APP_MODAL
from wx import PD_ELAPSED_TIME

from wx import MessageBox
from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import ProgressDialog

from wx import Yield as wxYield

from pyutmodelv2.PyutClass import PyutClass

from ogl.OglClass import OglClass

from pyutplugins.IPluginAdapter import IPluginAdapter
#
# TODO: Don't worry about this internal type; Will be fixed when we your the model type
#
from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClasses

from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription

from pyutplugins.plugintypes.ExportDirectoryResponse import ExportDirectoryResponse
from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat

from pyutplugins.ioplugins.python.PythonParseException import PythonParseException

from pyutplugins.ioplugins.python.PyutToPython import MethodsCodeType
from pyutplugins.ioplugins.python.PyutToPython import PyutToPython

from pyutplugins.ioplugins.python.ReverseEngineerPythonV3 import ReverseEngineerPythonV3
from pyutplugins.ioplugins.python.ReverseEngineerPythonV3 import OglClassesDict

from pyutplugins.ioplugins.python.DlgSelectMultiplePackages import DlgSelectMultiplePackages
from pyutplugins.ioplugins.python.DlgSelectMultiplePackages import ImportPackages
from pyutplugins.ioplugins.python.DlgSelectMultiplePackages import Package


FORMAT_NAME:        FormatName        = FormatName("Python File(s)")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('py')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Python code generation and reverse engineering')


class IOPython(IOPluginInterface):

    PLUGIN_VERSION: str = '2.0'

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        # from super class
        self._name    = PluginName('IOPython')
        self._author  = 'Humberto A. Sanchez II'
        self._version = IOPython.PLUGIN_VERSION
        self._inputFormat  = InputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportDirectoryName: str            = ''

        self._importPackages: ImportPackages = ImportPackages([])
        self._packageCount:   int = 0
        self._moduleCount:    int = 0

        self._readProgressDlg:     ProgressDialog = cast(ProgressDialog, None)

    def setImportOptions(self) -> bool:
        """
        We do need to ask for the input file names

        Returns:  'True', we support import
        """
        # TODO: update startDirectory when this is done: https://github.com/hasii2011/pyutplugins/issues/106
        with DlgSelectMultiplePackages(startDirectory='/Users/humberto.a.sanchez.ii/pyut-diagrams', inputFormat=self.inputFormat) as dlg:
            if dlg.ShowModal() == OK:
                self._packageCount   = dlg.packageCount
                self._moduleCount    = dlg.moduleCount
                self._importPackages = dlg.importPackages

                return True
            else:
                return False

    def setExportOptions(self) -> bool:
        response: ExportDirectoryResponse = self.askForExportDirectoryName(preferredDefaultPath=None)
        if response.cancelled is True:
            return False
        else:
            self._exportDirectoryName = response.directoryName
            return True

    def read(self) -> bool:
        """

        Returns:
        """
        BeginBusyCursor()
        wxYield()
        status: bool = True
        try:
            self._readProgressDlg = ProgressDialog('Parsing Files', 'Starting', parent=None, style=PD_APP_MODAL | PD_ELAPSED_TIME)
            reverseEngineer: ReverseEngineerPythonV3 = ReverseEngineerPythonV3()

            self._readProgressDlg.SetRange(self._moduleCount)

            pyutClasses: PyutClasses = self._collectPyutClassesInPass1(reverseEngineer=reverseEngineer)
            pyutClasses              = self._enhancePyutClassesInPass2(reverseEngineer=reverseEngineer, pyutClasses=pyutClasses)

            oglClassesDict: OglClassesDict = reverseEngineer.generateOglClasses(pyutClasses)
            reverseEngineer.generateLinks(oglClassesDict)

            self._layoutUmlClasses(oglClasses=OglClasses(list(oglClassesDict.values())))
            self._layoutLinks(oglLinks=reverseEngineer.oglLinks)
        except (ValueError, Exception, PythonParseException) as e:
            self._readProgressDlg.Destroy()
            MessageBox(f'{e}', 'Error', OK | ICON_ERROR)
            status = False
        else:
            self._readProgressDlg.Destroy()
            self._pluginAdapter.indicatePluginModifiedProject()
        finally:
            EndBusyCursor()
            self._pluginAdapter.refreshFrame()
            wxYield()

        return status

    def write(self, oglObjects: OglObjects):

        directoryName: str = self._exportDirectoryName

        self.logger.info("IoPython Saving...")
        pyutToPython: PyutToPython = PyutToPython()
        classes:           Dict[str, List[str]] = {}
        generatedClassDoc: List[str]            = pyutToPython.generateTopCode()
        # oglClasses: OglClasses = self._communicator.selectedOglObjects

        for oglClass in oglObjects:
            if isinstance(oglClass, OglClass):
                pyutClass:          PyutClass = oglClass.pyutObject
                generatedStanza:    str       = pyutToPython.generateClassStanza(pyutClass)
                generatedClassCode: List[str] = [generatedStanza]

                clsMethods: MethodsCodeType = pyutToPython.generateMethodsCode(pyutClass)

                # Add __init__ Method
                if PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR in clsMethods:
                    methodCode = clsMethods[PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR]
                    generatedClassCode += methodCode
                    del clsMethods[PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR]

                # Add others methods in order
                for pyutMethod in pyutClass.methods:
                    methodName: str = pyutMethod.name
                    if methodName != PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR:
                        try:
                            otherMethodCode: List[str] = clsMethods[methodName]
                            generatedClassCode += otherMethodCode
                        except (ValueError, Exception, KeyError) as e:
                            self.logger.warning(f'{e}')

                generatedClassCode.append("\n\n")
                # Save into classes dictionary
                classes[pyutClass.name] = generatedClassCode

        # Write class code to a file
        for (className, classCode) in list(classes.items()):
            self._writeClassToFile(classCode, className, directoryName, generatedClassDoc)

        self.logger.info("IoPython done !")

    def _collectPyutClassesInPass1(self, reverseEngineer: ReverseEngineerPythonV3) -> PyutClasses:

        cumulativePyutClasses: PyutClasses = PyutClasses({})
        for directory in self._importPackages:
            importPackage: Package = cast(Package, directory)

            currentPyutClasses: PyutClasses = reverseEngineer.doPass1(directoryName=importPackage.packageName,
                                                                      files=importPackage.moduleToImport,
                                                                      progressCallback=self._readProgressCallback)

            cumulativePyutClasses = PyutClasses(cumulativePyutClasses | currentPyutClasses)

        return cumulativePyutClasses

    def _enhancePyutClassesInPass2(self, reverseEngineer: ReverseEngineerPythonV3, pyutClasses: PyutClasses) -> PyutClasses:

        updatedPyutClasses: PyutClasses = PyutClasses({})
        for directory in self._importPackages:
            importPackage: Package = cast(Package, directory)

            updatedPyutClasses = reverseEngineer.doPass2(directoryName=importPackage.packageName,
                                                         files=importPackage.moduleToImport,
                                                         pyutClasses=pyutClasses,
                                                         progressCallback=self._readProgressCallback)

        return updatedPyutClasses

    def _writeClassToFile(self, classCode, className, directory, generatedClassDoc):

        filename: str = f'{directory}{osSep}{str(className)}.py'

        file = open(filename, "w")
        file.writelines(generatedClassDoc)
        file.writelines(classCode)

        file.close()

    def _readProgressCallback(self, currentFileCount: int, msg: str):
        """

        Args:
            currentFileCount:   The current file # we are working pm
            msg:    An updated message
        """

        self._readProgressDlg.Update(currentFileCount, msg)
