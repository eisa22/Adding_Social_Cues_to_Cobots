import URBasic
import time
import math
from Move_Robot import MoveToPositionCommand, HoverAndBreatheCommand
from Breathing_Motion_Controller import BreathingMotionController

def main():
    # Initialize robot
    robotModel = URBasic.robotModel.RobotModel()
    robot = URBasic.urScriptExt.UrScriptExt(host='192.168.31.224', robotModel=robotModel)
    robot.reset_error()
    print("Robot initialized")

    # Define positions
    initial_position = (
        math.radians(0), math.radians(-90), math.radians(0), 
        math.radians(-90), math.radians(0), math.radians(0)
    )
    hover_position = (
        math.radians(0), math.radians(-120), math.radians(-50), 
        math.radians(-115), math.radians(90), math.radians(0)
    )
    target_position = (
        math.radians(45), math.radians(-120), math.radians(-52), 
        math.radians(-114), math.radians(90), math.radians(0)
    )

    # Initialize breathing controller
    breathing_controller = BreathingMotionController(robot)
    
    # Move to initial position
    print("Moving to initial position...")
    robot.movej(q=initial_position, a=0.2, v=0.2)
    time.sleep(1)  # Allow some time for the command to initiate

    # Move to hover position and start breathing
    print("Moving to hover position...")
    hover_command = MoveToPositionCommand(robot, hover_position)
    hover_command.execute()
    while not hover_command.is_reached():
        print("Moving towards hover position...")
        time.sleep(0.5)
    print("Hover position reached. Starting breathing motion.")
    breathing_controller.start_breathing()

    # Wait for 3 seconds at the hover position
    time.sleep(3)

    # Move to target position and stop breathing
    print("Moving to target position...")
    breathing_controller.stop_breathing()
    target_command = MoveToPositionCommand(robot, target_position)
    target_command.execute()
    while not target_command.is_reached():
        print("Moving towards target position...")
        time.sleep(0.5)
    print("Target position reached.")

    # Wait for 3 seconds at the target position
    time.sleep(3)

    # Return to hover position and resume breathing
    print("Returning to hover position...")
    hover_command.execute()
    while not hover_command.is_reached():
        print("Returning to hover position...")
        time.sleep(0.5)
    print("Hover position reached. Resuming breathing motion.")
    breathing_controller.start_breathing()

if __name__ == "__main__":
    main()
