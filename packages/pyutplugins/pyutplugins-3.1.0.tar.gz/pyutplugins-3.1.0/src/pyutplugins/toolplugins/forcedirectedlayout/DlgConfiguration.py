
from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_CANCEL
from wx import ID_OK

from wx import OK

from wx import Size
from wx import StdDialogButtonSizer
from wx import Window

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from pyforcedirectedlayout.Configuration import Configuration

from pyutplugins.toolplugins.forcedirectedlayout.ConfigurationPanel import ConfigurationPanel


class DlgConfiguration(SizedDialog):

    def __init__(self, parent: Window):

        style:   int  = DEFAULT_DIALOG_STYLE
        dlgSize: Size = Size(470, 540)

        super().__init__(parent, title='Force Directed Configuration', size=dlgSize, style=style)

        self._configuration:   Configuration = Configuration()

        self.logger: Logger = getLogger(__name__)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')
        sizedPanel.SetSizerProps(proportion=1)

        self._configurationPanel: ConfigurationPanel = ConfigurationPanel(sizedPanel=sizedPanel)
        self._layoutStandardOkCancelButtonSizer()

        # self.Fit()
        # self.SetMinSize(self.GetSize())

    def _layoutStandardOkCancelButtonSizer(self):
        """
        Call this last when creating controls; Will take care of
        adding callbacks for the Ok and Cancel buttons
        """
        buttSizer: StdDialogButtonSizer = self.CreateStdDialogButtonSizer(OK | CANCEL)

        self.SetButtonSizer(buttSizer)
        self.Bind(EVT_BUTTON, self._onOk,    id=ID_OK)
        self.Bind(EVT_BUTTON, self._onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self._onClose)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        """
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onClose(self, event: CommandEvent):
        """
        """
        self.EndModal(CANCEL)
