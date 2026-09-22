from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
from Robot_Library import *
import time

HomePosition = CustomPosition(x=250, y=0, z=100, r=0)

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')

port1 = available_ports[2].device #COM4

robot1 = Dobot(port1)

robot1.move_to(wait=True, position=HomePosition)
count = 0
while(True):
    while(count < 3):
        SuckItem(robot1, (270, -70, -43, 0), suck=True)
        SuckItem(robot1, (270, 70, -43, 0), suck=False)
        SuckItem(robot1, (270, 70, -43, 0), suck=True)
        SuckItem(robot1, (270, -70, -43, 0), suck=False)
        count +=1
    count = 0
    while(count < 2):
        SuckItem(robot1, (290, -70, -43, 0), suck=True)
        SuckItem(robot1, (290, 70, -43, 0), suck=False)
        SuckItem(robot1, (290, 70, -43, 0), suck=True)
        SuckItem(robot1, (290, -70, -43, 0), suck=False)
        count += 1
    count = 0