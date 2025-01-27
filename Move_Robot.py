import URBasic
import time
import math

class RobotCommand:
    def __init__(self, robot):
        self.robot = robot

    def execute(self):
        pass

class MoveToPositionCommand(RobotCommand):
    def __init__(self, robot, target_position):
        super().__init__(robot)
        self.target_position = target_position

    def execute(self):
        print("Sending move command to target position:", self.target_position)
        self.robot.movej(q=self.target_position, a=1.0, v=2.0)
        time.sleep(1)  # Allow some time for the command to initiate

    def is_reached(self):
        actual_position = self.robot.get_actual_joint_positions()
        print("Checking position: Current =", actual_position, "Target =", self.target_position)
        return all(math.isclose(t, a, abs_tol=0.01) for t, a in zip(self.target_position, actual_position))

class HoverAndBreatheCommand(RobotCommand):
    def __init__(self, robot, breathing_controller):
        super().__init__(robot)
        self.breathing_controller = breathing_controller
        self.hover_position = (math.radians(0), math.radians(-90), math.radians(-90), math.radians(-90), math.radians(90), math.radians(0))

    def execute(self):
        print("Returning to hover position and starting breathing motion")
        self.robot.movej(q=self.hover_position, a=1.0, v=2.0)
        time.sleep(1)  # Allow some time for the command to initiate
        self.breathing_controller.start_breathing()

    def is_reached(self):
        actual_position = self.robot.get_actual_joint_positions()
        print("Checking hover position: Current =", actual_position, "Hover =", self.hover_position)
        return all(math.isclose(h, a, abs_tol=0.01) for h, a in zip(self.hover_position, actual_position))
