import URBasic
import time
from Move_Robot import MoveToPositionCommand
from Breathing_Motion_Controller import BreathingMotionController
from Dashboard import Dashboard
from Gripper_Control import ControlGripper
from TCP_Subscriber import TCPReceiver
from furhat_functions import Pose
from furhat_functions import *
from Positions import *
from furhat_remote_api import FurhatRemoteAPI
from furhat_functions import * 
import robotiq_gripper 
import threading
import logging  # Add logging module

# Robot data
USE_UR_ROBOT = False  # Set to True if using UR robot, False if using URSIM
robot_ip = "192.168.0.8"
robotModel = URBasic.robotModel.RobotModel()
robot = URBasic.urScriptExt.UrScriptExt(host=robot_ip, robotModel=robotModel)
tcp_receiver = TCPReceiver(robot_ip)
pose = Pose()
gripper = robotiq_gripper.RobotiqGripper()
dashboard = Dashboard()
robot_is_moving = False

# Definition of global variables for Furhat
is_parallel_looking = False
endeffector = Pose()
offset = Pose()
holder, human, body_rack, top_rack, finished_bin = Pose(), Pose(), Pose(), Pose(), Pose()
tcp_x, tcp_y, tcp_z = 0, 0, 0
is_parallel_cartesian = False
human_name = ""

# colors and parameters of parts:
parts = [["red", "white", "blue", "yellow"], ["blue", "yellow", "red", "red"]]

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Definition of move robot function
def move_robot(robot, pose):
    """
    Move the robot to the specified pose.
    pose: Tuple of joint angles and two booleans (hovering, gripper_state).
          Format: (j1, j2, j3, j4, j5, j6, hovering, gripper_state)
    """
    try:
        # Initialize controllers
        breathing_controller = BreathingMotionController(robot)

        # Unpack the pose
        if len(pose) != 8:
            raise ValueError("Pose must be a tuple of 6 joint angles and 2 booleans (hovering, gripper_state).")
        joint_angles = pose[:6]
        hovering = pose[6]
        gripper_state = pose[7]

        # Move to the target joint positions
        logging.info(f"Moving to target position: {joint_angles}")
        command = MoveToPositionCommand(robot, joint_angles)
        command.execute()

        while not command.is_reached():
            logging.info("Moving towards target position...")
            time.sleep(0.5)
        logging.info("Target position reached.")

        # Handle the gripper state
        if USE_UR_ROBOT:
            if gripper_state:
                try:
                    logging.info("Closing gripper.")
                    gripper.move_and_wait_for_pos(255, 255, 255)
                except RuntimeError as e:
                    logging.error(f"Error during gripper operation: {e}")
            else:
                logging.info("Opening gripper.")
                gripper.move_and_wait_for_pos(0, 255, 255)

        # Handle hovering and breathing state
        if hovering:
            logging.info("Starting hover breathing motion.")
            breathing_controller.start_breathing()
        else:
            breathing_controller.stop_breathing()

        time.sleep(1)  # Simulate holding at the position

    except Exception as e:
        logging.error(f"An error occurred during robot movement: {e}")

def execute_movement(robot, pose):
    """
    Executes a robot movement safely with error handling.
    :param robot: The robot instance.
    :param pose: The target pose (tuple of joint angles and states).
    """
    try:
        move_robot(robot, pose)
        logging.info("Target position reached.")
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Stopping the robot.")
        robot.stopj(a=2.0)  # Safely stop the robot

def execute_movement_thread(robot, positions):
    global robot_is_moving
    robot_is_moving = True
    for pos in positions:
        execute_movement(robot, pos)
        time.sleep(0.1)
    robot_is_moving = False

def start_robot_movement(robot, positions):
    movement_thread = threading.Thread(target=execute_movement_thread, args=(robot, positions))
    movement_thread.start()

# Main Program to execute

