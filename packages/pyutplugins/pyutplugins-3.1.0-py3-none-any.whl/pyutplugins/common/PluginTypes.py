from typing import cast
from typing import Dict
from typing import NewType

from dataclasses import dataclass

from ogl.OglClass import OglClass

from pyutmodelv2.PyutClass import PyutClass

from pyutplugins.common.ElementTreeData import ElementTreeData

ClassTree  = NewType('ClassTree',  Dict[str, ElementTreeData])    # string is ClassName


@dataclass
class ClassPair:

    pyutClass: PyutClass = cast(PyutClass, None)
    oglClass:  OglClass  = cast(OglClass, None)
