from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
from Robot_Library import *
import time

robot1, HomePosition = Initialize(2)

pallet_x = 0
while(pallet_x < 3): #Loops the program for every row
    pallet_y = 0
    while(pallet_y < 3): #Loops the program for every column
        SuckItem(robot1, (270 + pallet_x * 20, -70 - pallet_y * 20, -43, 0), suck=True)
        SuckItem(robot1, (270, 70, -43, 0), suck=False)

        robot1.move_to(position=HomePosition)
        input("press enter to confirm placement")
        pallet_y += 1

    pallet_x += 1
