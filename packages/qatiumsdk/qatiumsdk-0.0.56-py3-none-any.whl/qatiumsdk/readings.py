from typing import Optional, List
from datetime import date

# AssetSensors type
AssetSensors = List[str]

class BaseReading():
  date: date
  value: float

class Metrics():
  setting: Optional[BaseReading]
  status: Optional[BaseReading]
  upstreamPressure: Optional[BaseReading]
  downstreamPressure: Optional[BaseReading]
  flow: Optional[BaseReading]
  pressure: Optional[BaseReading]
  demand: Optional[BaseReading]
  level: Optional[BaseReading]

class ValveReadingsByDate():
  date: date
  readings: Metrics

class RangeMetrics():
  setting: List[BaseReading]
  status: List[BaseReading]
  upstreamPressure: List[BaseReading]
  downstreamPressure: List[BaseReading]
  flow: List[BaseReading]
  pressure: List[BaseReading]
  demand: List[BaseReading]
  level: List[BaseReading]

class AssetReadings(Metrics):
  async def latest(self) -> Metrics:
    pass

  async def forPeriod(self) -> List[ValveReadingsByDate]:
    pass
