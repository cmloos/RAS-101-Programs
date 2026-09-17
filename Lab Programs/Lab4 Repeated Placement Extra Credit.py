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

horrizontaldisplacement = 0
originhorizontaldisplacement = 0
while(originhorizontaldisplacement < 40 * 2):
    originverticaldisplacement = 0

    while(originverticaldisplacement < 40 * 2):
        SuckItem(robot1, (270 + originhorizontaldisplacement, -70 - originverticaldisplacement, -43, 0), suck=True)
        horrizontaldisplacement = 0

        while(horrizontaldisplacement < 40*2):
            SuckItem(robot1, (270 + horrizontaldisplacement, 70, -43, 0), suck=False)
            time.sleep(.5)
            SuckItem(robot1, (270 + horrizontaldisplacement, 70, -43, 0), suck=True)
            horrizontaldisplacement = horrizontaldisplacement + 10*2

        SuckItem(robot1, (270 + originhorizontaldisplacement, -70 - originverticaldisplacement, -43, 0), suck=False)
        originverticaldisplacement = originverticaldisplacement + 10*2

    originhorizontaldisplacement = originhorizontaldisplacement + 10*2

robot1.move_to(wait=True, position=HomePosition)