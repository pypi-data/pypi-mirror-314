from typing import Optional, List, Dict, Literal
from ..geojson import Point
from datetime import date

from ..readings import AssetReadings, AssetSensors
from .base import BaseAsset

JunctionGroups = {
  "Hydrant": "hydrant",
  "CustomerPoint": "customerPoint",
  "Junction": "junction"
}
JunctionGroupType = Literal["hydrant", "customerPoint", "junction"]

class JunctionSimulation:
  pressure: float
  demand: float
  isSupplied: bool
  waterAge: Optional[float]

class Junction(BaseAsset["Junction"]):
  demand: Optional[float]
  description: Optional[str]
  elevation: float
  emitter: Optional[float]
  geometry: Point
  group: JunctionGroupType
  readings: AssetReadings
  sensors: AssetSensors
  simulation: Optional[JunctionSimulation]
  warningThresholdMax: Optional[float]
  warningThresholdMin: Optional[float]
  zones: List[str]

  def getPeriodSimulation(self) -> List[Dict[str, JunctionSimulation]]:
    """
    Function that returns an array of the simulation values for the whole simulation period with its dates.

    Returns:
        List[Dict[str, JunctionSimulation]]: List of simulation results with dates.
    """
    pass