import time
from ....DeviceState import HueState
from ....DeviceControl import LightControl


class HueLight(HueState, LightControl):
    """
    Philips Hue light bulb.
    """

    ### Class variables
    # Android package
    android_package = "com.philips.lighting.hue2"
    ## Screen coordinates
    # Zone button
    x_zone = 360
    y_zone = 446.4
    # Toggle button
    x = 136.8
    y = 1022.4


    def start_app(self) -> None:
        """
        Start the Philips Hue app on the phone,
        and open the light control screen.

        Raises:
            IndexError: If no adb device is found.
        """
        phone = self.get_phone()
        # Open app
        phone.shell(f"monkey -p {self.android_package} -c android.intent.category.LAUNCHER 1")
        time.sleep(10)
        # Open zone controls
        phone.shell(f"input tap {self.x_zone} {self.y_zone}")


    def set_brightness(self) -> None:
        raise NotImplementedError("Brightness cannot be set randomly for Philips Hue lights controlled through the Hue app.")
    

    def set_color(self) -> None:
        raise NotImplementedError("Color cannot be set randomly for Philips Hue lights controlled through the Hue app.")


