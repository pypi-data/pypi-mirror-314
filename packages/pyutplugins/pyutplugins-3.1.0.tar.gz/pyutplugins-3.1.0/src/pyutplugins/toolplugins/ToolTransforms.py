
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglObject import OglObject

from pyutplugins.ExternalTypes import FrameInformation
from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.plugininterfaces.IOPluginInterface import IPluginAdapter
from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from pyutplugins.plugintypes.PluginDataTypes import PluginName


class ToolTransforms(ToolPluginInterface):
    """
     A plugin for making transformations : translation, rotations, ...

    TODO: Explore parameterizing x transform and adding other transforms
    """
    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Transformations')
        self._author    = 'C.Dutoit'
        self._version   = '1.1'

        self._menuTitle = 'Transformations'

    def setOptions(self) -> bool:
        return True

    def doAction(self):
        # self._pluginAdapter.getSelectedOglObjects(callback=self._stashSelectedObjects)
        self._pluginAdapter.getFrameInformation(callback=self._doAction)

    def _doAction(self, frameInformation: FrameInformation):

        selectedObjects: OglObjects = frameInformation.selectedOglObjects

        frameW: int = frameInformation.frameSize.width
        frameH: int = frameInformation.frameSize.height
        # (frameW, frameH) = self._pluginAdapter.umlFrame.GetSize()
        self.logger.warning(f'frameW: {frameW} - frameH: {frameH}')

        for obj in selectedObjects:
            oglObject: OglObject = cast(OglObject, obj)
            x, y = oglObject.GetPosition()
            newX: int = frameW - x
            self.logger.info(f"x,y: {x},{y} - newX: {newX}")
            oglObject.SetPosition(newX, y)

        self._pluginAdapter.indicatePluginModifiedProject()
        self._pluginAdapter.refreshFrame()
