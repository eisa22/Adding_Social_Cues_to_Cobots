import URBasic
import time
from Move_Robot import MoveToPositionCommand
from Breathing_Motion_Controller import BreathingMotionController
from Gripper_Control import ControlGripper
from TCP_Subscriber import TCPReceiver
from furhat_functions import Pose
from furhat_functions import *
from Positions import *
from furhat_remote_api import FurhatRemoteAPI
from furhat_functions import * 
import robotiq_gripper 
import threading
import time


# Robot data
USE_UR_ROBOT = False # Set to True if using UR robot, False if using URSIM
robot_ip = "192.168.31.224"
robotModel = URBasic.robotModel.RobotModel()
robot = URBasic.urScriptExt.UrScriptExt(host=robot_ip, robotModel=robotModel)
tcp_receiver = TCPReceiver(robot_ip)
pose = Pose()
gripper = robotiq_gripper.RobotiqGripper()
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
#         body,     balls,      top,        knobs       parameters
parts = [["yellow",    "yellow",    "red",     "blue"],
            ["blue",   "yellow",   "red",      "red"]]#,
            #["blue",   "white",    "blue",     "red"],
            #["red",    "white",    "red",      "yellow"],
            #["blue",   "yellow",   "blue",     "yellow"]]



 # Definition of move robot function
def move_robot(robot, pose):
    """
    Move the robot to the specified pose.
    pose: Tuple of joint angles and two booleans (hovering, gripper_state).
          Format: (j1, j2, j3, j4, j5, j6, hovering, gripper_state)
    """
    # Initialize controllers
    breathing_controller = BreathingMotionController(robot)
    #gripper = ControlGripper(robot)

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

    if USE_UR_ROBOT:
        if gripper_state:
            try:

                print("Closing gripper.")
                gripper.move_and_wait_for_pos(255,255,255)

            except RuntimeError as e:
                print(f"Error during gripper operation: {e}")

        else:
            print("Opening gripper.")
            gripper.move_and_wait_for_pos(0,255,255)

    # Handle hovering and breathing state
    if hovering:
        print("Starting hover breathing motion.")
        breathing_controller.start_breathing()
    else:
        breathing_controller.stop_breathing()
    time.sleep(1)  # Simulate holding at the position

