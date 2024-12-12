from typing import Union, Optional, Callable
from .geojson import Polygon, MultiPolygon
from .assets import Asset, Valve, Junction, Pipe, Tank, Pump, SupplySource

class Zone:
  id: str
  inlets: list[Asset]
  outlets: list[Asset]
  geometry: Union[Polygon, MultiPolygon]

  def getJunctions(self, predicate: Optional[Callable[[Junction], bool]] = None) -> list[Junction]:
    pass

  def getPipes(self, predicate: Optional[Callable[[Pipe], bool]] = None) -> list[Pipe]:
    pass

  def getValves(self, predicate: Optional[Callable[[Valve], bool]] = None) -> list[Valve]:
    pass

  def getTanks(self, predicate: Optional[Callable[[Tank], bool]] = None) -> list[Tank]:
    pass

  def getPumps(self, predicate: Optional[Callable[[Pump], bool]] = None) -> list[Pump]:
    pass

  def getSupplySources(self, predicate: Optional[Callable[[SupplySource], bool]] = None) -> list[SupplySource]:
    pass

  def getAssets(self, predicate: Optional[Callable[[Asset], bool]] = None) -> list[Asset]:
    pass

  def getAsset(self, asset_id: str) -> Optional[Asset]:
    pass

  def getBoundaryValves(self) -> list[Valve]:
    """
    Returns an array with all the boundary valves in the zone, as Valve objects.
    """
    pass