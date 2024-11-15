import URBasic
import time
import math
from Move_Robot import MoveToPositionCommand
from Breathing_Motion_Controller import BreathingMotionController
from Gripper_Control import ControlGripper
from TCP_Subscriber import TCPReceiver
from furhat_functions import Pose
from furhat_functions import *
from Positions import *

# Initialize global variables for the robot and subsystems
robot_ip = "192.168.1.10"
robotModel = URBasic.robotModel.RobotModel()
robot = URBasic.urScriptExt.UrScriptExt(host=robot_ip, robotModel=robotModel)
tcp_receiver = TCPReceiver(robot_ip)

def move_robot(robot, pose):
    """
    Move the robot to the specified pose.
    pose: Tuple of joint angles and two booleans (hovering, gripper_state).
          Format: (j1, j2, j3, j4, j5, j6, hovering, gripper_state)
    """
    # Initialize controllers
    breathing_controller = BreathingMotionController(robot)
    gripper = ControlGripper(robot)

    # Unpack the pose
    if len(pose) != 8:
        raise ValueError("Pose must be a tuple of 6 joint angles and 2 booleans (hovering, gripper_state).")
    joint_angles = pose[:6]
    hovering = pose[6]
    gripper_state = pose[7]

    # Move to the target joint positions
    print(f"Moving to target position: {joint_angles}")
    command = MoveToPositionCommand(robot, joint_angles)
    command.execute()
    while not command.is_reached():
        print("Moving towards target position...")
        time.sleep(0.5)
    print("Target position reached.")

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
    time.sleep(3)  # Simulate holding at the position

def main():
    """
    Main function to execute a sequence of robot movements.
    """
    

    print("Waiting for everything to be ready...")
    time.sleep(2)
    print("Robot initialized.")

    try:
        # Execute the movements
        move_robot(robot, home_go)
        print("Home position reached.")

        time.sleep(1)
        move_robot(robot, pos_pick_top_h_go)
        print("Pick top position reached.")

        time.sleep(3)

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Stopping the robot.")
        robot.stopj(a=2.0)  # Safely stop the robot


if __name__ == "__main__":
    # Reset errors and initialize connection
    print("Resetting robot errors and initializing connection...")
    # robot.reset_error()  # Uncomment if the robot requires error resetting
    main()
