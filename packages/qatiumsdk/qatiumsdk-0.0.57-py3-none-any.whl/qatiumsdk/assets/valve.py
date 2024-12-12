from typing import Literal, Optional, List, Dict, Any
from ..geojson import Point
from ..readings import AssetReadings, AssetSensors
from .base import BaseAsset

ValveStatus = {
  "OPEN": "OPEN",
  "ACTIVE": "ACTIVE",
  "CLOSED": "CLOSED"
}
ValveStatusType = Literal["OPEN", "ACTIVE", "CLOSED"]

ValveFamilies = {
  "PRV": "PRV",
  "PSV": "PSV",
  "PBV": "PBV",
  "FCV": "FCV",
  "TCV": "TCV",
  "GPV": "GPV"
}
ValveFamilyType = Literal["PRV", "PSV", "PBV", "FCV", "TCV", "GPV"]

ValveGroups = {
  "Regulating": "regulating",
  "ShutOff": "shutOff"
}
ValveGroupType = Literal["regulating", "shutOff"]

class ValveSimulation:
  status: ValveStatusType
  setting: float
  flow: Optional[float]
  velocity: Optional[float]
  unitaryHeadloss: Optional[float]
  isSupplied: bool

class Valve(BaseAsset["Valve"]):
  description: Optional[str]
  geometry: Point
  elevation: float
  diameter: float
  group: ValveGroupType
  family: ValveFamilyType
  setting: float
  curveId: Optional[str]
  minorLoss: float
  status: ValveStatusType
  simulation: Optional[ValveSimulation]
  readings: AssetReadings
  sensors: AssetSensors
  zones: List[str]

  def getPeriodSimulation(self) -> List[Dict[Any, ValveSimulation]]:
    """
    Function that returns an array of the simulation values for the whole simulation period with its dates.

    Returns:
        List[Dict[str, ValveSimulation]]: List of simulation results with dates.
    """
    pass
