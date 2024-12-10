
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from wx import EVT_BUTTON
from wx import EVT_CHOICE
from wx import EVT_CLOSE
from wx import EVT_MOTION
from wx import FD_CHANGE_DIR
from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE
from wx import ID_CANCEL
from wx import ID_OK
from wx import TE_READONLY

from wx import Button
from wx import Choice
from wx import CommandEvent
from wx import FileDialog
from wx import TextCtrl
from wx import MouseEvent

from wx import Yield as wxYield

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyutplugins.common.ui.BaseEditDialog import BaseEditDialog

from pyutplugins.ioplugins.wximage.WxImageFormat import WxImageFormat

from pyutplugins.preferences.PluginPreferences import PluginPreferences


class DlgWxImageOptions(BaseEditDialog):

    def __init__(self, parent):

        super().__init__(parent, title='Native Image Generation Options')

        self.logger: Logger = getLogger(__name__)

        self._fileSelectBtn:     Button   = cast(Button, None)
        self._selectedFile:      TextCtrl = cast(TextCtrl, None)
        self._imageFormatChoice: Choice   = cast(Choice, None)

        self._outputFileName: str           = PluginPreferences().wxImageFileName
        self._imageFormat:    WxImageFormat = WxImageFormat.PNG

        self._layoutFileSelection(parent=self.GetContentsPane())
        self._layoutImageFormatChoice(parent=self.GetContentsPane())

        self._layoutStandardOkCancelButtonSizer()
        self._bindEventHandlers()

    @property
    def imageFormat(self) -> WxImageFormat:
        return self._imageFormat

    @imageFormat.setter
    def imageFormat(self, newFormat: WxImageFormat):
        self._imageFormat = newFormat

    @property
    def outputFileName(self) -> str:
        return self._outputFileName

    @outputFileName.setter
    def outputFileName(self, newName: str):
        self._outputFileName = newName

    def _bindEventHandlers(self):

        self.Bind(EVT_BUTTON, self._onFileSelectClick,   self._fileSelectBtn)
        self.Bind(EVT_CHOICE, self._onImageFormatChoice, self._imageFormatChoice)
        #
        self._selectedFile.Bind(EVT_MOTION, self._fileSelectionMotion, self._selectedFile)
        self.Bind(EVT_BUTTON, self._onOk, id=ID_OK)
        self.Bind(EVT_CLOSE, self._onClose, id=ID_CANCEL)

    def _fileSelectionMotion(self, event: MouseEvent):

        ctrl: TextCtrl = event.GetEventObject()

        tip = ctrl.GetToolTip()
        tip.SetTip(self._outputFileName)

    # noinspection PyUnusedLocal
    def _onFileSelectClick(self, event: CommandEvent):

        self.logger.warning(f'File Select Click')
        wxYield()

        fmtSelIdx:    int = self._imageFormatChoice.GetCurrentSelection()
        outputFormat: str = self._imageFormatChoice.GetString(fmtSelIdx)

        dlg: FileDialog = FileDialog(self,
                                     message='Choose the export file name',
                                     defaultFile=self._outputFileName,
                                     style=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR
                                     )
        if dlg.ShowModal() == ID_OK:
            wxYield()
            path:     str = dlg.GetPath()
            fileName: str = dlg.GetFilename()

            self._selectedFile.SetValue(fileName)       # for simple viewing
            self._selectedFile.SetModified(True)
            self._outputFileName = path                 # for actual us

        dlg.Destroy()

    def _onImageFormatChoice(self, event: CommandEvent):

        ctrl:      Choice = event.GetEventObject()
        idx:       int    = ctrl.GetCurrentSelection()
        newValue:  str    = ctrl.GetString(idx)

        newFormat: WxImageFormat = WxImageFormat(newValue)

        self._imageFormat = newFormat

    def _layoutFileSelection(self, parent: SizedPanel):

        box: SizedStaticBox = SizedStaticBox(parent, -1, "Output Filename")
        box.SetSizerProps(expand=True, proportion=1)

        currentFile: str = self._outputFileName

        sizedPanel: SizedPanel = SizedPanel(box)
        sizedPanel.SetSizerType('horizontal')

        self._fileSelectBtn = Button(sizedPanel, label="&Select",)
        self._selectedFile  = TextCtrl(sizedPanel, value=currentFile, style=TE_READONLY)

        self._selectedFile.SetToolTip(currentFile)

    def _layoutImageFormatChoice(self, parent: SizedPanel):

        imageChoices: List[str] = [WxImageFormat.PNG.value, WxImageFormat.JPG.value, WxImageFormat.BMP.value, WxImageFormat.TIFF.value]

        box: SizedStaticBox = SizedStaticBox(parent, -1, "Image Format")
        box.SetSizerProps(expand=True, proportion=1)

        self._imageFormatChoice = Choice(box, choices=imageChoices)
