
from typing import cast

from logging import Logger
from logging import getLogger

from wx import OK
from wx import Window

from ogl.OglLink import OglLink

from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginName

from pyutplugins.toolplugins.orthogonalrouting.DlgConfiguration import DlgConfiguration
from pyutplugins.toolplugins.orthogonalrouting.OrthogonalConnectorAdapter import OrthogonalConnectorAdapter

FORMAT_NAME:        FormatName        = FormatName('Orthogonal Configuration')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('json')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Save Configuration')

NO_PARENT_WINDOW:    Window         = cast(Window, None)


class ToolOrthogonalRouting(ToolPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Orthogonal Routing')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '1.0'

        self._menuTitle = 'Orthogonal Routing'

    def setOptions(self) -> bool:
        with DlgConfiguration(NO_PARENT_WINDOW, pluginAdapter=self._pluginAdapter) as dlg:
            if dlg.ShowModal() == OK:
                return True
            else:
                self.logger.warning(f'Cancelled')
                return False

    def doAction(self):
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, oglObjects: OglObjects):

        self.logger.info(f'_doAction')

        adapter: OrthogonalConnectorAdapter = OrthogonalConnectorAdapter(pluginAdapter=self._pluginAdapter)
        oglLink: OglLink = cast(OglLink, None)
        for el in oglObjects:
            if isinstance(el, OglLink):
                try:
                    oglLink = cast(OglLink, el)
                    adapter.runConnector(oglLink=oglLink)

                except (AttributeError, TypeError) as e:
                    self.logger.error(f'{e} - {oglLink=}')
