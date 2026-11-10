from Robot_Library import *
import time

Conveyor_Speed = 60 #The speed that the conveyor will move in mm/s
IR_Port = 4 #The Port of the IR sensor
X_Jump = 20 #Indicates the distance between the x coordinates for each of the blocks on the tray

robot, Home_Position = Initialize()
InitializeIR(robot, IR_Port)
RunConveyor(robot, Conveyor_Speed)
runs = 0

try:
    while runs < 4:
        SuckItem(robot, (270 + runs*X_Jump, -70, -45, 0), suck=True)
        SuckItem(robot, (200, 140, 10, 0), suck=False)
        robot.move_to(wait=False, position=Home_Position)

        objectSensed = False
        while not objectSensed:
            objectSensed = ReadIR(robot, IR_Port)
            time.sleep(.1)

        StopConveyor(robot)

        while objectSensed:
            objectSensed = ReadIR(robot, IR_Port)
            time.sleep(.1)

        time.sleep(1)

        while not objectSensed:
            objectSensed = ReadIR(robot, IR_Port)
            time.sleep(.1)

        time.sleep(5)
        RunConveyor(robot, Conveyor_Speed)

        runs +=1
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    StopConveyor(robot)
    robot.close()