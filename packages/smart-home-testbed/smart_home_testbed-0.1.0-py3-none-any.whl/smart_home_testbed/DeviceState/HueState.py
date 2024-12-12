from typing import Awaitable
from enum import Enum
import contextlib
import asyncio
from aiohue import HueBridgeV2, create_app_key
from .LightState import LightState


class HueState(LightState):
    """
    Class to represent the state of a Philips Hue light bulb.
    """


    class StateKeys(Enum):
        """
        Enum for the keys in the dictionary representing the state of the Philips Hue device.
        """
        IS_ON      = "is_on"
        BRIGHTNESS = "brightness"
        COLOR_X    = "color_x"
        COLOR_Y    = "color_y"

    
    @staticmethod
    async def _get_app_key(bridge_ip: str) -> Awaitable[str]:
        """
        Asynchronously get the app key for the Philips Hue bridge.

        Args:
            bridge_ip (str): IP address of the Philips Hue bridge.
        Returns:
            Awaitable[str]: async function which returns the app key.
        """
        input("Press the link button on the bridge and press enter to continue...")
        return await create_app_key(bridge_ip, "authentication_example")
    

    @classmethod
    def get_app_key(cls, bridge_ip: str) -> str:
        """
        Get the app key for the Philips Hue bridge.

        Args:
            bridge_ip (str): IP address of the Philips Hue bridge.
        Returns:
            str: app key.
        """
        with contextlib.suppress(KeyboardInterrupt):
            asyncio.run(cls._get_app_key(bridge_ip))

    
    async def _async_get_state(self) -> Awaitable[dict]:
        """
        Get the state of the Philips Hue light asynchronously.

        Returns:
            Awaitable[dict]: async function which returns the status of the Philips Hue light.
        """
        async with HueBridgeV2(self.ipv4, self.appkey) as bridge:
            light = next(l for l in bridge.lights.items)
            return {
                self.StateKeys.IS_ON:      light.is_on,
                self.StateKeys.BRIGHTNESS: light.brightness,
                self.StateKeys.COLOR_X:    light.color.xy.x,
                self.StateKeys.COLOR_Y:    light.color.xy.y
            }
        
    
    def get_state(self) -> dict:
        """
        Get the state of the Philips Hue light.

        Returns:
            dict: The status of the Philips Hue light.
        """
        return asyncio.run(self._async_get_state())
