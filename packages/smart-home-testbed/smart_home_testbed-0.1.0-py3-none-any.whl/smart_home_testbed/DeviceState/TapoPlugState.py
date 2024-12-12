from typing import Awaitable
from .TapoState import TapoState


class TapoPlugState(TapoState):
    """
    Class to represent the state of a Tapo plug.
    """

    async def _async_get_state(self) -> Awaitable[bool]:
        """
        Asynchronously get the state of the Tapo plug.

        Returns:
            Awaitable[bool]: async function which returns True if the plug is on, False otherwise.
        """
        dev = await self.client.p110(self.ipv4)
        info = await dev.get_device_info()
        return info.device_on
