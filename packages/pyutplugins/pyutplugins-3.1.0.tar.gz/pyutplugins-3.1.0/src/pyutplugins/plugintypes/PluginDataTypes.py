
from typing import Dict
from typing import List
from typing import NewType

from enum import Enum

from dataclasses import dataclass
from dataclasses import field

#
#  Both of these hold the class plugintypes for the Plugins
#
PluginList  = NewType('PluginList',  List[type])
PluginIDMap = NewType('PluginIDMap', Dict[int, type])


def createPlugIdMapFactory() -> PluginIDMap:
    return PluginIDMap({})


PluginName        = NewType('PluginName', str)
FormatName        = NewType('FormatName', str)
PluginExtension   = NewType('PluginExtension', str)
PluginDescription = NewType('PluginDescription', str)


class PluginMapType(Enum):
    INPUT_MAP  = 'InputMap'
    OUTPUT_MAP = 'OutputMap'
    TOOL_MAP   = 'ToolMap'


#
# Some nice syntactic sugar
#
@dataclass
class BasePluginMap:
    mapType:     PluginMapType = PluginMapType.INPUT_MAP
    pluginIdMap: PluginIDMap   = field(default_factory=createPlugIdMapFactory)

    def __init__(self):
        self.pluginIdMap = PluginIDMap({})

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'{self.mapType} plugin count: {len(self.pluginIdMap)}'


@dataclass
class InputPluginMap(BasePluginMap):
    def __init__(self):
        super().__init__()
        self.mapType = PluginMapType.INPUT_MAP

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'{self.mapType} plugin count: {len(self.pluginIdMap)}'


@dataclass
class OutputPluginMap(BasePluginMap):
    def __init__(self):
        super().__init__()
        self.mapType = PluginMapType.OUTPUT_MAP


@dataclass
class ToolsPluginMap(BasePluginMap):
    def __init__(self):
        super().__init__()
        self.mapType = PluginMapType.TOOL_MAP
