from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
import pydobotplus.dobotplus as dp
import struct
import math

def SuckItem(robot: Dobot, position: tuple, jumpheight: float = 20, suck: bool = True):
    x, y, z, r = position #sets up the coordinates of the desired position

    targetposition = CustomPosition(x, y, z, r) #designates the desired position as a CustomPosition object
    jumpposition = CustomPosition(x, y, z + jumpheight, r) #Designates the position above the desired position as jumpposition, which is where the tool will first move before going to the desired position.

    robot.move_to(jumpposition.x, jumpposition.y, jumpposition.z, jumpposition.r) #Moves the tool to the jump position
    robot.move_to(targetposition.x, targetposition.y, targetposition.z, targetposition.r, wait=True) #Moves the tool to the desired position
    robot.suck(enable=suck) #enables or disables the suction cup for the purposes of grabbing or releasing an object
    robot.move_to(jumpposition.x, jumpposition.y, jumpposition.z, jumpposition.r) #moves the tool back to the jump position

def Initialize(port_index=None, position: tuple = (250, 0, 100, 0), home_on_initialize=True):
    x, y, z, r = position #Splits the position tuple into 4 different coordinates
    targetposition = CustomPosition(x, y, z, r) #Assigns the different coordinates from the position tupple into a customposition object

    if port_index is not None: #If a port was specified, use it for initialization
        available_ports = list_ports.comports() #Grabs all available Com ports
        print(available_ports) #Lists all available Com ports

        port = available_ports[port_index].device #Assigns a port based on the port_index from the function's calling parameters
        robot = Dobot(port) #Assigns a Dobot object to the port
    else: #If no port was specified, use the _FindDobotPort function to find the port for initialization
        robot = Dobot(_FindDobotPort())

    if home_on_initialize: robot.move_to(wait=False, position=targetposition) #If home_on_initialize was set to True, which it is by default, then this command will home the robotic arm

    return robot, targetposition #returns the dobot object and the customposition object to the caller

def _FindDobotPort():
    """This function finds the com port related to the dobot. It will not work if there are multiple dobots connected to the computer."""
    for ports in list_ports.comports(): #Makes a list from all of the listed ports from the "list_ports" command
        if "USB Serial" in ports.description: #If one of the descriptions in the list matches "USB Serial", then it will be passed back as the target port
            return ports.device #Returns the port found in this function

    raise RuntimeError("No Dobot Found. Is one plugged in?") #If there isn't a com port that matches the proper description, then this line will throw an error asking the user if the dobot is plugged in.


PULSES_PER_MM = 500 / math.pi  #This is a universal variable. It is inferred from one data point: 50 mm/s -> 7957 pulses/s. It is used to tell the stepper motor how many pulses it needs to do for the RunConveyor function

def RunConveyor(robot: Dobot, speed_mm_per_second: float, interface: int = 0):
    """This function operates the conveyor belt. It defaults to the port on the magicbox labled STP1 (interface = 0).
    If a different interface is specified, it will use that (interface = 1). The speed indicated when calling the
    function is required for this function to work."""

    msg = dp.Message() #Creates a message based on the object provided by the pydobot library
    msg.id=0x87 #Sets the id of the message to 0x87. This tells the magicbox that we want the stepper motor to be used
    msg.ctrl = 0x11 #This is the "control byte" that the magicbox will receive. It is different to what is found in pydobotplus because the one included there didn't work (likely because it is trying to talk to the arm and not the magicbox)
    msg.params = bytearray([interface, 0x01]) #This line is the basis of the message that the magicbox will receive. "interface" tells the magicbox which stepper port it will use, and "0x01" is the enable command for the stepper.
    msg.params.extend(struct.pack('<i', int(speed_mm_per_second * PULSES_PER_MM))) #Adds additional bits for the stepper motor to interperet
    return robot._send_command(msg)

def StopConveyor(robot: Dobot, interface: int = 0): #This function acts as a "stop" command for the stepper motor. It does not "release" control of the stepper.
    return RunConveyor(robot, 0, interface)

# def DisableConveyor(robot: Dobot, interface: int = 0):
#     msg = dp.Message()  # Creates a message based on the object provided by the pydobot library
#     msg.id = 0x87  # Sets the id of the message to 0x87. This tells the magicbox that we want the stepper motor to be used
#     msg.ctrl = 0x11  # This is the "control byte" that the magicbox will receive. It is different to what is found in pydobotplus because the one included there didn't work (likely because it is trying to talk to the arm and not the magicbox)
#     msg.params = bytearray([interface,0x00])  # This line is the basis of the message that the magicbox will receive. "interface" tells the magicbox which stepper port it will use, and "0x01" is the enable command for the stepper.
#     msg.params.extend(struct.pack('<i',int(speed_mm_per_second * PULSES_PER_MM)))  # Adds additional bits for the stepper motor to interperet
#     return robot._send_command(msg)

def InitializeIR(robot: Dobot, port_index: int = 0, enable: bool = True):
    """This function initializes the IR sensor and allows it to sense objects in front of it. The port_index defaults to
    the first port (port1), however it can be changed by passing a different number to port_index. Additionally, this
    function may be used to disable the sensor via sending a different value to the 'enable' parameter."""
    message = dp.Message() #Creates a Message object based on the dobotplus library
    message.id = 0x8A #Sets the ID of the message to be able to tell the magicbox that we want the ir sensor to be enabled/disabled
    message.ctrl = 0x11 #sets the control section of the message to tell the magicbox that we wish to write variables to the IR sensor
    message.params = bytearray([int(enable), port_index, 0x01]) #This adds three words onto the message, telling the ir sensor to enable/disable, which port its on, and the version of the sensor.
    return robot._send_command(message) #Sends the command to the magicbox

def ReadIR(robot: Dobot, port_index: int = 0) -> bool:
    """This function allows the code to get the state of the sensor. a false reading indicates that the beam is clear,
    while a true reading indicates that an object is being detected"""
    message = dp.Message() #Creates a message object
    message.id = 0x8A #Tells the magicbox that we are reffering to the ir sensor
    message.ctrl = 0x10 #Tells the magicbox that we want to read the state of the IR sensor
    message.params = bytearray([port_index]) #Tells the magicbox what port we are trying to read
    reply = robot._send_command(message) #Creates an object based on what was returned by the magicbox
    return bool(reply.params[0]) #Changes the parameter object from the message from the magicbox to a boolean before returning it to the caller