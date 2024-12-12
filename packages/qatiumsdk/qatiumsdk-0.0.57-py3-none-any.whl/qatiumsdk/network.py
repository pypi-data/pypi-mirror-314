from datetime import datetime
from js import Date
from typing import Any, Callable, Literal, Union, Optional
from .types import Success, Failure, Bounds
from .assets import Asset, Valve, Pipe, Tank, Junction, Pump, SupplySource
from .zone import Zone

class AssetStatus:
  OPEN = 'OPEN'
  CLOSED = 'CLOSED'
  ACTIVE = 'ACTIVE'

class ValveFamilies:
  PRV = 'PRV'
  PSV = 'PSV'
  PBV = 'PBV'
  FCV = 'FCV'
  TCV = 'TCV'
  GPV = 'GPV'

class NetworkMetadata:
  id: str
  name: str

Unit = Union[None, Literal[
  'mm',
  'in',
  'kw',
  'hp',
  'm',
  'ft',
  'm^3',
  'ft^3',
  'ft^3/s',
  'l/s',
  'l/m',
  'l/min',
  'Ml/d',
  'm^3/h',
  'm^3/d',
  'gal/min',
  'Mgal/d',
  'Mgallon-imp/d',
  'acre ft/d',
  'km',
  'mi',
  'mwc',
  'm/s',
  'mwc/km',
  'ft/s',
  'ft/kft',
  'psi',
  'percentage',
  'h'
]]

class UnitParameters:
  pipe_diameter: Unit
  valve_diameter: Unit
  tank_diameter: Unit
  power: Unit
  roughness: Unit
  element_length: Unit
  network_length: Unit
  volume: Unit
  flow: Unit
  elevation: Unit
  velocity: Unit
  unitary_headloss: Unit
  pressure: Unit
  capacity: Unit
  valve_status: Unit
  pump_status: Unit
  pipe_status: Unit
  relative_head: Unit
  water_age: Unit
  percentage: Unit
  customer: Unit
  level: Unit

class UnitsData:
  system: Literal["international", "usCustomary"]
  parameters: UnitParameters

class Time:
  def __init__(self, time: datetime, timezone: str):
    self.time = time
    self.timezone = timezone

