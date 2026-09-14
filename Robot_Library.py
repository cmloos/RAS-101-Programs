from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition

def SuckItem(robot: Dobot, position: tuple, jumpheight: float = 20, suck: bool = True):
    x, y, z, r = position #sets up the coordinates of the desired position

    targetposition = CustomPosition(x, y, z, r) #designates the desired position as a CustomPosition object
    jumpposition = CustomPosition(x, y, z + jumpheight, r) #Designates the position above the desired position as jumpposition, which is where the tool will first move before going to the desired position.

    robot.moveto(jumpposition) #Moves the tool to the jump position
    robot.moveto(position, wait=True) #Moves the tool to the desired position
    robot.suck(enable=suck) #enables or disables the suction cup for the purposes of grabbing or releasing an object
    robot.moveto(jumpposition) #moves the tool back to the jump position