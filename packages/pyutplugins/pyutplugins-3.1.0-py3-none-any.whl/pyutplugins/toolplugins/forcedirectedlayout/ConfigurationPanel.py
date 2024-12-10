
from typing import cast

from logging import Logger
from logging import getLogger

from wx import DefaultPosition
from wx import EVT_SPINCTRL
from wx import EVT_SPINCTRLDOUBLE
from wx import SP_VERTICAL
from wx import SpinCtrl
from wx import SpinCtrlDouble
from wx import SpinDoubleEvent
from wx import SpinEvent

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from codeallybasic.MinMax import MinMax

from codeallyadvanced.ui.widgets.DialSelector import DialSelector
from codeallyadvanced.ui.widgets.DialSelector import DialSelectorParameters
from codeallyadvanced.ui.widgets.MinMaxControl import MinMaxControl

from pyforcedirectedlayout.Configuration import Configuration
from pyforcedirectedlayout.Configuration import X_RANGE_MAX
from pyforcedirectedlayout.Configuration import X_RANGE_MIN
from pyforcedirectedlayout.Configuration import Y_RANGE_MAX
from pyforcedirectedlayout.Configuration import Y_RANGE_MIN


NO_DIAL_SELECTOR: DialSelector = cast(DialSelector, None)


class ConfigurationPanel:
    """
    Not really a panel.  This builds the components inside a parent SizedPanel.
    It assumes the parent panel is vertically oriented
    """
    def __init__(self, sizedPanel: SizedPanel):

        self.logger: Logger = getLogger(__name__)

        self._configuration:   Configuration = Configuration()

        self._damping:       DialSelector = NO_DIAL_SELECTOR
        self._springLength:  DialSelector = NO_DIAL_SELECTOR
        self._maxIterations: DialSelector = NO_DIAL_SELECTOR

        self._layoutForceParameters(parentPanel=sizedPanel)
        self._layoutRandomizeParameters(parentPanel=sizedPanel)
        self._layoutAlgorithmParameters(parentPanel=sizedPanel)

    def _layoutForceParameters(self, parentPanel: SizedPanel):
        """
        Sets the protected properties:

        self._damping
        self._springLength
        self._maxIterations

        Args:
            parentPanel:  The panel that hosts these components
        """

        localPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Directed Layout Parameters')
        localPanel.SetSizerType('horizontal')
        localPanel.SetSizerProps(expand=True, proportion=2)

        dampingParameters: DialSelectorParameters = DialSelectorParameters(minValue=0.1, maxValue=1.0, dialLabel='Damping',
                                                                           formatValueCallback=self._formatDampingValue,
                                                                           valueChangedCallback=self._dampingChanged)
        damping:           DialSelector           = DialSelector(localPanel, parameters=dampingParameters)
        damping.tickFrequency = 10
        damping.tickValue     = 0.1
        damping.value         = self._configuration.damping

        springLengthParameters: DialSelectorParameters = DialSelectorParameters(minValue=100, maxValue=500, dialLabel='Spring Length',
                                                                                formatValueCallback=self._formatSpringLength,
                                                                                valueChangedCallback=self._springLengthChanged)

        springLength:           DialSelector           = DialSelector(localPanel, parameters=springLengthParameters)
        springLength.tickFrequency = 20
        springLength.tickValue     = 25
        springLength.value         = self._configuration.springLength

        maxIterationsParameters: DialSelectorParameters = DialSelectorParameters(minValue=100,
                                                                                 maxValue=1000,
                                                                                 dialLabel='Maximum Iterations',
                                                                                 formatValueCallback=self._formatMaxIterations,
                                                                                 valueChangedCallback=self._maxIterationsChanged)
        maxIterations: DialSelector = DialSelector(localPanel, parameters=maxIterationsParameters)
        maxIterations.tickFrequency = 50
        maxIterations.tickValue     = 20
        maxIterations.value         = self._configuration.maxIterations

        self._damping       = damping
        self._springLength  = springLength
        self._maxIterations = maxIterations

    def _layoutRandomizeParameters(self, parentPanel: SizedPanel):

        localPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Randomize Initial Layout Parameters')
        localPanel.SetSizerType('vertical')
        localPanel.SetSizerProps(expand=True, proportion=1)

        horizontalPanel: SizedPanel = SizedPanel(localPanel)
        horizontalPanel.SetSizerType('horizontal')
        horizontalPanel.SetSizerProps(expand=True, proportion=1)

        minMaxX: MinMaxControl = MinMaxControl(sizedPanel=horizontalPanel, displayText='Minimum/Maximum X Value',
                                               minValue=X_RANGE_MIN, maxValue=X_RANGE_MAX,
                                               valueChangedCallback=self._onMinMaxX,
                                               setControlsSize=False)
        minMaxX.minMax = self._configuration.minMaxX

        minMaxY: MinMaxControl = MinMaxControl(sizedPanel=horizontalPanel, displayText='Minimum/Maximum Y Value',
                                               minValue=Y_RANGE_MIN, maxValue=Y_RANGE_MAX,
                                               valueChangedCallback=self._onMinMaxY,
                                               setControlsSize=False)
        minMaxY.minMax = self._configuration.minMaxY

    def _layoutAlgorithmParameters(self, parentPanel: SizedPanel):

        algorithmFactorsPanel: SizedStaticBox = SizedStaticBox(parentPanel, label='Algorithm Parameters')
        algorithmFactorsPanel.SetSizerType('horizontal')
        algorithmFactorsPanel.SetSizerProps(expand=True, proportion=1)

        attractionPanel: SizedStaticBox = SizedStaticBox(algorithmFactorsPanel, label='Node Attraction Force')
        attractionPanel.SetSizerType('vertical')
        attractionPanel.SetSizerProps(proportion=0)

        attractionForce: SpinCtrlDouble = SpinCtrlDouble(attractionPanel, min=0.1, max=1.0, inc=0.1, pos=(-1, -1), size=(50, 35))
        # attractionForce.SetSizerProps(expand=True)
        attractionForce.SetDigits(2)
        attractionForce.SetValue(self._configuration.attractionForce)
        attractionForce.Bind(EVT_SPINCTRLDOUBLE, self._attractionForceChanged)

        repulsionPanel: SizedStaticBox = SizedStaticBox(algorithmFactorsPanel, label='Node Repulsion Force')
        repulsionPanel.SetSizerType('vertical')
        repulsionPanel.SetSizerProps(proportion=0)

        repulsionForce: SpinCtrl = SpinCtrl(repulsionPanel, size=(75, 35), pos=DefaultPosition, style=SP_VERTICAL)
        repulsionForce.SetRange(500, 15000)
        repulsionForce.SetValue(self._configuration.repulsionForce)
        repulsionForce.SetIncrement(100)
        repulsionForce.Bind(EVT_SPINCTRL, self._repulsionForceChanged)

    def _formatDampingValue(self, valueToFormat: float):

        return f'{valueToFormat:.2f}'

    def _formatSpringLength(self, valueToFormat: int):
        return f'{valueToFormat}'

    def _formatMaxIterations(self, valueToFormat: int):
        return f'{valueToFormat}'

    def _dampingChanged(self, newValue: int):
        self._configuration.damping = newValue

    def _springLengthChanged(self, newValue: int):
        self._configuration.springLength = newValue

    def _maxIterationsChanged(self, newValue: int):
        self._configuration.maxIterations = newValue

    def _onMinMaxX(self, minMaxX: MinMax):
        self._configuration.minMaxY = minMaxX

    def _onMinMaxY(self, minMaxY: MinMax):
        self._configuration.minMaxY = minMaxY

    def _attractionForceChanged(self, event: SpinDoubleEvent):

        floatSpin: SpinCtrlDouble = event.GetEventObject()

        self._configuration.attractionForce = floatSpin.GetValue()

    def _repulsionForceChanged(self, event: SpinEvent):

        spinCtrl: SpinCtrl = event.GetEventObject()

        self._configuration.repulsionForce = spinCtrl.GetValue()
