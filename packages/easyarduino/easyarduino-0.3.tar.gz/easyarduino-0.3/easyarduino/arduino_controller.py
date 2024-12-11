from pyfirmata import Arduino, util
from pyfirmata import SERVO
import time

class ArduinoController:
    def __init__(self, port: str):
        self.board = Arduino(port)
        self.iterator = util.Iterator(self.board)
        self.iterator.start()

    # --- Digital Pin Control ---
    def digital_write(self, pin: int, state: bool):
        """Set a digital pin to HIGH (True) or LOW (False)"""
        self.board.digital[pin].write(state)

    def digital_read(self, pin: int) -> bool:
        """Read the state of a digital pin (True or False)"""
        return self.board.digital[pin].read()

    # --- Analog Pin Control ---
    def analog_read(self, pin: int) -> int:
        """Read the value of an analog pin (0 to 1023)"""
        return self.board.analog[pin].read() * 1023 if self.board.analog[pin].read() is not None else 0

    def analog_write(self, pin: int, value: int):
        """Write a value (0 to 255) to an analog pin (PWM output)"""
        self.board.analog[pin].write(value / 255.0)  # PyFirmata uses values from 0.0 to 1.0

    # --- Servo Control ---
    def servo_write(self, pin: int, angle: int):
        """Write an angle (0-180) to a servo connected to a PWM pin"""
        self.board.digital[pin].mode = SERVO
        self.board.digital[pin].write(angle)

    def servo_read(self, pin: int) -> int:
        """Read the current angle of a servo (if supported)"""
        # Currently, PyFirmata doesn't provide direct servo reading,
        # so you may need a feedback sensor to measure the angle manually.
        return self.board.digital[pin].read()

    # --- Pin Mode Control ---
    def set_pin_mode(self, pin: int, mode: str):
        """Set the pin mode (INPUT, OUTPUT, PWM, or SERVO)"""
        if mode == "INPUT":
            self.board.digital[pin].mode = self.board.INPUT
        elif mode == "OUTPUT":
            self.board.digital[pin].mode = self.board.OUTPUT
        elif mode == "PWM":
            self.board.digital[pin].mode = self.board.PWM
        elif mode == "SERVO":
            self.board.digital[pin].mode = self.board.SERVO
        else:
            raise ValueError("Invalid mode. Choose from 'INPUT', 'OUTPUT', 'PWM', or 'SERVO'.")

    # --- I2C Communication ---
    def i2c_write(self, address: int, data: list):
        """Write data to an I2C device"""
        self.board.i2c_write(address, data)

    def i2c_read(self, address: int, length: int) -> list:
        """Read data from an I2C device"""
        return self.board.i2c_read(address, length)

    # --- SPI Communication ---
    def spi_transfer(self, data: bytes) -> bytes:
        """Transfer data via SPI"""
        return self.board.spi_transfer(data)

    # --- Analog Input with smoothing ---
    def analog_read_smooth(self, pin: int, num_samples: int = 10) -> int:
        """Read and smooth analog input by averaging multiple readings"""
        readings = [self.analog_read(pin) for _ in range(num_samples)]
        return sum(readings) // num_samples

    # --- Getting Firmata version ---
    def get_firmata_version(self):
        """Get the version of the Firmata firmware running on the Arduino"""
        return self.board.get_firmata_version()

    # --- Get board information ---
    def get_board_info(self):
        """Get board information (name, port, capabilities)"""
        return self.board.name, self.board.port, self.board.capabilities

    # --- Shutdown ---
    def close(self):
        """Disconnect from the board"""
        self.board.exit()
