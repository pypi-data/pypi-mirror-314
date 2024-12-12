from pyodide import ffi
from typing import List, Union, Optional, Dict, Any

from .types import Coordinate, ElementIdentifier, Success, Failure, ElementId, Bounds, ElementType
from .assets import valve, junction, pipe

class StyleProperties():
    isShadowVisible: Optional[bool]
    shadowColor: Optional[str]
    outlineOpacity: Optional[float]
    isElementVisible: Optional[bool]
    elementColor: Optional[str]
    iconId: Optional[str]

Styles = Dict[str, StyleProperties]

class Padding():
    top: int
    bottom: int
    left: int
    right: int

class CameraOptions():
    zoom: Optional[float]
    pitch: Optional[float]
    transitionDuration: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]
    bearing: Optional[float]
    padding: Optional[Padding]

class FlightOptions():
    padding: Padding
    flightDuration: float
    maxZoom: float

class Camera():
    zoom: float
    pitch: float
    bearing: float
    center: Coordinate

class Map:
  def __init__(self, sdk):
    self.sdk = sdk

  async def fit_to(self, bounds_or_ids: Union[List[str], Bounds], options: Optional[FlightOptions] = None) -> None:
    """
    Centers the map viewport, while fitting a set of destination network
    elements or bounds, using the animation options set in the optional
    options parameter.

    Args:
        bounds_or_ids: Accepts an asset/zone ID array or bounds as destination.
        options: _(Optional)_ Options object that accepts:
          - `padding` _(Optional)_ Dimensions in pixels applied on each side of the viewport for shifting the vanishing point.
          - `flightDuration` _(Optional)_ The animation’s duration, measured in milliseconds.
          - `maxZoom` _(Optional)_ The max level of zoom allowed to perform the action.

    Returns:
        A promise with no value to allow async calls, resolved when the camera movement has finished.

    Example:
        Center the map to the Horseshoebay tank, using a slow animation (5 seconds),
        with a padding of 100 pixels on each side:
        ```
        sdk.map.fit_to(['Horseshoebay'], {
          'flightDuration': 5000,
          'maxZoom': 20,
          'padding': {
              'top': 100,
              'right': 100,
              'bottom': 100,
              'left': 100
          }
        })
        ```
    """
    return await self.sdk.map.fitTo(bounds_or_ids, ffi.to_js(options))

  async def move_to(self, options: Optional[CameraOptions] = None) -> Union[Success, Failure]:
    """
    Transitions the camera view, following a set of travel options.

    Args:
        options (CameraOptions): Options object that accepts:
          - `padding` (Optional): Dimensions in pixels applied on each side of the viewport.
          - `transitionDuration` (Optional): The animation’s duration, measured in milliseconds.
          - `zoom` (Optional): Target zoom level.
          - `pitch` (Optional): Angle towards the horizon, measured in degrees (0-85).
          - `latitude` (Optional): Geographic latitude (-90 to 90).
          - `longitude` (Optional): Geographic longitude (-180 to 180).
          - `bearing` (Optional): The direction the camera is facing, measured in degrees (0° is north, 90° is east, etc.).

    Returns:
        Success | Failure: Indicates whether the camera movement was successful or not.

    Example:
        Move the camera to Mandalay in Magnetic Island, AU:
        ```
        sdk.map.move_to({
            'latitude': -19.157,
            'longitude': 146.849
        })
        ```

        Do a tilted camera travel to the same location:
        ```
        sdk.map.move_to({
            'zoom': 18,
            'pitch': 45,
            'transitionDuration': 2000,
            'latitude': -19.157,
            'longitude': 146.849
        })
        ```
    """
    return await self.sdk.map.moveTo(ffi.to_js(options))

  def set_highlights(self, element_ids: List[ElementId]) -> None:
    """
    Highlights the network elements passed as parameters (assets or zones) in element_ids (an array of element IDs).
    If the element_ids array is empty, all highlights are cleared (equivalent to using clearHighlights()).

    Args:
        element_ids (List[ElementId]): An array of asset/zone IDs to be highlighted.

    Example:
        Highlights two tanks in Magnetic Island:
        ```
        sdk.map.set_highlights(['Nellybay', 'Horseshoebay'])
        ```
    """
    return self.sdk.map.setHighlights(ffi.to_js(element_ids))

  def clear_highlights(self) -> Success:
    """
    Clears all the highlights in the map.

    Returns:
        Success: Indicates whether the highlights were successfully cleared.
    """
    return self.sdk.map.clearHighlights()

  def get_selected_element(self) -> Optional[ElementIdentifier]:
    """
    Returns a SelectedElement object representing the currently selected element in the map, or None
    if nothing is selected. The SelectedElement object contains the element ID and the type of element.

    Returns:
        Optional[ElementIdentifier]: The selected element's ID and type, or None if nothing is selected.

    Example:
        ```
        selected_element = sdk.map.get_selected_element()
        selected_element['id']  # The element ID
        selected_element['type']  # Type in "Pipe", "Junction", "Valve", "Pump", "SupplySource", "Tank", or "Zone"
        ```
    """
    return self.sdk.map.getSelectedElement()

  def add_overlay(self, layers: List[Any]) -> Union[Success, Failure]:
    """
    Adds a custom visual overlay on top of the map.

    At the moment, the map overlays are using DeckGL, and the content added might not be fully in sync with the map below.

    Be aware you'll only be able to declare a single overlay. Any subsequent calls to this method will overwrite the previous overlay.

    Args:
        layers (List[Any]): A list of layer objects containing all data and styling, from any of the supported layer types.

    Returns:
        Success | Failure: Indicates whether the overlay was successfully added or not.
    """
    return self.sdk.map.addOverlay(ffi.to_js(layers))

  def show_overlay(self) -> Union[Success, Failure]:
    """
    Forces all the layers in the overlay to be shown.

    Returns:
        Success | Failure: Indicates whether the layers were successfully shown.
    """
    return self.sdk.map.showOverlay()

  def hide_overlay(self) -> Union[Success, Failure]:
    """
    Hides/removes all the layers of the overlay.

    Returns:
        Success | Failure: Indicates whether the layers were successfully hidden or removed.
    """
    return self.sdk.map.hideOverlay()

  def get_camera(self) -> Camera:
    """
    Returns the current state of the map camera.

    Returns:
        Camera: An object containing the camera's current state, including:
          - `zoom`: Target zoom level.
          - `pitch`: Angle towards the horizon, measured in degrees (0-85).
          - `center`: A dictionary with the longitude and latitude at which the camera is pointed.
          - `bearing`: The direction the camera is facing, measured clockwise from true north.

    Example:
        ```
        camera = sdk.map.get_camera()
        print(camera.zoom)  # Target zoom level
        print(camera.center)  # {'lng': longitude, 'lat': latitude}
        ```
    """
    return self.sdk.map.getCamera()

  def add_styles(self, styles: Styles) -> Union[Success, Failure]:
    """
    Allows changing the styles of elements on the map.

    Args:
        styles (Styles): A dictionary where the keys are asset IDs and the values are style properties.

    Returns:
        Success | Failure: Indicates whether the operation was successful.

    Example:
        Highlight some tanks in yellow:
        ```
        sdk.map.add_styles({
            "Horseshoebay": {
                "isShadowVisible": True,
                "outlineOpacity": 1,
                "shadowColor": "yellow"
            },
            "Nellybay": {
                "isShadowVisible": True,
                "outlineOpacity": 1,
                "shadowColor": "yellow"
            }
        })
        ```
    """
    return self.sdk.map.addStyles(ffi.to_js(styles))

  def remove_styles(self) -> Success:
    """
    Deletes styles applied with the addStyles method.

    Returns:
        Success: Indicates whether the styles were successfully removed.
    """
    return self.sdk.map.removeStyles()

  def select_asset(self, asset: Union[Dict[str, Any], Dict[str, Any]]) -> None:
    """
    Selects an asset or zone on the map.

    Args:
        asset (Union[Dict[str, Any], Dict[str, Any]]): An object containing geometry, type, and ID of the asset to select or geometry and ID for the zone.

    Example:
        Select the first zone in the network:

        ```
        zone = sdk.network.getZones()[0]
        sdk.map.select_asset(zone.id)
        ```
    """
    return self.sdk.map.selectAsset(ffi.to_js(asset))

  def hide_map_layer(self, type: ElementType, group: Optional[Union[valve.ValveGroupType, junction.JunctionGroupType, pipe.PipeGroupType]] = None) -> None:
    """
    Hides a base map layer for a specific asset type and optionally, group.

    Args:
        type (ElementType): The asset type to hide from the base map.
        group (Optional[Union[valve.ValveGroupType, junction.JunctionGroupType, pipe.PipeGroupType]]): The asset group to hide, when applicable.

    Example:
        Hide lateral pipe layer:
        ```
        sdk.map.hide_map_layer("Pipe", "lateral")
        ```
    """
    return self.sdk.map.hideMapLayer(type, ffi.to_js(group))


  def show_map_layer(self, type: ElementType, group: Optional[Union[valve.ValveGroupType, junction.JunctionGroupType, pipe.PipeGroupType]] = None) -> None:
    """
    Shows a base map layer for a specific asset type and optionally, group.

    Args:
        type (ElementType): The asset type to show from the base map.
        group (Optional[Union[valve.ValveGroupType, junction.JunctionGroupType, pipe.PipeGroupType]]): The asset group to show, when applicable.

    Example:
        Show customer points:

        ```
        sdk.map.show_map_layer("Junction", "customerPoint")
        ```
    """
    return self.sdk.map.showMapLayer(type, ffi.to_js(group))

  def update_icon(self, elements: List[str], icon_id: str) -> Union[Success, Failure]:
    """
    Allows changing the icons of elements on the map. An icon must be registered before assigning it to any element.

    Args:
        elements (List[str]): Array of asset IDs to change the icon of.
        icon_id (str): Name of the icon to be used by the feature, which must be previously registered.

    Returns:
        Success | Failure: Indicates whether the icon was successfully updated or not.

    Example:
        Change icon of some regulation valves:

        ```
        sdk.map.update_icon(['Nellybay_PSV', 'Arcadia_DMA_PRV', 'Picnic_Mainland_FCV'], "my-icon")
        ```
    """
    return self.sdk.map.updateIcon(ffi.to_js(elements), icon_id)


  async def register_icon(self, id: str, svg: str) -> Union[Success, Failure]:
    """
    Registers an SVG icon to the map instance.

    Args:
        id (str): Icon ID.
        svg (str): Icon SVG contents.

    Returns:
        Promise[Success | Failure]: A promise with success or failure message, resolved when the icon has been registered.

    Example:
        ```
        sdk.map.register_icon('custom-icon', '<svg></svg>')
        ```
    """
    return await self.sdk.map.registerIcon(id, svg)