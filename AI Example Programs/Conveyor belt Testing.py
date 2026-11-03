#Generated Via Claude

import struct
from serial.tools import list_ports
from pydobotplus import Dobot
import pydobotplus.dobotplus as dp

PULSES_PER_MM = 500 / 3.141592653589793  # inferred from one data point: 50 mm/s -> 7957 pulses/s

def FindDobotPort():
    for p in list_ports.comports():
        if "USB Serial" in p.description:
            return p.device
    raise RuntimeError("No 'USB Serial Device' port found. Is the Dobot plugged in?")

def RunConveyor(robot: Dobot, speed_mm_per_sec: float, interface: int = 0):
    """Runs the belt. interface 0 = STP1, 1 = STP2. Negative speed should reverse it (untested)."""
    msg = dp.Message()
    msg.id = 0x87
    msg.ctrl = 0x11  # the control byte DobotLab uses; 0x01 / 0x03 never moved the belt
    msg.params = bytearray([interface, 0x01])
    msg.params.extend(struct.pack('<i', int(speed_mm_per_sec * PULSES_PER_MM)))
    return robot._send_command(msg)

def StopConveyor(robot: Dobot, interface: int = 0):
    return RunConveyor(robot, 0, interface)  # DobotLab also stops with enable=1, speed=0

import time
from Robot_Library import *

robot1 = Dobot(FindDobotPort())
try:
    RunConveyor(robot1, -100)
    time.sleep(3)
finally:
    StopConveyor(robot1)  # runs even if something crashes, so the belt doesn't keep going
    robot1.close()