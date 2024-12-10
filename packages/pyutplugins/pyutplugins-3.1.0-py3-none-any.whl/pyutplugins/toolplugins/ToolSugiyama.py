
from typing import List
from typing import Union

from logging import Logger
from logging import getLogger

from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugintypes.PluginDataTypes import PluginName

from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.toolplugins.sugiyama.RealSugiyamaNode import RealSugiyamaNode
from pyutplugins.toolplugins.sugiyama.Sugiyama import Sugiyama
from pyutplugins.toolplugins.sugiyama.SugiyamaLink import SugiyamaLink
from pyutplugins.toolplugins.sugiyama.VirtualSugiyamaNode import VirtualSugiyamaNode


class ToolSugiyama(ToolPluginInterface):
    """
    ToSugiyama : Automatic layout algorithm based on Sugiyama levels.
    """
    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Sugiyama Automatic Layout')
        self._author    = 'Nicolas Dubois <nicdub@gmx.ch>'
        self._version   = '1.1'

        self._menuTitle = 'Sugiyama Automatic Layout'

        #
        # TODO Move to separate class
        #
        # Sugiyama nodes and links
        self.__realSugiyamaNodesList: List[RealSugiyamaNode] = []   # List of all RealSugiyamaNode
        self.__sugiyamaLinksList:     List[SugiyamaLink]     = []   # List of all SugiyamaLink

        #  Hierarchy graph
        #  List of Real and Virtual Sugiyama nodes that take part in hierarchy
        self.__hierarchyGraphNodesList:    List[Union[RealSugiyamaNode, VirtualSugiyamaNode]] = []
        #  List of Sugiyama nodes that are not in hierarchy
        self.__nonHierarchyGraphNodesList: List[VirtualSugiyamaNode] = []
        self.__nonHierarchyGraphLinksList: List[SugiyamaLink]        = []

        #  All nodes of the hierarchy are assigned to a level.
        #  A level is a list of nodes (real or virtual).
        self.__levels: List = []  # List of levels

    def setOptions(self) -> bool:
        """
        Prepare for the tool action.
        This can be used to ask some questions to the user.

        Returns: If False, the import should be cancelled.  'True' to proceed
        """
        return True

    def doAction(self):
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, selectedOglObjects: OglObjects):

        selectedObjects: OglObjects = selectedOglObjects

        self.logger.info(f'Begin Sugiyama algorithm')

        sugiyama: Sugiyama = Sugiyama(pluginAdapter=self._pluginAdapter)
        sugiyama.createInterfaceOglALayout(oglObjects=selectedObjects)
        sugiyama.levelFind()
        sugiyama.addVirtualNodes()
        sugiyama.barycenter()

        # noinspection PyProtectedMember
        self.logger.info(f'Number of hierarchical intersections: {sugiyama._getNbIntersectAll()}')

        sugiyama.addNonHierarchicalNodes()
        sugiyama.fixPositions()

        self._pluginAdapter.indicatePluginModifiedProject()
        self._pluginAdapter.refreshFrame()

        self.logger.info('End Sugiyama algorithm')
