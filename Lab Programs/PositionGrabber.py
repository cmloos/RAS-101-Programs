from tokenize import endpats

from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
import time

HomePosition = CustomPosition(x=250, y=0, z=100, r=0)

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')

port1 = available_ports[31].device #ACM0

robot1 = Dobot(port1)

while True:
    print(robot1.get_pose())
    time.sleep(1)
