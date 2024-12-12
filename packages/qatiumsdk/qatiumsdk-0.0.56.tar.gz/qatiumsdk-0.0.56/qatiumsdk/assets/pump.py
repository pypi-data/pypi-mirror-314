from typing import Optional, List, Union, Literal, Dict
from ..geojson import Point
from datetime import date
from ..readings import AssetReadings, AssetSensors
from .base import BaseAsset

class PumpStatus:
  OPEN = 'OPEN'
  CLOSED = 'CLOSED'

class PumpSimulation:
  status: PumpStatus
  setting: float
  upstreamPressure: float
  downstreamPressure: float
  flow: Optional[float]
  velocity: Optional[float]
  unitaryHeadloss: Optional[float]
  isSupplied: bool

class Pump(BaseAsset["Pump"]):
  description: Optional[str]
  geometry: Point
  elevation: float
  head: Optional[str]
  pattern: Optional[str]
  power: Optional[float]
  setting: float
  status: PumpStatus
  installationDate: Optional[date]
  simulation: Optional[PumpSimulation]
  readings: AssetReadings
  sensors: AssetSensors
  zones: List[str]
  warningThresholdMin: Optional[float]
  warningThresholdMax: Optional[float]

  def getPeriodSimulation(self) -> List[Dict[str, PumpSimulation]]:
    """
    Function that returns an array of the simulation values for the whole simulation period with its dates.

    Returns:
        List[Dict[str, PumpSimulation]]: List of simulation results with dates.
    """
    pass
