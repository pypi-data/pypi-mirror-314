from typing import Union

from .valve import *
from .junction import *
from .pump import *
from .pipe import *
from .tank import *
from .supply_source import *
from .base import *

Asset = Union[
  Valve,
  Junction,
  Pipe,
  Tank,
  Pump,
  SupplySource
]
