from typing import Union
from pyodide import ffi  # For ffi.to_js conversion
from .types import Success, Failure  # Assuming these are defined in types module

class Secrets:
  """
  The Secrets class for managing API integration secrets.
  """

  def __init__(self, sdk):
    """
    Initializes the Secrets class with the SDK.
    """
    self.sdk = sdk

  async def get(self, key: str) -> str:
    """
    Retrieves an API integration secret from storage.

    Resolves to no-op when running in developer mode unless your developer account is
    approved by Qatium to do 3rd party API integrations.

    Args:
        key (str): The name of the secret.

    Returns:
        str: The secret value.
    """
    js_key = ffi.to_js(key)  # Convert key to JS-compatible format
    return await self.sdk.integrations.secrets.get(js_key)

  async def has(self, key: str) -> bool:
    """
    Retrieves whether an API integration secret exists.

    Resolves to no-op when running in developer mode unless your developer account is
    approved by Qatium to do 3rd party API integrations.

    Args:
        key (str): The name of the secret.

    Returns:
        bool: True if the secret exists, False otherwise.
    """
    js_key = ffi.to_js(key)  # Convert key to JS-compatible format
    return await self.sdk.integrations.secrets.has(js_key)

  async def set(self, key: str, value: str) -> Union[Success, Failure]:
    """
    Securely stores an API integration secret in storage.

    Resolves to no-op when running in developer mode unless your developer account is
    approved by Qatium to do 3rd party API integrations.

    Args:
        key (str): The name of the secret.
        value (str): The value of the secret.

    Returns:
        Success | Failure: The operation status.
    """
    js_key = ffi.to_js(key)  # Convert key to JS-compatible format
    js_value = ffi.to_js(value)  # Convert value to JS-compatible format
    return await self.sdk.integrations.secrets.set(js_key, js_value)
