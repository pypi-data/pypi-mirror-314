
from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass

from ogl.OglLink import OglLink

from pyutplugins.ExternalTypes import CreatedLinkCallback
from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import LinkInformation
from pyutplugins.ExternalTypes import ObjectBoundaryCallback
from pyutplugins.ExternalTypes import OglObjectType
from pyutplugins.ExternalTypes import FrameInformationCallback
from pyutplugins.ExternalTypes import FrameSizeCallback
from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback


@dataclass
class ScreenMetrics:
    screenWidth:  int = 0
    screenHeight: int = 0

    dpiX: int = 0
    dpiY: int = 0


class IPluginAdapter(ABC):
    """
    This the interface specification that allows the pyutplugins to manipulate the Pyut UML Frame
    The Pyut application must implement this and override the appropriate methods and/or
    set appropriate protected variables after call this class
    constructor

    """
    def __init__(self):
        pass

    @property
    @abstractmethod
    def pyutVersion(self) -> str:
        """
        Returns:  The current Pyut version
        """
        pass

    @property
    @abstractmethod
    def screenMetrics(self) -> ScreenMetrics:
        """
        Returns:  appropriate metrics;  wxPython is a helpe
        """
        pass

    @property
    @abstractmethod
    def currentDirectory(self) -> str:
        """
        Returns:  The current directory
        """
        pass

    @abstractmethod
    def getFrameSize(self, callback: FrameSizeCallback):
        pass

    @abstractmethod
    def getFrameInformation(self, callback: FrameInformationCallback):
        pass

    @abstractmethod
    def getSelectedOglObjects(self, callback: SelectedOglObjectsCallback):
        """
        Requests all the selected in the currently displayed frame

        Args:
            callback:  This method is invoked with a list of all the selected OglObjects
        """
        pass

    @abstractmethod
    def getObjectBoundaries(self, callback: ObjectBoundaryCallback):
        """
        Request the boundaries around all the UML objects
        on the current frame

        Args:
            callback:  The callback that receives the boundaries
        """
        pass

    @abstractmethod
    def refreshFrame(self):
        """
        Refresh the currently displayed frame
        """
        pass

    @abstractmethod
    def selectAllOglObjects(self):
        """
        Select all the Ogl shapes in the currently displayed frame
        """
        pass

    @abstractmethod
    def deselectAllOglObjects(self):
        """
        Deselect all the Ogl shapes in the currently displayed frame
        """
        pass

    @abstractmethod
    def addShape(self, shape: OglObjectType):
        """
        Add an Ogl shape to the currently displayed frame
        Args:
            shape:
        """
        pass

    @abstractmethod
    def loadProject(self, pluginProject: PluginProject):
        """
        Abstract
        This is the preferred way for pyutplugins to projects into Pyut

        Args:
            pluginProject:

        """
        pass

    @abstractmethod
    def requestCurrentProject(self, callback: CurrentProjectCallback):
        """
        Request the current project.   The adapter or its surrogate
        has to convert from a PyutProject to a PluginProject type
        """
        pass

    @abstractmethod
    def indicatePluginModifiedProject(self):
        """
        Plugins always work on the current frame or project
        """
        pass

    @abstractmethod
    def deleteLink(self, oglLink: OglLink):
        pass

    @abstractmethod
    def createLink(self, linkInformation: LinkInformation, callback: CreatedLinkCallback):
        pass
