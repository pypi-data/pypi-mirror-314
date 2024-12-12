from typing import Optional, List, Union, Literal, Dict
from ..geojson import Point
from datetime import date
from ..readings import AssetReadings, AssetSensors
from .base import BaseAsset

class TankSimulation:
  level: float
  pressure: float
  volume: float
  waterAge: Optional[float]

class Tank(BaseAsset["Tank"]):
  canOverflow: Optional[str]
  description: Optional[str]
  geometry: Point
  diameter: float
  elevation: float
  initialLevel: float
  maximumLevel: float
  minimumLevel: float
  minimumVolume: float
  installationDate: Optional[date]
  simulation: Optional[TankSimulation]
  readings: AssetReadings
  sensors: AssetSensors
  zones: List[str]
  volumeCurveId: Optional[str]
  warningThresholdMin: Optional[float]
  warningThresholdMax: Optional[float]

  def getPeriodSimulation(self) -> List[Dict[str, TankSimulation]]:
    """
    Function that returns an array of the simulation values for the whole simulation period with its dates.

    Returns:
        List[Dict[str, TankSimulation]]: List of simulation results with dates.
    """
    pass
