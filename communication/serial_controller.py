"""

Handles communication between Raspberry Pi
and Arduino.

"""

import serial
import time


class SerialController:

    def __init__(
        self,
        port="/dev/ttyUSB0",
        baudrate=115200
    ):

        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def connect(self):

        try:

            self.serial = serial.Serial(

                self.port,

                self.baudrate,

                timeout=2

            )

            time.sleep(2)

            print("Arduino Connected")

            return True

        except Exception as e:

            print("Connection Error:", e)

            return False

    def disconnect(self):

        if self.serial:

            self.serial.close()

            print("Connection Closed")

    def send_angles(

        self,

        base,

        shoulder,

        elbow,

        wrist,

        gripper

    ):

        if self.serial is None:

            print("Arduino not connected")

            return

        command = (

            f"{base},"

            f"{shoulder},"

            f"{elbow},"

            f"{wrist},"

            f"{gripper}\n"

        )

        self.serial.write(

            command.encode()

        )

        print("Sent:", command)

    def wait_for_ack(self):

        if self.serial is None:

            return

        response = self.serial.readline()

        response = response.decode().strip()

        print("Arduino:", response)

        return response


if __name__ == "__main__":

    controller = SerialController(

        port="COM3",

        baudrate=115200

    )

    if controller.connect():

        controller.send_angles(

            90,

            120,

            60,

            80,

            30

        )

        controller.wait_for_ack()

        controller.disconnect()