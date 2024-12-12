from typing import Any
from .network import Network, AssetStatus
from .ui import UI
from .map import Map
from .commands import Commands
from .integrations import Integrations
import _sdk

class SDK:
  def __init__(self, sdk):
    self.sdk = sdk
    self.network = Network(sdk)
    self.ui = UI(sdk)
    self.map = Map(sdk)
    self.commands = Commands(sdk)
    self.integrations = Integrations(sdk)

sdk = SDK(_sdk)
