from ....DeviceState import ScreenshotState
from ....DeviceControl import TuyaControl, PlugControl


class TuyaPlug(ScreenshotState, TuyaControl, PlugControl):
    """
    Tuya generic plug.
    """

    ## Screen coordinates
    # Device controls screen coordinates
    device_x = 345.6
    device_y = 360
    # Toggle coordinates
    x = 360
    y = 561.6
