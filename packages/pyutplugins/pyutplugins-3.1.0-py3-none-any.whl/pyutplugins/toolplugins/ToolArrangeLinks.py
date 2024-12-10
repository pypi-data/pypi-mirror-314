
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglLink import OglLink

from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from pyutplugins.plugintypes.PluginDataTypes import PluginName

from pyutplugins.ExternalTypes import OglObjects


class ToolArrangeLinks(ToolPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Arrange Links')
        self._author    = 'Cedric DUTOIT <dutoitc@shimbawa.ch>'
        self._version   = '1.1'

        self._menuTitle = 'Arrange links'

    def setOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            If `False`, the import is canceled.
        """
        return True

    def doAction(self):

        self._pluginAdapter.selectAllOglObjects()
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, oglObjects: OglObjects):

        modified: bool = False
        for oglObject in oglObjects:
            if isinstance(oglObject, OglLink):
                oglLink: OglLink = cast(OglLink, oglObject)
                self.logger.info(f"Optimizing: {oglLink}")
                oglLink.optimizeLine()
                modified = True
            else:
                self.logger.debug(f"No line optimizing for: {oglObject}")

        if modified is True:
            self._pluginAdapter.refreshFrame()
            self._pluginAdapter.indicatePluginModifiedProject()
