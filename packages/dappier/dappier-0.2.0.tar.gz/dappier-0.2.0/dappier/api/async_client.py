import httpx
import logging
import asyncio
from dappier.types import BASE_URL

class DappierAsyncClient:
  def __init__(self, api_key) -> None:
    """
    Initialize the API clinet.

    :param api_key: The api key used to interact with the Dappier apis.
    """
    self.api_key = api_key

    self._baseUrl = BASE_URL
    self._headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
    }
    self.client = httpx.AsyncClient(base_url=self._baseUrl, headers=self._headers, timeout=60.0)
  
  async def close(self):
    """
    Explicitly close the AsyncClinet to release resources.
    """
    if not self.client.is_closed:
      await self.client.aclose()
  
  async def __aenter__(self):
    """
    Suppport async context management to automatically open the client.
    """
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    """
    Support async context management to automatically close the client.
    """
    await self.close()

  def __del__(self):
    """
    Ensure the client is closed, If it is not closed explicitly.
    """
    if self.client and not self.client.is_closed:
      logging.warning(
        "DappierAsyncClient instance was not closed properly."
        "Use `async with` or explicitly call `close()` to manage resources."
      )
      asyncio.create_task(self.client.aclose())
