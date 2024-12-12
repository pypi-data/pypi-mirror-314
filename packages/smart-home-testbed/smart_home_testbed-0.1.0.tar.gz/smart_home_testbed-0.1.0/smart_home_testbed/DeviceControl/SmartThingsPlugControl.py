from .SmartThingsControl import SmartThingsControl
from .PlugControl import PlugControl


class SmartThingsPlugControl(SmartThingsControl, PlugControl):
    """
    Abstract class to control a generic plug through SmartThings.
    """

    # Toggle coordinates
    x = 626.4
    y = 273.6
