import URBasic
import time
import math
from Move_Robot import MoveToPositionCommand
from Breathing_Motion_Controller import BreathingMotionController
from Gripper_Control import ControlGripper

# Initialize robot, breathing controller, and gripper controller globally
#robotModel = URBasic.robotModel.RobotModel()
#robot = URBasic.urScriptExt.UrScriptExt(host='192.168.0.13', robotModel=robotModel)
#breathing_controller = BreathingMotionController(robot)
#gripper = ControlGripper(robot)

def move_robot(robot, pose):
    """
    Move the robot to the specified pose.
    pose: Tuple of joint angles and two booleans (hovering, gripper_state).
          Format: (j1, j2, j3, j4, j5, j6, hovering, gripper_state)
    """

    breathing_controller = BreathingMotionController(robot)
    gripper = ControlGripper(robot)
    # Unpack the pose
    joint_angles = pose[:6]
    hovering = pose[6]
    gripper_state = pose[7]

    # Move to the target joint positions
    print("Moving to target position...")
    command = MoveToPositionCommand(robot, joint_angles)
    command.execute()
    #while not command.is_reached():
        #print("Moving towards target position...")
        #time.sleep(0.5)
    #print("Target position reached.")

    # Handle the gripper state
    if gripper_state:
        print("Closing gripper.")
        gripper.close_gripper()
    else:
        print("Opening gripper.")
        gripper.open_gripper()

    # Handle hovering and breathing state
    if hovering:
        print("Starting hover breathing motion.")
        breathing_controller.start_breathing()
    else:
        breathing_controller.stop_breathing()
    time.sleep(3)  # Wait to simulate holding at the position

def main():
    # Define target positions
    initial_position = (
        math.radians(0), math.radians(-90), math.radians(0), 
        math.radians(-90), math.radians(0), math.radians(0), False, False
    )
    hover_position = (
        math.radians(0), math.radians(-120), math.radians(-50), 
        math.radians(-115), math.radians(90), math.radians(0), True, False
    )
    target_position = (
        math.radians(45), math.radians(-120), math.radians(-52), 
        math.radians(-114), math.radians(90), math.radians(0), False, True
    )

    # Execute the movements
    move_robot(initial_position)
    time.sleep(1)
    move_robot(hover_position)
    time.sleep(3)
    move_robot(target_position)
    time.sleep(3)
    move_robot(hover_position)  # Return to hover and start breathing again

if __name__ == "__main__":
    # Reset errors and initialize connection
    robot.reset_error()
    print("Robot initialized")
    main()
