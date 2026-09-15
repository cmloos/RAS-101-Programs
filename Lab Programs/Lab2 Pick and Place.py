from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
from Robot_Library import *
import time

HomePosition = CustomPosition(x=250, y=0, z=100, r=0)

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')

port1 = available_ports[31].device #ACM0

robot1 = Dobot(port1)

robot1.move_to(wait=True, position=HomePosition)

#Pick up the block and place it on the other grid
SuckItem(robot1, (270, 70, -45, 0), suck=True)
SuckItem(robot1, (270, -70, -45, 0), suck=False)

SuckItem(robot1, (270, 90, -45, 0), suck=True)
SuckItem(robot1, (270, -70, -35, 0), suck=False)

robot1.move_to(wait=True, position=HomePosition)

#Pick up the block (which was placed earlier) and place it back on the first grid
SuckItem(robot1, (270, -70, -45, 0), suck=True)
SuckItem(robot1, (270, 90, -35, 0), suck=False)

SuckItem(robot1, (270, -70, -45, 0), suck=True)
SuckItem(robot1, (270, 70, -45, 0), suck=False)

robot1.move_to(wait=True, position=HomePosition)