
from typing import Dict
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from wx import OK
from wx import PD_APP_MODAL
from wx import PD_ELAPSED_TIME
from wx import ProgressDialog
from wx import Window

from wx import Yield as wxYield

from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutUseCase import PyutUseCase
from pyutmodelv2.PyutLink import PyutLinks
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutClass import PyutClass

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink

from pyforcedirectedlayout.ForceDirectedLayout import ForceDirectedLayout
from pyforcedirectedlayout.LayoutTypes import LayoutStatus

from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface
from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.toolplugins.forcedirectedlayout.DlgConfiguration import DlgConfiguration
from pyutplugins.toolplugins.forcedirectedlayout.OglNode import OglNode

NO_PARENT_WINDOW:    Window         = cast(Window, None)
NO_PROGRESS_DIALOG:  ProgressDialog = cast(ProgressDialog, None)

NameDictionary = NewType('NameDictionary', Dict[str, OglClass])


class ToolForceDirectedLayout(ToolPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):
        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Force Directed Layout')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '1.0'

        self._menuTitle = 'Force Directed Layout'

        self._fdl: ForceDirectedLayout = ForceDirectedLayout()
        self._layoutProgressDialog: ProgressDialog = NO_PROGRESS_DIALOG

    def setOptions(self) -> bool:

        with DlgConfiguration(NO_PARENT_WINDOW) as dlg:
            if dlg.ShowModal() == OK:
                return True
            else:
                self.logger.warning(f'Cancelled')
                return False

    def doAction(self):
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, oglObjects: OglObjects):
        pass

        if len(oglObjects) == 0:
            self.displayNoSelectedOglObjects()
        else:
            nameDictionary: NameDictionary = self._buildNameDictionary(oglObjects=oglObjects)

            for oglObject in oglObjects:

                if isinstance(oglObject, OglClass):
                    oglClass: OglClass = cast(OglClass, oglObject)
                    parentOglNode: OglNode = OglNode(oglClass=oglClass)
                    self._fdl.addNode(parentOglNode)
                    pyutClass: PyutClass = oglClass.pyutObject
                    links:     PyutLinks = pyutClass.links
                    for link in links:
                        pyutLink: PyutLink = cast(PyutLink, link)
                        self.logger.info(f'{pyutLink}')
                        childPyutClass: PyutClass | PyutSDInstance | PyutUseCase = pyutLink.destination
                        childClassName: str       = childPyutClass.name

                        try:
                            oglChildClass:  OglClass  = nameDictionary[childClassName]
                            childOglNode: OglNode = OglNode(oglClass=oglChildClass)
                            parentOglNode.addChild(childOglNode)
                        except KeyError:
                            self.logger.warning(f'{childClassName}: not selected')

            self._fdl.arrange(statusCallback=self._layoutStatusCallBack)
            self._reArrangeLinks(oglObjects=oglObjects)
            self._pluginAdapter.refreshFrame()
            self._pluginAdapter.indicatePluginModifiedProject()

    def _reArrangeLinks(self, oglObjects: OglObjects):

        for oglObject in oglObjects:
            if isinstance(oglObject, OglLink):
                oglLink: OglLink = cast(OglLink, oglObject)
                self.logger.info(f"Optimizing: {oglLink}")
                oglLink.optimizeLine()

    def _buildNameDictionary(self, oglObjects: OglObjects):

        nameDictionary: NameDictionary = NameDictionary({})

        for oglObject in oglObjects:
            if isinstance(oglObject, OglClass):
                oglClass: OglClass = cast(OglClass, oglObject)
                pyutClass: PyutClass = oglClass.pyutObject
                nameDictionary[pyutClass.name] = oglClass

        return nameDictionary

    def _layoutStatusCallBack(self, status: LayoutStatus):

        if self._layoutProgressDialog is None:
            self._layoutProgressDialog = ProgressDialog('Arranging', 'Starting', parent=None, style=PD_APP_MODAL | PD_ELAPSED_TIME)
            self._layoutProgressDialog.SetRange(status.maxIterations)

        statusMsg: str = (
            f'totalDisplacement: {status.totalDisplacement: .3f}\n'
            f'iterations: {status.iterations}\n'
            f'stopCount: {status.stopCount}\n'
        )
        self._layoutProgressDialog.Update(status.iterations, statusMsg)

        self._pluginAdapter.refreshFrame()

        wxYield()
