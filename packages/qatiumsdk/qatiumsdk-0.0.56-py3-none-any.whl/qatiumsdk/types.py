from typing import Literal, Union
from .assets.base import ElementType

class Success:
  status: Literal["success"]

class Failure:
  status: Literal["failure"]
  error: Union[Exception, str]

ElementId = Union[str, str]  # AssetId and ZoneId are both strings

class Coordinate:
  lng: float
  lat: float

class Bounds:
  ne: Coordinate
  sw: Coordinate

class ElementIdentifier:
  id: ElementId
  type: ElementType
