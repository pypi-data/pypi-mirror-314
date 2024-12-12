from typing import Awaitable
from ....DeviceState import SmartThingsState
from ....DeviceControl import SmartThingsPlugControl


class SmartThingsOutlet(SmartThingsState, SmartThingsPlugControl):
    """
    SmartThings Outlet.
    """

    ## Class attributes
    # Screen to open the device controls from the "Devices" tab
    device_x = 187.2
    device_y = 532.8


    async def _async_get_state(self) -> Awaitable[bool]:
        """
        Asynchronously get the state of the plug.

        Returns:
            Awaitable[bool]: async function which returns True if the plug is on, False otherwise.
        """
        state = await super()._async_get_state()
        return state.switch
