#Generated Via Claude

import time
from Robot_Library import *
import pydobotplus.dobotplus as dp
import struct

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

IR_PORT_INDEX = 4  # the port byte DobotLab sent for the sensor on box port 5

def EnableIR(robot: Dobot, port_index: int = IR_PORT_INDEX, enable: bool = True):
    msg = dp.Message()
    msg.id = 0x8A
    msg.ctrl = 0x11
    msg.params = bytearray([int(enable), port_index, 0x01])  # enable, port, version(?)
    return robot._send_command(msg)

def ReadIR(robot: Dobot, port_index: int = IR_PORT_INDEX) -> bool:
    """True = object detected, False = beam clear."""
    msg = dp.Message()
    msg.id = 0x8A
    msg.ctrl = 0x10
    msg.params = bytearray([port_index])
    reply = robot._send_command(msg)
    return bool(reply.params[0])

BELT_SPEED = 50      # mm/s
RUN_SECONDS = 60     # safety limit so the program always ends

robot1 = Dobot(FindDobotPort())
try:
    EnableIR(robot1)
    time.sleep(0.3)

    RunConveyor(robot1, BELT_SPEED)
    running = True
    start = time.time()

    while time.time() - start < RUN_SECONDS:
        detected = ReadIR(robot1)
        if detected and running:
            StopConveyor(robot1)
            running = False
            print("Object detected, belt stopped")
        elif not detected and not running:
            RunConveyor(robot1, BELT_SPEED)
            running = True
            print("Beam clear, belt running")
        time.sleep(0.02)
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    StopConveyor(robot1)
    robot1.close()