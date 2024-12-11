import serial

def get_arduino_ports():
    """Returns a list of available serial ports."""
    return serial.tools.list_ports.comports()

def connect_to_arduino(port: str):
    """Connect to the Arduino board at the specified port."""
    from pyfirmata import Arduino
    board = Arduino(port)
    return board