class Network:
  def __init__(self, sdk):
    self.sdk = sdk

  def get_metadata(self) -> NetworkMetadata:
    """
    Returns the network metadata, including the network UUID and user provided name.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Returns:
      Object with network `id` and `name`
    """
    return self.sdk.network.getMetadata()

  def is_simulation_loading(self) -> bool:
    """
    Returns true if the simulation is loading for the current time (see `get_time()`),
    or false if it has finished loading.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    """
    return self.sdk.network.isSimulationLoading()
  
  def is_simulation_period_completed(self) -> bool:
    """
    Returns true if the simulation is loading for the whole period,
    or false if it has finished loading.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    """
    return self.sdk.network.isSimulationPeriodCompleted()
  
  def is_simulation_error(self) -> bool:
    """
    Returns true if the simulation has failed, or false if it has finished successfully.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    """
    return self.sdk.network.isSimulationError()
  
  def is_scenario_active(self) -> bool:
    """
    Returns true when the network is in scenario mode (user changes are active), or false when otherwise.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    """
    return self.sdk.network.isScenarioActive()

  def get_units(self) -> UnitsData:
    """
    Returns the network units. Take into account these unit values to perform appropriate conversions when
    working with asset parameters, simulation results or creating an scenario

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    """
    return self.sdk.network.getUnits()
  
  def get_bounds(self) -> Bounds:
    """
    Returns a time object with the current network date and timezone.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    """
    return self.sdk.network.getBounds()
  
  def get_time(self) -> Time:
    """
    Returns a time object with the current network date and timezone.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    """
    time = self.sdk.network.getTime()
    date = datetime.fromtimestamp(time.time.valueOf() / 1000)
    return Time(time=date, timezone=time.timezone)
  
  def get_start_time(self) -> Time:
    """
    Returns a time object with the network's day starting date and timezone.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    """
    time = self.sdk.network.getStartTime()
    date = datetime.fromtimestamp(time.time.valueOf() / 1000)
    return Time(time=date, timezone=time.timezone)

  def get_neighbor_assets(self, asset_id: str) -> list[Asset]:
    """
    Returns an array containing all assets immediately neighbouring the specified asset ID.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      assetId - target asset to find neighbours of

    Returns:
      Array of asset objects
    
    Example:
    Find neighbours of a pipe
    ```
    pipe = sdk.network.get_pipes()[0]
    neighbors = sdk.network.get_neighbor_assets(pipe.id)
    # [J1, J2]
    ```
    """
    return self.sdk.network.getNeighborAssets(asset_id)

  def get_connected_assets(self, start_ids: list[str], stop_condition: Callable[[Asset], bool]) -> list[Asset]:
    """
    Returns an array of assets that are connected (i.e: can be reached traversing the network)
    to the given assets, and satisfy the given stop condition. The original assets are returned as well.
   
    The stopCondition function is called for each asset that is connected to the assets with the given
    IDs. If the function returns true, the method will stop traversing the network and any subsequent
    assets will not be returned. If the function returns false, the method will continue traversing
    the network.
  
    The difference between getNeighborAssets and getConnectedAssets is that the latter can return any
    assets that are connected to the given assets, while the former returns only the direct neighbors.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      start_ids - array of asset IDs to start traversing the network from
      stop_condition - lambda expression to evaluate whether continuing traversing the network or not
    
    Returns:
      Array of asset objects
    
    Example:
    Retrieve all the valves that are reachable from the “Horseshoebay” tank in Magnetic Island
    ```
    connected_assets = sdk.network.get_connected_assets(
      ['Horseshoebay'],
      lambda asset: asset.type == 'Valve'
    )
    ```
    """
    return self.sdk.network.getConnectedAssets(start_ids, stop_condition)

  def get_shortest_path(self, from_id: str, to_asset: Callable[[Asset], bool], connection_weight: Callable[[Asset, Asset], float]) -> list[Asset]:
    """
    Returns the shortest path between the given assets, and satisfies the given stop condition.
    The shortest path is the one that has the highest amount of connection weight.
   
    The toAsset function is called for each asset in the network. If the function returns true,
    the method will stop traversing the network and any subsequent assets will not be returned.
   
    The connectionWeight function is called for each possible connection, with two parameters:
    the current asset that is being traversed, and the asset that is being evaluated. It
    should return a number representing the weight of the connection. If multiple connections
    are possible, higher weights are preferred. If the function returns the same number, the
    connection with the lowest ID is preferred. See the examples below for more details.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      fromId - asset ID to start traversing the network from
      toAsset - lambda expression to evaluate whether continuing traversing the network or not
      connectionWeight - lambda expression to evaluate the weight of the next link in the traversal
    
    Returns:
      Array of asset objects
    
    Example:
    Find the path with the widest diameter pipes between the “Nellybay” and the “Cocklebay” tanks in Magnetic Island
    ```
    wider_path = sdk.network.get_shortest_path(
      'Nellybay',
      lambda asset: asset.id == 'Cocklebay',
      lambda start, end: 1 if start.type != 'Pipe' or end.type != 'Pipe' else start.diameter > end.diameter
    )
    ```
    """
    return self.sdk.network.getShortestPath(from_id, to_asset, connection_weight)

  def get_asset(self, asset_id: str) -> Optional[Asset]:
    """
    Get an asset by its id

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      assetId - the id of the asset
    
    Returns:
      the asset or None if not found
    
    Example:
    ```
    # Get a junction
    junction = sdk.network.getAsset('J1')
    # Get a tank
    tank = sdk.network.getAsset('T1')
    ```
    """
    return self.sdk.network.getAsset(asset_id)
  
  def get_assets(self, predicate: Optional[Callable[[Asset], bool]] = None) -> list[Asset]:
    """
    Retrieve all assets that match a predicate.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    
    Args:
      predicate (function): A function that takes an asset and returns a boolean value.

    Returns:
      list[Asset]: A list of assets that match the predicate.
    
    Example:
    Return all assets with an ID containing hello
    ```
    assets = sdk.network.get_assets(lambda asset: 'hello' in asset.id)
    ```
    """
    return self.sdk.network.getAssets(predicate)
  
  def get_junctions(self, predicate: Optional[Callable[[Junction], bool]] = None) -> list[Junction]:
    """
    Retrieve all junctions that match a predicate.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    
    Args:
      predicate (function): A function that takes an asset and returns a boolean value.

    Returns:
      list[Junction]: A list of junctions that match the predicate.
    
    Example:
    Return all junctions located at more than 100m of altitude
    ```
    junctions = sdk.network.get_junctions(lambda j: j.elevation > 100)
    ```
    """
    return self.sdk.network.getJunctions(predicate)

  def get_tanks(self, predicate: Optional[Callable[[Tank], bool]] = None) -> list[Tank]:
    """
    Retrieve all tanks that match a predicate.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    
    Args:
      predicate (function): A function that takes an asset and returns a boolean value.

    Returns:
      list[Tank]: A list of tanks that match the predicate.
    
    Example:
    Return all tanks with a level greater than 10m
    ```
    tanks = sdk.network.get_tanks(lambda pipe: pipe.level > 10)
    ```
    """
    return self.sdk.network.getTanks(predicate)

  def get_pipes(self, predicate: Optional[Callable[[Pipe], bool]] = None) -> list[Pipe]:
    """
    Retrieve all pipes that match a predicate.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    
    Args:
      predicate (function): A function that takes an asset and returns a boolean value.

    Returns:
      list[Pipe]: A list of pipes that match the predicate.
    
    Example:
    Return all pipes with a diameter greater than 20 cm
    ```
    pipes = sdk.network.get_pipes(lambda pipe: pipe.diameter > 20)
    ```
    """
    return self.sdk.network.getPipes(predicate)

  def get_valves(self, predicate: Optional[Callable[[Valve], bool]] = None) -> list[Valve]:
    """
    Retrieve all valves that match a predicate.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    
    Args:
      predicate (function): A function that takes an asset and returns a boolean value.

    Returns:
      list[Valve]: A list of valves that match the predicate.
    
    Example:
    Return all FCV valves in the network
    ```
    fcvs = sdk.network.get_valves(lambda valve: valve.family == ValveFamilies.FCV)
    ```
    """
    return self.sdk.network.getValves(predicate)
  
  def get_pumps(self, predicate: Optional[Callable[[Pump], bool]] = None) -> list[Pump]:
    """
    Retrieve all pumps that match a predicate.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    
    Args:
      predicate (function): A function that takes an asset and returns a boolean value.

    Returns:
      list[Pump]: A list of pumps that match the predicate.
    
    Example:
    Return all pumps located at more than 100m of altitude
    ```
    pumps = sdk.network.get_pumps(lambda p: p.elevation > 100)
    ```
    """
    return self.sdk.network.getPumps(predicate)
  
  def get_supply_sources(self, predicate: Optional[Callable[[SupplySource], bool]] = None) -> list[SupplySource]:
    """
    Retrieve all supply sources that match a predicate.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).
    
    Args:
      predicate (function): A function that takes an asset and returns a boolean value.

    Returns:
      list[Pump]: A list of supply sources that match the predicate.
    
    Example:
    Return all supply sources located at more than 100m of altitude
    ```
    pumps = sdk.network.get_supply_sources(lambda ss: ss.elevation > 100)
    ```
    """
    return self.sdk.network.getSupplySources(predicate)
  
  def get_zone(self, zone_id: str) -> Optional[Zone]:
    """
    Get an zone by its ID

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      zone_id - the ID of the zone
    
    Returns:
      the zone or None if not found
    
    Example:
    ```
    zone = sdk.network.get_zone('Z1')
    ```
    """
    return self.sdk.network.getZone(zone_id)
  
  def get_zones(self, predicate: Optional[Callable[[Zone], bool]] = None) -> list[Zone]:
    """
    Retrieve all zones that match a predicate.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      predicate (function): A function that takes a zone and returns a boolean value.

    Returns:
      list[Zone]: A list of zones that match the predicate.
    
    Example:
    Return all zones with more than 3 inlets
    ```
    pumps = sdk.network.get_zones(lambda z: len(z.inlets) > 3)
    ```
    """
    return self.sdk.network.getZones(predicate)

  def set_demand(self, junction_id: str, demand: float, start_date: Optional[datetime] = None) -> Union[Success, Failure]:
    """
    Sets the demand of a junction to the given value. Returns `success` if the demand was
    successfully set, or `failure` if the junction doesn't exist or the demand could not be set.

    The demand value is set in the `flow` network units (see `get_units()`)

    The provided `start_date` will be automatically adjusted depending on the network configuration.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      junction_id (str): The unique identifier of the junction to set the status for.
      demand: Demand value to be set.
      start_date: _(Optional)_ Date from which the change is applied. Defaults to network timeline date (see `get_time()`)

    Returns:
      Success | Failure: Indicates whether the network operation succeeded or not.

    Example:
    Set the demand of a junction to 10 l/s
    ```
    junction = sdk.network.get_junctions()[0]
    demand = 10

    if sdk.network.get_units().flow != 'l/s':
      # Adapt to proper units
      demand = ...

    sdk.network.set_demand(junction.id, demand)
    ```
    """
    if start_date is None:
      return self.sdk.network.setDemand(junction_id, demand)

    js_date = Date.new(start_date.timestamp() * 1000)
    return self.sdk.network.setDemand(junction_id, demand, js_date)

  def set_junction_pressure(self, junction_id: str, pressure: float, start_date: Optional[datetime] = None) -> Union[Success, Failure]:
    """
    Sets the pressure of a junction to the given value. Returns `success` if the pressure was
    successfully set, or `failure` if the junction doesn't exist or the pressure could not be set.

    The pressure value is set in the `pressure` network units (see `get_units()`)

    The provided `start_date` will be automatically adjusted depending on the network configuration.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      junction_id (str): The unique identifier of the junction to set the status for.
      pressure: Pressure value to be set.
      start_date: _(Optional)_ Date from which the change is applied. Defaults to network timeline date (see `get_time()`)

    Returns:
      Success | Failure: Indicates whether the network operation succeeded or not.

    Example:
    Set the pressure of a junction to 10 mwc
    ```
    junction = sdk.network.get_junctions()[0]
    pressure = 10

    if sdk.network.get_units().pressure != 'mwc':
      # Adapt to proper units
      pressure = ...

    sdk.network.set_junction_pressure(junction.id, pressure)
    ```
    """
    if start_date is None:
      return self.sdk.network.setJunctionPressure(junction_id, pressure)

    js_date = Date.new(start_date.timestamp() * 1000)
    return self.sdk.network.setJunctionPressure(junction_id, pressure, js_date)

  def restore_demand(self, junction_id: str, start_date: Optional[datetime] = None) -> Union[Success, Failure]:
    """
    Restores the demand of a junction to the original demand in the base demand curve. Returns `success`
    if the demand was successfully restored, or `failure` if the junction doesn't exist or the demand
    could not be restored.

    The provided `start_date` will be automatically adjusted depending on the network configuration.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      junction_id (str): The unique identifier of the junction to set the status for.
      start_date: _(Optional)_ Date from which the change is applied. Defaults to network timeline date (see `get_time()`)

    Returns:
      Success | Failure: Indicates whether the network operation succeeded or not.

    Example:
    Restore the demand to its original value after applying a demand of 10 l/s
    ```
    junction = sdk.network.get_junctions()[0]
    sdk.network.set_demand(junction.id, 10)
    sdk.network.restore_demand(junction.id)
    ```
    """
    if start_date is None:
      return self.sdk.network.restoreDemand(junction_id)

    js_date = Date.new(start_date.timestamp() * 1000)
    return self.sdk.network.restoreDemand(junction_id, js_date)

  def restore_junction_pressure(self, junction_id: str, start_date: Optional[datetime] = None) -> Union[Success, Failure]:
    """
    Restores the pressure of a junction to the original pressure, derived from the demand in the base demand
    curve. Returns `success` if the pressure was successfully restored, or `failure` if the junction
    doesn't exist or the pressure could not be restored.

    The provided `start_date` will be automatically adjusted depending on the network configuration.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      junction_id (str): The unique identifier of the junction to set the status for.
      start_date: _(Optional)_ Date from which the change is applied. Defaults to network timeline date (see `get_time()`)

    Returns:
      Success | Failure: Indicates whether the network operation succeeded or not.

    Example:
    Restore the pressure to its original value after applying a pressure of 10 mwc
    ```
    junction = sdk.network.get_junctions()[0]
    sdk.network.set_junction_pressure(junction.id, 10)
    sdk.network.restore_junction_pressure(junction.id)
    ```
    """
    if start_date is None:
      return self.sdk.network.setJunctionPressure(junction_id)

    js_date = Date.new(start_date.timestamp() * 1000)
    return self.sdk.network.setJunctionPressure(junction_id, js_date)

  def set_setting(self, asset_id: str, setting: float, start_date: Optional[datetime] = None) -> Union[Success, Failure]:
    """
    Sets the setting of an asset to the given value. Returns `success` if the setting was
    successfully set, or `failure` if the asset doesn’t exist or the setting could not be set.

    The setting value units depend on the asset type, being:
    - Pump: relative speed setting scaled to 1.0 (where 1 is 100% speed)
    - Regulation Valve: valve setting, changing with valve type (for example, FCV = target regulation flow)
    - TCV: valve throttling amount scaled to 1.0 (where 1 is 100% open)

    The provided `startDate` will be automatically adjusted depending on the network configuration.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      asset_id (str): The unique identifier of the asset to set the status for.
      setting: Setting value to be set
      start_date: _(Optional)_ Date from which the change is applied. Defaults to network timeline date (see `get_time()`)

    Returns:
      Success | Failure: Indicates whether the network operation succeeded or not.

    Example:
    Set the setting of a PRV to 10 mwc
    ```
    valve_id = 'my-prv'
    pressure = 10

    if sdk.network.get_units().pressure != 'mwc':
      # Adapt to proper units
      pressure = ...

    sdk.network.set:setting(valve_id, pressure)
    ```
    """
    if start_date is None:
      return self.sdk.network.setSetting(asset_id, setting)

    js_date = Date.new(start_date.timestamp() * 1000)
    return self.sdk.network.setSetting(asset_id, setting, js_date)

  def set_status(self, asset_id: str, status: Literal['OPEN', 'CLOSED'], start_date: Optional[datetime] = None) -> Union[Success, Failure]:
    """
    Sets the status of an asset to the given value. Returns `success` if the status was
    successfully set, or `failure` if the asset doesn't exist or the status could not be set.

    The status value type depends on the asset type, being:
    - Pump: "OPEN" to switch on the pump, "CLOSED" to switch it off
    - TCV: "OPEN" to 100% open it, "CLOSED" to 100% close it
    - Pipe: "OPEN" to mark it as an open pipe (allows flow), "CLOSED" to mark it as closed (does not allow flow)

    The provided `startDate` will be automatically adjusted depending on the network configuration.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      asset_id (str): The unique identifier of the asset to set the status for.
      status (OPEN | CLOSED): The new status of the asset.
      start_date: _(Optional)_ Date from which the change is applied. Defaults to network timeline date (see `get_time()`)

    Returns:
      Success | Failure: Indicates whether the network operation succeeded or not.

    Example:
    ```
    pump = sdk.network.get_pumps()[0]
    # Shut down the pump
    sdk.network.set_status(pump.id, 'CLOSED')
    ```
    """
    if start_date is None:
      return self.sdk.network.setStatus(asset_id, status)

    js_date = Date.new(start_date.timestamp() * 1000)
    return self.sdk.network.setStatus(asset_id, status, js_date)

  def set_time(self, time: datetime) -> None:
    """
    Sets the network time to the given date.

    This method is part of the Network API (https://developer.qatium.app/api/sdk/network).

    Args:
      time (datetime): The new date to set the network time to.

    Returns:
      None

    Example:
    Set the network time to 2022-01-01
    ```
    sdk.network.set_time(datetime(2022, 1, 1))
    ```
    """
    js_date = Date.new(time.timestamp() * 1000)
    return self.sdk.network.setTime(js_date)