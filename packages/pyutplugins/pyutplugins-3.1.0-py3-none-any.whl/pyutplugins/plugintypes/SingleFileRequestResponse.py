
from dataclasses import dataclass

from pyutplugins.plugintypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class SingleFileRequestResponse(BaseRequestResponse):
    fileName: str = ''
