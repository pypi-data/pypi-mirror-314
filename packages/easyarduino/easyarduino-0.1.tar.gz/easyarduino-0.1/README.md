```markdown
# easyarduino - Python Library for Arduino Control

`easyarduino` is a Python library designed to simplify the process of controlling an Arduino board using the `pyfirmata` library. It provides an easy-to-use interface for managing digital and analog pins, controlling servos, handling I2C/SPI communication, and more.

## Installation

To use this library, you need Python and `easyarduino` installed. You can install the required dependencies with the following command:
```
```bash
pip install easyarduino
```

## Features

- **Digital Pin Control**: Read and write to digital pins (HIGH or LOW).
- **Analog Pin Control**: Read analog values (0 to 1023) and write PWM values (0 to 255).
- **Servo Control**: Control servos by setting their angles (0 to 180 degrees).
- **Pin Mode Control**: Set pin modes to `INPUT`, `OUTPUT`, `PWM`, or `SERVO`.
- **I2C Communication**: Read and write data to I2C devices.
- **SPI Communication**: Transfer data over SPI.
- **Analog Input Smoothing**: Read and smooth analog input by averaging multiple readings.
- **Firmata Version**: Retrieve the version of the Firmata firmware running on the Arduino.
- **Board Info**: Retrieve information about the connected Arduino board.

## Usage

### 1. Importing the Library

First, import the necessary classes and functions from the library:

```python
from easyarduino import ArduinoController, get_arduino_ports, connect_to_arduin
```

### 2. Initializing the Controller

To initialize the controller, pass the serial port of your Arduino board. You can find the available ports using the `get_arduino_ports` function.

#### Example: Initialize Arduino Controller

```python
# Initialize the controller with the appropriate serial port
controller = ArduinoController(port='/dev/ttyACM0')  # Replace with your board's port
```

### 3. Digital Pin Control

#### `digital_write(pin, state)`
Write a HIGH or LOW value to a digital pin.

```python
# Write HIGH to pin 13
controller.digital_write(pin=13, state=True)

# Write LOW to pin 13
controller.digital_write(pin=13, state=False)
```

#### `digital_read(pin)`
Read the state of a digital pin.

```python
# Read the state of pin 13
state = controller.digital_read(pin=13)
print(state)  # Will print True or False
```

### 4. Analog Pin Control

#### `analog_read(pin)`
Read the analog value from a pin (range 0-1023).

```python
# Read analog value from pin A0
analog_value = controller.analog_read(pin=0)
print(analog_value)  # Will print a value between 0 and 1023
```

#### `analog_write(pin, value)`
Write a PWM value (0-255) to an analog pin.

```python
# Write PWM value to pin 9
controller.analog_write(pin=9, value=128)  # Half brightness
```

### 5. Servo Control

#### `servo_write(pin, angle)`
Write an angle (0 to 180 degrees) to a servo motor connected to a PWM pin.

```python
# Move the servo connected to pin 9 to 90 degrees
controller.servo_write(pin=9, angle=90)
```

#### `servo_read(pin)`
Read the current angle of the servo (if supported by the hardware). This function may return None if direct servo feedback is not available.

```python
# Read the current angle of the servo
angle = controller.servo_read(pin=9)
print(angle)  # Returns the current angle of the servo
```

### 6. Pin Mode Control

#### `set_pin_mode(pin, mode)`
Set the mode of a pin. The available modes are `INPUT`, `OUTPUT`, `PWM`, and `SERVO`.

```python
# Set pin 13 as OUTPUT
controller.set_pin_mode(pin=13, mode="OUTPUT")

# Set pin 9 as PWM for controlling a motor
controller.set_pin_mode(pin=9, mode="PWM")
```

### 7. I2C Communication

#### `i2c_write(address, data)`
Write data to an I2C device.

```python
# Write a list of data to an I2C device at address 0x40
controller.i2c_write(address=0x40, data=[0x01, 0x02, 0x03])
```

#### `i2c_read(address, length)`
Read data from an I2C device.

```python
# Read 4 bytes of data from I2C device at address 0x40
data = controller.i2c_read(address=0x40, length=4)
print(data)
```

### 8. SPI Communication

#### `spi_transfer(data)`
Transfer data via SPI.

```python
# Send data through SPI
response = controller.spi_transfer(data=b'hello')
print(response)  # Will print the response from the SPI transfer
```

### 9. Analog Input Smoothing

#### `analog_read_smooth(pin, num_samples)`
Read and average multiple analog readings to smooth the input. This is useful for reducing noise from analog sensors.

```python
# Smooth the analog input on pin A0 by taking 10 readings
smooth_value = controller.analog_read_smooth(pin=0, num_samples=10)
print(smooth_value)  # The smoothed average value
```

### 10. Get Firmata Version

#### `get_firmata_version()`
Get the version of the Firmata firmware running on the Arduino.

```python
# Get the Firmata version
firmata_version = controller.get_firmata_version()
print(firmata_version)
```

### 11. Get Board Information

#### `get_board_info()`
Retrieve information about the connected Arduino board, including its name, port, and capabilities.

```python
# Get information about the Arduino board
board_info = controller.get_board_info()
print(board_info)  # Will print a tuple with name, port, and capabilities
```

### 12. Shutdown

#### `close()`
Close the connection to the Arduino board and release resources.

```python
# Disconnect from the Arduino board
controller.close()
```

## Example: Full Usage

```python
from easyarduino import ArduinoController

# Initialize the Arduino Controller
controller = ArduinoController(port='/dev/ttyACM0')

# Set pin modes
controller.set_pin_mode(13, "OUTPUT")

# Write to a digital pin
controller.digital_write(13, True)

# Read from a digital pin
pin_state = controller.digital_read(13)
print(f"Pin 13 state: {pin_state}")

# Control a servo
controller.servo_write(9, 90)

# Get the board info
board_info = controller.get_board_info()
print(f"Board Info: {board_info}")

# Disconnect from the board
controller.close()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
