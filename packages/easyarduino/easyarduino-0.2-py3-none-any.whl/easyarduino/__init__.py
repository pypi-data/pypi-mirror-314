# Import the main components of the package for easier access
from .arduino_controller import ArduinoController
from .utils import get_arduino_ports, connect_to_arduino

# __all__ to specify what gets imported when using 'from easyarduino import *'
__all__ = ['ArduinoController', 'get_arduino_ports', 'connect_to_arduino']
