from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import EVT_CHECKBOX
from wx import EVT_CHOICE
from wx import EVT_TEXT
from wx import ID_ANY

from wx import CommandEvent
from wx import StaticText
from wx import TextCtrl
from wx import Window
from wx import CheckBox
from wx import Choice

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from codeallybasic.Dimensions import Dimensions

from codeallyadvanced.ui.widgets.DimensionsControl import DimensionsControl

from pyutplugins.ioplugins.mermaid.MermaidDirection import MermaidDirection

from pyutplugins.preferences.PluginPreferences import PluginPreferences

from pyutplugins.toolplugins.orthogonal.LayoutAreaSize import LayoutAreaSize


class PluginPreferencesPage(SizedPanel):

    def __init__(self, parent: Window):
        self.logger: Logger = getLogger(__name__)

        super().__init__(parent)
        self.SetSizerType('vertical')

        self._preferences: PluginPreferences = PluginPreferences()
        self._pdfFileNameWxId:   int = wxNewIdRef()
        self._imageFileNameWxId: int = wxNewIdRef()

        self._layoutSizeControls:     DimensionsControl = cast(DimensionsControl, None)
        self._stepSugiyama:           CheckBox          = cast(CheckBox, None)
        self._mermaidLayoutDirection: Choice            = cast(Choice, None)

        self._createWindow(self)

        self._setControlValues()
        parent.Bind(EVT_TEXT,     self._onNameChange,  id=self._pdfFileNameWxId)
        parent.Bind(EVT_TEXT,     self._onNameChange,  id=self._imageFileNameWxId)

        parent.Bind(EVT_CHECKBOX, self._onSugiyamaValueChanged,   self._stepSugiyama)
        parent.Bind(EVT_CHOICE,   self._onLayoutDirectionChanged, self._mermaidLayoutDirection)

    @property
    def name(self) -> str:
        return 'Plugins'

    def _createWindow(self, parent: SizedPanel):

        self._stepSugiyama = CheckBox(parent, label='Step Sugiyama Layout')

        self._layoutMermaidPreferences(parent)

        self._layoutSizeControls = DimensionsControl(sizedPanel=parent, displayText="Orthogonal Layout Width/Height",
                                                     minValue=100, maxValue=4096,
                                                     valueChangedCallback=self._layoutSizeChanged,
                                                     setControlsSize=False)

        # noinspection PyUnresolvedReferences
        self._layoutSizeControls.SetSizerProps(proportion=2, expand=False)

        self._layoutNamePreferences(parent=parent)

    def _layoutMermaidPreferences(self, parent):

        directions: List[str] = [s for s in MermaidDirection]

        ssb: SizedStaticBox = SizedStaticBox(parent, label='Mermaid Diagram Layout Direction')
        ssb.SetSizerProps(proportion=2, expand=False)

        self._mermaidLayoutDirection = Choice(ssb, choices=directions)

    def _layoutNamePreferences(self, parent: SizedPanel):
        sizedForm: SizedPanel = SizedPanel(parent)
        sizedForm.SetSizerType('form')
        sizedForm.SetSizerProps(proportion=2)
        StaticText(sizedForm, ID_ANY, 'PDF Filename:')
        # TODO need plugin preference
        TextCtrl(sizedForm, id=self._pdfFileNameWxId, value=self._preferences.pdfExportFileName, size=(125, 25))

        StaticText(sizedForm, ID_ANY, 'Image Filename:')
        TextCtrl(sizedForm, self._imageFileNameWxId, self._preferences.wxImageFileName, size=(125, 25))

    def _setControlValues(self):
        layoutDimensions: Dimensions = Dimensions()
        layoutDimensions.width  = self._preferences.orthogonalLayoutSize.width
        layoutDimensions.height = self._preferences.orthogonalLayoutSize.height

        self._layoutSizeControls.dimensions = layoutDimensions

        self._stepSugiyama.SetValue(self._preferences.sugiyamaStepByStep)

    def _onNameChange(self, event: CommandEvent):

        eventID:  int = event.GetId()
        newValue: str = event.GetString()

        match eventID:
            case self._imageFileNameWxId:
                self._preferences.wxImageFileName = newValue
            case self._pdfFileNameWxId:
                self._preferences.pdfExportFileName = newValue
            case _:
                self.logger.error(f'Unknown event id')

    def _layoutSizeChanged(self, newValue: Dimensions):
        layoutAreaSize: LayoutAreaSize = LayoutAreaSize(width=newValue.width, height=newValue.height)
        self._preferences.orthogonalLayoutSize = layoutAreaSize
        self._valuesChanged = True

    def _onSugiyamaValueChanged(self, event: CommandEvent):

        newValue: bool = event.IsChecked()
        self._preferences.sugiyamaStepByStep = newValue

    # noinspection PyUnusedLocal
    def _onLayoutDirectionChanged(self, event: CommandEvent):
        idx:     int = self._mermaidLayoutDirection.GetSelection()
        enumStr: str = self._mermaidLayoutDirection.GetString(idx)

        prefValue: MermaidDirection = MermaidDirection.toEnum(enumStr=enumStr)

        self._preferences.mermaidLayoutDirection = prefValue
