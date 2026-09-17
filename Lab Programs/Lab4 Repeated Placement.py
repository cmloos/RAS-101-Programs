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

SuckItem(robot1, (270, -90, -43, 0), suck=True)

horrizontaldisplacement = 0
while(horrizontaldisplacement < 40*2):
    verticaldisplacement = 0
    while(verticaldisplacement < 40*2):
        SuckItem(robot1, (270+horrizontaldisplacement, 70+verticaldisplacement, -43, 0), suck=False)
        time.sleep(1)
        SuckItem(robot1, (270+horrizontaldisplacement, 70+verticaldisplacement, -43, 0), suck=True)
        verticaldisplacement = verticaldisplacement + 10*2
    horrizontaldisplacement = horrizontaldisplacement + 10*2

SuckItem(robot1, (270, -90, -43, 0), suck=False)
robot1.move_to(wait=True, position=HomePosition)    