def execute_movement(robot, pose):
    """
    Executes a robot movement safely with error handling.
    :param robot: The robot instance.
    :param pose: The target pose (tuple of joint angles and states).
    """
    try:
        move_robot(robot, pose)
        print("Target position reached.")
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Stopping the robot.")
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
    # Initialize controllers
    print("____Init Robot____")
    tcp_receiver.run_parallel_get_cartesian_coordinates(pose, True)

    if USE_UR_ROBOT:
        gripper.connect(robot_ip, 63352)
        print("Gripper connected")
        gripper.activate()
        print("Gripper activated")
    execute_movement(robot, home_go)

    
    print("____Finished Init Robot____")

    # Initialize Furhat
    print("____Init Furhat____")
    global endeffector, offset, holder, human, body_rack, top_rack, finished_bin, human_name
    fh = FurhatRemoteAPI("localhost")
    fh.set_voice(name="Matthew")
    fh.set_face(character="Jamie", mask="default")
    set_led_color_name(fh, "none")
    set_pose(offset, 0.3, 0.35, -1.0)
    set_pose(holder, 0.2, 0.15, 0.4)
    set_pose(human, 0.2, 0.4, 0.65)
    set_pose(body_rack, -0.2, 0.1, -0.3)
    set_pose(top_rack, -0.35, 0.1, -0.3)
    set_pose(finished_bin, 0.6, -0.2, 1.0)
    look(fh, human, offset)
    say(fh, "init done", 1.5)
    welcome_message = False
    print("____Finished Init Furhat____")

    input("--- Press enter to start! ---")
    time.sleep(1.0)

    # Welcome message
    if welcome_message:

        look(fh, human, offset)
        gesture(fh, "BigSmile")
        time.sleep(1.5)
        say(fh, "Hi, i am furhat. Today I will be working with you.", 4.0)

        name_correct = False
        while not name_correct:
            say(fh, "What is your name?", 2.0)
            human_name = listen_and_say_back(fh, "Hello ", 3.0)
            print(human_name)
            say(fh, "Did I say that correctly?", 1.5)
            name_correct = listen_for(fh, ["yes", "ok", "okay", "ja", "ya", "correct"], is_print=True)
        say(fh, f"Awesome, let's start working {human_name}!", 3.0)
        gesture(fh, "Smile")
        time.sleep(2.0)
        
    say(fh, "Hi, i am Furhat. Today I will be working with you.", 4.0)

    for p in parts:
        # Before next controller is started, robot is in body rack position
        look(fh, human, offset)
        say(fh, "Say next when we can continue with a new controller!", 3.0)
        listen_for_and_retry_silent(fh, ["next"], 2, is_print=True)
        gesture(fh, "BrowRaise")
        time.sleep(1.5)

        # Body Part
        # Start robot movement in a separate thread
        positions = [pos_pick_body_h_go, pos_pick_body_go, pos_pick_body, pos_pick_body_h, pos_pick_body_app, pos_place_body_h]
        start_robot_movement(robot, positions)
        say(fh, f"I bring you a {p[0]} body part. Meanwhile get the box and assemble it according to the provided guide.")
        set_led_color_name(fh, p[0])
        look(fh, body_rack, offset)

        # Wait until movement is finished
        while robot_is_moving:
            time.sleep(0.1)
        
        

        #Place body part
        look(fh, holder, offset)
        positions = [pos_place_body, pos_place_body_go, pos_place_body_rem_go]
        start_robot_movement(robot, positions)
        say(fh, f"Careful, now I am going to place the body into the holder")

        # Wait until movement is finished
        while robot_is_moving:
            time.sleep(0.1)

        positions = [pos_pick_body_app, home_go, pos_pick_top_h_go, pos_pick_top_go, pos_pick_top, pos_pick_top_h, pos_pick_body_app]
        start_robot_movement(robot, positions)

        

    # Ball Part
        look(fh, human, offset)
        set_led_color_name(fh, p[1])
        
        say(fh, f"Now I will get you the top plate. Meanawhile please mount two {p[1]} ball parts.", 3.0)
        time.sleep(3.5)
        say(fh, f"When finished with the two {p[1]} ball parts apply the stickers to the box according to the guide.", 3.0)
        # Wait until movement is finished
        say(fh, "Say ok when you are done!", 3.0)
        gesture(fh, "Smile")
        look(fh, holder, offset)
        listen_for_and_retry_silent(fh, ["ok", "okay", "OK", "Ok", "Okay"], 2.2, is_print=True)
        look(fh, human, offset)
        set_led_color_name(fh, "none")

        # Wait until movement is finished
        while robot_is_moving:
            time.sleep(0.1)
        

        say(fh, f"Careful, I will now put the topplate on the remote control.", 3.0)
        positions = [pos_place_top_h, pos_place_top, pos_place_top_go]
        start_robot_movement(robot, positions)
        look(fh, holder, offset)

        # Wait until movement is finished
        while robot_is_moving:
            time.sleep(0.1)

        
       
        gesture(fh, "Smile")
        set_led_color_name(fh, "none")

        positions = [pos_place_top_rem_go, pos_pick_body_app, home_go]
        start_robot_movement(robot, positions)
        
      

        # Mount screws
        look(fh, holder, offset)
        say(fh, f"Screw down the {p[2]} top with two screws", 4.0)
        say(fh, "Say ok when you are done!", 2.0)
        look(fh, holder, offset)
        gesture(fh, "Smile")
        listen_for_and_retry_silent(fh, ["ok", "okay", "OK", "Ok", "Okay"], 2.2, is_print=True)
        look(fh, human, offset)
        say(fh, "Great job, we are almoust done!")
        gesture(fh, "Smile")
        set_led_color_name(fh, "none")
        
        # Wait until movement is finished
        while robot_is_moving:
            time.sleep(0.1)

        # Knob Part
        #time.sleep(1.0)
        look(fh, human, offset)
        set_led_color_name(fh, p[3])
        say(fh, f"Mount two {p[3]} knobs", 3.0)
        say(fh, "Say ok when finished!", 2.5)
        look(fh, holder, offset)
        gesture(fh, "BigSmile")
        listen_for_and_retry_silent(fh, ["ok", "okay", "OK", "Ok", "Okay", "next"], 2.2, is_print=True)
        look(fh, human, offset)
        set_led_color_name(fh, "none")

        # Part inspection
        look(fh, human, offset)
        set_led_color_name(fh, "none")
        say(fh, f"Please inspect the controller", 3.0)
        look(fh, holder, offset)
        set_led_color_name(fh, p[0])
        say(fh, f"{p[0]} body", 2.0)
        set_led_color_name(fh, p[1])
        say(fh, f"{p[1]} ball parts", 2.5)
        set_led_color_name(fh, p[2])
        say(fh, f"{p[2]} top", 2.0)
        set_led_color_name(fh, p[3])
        say(fh, f"{p[3]} knobs", 2.5)
        look(fh, human, offset)
        say(fh, "Say ok when you inspected it!", 3.0)
        set_led_color_name(fh, "none")
        listen_for_and_retry_silent(fh, ["ok", "okay", "OK", "Ok", "Okay"], 2.2, is_print=True)

        # Finished Controller
        # Humans puts finished controller in bin for finished controllers
        gesture(fh, "BigSmile")
        time.sleep(1.0)
        say(fh, f"Well done {human_name}! Please take the controller and put it into the box. Then close the box and put it aside.", 2.0)
        gesture(fh, "BigSmile")
        look(fh, finished_bin, offset)
        time.sleep(3)

    # End message
    look(fh, human, offset)
    say(fh, f"Thank you for your great work {human_name}! Goodbye", 5.0)
    gesture(fh, "BigSmile")
    time.sleep(3.0)
    print("program finished")




if __name__ == "__main__":
    # Reset errors and initialize connection
    print("Resetting robot errors and initializing connection...")
    # robot.reset_error()  # Uncomment if the robot requires error resetting
    main()
