
from typing import TextIO
from typing import cast

from math import ceil
from math import floor

from os import sep as osSep

from logging import Logger
from logging import getLogger

from pyutmodelv2.PyutClass import PyutClass

from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype

from ogl.OglClass import OglClass

from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface
from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat

from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.plugintypes.ExportDirectoryResponse import ExportDirectoryResponse

from pyutplugins.ExternalTypes import OglObjects


FORMAT_NAME:        FormatName        = FormatName('Ascii')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('ascii')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Export OGL as ASCII')


class IOAscii(IOPluginInterface):
    """
    Write ASCII and can read ASCII
    This just the skeleton.  Not sure if I want to do this
    """

    def __init__(self, pluginAdapter: IPluginAdapter):
        """

        Args:
            pluginAdapter:   A class that implements IPluginAdapter
        """
        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name    = PluginName('ASCII Class Export')
        self._author  = 'Philippe Waelti & Humberto A. Sanchez II>'
        self._version = '2.0'

        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportDirectory: str = ''

    def setImportOptions(self) -> bool:
        """
        We do not support import
        Returns:  False
        """
        return False

    def setExportOptions(self) -> bool:

        response: ExportDirectoryResponse = self.askForExportDirectoryName(preferredDefaultPath=None)
        if response.cancelled is True:
            return False
        else:
            self._exportDirectory = response.directoryName
            self.logger.debug(f'selectedDir: {self._exportDirectory}')
            return True

    def read(self) -> bool:
        return False

    def write(self, oglObjects: OglObjects):

        for oglObject in oglObjects:

            if not isinstance(oglObject, OglClass):
                continue

            pyutClass: PyutClass = cast(PyutClass, oglObject.pyutObject)
            filename:  str       = pyutClass.name

            fqFileName: str = f'{self._exportDirectory}{osSep}{filename}.{PLUGIN_EXTENSION}'

            with open(f'{fqFileName}', "w") as fd:

                file: TextIO = cast(TextIO, fd)
                base = [pyutClass.name]

                pyutStereotype: PyutStereotype = pyutClass.stereotype
                if pyutStereotype != PyutStereotype.NO_STEREOTYPE:
                    base.append(f'<<{pyutStereotype.value}>>')

                fields  = [str(x) for x in pyutClass.fields]
                methods = [str(x) for x in pyutClass.methods]

                lineLength = max([len(x) for x in base + fields + methods]) + 4

                file.write(lineLength * "-" + "\n")

                for line in base:
                    spaces = lineLength - 4 - len(line)
                    file.write("| " + int(floor(spaces / 2.0)) * " " + line + int(ceil(spaces / 2.0)) * " " + " |\n")

                file.write("|" + (lineLength - 2) * "-" + "|\n")

                for line in fields:
                    file.write("| " + line + (lineLength - len(line) - 4) * " " + " |\n")

                file.write("|" + (lineLength - 2) * "-" + "|\n")

                for line in methods:
                    file.write("| " + line + (lineLength - len(line) - 4) * " " + " |\n")

                file.write(lineLength * "-" + "\n\n")

                file.write(pyutClass.description)
