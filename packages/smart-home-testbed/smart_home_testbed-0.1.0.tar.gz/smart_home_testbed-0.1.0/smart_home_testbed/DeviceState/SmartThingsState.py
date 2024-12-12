from typing import List, Any, Awaitable
import asyncio
import aiohttp
from pysmartthings import SmartThings, DeviceEntity
from .DeviceState import DeviceState


class SmartThingsState(DeviceState):
    """
    Abstract class which represents a generic SmartThings device's state.
    """


    @staticmethod
    async def _get_all_devices(token: str) -> Awaitable[List[DeviceEntity]]:
        """
        Asynchronously get all the devices connected to SmartThings.

        Args:
            token (str): SmartThings API token.
        Returns:
            Awaitable[List]: async function which returns the list of all devices.
        """
        async with aiohttp.ClientSession() as session:
            api = SmartThings(session, token)
            devices = await api.devices()
            return devices
        
    
    @classmethod
    def get_all_devices(cls) -> List[DeviceEntity]:
        """
        Get all the devices connected to SmartThings.

        Returns:
            List: list of all devices
        """
        return asyncio.run(cls._get_all_devices())
    

    @classmethod
    def print_all_devices(cls) -> None:
        """
        Print the label, name and id of all devices connected to SmartThings.
        """
        for device in cls.get_all_devices():
            print(device.label, device.name, device.device_id)

    
    async def _async_get_state(self) -> Awaitable[Any]:
        """
        Asynchronously get the SmartThings device status.

        Returns:
            Awaitable[Any]: async function which returns the device status.
        """
        async with aiohttp.ClientSession() as session:
            api = SmartThings(session, self.token)
            devices = await api.devices(device_ids=[self.id])
            device = devices[0]
            await device.status.refresh()
            return device.status
    

    def get_state(self) -> Any:
        """
        Get the device status.

        Returns:
            Any: device status
        """
        return asyncio.run(self._async_get_state())
