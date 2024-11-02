import time
import math
import threading
import URBasic
# Command Interface
class RobotCommand:
    def execute(self):
        raise NotImplementedError("Each command must implement an execute method.")

# Command: Move to Position
class MoveToPositionCommand(RobotCommand):
    def __init__(self, robot, position, acceleration=0.2, velocity=0.2):
        self.robot = robot
        self.position = position
        self.acceleration = acceleration
        self.velocity = velocity

    def execute(self):
        print(f"Moving to position: {self.position}")
        self.robot.movej(q=self.position, a=self.acceleration, v=self.velocity)

# Command: Wait
class WaitCommand(RobotCommand):
    def __init__(self, duration):
        self.duration = duration

    def execute(self):
        print(f"Waiting for {self.duration} seconds")
        time.sleep(self.duration)