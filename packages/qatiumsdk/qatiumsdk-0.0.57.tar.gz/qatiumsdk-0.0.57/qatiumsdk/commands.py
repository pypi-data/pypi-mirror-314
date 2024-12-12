from typing import Dict, List, Any, Callable, Awaitable, Optional
from pyodide import ffi

Arguments = Dict[str, str]

class CommandDescription:
  """
  The description of a command.
  """
  def __init__(self, name: str, description: str, aliases: List[str], arguments: Arguments, returnType: Dict[str, str]):
    self.name = name
    self.description = description
    self.aliases = aliases
    self.arguments = arguments
    self.returnType = returnType


class CommandAnswer:
  """
  Represents the answer of a command.
  """
  def __init__(self, data: Optional[Dict[str, Any]] = None, openPanel: bool = False):
    self.data = data or {}
    self.openPanel = openPanel

CommandFn = Callable[[Dict[str, str]], Awaitable[Dict[str, Any]]]

class Command:
  """
  A command with a unique identifier, description, and a function that executes the command.
  """
  def __init__(self, id: str, description: CommandDescription, fn: CommandFn):
    self.id = id
    self.description = description
    self.fn = fn


class Commands:
  def __init__(self, sdk):
    """
    Initializes the Commands class with the SDK.
    """
    self.sdk = sdk

  def available_commands(self) -> List[Command]:
    """
    Returns the available commands to call. You can use this method to connect your plugin with other plugins, or with other components.

    Returns:
        List[Command]: A list of available commands.
    """
    return self.sdk.commands.availableCommands()

  def add_command(self, description: Dict[str, Any], fn: CommandFn) -> None:
    """
    Allows the plugin to expose commands to be used by other components like Digital assistant (Q), other plugins, or other components.

    Args:
        description (Dict[str, Any]): The description of the command.
        fn (CommandFn): The function that will be executed when the command is called.

    Example:
        ```
        async def set_junction_demand_command(args: Dict[str, str]) -> CommandAnswer:
          junctionId = args.junctionId
          demand = args.demand

          # Simulate setting the demand in the network
          sdk.network.setDemand(junctionId, float(demand))

          return {
              "data": {
                  "junctionId": junctionId,
                  "newDemand": demand
              },
              "openPanel": True
          }


        # Define the command description
        command_description = {
          "name": "Set junction demand",
          "description": "Sets the demand of a junction",
          "aliases": [
            "set demand",
            "change demand",
            "increase flow in junction",
            "set flow in junction"
          ],
          "arguments": {
            "junctionId": "the id of the junction",
            "demand": "the new demand of the junction"
          },
          "returnType": {
            "junctionId": "the id of the junction",
            "newDemand": "the new demand of the junction"
          }
        }

        # Add the command to the SDK
        sdk.commands.addCommand(command_description, set_junction_demand_command)
        ```
    """
    js_description = ffi.to_js(description)
    js_fn = ffi.to_js(fn)
    self.sdk.commands.addCommand(js_description, js_fn)