
from typing import List

from dataclasses import dataclass
from dataclasses import field

from pyutplugins.plugintypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class MultipleFileRequestResponse(BaseRequestResponse):

    fileList:      List[str] = field(default_factory=list)
    directoryName: str       = ''
