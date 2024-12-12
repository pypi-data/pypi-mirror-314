from typing import Optional, List, Union, Literal, Dict
from ..geojson import Point
from datetime import date
from ..readings import AssetReadings, AssetSensors
from .base import BaseAsset

class SupplySourceSimulation:
  head: float
  waterAge: Optional[float]

class SupplySource(BaseAsset["SupplySource"]):
  description: Optional[str]
  geometry: Point
  elevation: float
  head: Optional[float]
  pattern: Optional[str]
  simulation: Optional[SupplySourceSimulation]
  readings: AssetReadings
  sensors: AssetSensors
  zones: List[str]
  volumeCurveId: Optional[str]
  warningThresholdMin: Optional[float]
  warningThresholdMax: Optional[float]

  def getPeriodSimulation(self) -> List[Dict[str, SupplySourceSimulation]]:
    """
    Function that returns an array of the simulation values for the whole simulation period with its dates.

    Returns:
        List[Dict[str, SupplySourceSimulation]]: List of simulation results with dates.
    """
    pass
