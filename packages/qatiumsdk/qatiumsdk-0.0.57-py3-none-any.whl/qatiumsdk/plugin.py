from typing import Optional, Any
from .types import ElementIdentifier

class Plugin:
  def init(self) -> None:
    """
    Called once by Qatium. Used to initialize things in the plugin.
    Examples:
    - Getting bounds or units of the network
    - Exposing plugin commands
    - Registering icons in the map
    """
    pass  # This can be overridden by the plugin implementation

  def run(self) -> None:
    """
    Called whenever the plugin needs to be re-rendered. Can be called multiple times with variable frequency.
    Avoid timing code here and avoid side effects. Use this method to perform any computations using the SDK.
    """
    pass

  def onNetworkChanged(self) -> None:
    """
    Notified every time the network changes. This can happen due to:
    - Scenarios initiated by the user
    - New SCADA readings
    - The user changing the network date
    - Etc.
    """
    pass

  def onZoomChanged(self) -> None:
    """
    Notified every time the zoom changes due to user interaction.
    """
    pass

  def reset(self) -> None:
    """
    Notified every time the scenario gets deleted, causing all user-made changes to be reset to the initial state.
    """
    pass

  def cleanUp(self) -> None:
    """
    Notified when the plugin is getting cleaned up (e.g., when the user exits the network view or disables the plugin).
    Can be used to abort in-progress operations.
    """
    pass

  def onMessage(self, message: Any) -> None:
    """
    Notified every time the plugin receives a message from the plugin UI panel.
    Args:
        message (Any): The message sent from the UI.

    Example:
    Panel code:
    import { sendMessage } from "@qatium/sdk/ui";
    sendMessage("my-message");

    Plugin code:
    class MyPlugin(Plugin):
      def onMessage(self, message):
        print(message)  # Outputs: "my-message"
    """
    pass

  def onElementSelected(self, element: Optional[ElementIdentifier]) -> None:
    """
    Notified every time the user selects an Asset on the map.
    Args:
        element (Optional[ElementIdentifier]): The selected element.

    Example:
    onElementSelected(element):
      sdk.ui.sendMessage({
        "event": "selected-element-changed",
        "id": element.id if element else None
      })
    """
    pass
