from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
from Robot_Library import *
import time

HomePosition = CustomPosition(x=250, y=0, z=100, r=0)

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')

port1 = available_ports[1].device #COM4

robot1 = Dobot(port1)

robot1.move_to(wait=True, position=HomePosition)

originxdisplacement = 0
while(originxdisplacement < 40):
    originydisplacement = 0
    while(originydisplacement < 40):
        SuckItem(robot1, (270+originxdisplacement, -70-originydisplacement, -43, 0), suck=True)
        SuckItem(robot1, (270, 70, -43, 0), suck=False)

        SuckItem(robot1, (270, 70, -43, 0), suck=True)
        SuckItem(robot1, (270+originxdisplacement, -70-originydisplacement, -43, 0), suck=False)
        originydisplacement = originydisplacement + 20

    originxdisplacement = originxdisplacement + 20