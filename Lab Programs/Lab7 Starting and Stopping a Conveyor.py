from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
import inspect
from Robot_Library import *
import time

port = 3
robot1, HomePosition = Initialize(port) #COM7

import inspect
print(inspect.getsource(robot1._set_stepper_motor))