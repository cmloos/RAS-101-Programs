from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
from Robot_Library import *
import time

port = 3
robot, HomePosition = Initialize(port)

robot.move_to(wait=True, position=HomePosition)

SuckItem(robot, (270, 70, -43, 0), suck=True)
SuckItem(robot, (270, -70, -43, 0), suck=False)

SuckItem(robot, (270, 130, -43, 0), suck=True)
SuckItem(robot, (270, -130, -43, 0), suck=False)

SuckItem(robot, (330, 130, -43, 0), suck=True)
SuckItem(robot, (330, -130, -43, 0), suck=False)

SuckItem(robot, (330, 70, -43, 0), suck=True)
SuckItem(robot, (330, -70, -43, 0), suck=False)

robot.move_to(wait=True, position=HomePosition)

time.sleep(3)

SuckItem(robot, (270, -70, -43, 0), suck=True)
SuckItem(robot, (270, 0, -50, 45), suck=False)

SuckItem(robot, (270, -130, -43, 0), suck=True)
SuckItem(robot, (270, 0, -40, -45), suck=False)

SuckItem(robot, (330, -130, -43, 0), suck=True)
SuckItem(robot, (270, 0, -20, 45), suck=False)

SuckItem(robot, (330, -70, -43, 0), suck=True)
SuckItem(robot, (270, 0, -15, -45), suck=False)

robot.move_to(wait=True, position=HomePosition)
time.sleep(1)

robot.move_to(210, 200, -45, 0, wait=False)
robot.move_to(210, -200, -45, 0, wait=False)
time.sleep(1)

robot.move_to(wait=True, position=HomePosition)