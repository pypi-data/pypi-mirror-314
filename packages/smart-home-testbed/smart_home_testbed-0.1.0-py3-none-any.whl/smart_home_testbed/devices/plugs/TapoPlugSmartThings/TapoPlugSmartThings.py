from ....DeviceState import TapoPlugState
from ....DeviceControl import SmartThingsPlugControl


class TapoPlugSmartThings(TapoPlugState, SmartThingsPlugControl):
    """
    Tapo P110 plug,
    controlled by the SmartThings app.
    """

    ## Class attributes
    # Screen coordinates to open the device controls
    device_x = 187.2
    device_y = 792
