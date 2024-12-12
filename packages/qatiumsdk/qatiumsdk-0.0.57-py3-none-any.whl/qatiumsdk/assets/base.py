from typing import Generic, Literal, TypeVar
from .common import Level

AssetTypes = {
  "PIPE": "Pipe",
  "JUNCTION": "Junction",
  "VALVE": "Valve",
  "PUMP": "Pump",
  "SUPPLY_SOURCE": "SupplySource",
  "TANK": "Tank"
}

AssetType = Literal["Pipe", "Junction", "Valve", "Pump", "SupplySource", "Tank"]

ElementTypes = {
  **AssetTypes,
  "ZONE": "Zone"
}

ElementTypeKeys = Literal["PIPE", "JUNCTION", "VALVE", "PUMP", "SUPPLY_SOURCE", "TANK", "ZONE"]
ElementType = Literal["Pipe", "Junction", "Valve", "Pump", "SupplySource", "Tank", "Zone"]

T = TypeVar('T', bound=AssetType)

class BaseAsset(Generic[T]):
  """
  BaseAsset type with a generic type T representing the AssetType.
  """
  id: str
  originalId: str
  clusterId: str
  level: Level
  type: T