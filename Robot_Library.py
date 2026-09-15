from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition

def SuckItem(robot: Dobot, position: tuple, jumpheight: float = 20, suck: bool = True):
    x, y, z, r = position #sets up the coordinates of the desired position

    targetposition = CustomPosition(x, y, z, r) #designates the desired position as a CustomPosition object
    jumpposition = CustomPosition(x, y, z + jumpheight, r) #Designates the position above the desired position as jumpposition, which is where the tool will first move before going to the desired position.

    robot.move_to(jumpposition.x, jumpposition.y, jumpposition.z, jumpposition.r) #Moves the tool to the jump position
    robot.move_to(targetposition.x, targetposition.y, targetposition.z, targetposition.r, wait=True) #Moves the tool to the desired position
    robot.suck(enable=suck) #enables or disables the suction cup for the purposes of grabbing or releasing an object
    robot.move_to(jumpposition.x, jumpposition.y, jumpposition.z, jumpposition.r) #moves the tool back to the jump position