def main():
    """
    Main function to execute a sequence of robot movements.
    """
    try:
        # Initialize controllers
        logging.info("____Init Robot____")
        tcp_receiver.run_parallel_get_cartesian_coordinates(pose, True)

        if USE_UR_ROBOT:
            gripper.connect(robot_ip, 63352)
            logging.info("Gripper connected")
            gripper.activate()
            logging.info("Gripper activated")
        
        execute_movement(robot, home_go)

        # Start the dashboard
        dashboard.start_dashboard()
        
        logging.info("____Finished Init Robot____")

        welcome_message = True
        while robot_is_moving:
                time.sleep(0.1)
        input("--- Press enter to start! ---")
        time.sleep(1.0)

        # Welcome message
        if welcome_message:
            dashboard.pop_dashboard(f"This is the instruction guide for the RC-Assembly task")
            time.sleep(3.0)

        for p in parts:
            # Body Part
            dashboard.show_green_tick(show=False)
            dashboard.pop_dashboard(f"Get the box and assemble it according to the provided guide.")
            positions = [pos_pick_body_h_go, pos_pick_body_go, pos_pick_body, pos_pick_body_h, pos_pick_body_app, pos_place_body_h, pos_place_body, pos_place_body_go, pos_place_body_rem_go, pos_pick_body_app]
            start_robot_movement(robot, positions)
            
            while robot_is_moving:
                time.sleep(0.1)

            dashboard.show_green_tick(show=True)
            dashboard.pop_dashboard(f"[PRESS ENTER to continue]")
            input("--- Press enter to continue ---")
            dashboard.show_green_tick(show=False)
     
            while robot_is_moving:
                time.sleep(0.1)
            # Get Top Part
            positions = [home_go, pos_pick_top_h_go, pos_pick_top_go, pos_pick_top, pos_pick_top_h, pos_pick_body_app]
            start_robot_movement(robot, positions)

         

        

            # Ball Part
            dashboard.pop_dashboard(f"Mount two {p[1]} ball parts, meanwhile i get you the top plate.")
            time.sleep(3)
            dashboard.show_green_tick(show=True)
            dashboard.pop_dashboard(f"[PRESS ENTER to continue]")
            input("--- Press enter to continue ---")
            dashboard.show_green_tick(show=False)
            
            positions = [pos_place_top_h, pos_place_top, pos_place_top_go, pos_place_top_rem_go, pos_pick_body_app, home_go]
            start_robot_movement(robot, positions)
            dashboard.pop_dashboard(f"While top plate is placed, apply stickers to box according to the guide.")
            
            while robot_is_moving:
                time.sleep(0.1)
            dashboard.show_green_tick(show=True)
            dashboard.pop_dashboard(f"[PRESS ENTER to continue]")
            input("--- Press enter to continue ---")
            dashboard.show_green_tick(show=False)
            

        

            # Mount screws
            dashboard.pop_dashboard(f"Screw down the {p[2]} top with two screws.")
            time.sleep(4)
            dashboard.show_green_tick(show=True)
            dashboard.pop_dashboard(f"[PRESS ENTER to continue]")
            input("--- Press enter to continue ---")
            dashboard.show_green_tick(show=False)
            
            

            # Knob Part
            dashboard.pop_dashboard(f"Mount two {p[3]} knobs. ")
            time.sleep(3)
            dashboard.show_green_tick(show=True)
            dashboard.pop_dashboard(f"[PRESS ENTER to continue]")
            input("--- Press enter to continue ---")
            dashboard.show_green_tick(show=False)

            # Part inspection
            dashboard.pop_dashboard(f"Please inspect the controller:")
            time.sleep(3)
            
            dashboard.pop_dashboard(f"{p[0]} body")
            time.sleep(3)
            dashboard.pop_dashboard(f"{p[1]} ball parts")
            time.sleep(3)
            dashboard.pop_dashboard(f"{p[2]} top")
            time.sleep(3)
            dashboard.pop_dashboard(f"{p[3]} knobs")
            time.sleep(3)

            dashboard.pop_dashboard(f"If correct, take the controller and put it into the box. Then close the box and put it aside.")
            time.sleep(3)
            dashboard.show_green_tick(show=True)
            dashboard.pop_dashboard(f"[PRESS ENTER to continue]")
            input("--- Press enter to continue ---")
            dashboard.show_green_tick(show=False)
            

        # End message
        dashboard.pop_dashboard(f"Task finished.")
        time.sleep(2.0)
        print("program finished")

    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")
    finally:
        dashboard.pop_dashboard(f"Task finished. Thank you!")
        logging.info("Program finished.")

if __name__ == "__main__":
    # Reset errors and initialize connection
    logging.info("Resetting robot errors and initializing connection...")
    # robot.reset_error()  # Uncomment if the robot requires error resetting
    main()
