from ppadb.device import Device as AdbDevice
from ppadb.client import Client as AdbClient
import cv2
import numpy as np


class DeviceControl:
    """
    Abstract class which provides methods to control a device.
    """

    ADB_SERVER_IP   = "127.0.0.1"
    ADB_SERVER_PORT = 5037


    def get_phone(self) -> AdbDevice:
        """
        Get the adb device object.

        Returns:
            ppadb.device.Device: The adb device object.
        Raises:
            IndexError: If no adb device is found.
        """
        adb = AdbClient(host=DeviceControl.ADB_SERVER_IP, port=DeviceControl.ADB_SERVER_PORT)
        return adb.devices()[0]
    

    def start_app(self) -> None:
        """
        Start the device's app on the phone.

        Raises:
            IndexError: If no adb device is found.
        """
        phone = self.get_phone()
        phone.shell(f"monkey -p {self.android_package} -c android.intent.category.LAUNCHER 1")


    def close_app(self) -> None:
        """
        Close the device's app on the device.

        Raises:
            IndexError: If no adb device is found.
        """
        phone = self.get_phone()
        phone.shell(f"am force-stop {self.android_package}")

    
    def screenshot(self) -> np.ndarray:
        """
        Take a screenshot of the device's screen.
        
        Returns:
            numpy.ndarray: The screenshot as a numpy array.
        Raises:
            IndexError: If no adb device is found.
        """
        screenshot_bytes = self.get_phone().screencap()
        screenshot_array = np.frombuffer(screenshot_bytes, dtype=np.uint8)
        return cv2.imdecode(screenshot_array, cv2.IMREAD_UNCHANGED)
