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

def Initialize(port_index=0, position: tuple = (250, 0, 100, 0), home_on_initialize=True):
    x, y, z, r = position #Splits the position tuple into 4 different coordinates
    targetposition = CustomPosition(x, y, z, r) #Assigns the different coordinates from the position tupple into a customposition object

    available_ports = list_ports.comports() #Grabs all available Com ports
    print(available_ports) #Lists all available Com ports

    port = available_ports[port_index].device #Assigns a port based on the port_index from the function's calling parameters
    robot = Dobot(port) #Assigns a Dobot object to the port
    if home_on_initialize: robot.move_to(targetposition, wait=False) #If home_on_initialize was set to True, which it is by default, then this command will home the robotic arm

    return robot, position #returns the dobot object and the customposition object to the caller