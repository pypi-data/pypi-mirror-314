from typing import Any, Awaitable
import asyncio
from tapo import ApiClient
from .DeviceState import DeviceState


class TapoState(DeviceState):
    """
    Class to represent the state of a generic Tapo device.
    """


    def __init__(self, ipv4: str, **kwargs) -> None:
        """
        Constructor.
        Initializes the Tapo device with its IP address,
        and creates a Tapo API client.

        Args:
            ipv4 (str): The Tapo device's IPv4 address.
            kwargs (dict): device-specific additional parameters,
                           including user's credentials.
        """
        self.ipv4 = ipv4
        self.client = ApiClient(
            kwargs.get("username", ""),
            kwargs.get("password", "")
        )
    

    async def _async_get_state(self) -> Awaitable[Any]:
        """
        Asynchronously get the status of the generic Tapo device.

        Returns:
            Awaitable[Any]: async function which returns the Tapo device's status.
        """
        dev = await self.client.generic_device(self.ipv4)
        info = await dev.get_device_info()
        return info
    

    def get_state(self) -> Any:
        """
        Get the state of the Tapo device.

        Returns:
            Any: Tapo device status
        """
        return asyncio.run(self._async_get_state())
