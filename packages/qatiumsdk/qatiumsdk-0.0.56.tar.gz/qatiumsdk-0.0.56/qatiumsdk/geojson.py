from typing import List, Literal

# Position type: A list with either 2 or 3 numbers representing coordinates
Position = List[float]  # [float, float] or [float, float, float]

# Point type extending from GeoJsonObject
class Point:
  type: Literal["Point"]
  coordinates: Position

class LineString:
  type: Literal["LineString"]
  coordinates: List[Position]

class MultiLineString:
  type: Literal["MultiLineString"]
  coordinates: List[List[Position]]

class Polygon:
  type: Literal["Polygon"]
  coordinates: List[List[Position]]

class MultiPolygon:
  type: Literal["MultiPolygon"]
  coordinates: List[List[List[Position]]]
