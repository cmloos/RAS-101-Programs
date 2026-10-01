from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
from Robot_Library import *
import time

port = 3
robot1, HomePosition = Initialize(port) #COM7

robot1.conveyor_belt(speed=0.5, direction=1, interface=1)

time.sleep(1)