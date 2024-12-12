import asyncio
from kasa import Discover
from .DeviceState import DeviceState


class TpLinkPlugState(DeviceState):
    """
    Class to represent the state of a TP-Link plug.
    """


    def get_state(self) -> bool:
        """
        Get the state of the plug.

        Returns:
            bool: True if the plug is on, False otherwise.
        Raises:
            TimeoutError: If the plug is not reachable.
        """
        dev = asyncio.run(Discover.discover_single(self.ipv4))
        return dev.is_on
