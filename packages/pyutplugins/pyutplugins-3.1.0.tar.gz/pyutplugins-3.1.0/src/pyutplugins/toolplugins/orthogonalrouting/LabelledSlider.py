
from typing import Callable
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BoxSizer
from wx import CommandEvent
from wx import EVT_SLIDER
from wx import EXPAND
from wx import ID_ANY
from wx import LEFT
from wx import Panel
from wx import SL_AUTOTICKS
from wx import SL_HORIZONTAL
from wx import SL_LABELS
from wx import Size
from wx import DefaultSize
from wx import Slider
from wx import VERTICAL

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

ValueChangedHandler = Callable[[CommandEvent], None]


class LabelledSlider:
    """
    The impetus of this component was to work around a bug that I described
    at stack overflow https://stackoverflow.com/questions/78414996/wxpython-slider-incorrectly-displays-with-sized-panels/78425220#78425220
    and that Richard Townsend bull dogged on to get me a workaround.

    (https://discuss.wxpython.org/t/wxpython-slider-incorrectly-displays-with-sized-panels/36915/8)

    Since bare sliders always need labels, voila, here is the wrapper component

    """
    def __init__(self, sizedPanel: SizedPanel, label: str, value: int, minValue: int, maxValue, size: Size = DefaultSize, toolTip: str = ''):
        """

        Args:
            sizedPanel:     Parent Sized Panel
            label:          The label to display
            value:          The value to set the control to
            minValue:       The slider minimal value
            maxValue:       The slider maximum value
            size:           The Size of the component
            toolTip:        A tool tip to display on a mouse over
        """

        self.logger: Logger = getLogger(__name__)

        self._slider:   Slider              = cast(Slider, None)
        self._callback: ValueChangedHandler = cast(ValueChangedHandler, None)

        self._layoutComponent(sizedPanel, label, value=value, minValue=minValue, maxValue=maxValue, size=size, toolTip=toolTip)

        sizedPanel.Bind(EVT_SLIDER, handler=self._onSliderChanged, source=self._slider)

    def _valueChangedHandler(self, handler: ValueChangedHandler):
        self._callback = handler

    # noinspection PyTypeChecker
    valueChangedHandler = property(fget=None, fset=_valueChangedHandler, doc='This method called when slider value changes')

    def _layoutComponent(self, parentPanel: SizedPanel, label: str, value: int, minValue: int, maxValue, size: Size, toolTip: str):

        sizedStaticBox: SizedStaticBox = SizedStaticBox(parent=parentPanel, label=label)
        sizedStaticBox.SetSizerType('vertical')
        sizedStaticBox.SetSizerProps(expand=True, proportion=1)

        sliderPanel: Panel  = Panel(sizedStaticBox)

        sliderStyle: int    = SL_HORIZONTAL | SL_AUTOTICKS | SL_LABELS
        slider:      Slider = Slider(sliderPanel, id=ID_ANY, value=value, minValue=minValue, maxValue=maxValue, size=size, style=sliderStyle)

        sliderPanelSizer: BoxSizer = BoxSizer(VERTICAL)
        # Add (self, window, proportion=0, flag=0, border=0, userData=None)
        sliderPanelSizer.Add(slider, 1, EXPAND | LEFT, 5)
        sliderPanel.SetSizer(sliderPanelSizer)

        sliderPanel.Layout()

        slider.SetToolTip(toolTip)

        self._slider = slider

    def _onSliderChanged(self, event: CommandEvent):

        assert self._callback is not None, 'Developer error.  You want to set the valueChangedHandler'
        self._callback(event)
