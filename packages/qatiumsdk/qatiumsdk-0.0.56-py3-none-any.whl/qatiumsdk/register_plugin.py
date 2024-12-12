import _sdk
from pyodide import ffi
from .sdk_version import sdk_version
from .plugin import Plugin

def init(plugin: Plugin):
  version = ffi.to_js(sdk_version)
  plugin = ffi.to_js(plugin)

  _sdk.register_plugin(plugin, version)