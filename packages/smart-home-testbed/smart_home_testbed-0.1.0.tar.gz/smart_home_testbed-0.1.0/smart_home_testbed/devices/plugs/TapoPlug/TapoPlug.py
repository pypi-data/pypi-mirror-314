from ....DeviceState import TapoPlugState
from ....DeviceControl import TapoPlugControl


class TapoPlug(TapoPlugState, TapoPlugControl):
    """
    Tapo P110 plug.
    """
    
    # Screen coordinates for device controls
    device_x = 532.8
    device_y = 446.4
