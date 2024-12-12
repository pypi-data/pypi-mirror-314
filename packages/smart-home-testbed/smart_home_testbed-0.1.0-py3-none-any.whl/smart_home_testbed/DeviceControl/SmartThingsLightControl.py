from .SmartThingsControl import SmartThingsControl
from .LightControl import LightControl


class SmartThingsLightControl(SmartThingsControl, LightControl):
    """
    Abstract class to control a generic light bulb through SmartThings.
    """

    ## Screen event coordinates
    # Toggle
    x = 626.4
    y = 273.6
    # Brightness and color gauges
    x_left_gauge = 21
    x_right_gauge = 692
    # Brightness
    y_brightness = 504
    # Color
    y_color = 1036.8
