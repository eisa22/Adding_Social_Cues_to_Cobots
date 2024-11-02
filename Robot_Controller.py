import time
import math
import threading
import URBasic
from Breathing_Motion_Controller import HoverAndBreatheCommand, BreathingMotionController
from Move_Robot import MoveToPositionCommand, WaitCommand

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

