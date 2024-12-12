from typing import Any, Literal, Optional, Union
from pyodide import ffi
from js import Object

class UI:
  def __init__(self, sdk):
    self.sdk = sdk

  def send_message(self, message: Any):
    """
    Send a message to the user interface.

    Args:
        message (str): The message to send to the user interface.
    """
    self.sdk.ui.sendMessage(ffi.to_js(message, dict_converter=Object.fromEntries))

  def is_map_view(self) -> bool:
    """
    Returns whether the map view is active or not.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).

    Returns:
      True if the map view is active, False if it is not
    """
    return self.sdk.ui.isMapView()

  def is_synoptic_view(self) -> bool:
    """
    Returns whether the synoptic view is active or not.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).

    Returns:
      True if the synoptic view is active, False if it is not
    """
    return self.sdk.ui.isSynopticView()

  def is_network_level_visible(self, level: Literal['arterial', 'distribution']) -> bool:
    """
    Returns whether an asset level is visible in the map.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).

    Args:
      level: Asset level as `arterial` or `distribution`

    Returns:
      True if the asset level is active, False if it is not
    """
    return self.sdk.ui.isNetworkLevelVisible(level)

  def is_map_layer_visible(
      self,
      type: Literal['Pipe', 'Junction', 'Valve', 'Pump', 'SupplySource', 'Tank'],
      layer: Optional[Literal['regulating', 'shutOff', 'hydrant', 'junction', 'supplySource', 'main', 'lateral']]) -> bool:
    """
    Returns whether the layer for the `AssetType` is visible in the map.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).

    Args:
      type: `Pipe`, `Junction`, `Valve`, `Pump`, `SupplySource` or `Tank`
      layer: (Optional) When type is `Valve`: `regulating`, `shutOff`, when type is `Junction`: `hydrant`, `junction`, `customerPoint`, when type is `Pipe`: `main`, `lateral`

    Returns:
      True if the layer isvisible, False if it is not
    """
    return self.sdk.ui.isMapLayerVisible(type, layer)

  def is_panel_open(self) -> bool:
    """
    Returns whether the plugin's UI panel is visible or not.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).

    Returns:
      True if the panel is visible, False if it is not
    """
    return self.sdk.ui.isPanelOpen()

  def open_panel(self):
    """
    Forcely opens the plugin's UI panel.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).
    """
    self.sdk.ui.openPanel()

  def close_panel(self):
    """
    Forcely closes the plugin's UI panel.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).
    """
    self.sdk.ui.closePanel()

  def is_plugin_visible(self) -> bool:
    """
    Returns whether the plugin's custom visuals (highlights, map overlays and styles) are visible or not.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).

    Returns:
      True if the plugin visuals are visible, False if are not
    """
    return self.sdk.ui.isPluginVisible()

  def get_language(self) -> Literal['es', 'en']:
    """
    Returns the active UI language.

    This method is part of the UI API (https://developer.qatium.app/api/sdk/ui).

    Returns:
      The code for the active language
    """
    return self.sdk.ui.getLanguage()
