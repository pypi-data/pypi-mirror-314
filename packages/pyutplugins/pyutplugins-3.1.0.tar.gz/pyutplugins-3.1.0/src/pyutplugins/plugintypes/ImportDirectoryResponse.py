
from dataclasses import dataclass

from pyutplugins.plugintypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class ImportDirectoryResponse(BaseRequestResponse):
    directoryName: str = ''
