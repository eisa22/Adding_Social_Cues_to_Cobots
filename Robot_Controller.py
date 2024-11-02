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

# Command: Hover and Start Breathing
class HoverAndBreatheCommand(RobotCommand):
    def __init__(self, robot, breathing_controller):
        self.robot = robot
        self.breathing_controller = breathing_controller

    def execute(self):
        print("Returning to hover position and starting breathing motion")
        hover_position = (math.radians(0), math.radians(-90), math.radians(-90), math.radians(-90), math.radians(90), math.radians(0))
        self.robot.movej(q=hover_position, a=0.1, v=0.1)
        self.breathing_controller.start_breathing()

# Breathing Motion Controller
class BreathingMotionController:
    def __init__(self, robot):
        self.robot = robot
        self.breathing_period = 5.0
        self.breathing_amplitude = 0.02
        self.breathing = False
        self.base_joint_positions = None

    def start_breathing(self):
        if not self.breathing:
            print("Starting breathing motion")
            self.breathing = True
            self.base_joint_positions = self.robot.get_actual_joint_positions()
            threading.Thread(target=self.perform_breathing_motion, daemon=True).start()

    def stop_breathing(self):
        print("Stopping breathing motion")
        self.breathing = False

    def perform_breathing_motion(self):
        while self.breathing:
            current_time = time.time()
            offset = self.breathing_amplitude * math.sin(2 * math.pi * current_time / self.breathing_period)
            breathing_pose = [base + offset for base in self.base_joint_positions]
            self.robot.movej(q=breathing_pose, a=0.05, v=0.05)
            time.sleep(0.1)

# Robot Controller with Command Queue
class RobotController:
    def __init__(self, robot, breathing_controller):
        self.robot = robot
        self.breathing_controller = breathing_controller
        self.command_queue = []
        self.current_command = None
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def add_command(self, command):
        self.command_queue.append(command)

    def run(self):
        while self.running:
            if self.command_queue:
                self.breathing_controller.stop_breathing()  # Stop breathing before executing a new command
                self.current_command = self.command_queue.pop(0)
                self.current_command.execute()
            else:
                if not self.breathing_controller.breathing:
                    # Start breathing if there are no commands and it's not already breathing
                    self.breathing_controller.start_breathing()
            time.sleep(0.1)  # Avoid tight loop

    def stop(self):
        self.running = False

# Main Program
def main():
    # Initialize Robot Model and Controller
    robotModel = URBasic.robotModel.RobotModel()
    robot = URBasic.urScriptExt.UrScriptExt(host='192.168.31.224', robotModel=robotModel)
    
    breathing_controller = BreathingMotionController(robot)
    robot_controller = RobotController(robot, breathing_controller)

    # Example Usage
    target_position = (math.radians(125.30), math.radians(-136), math.radians(-95), math.radians(-38), math.radians(90), math.radians(315))
    robot_controller.add_command(MoveToPositionCommand(robot, target_position))
    robot_controller.add_command(WaitCommand(3))
    robot_controller.add_command(HoverAndBreatheCommand(robot, breathing_controller))

if __name__ == "__main__":
    main()

