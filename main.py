from furhat_remote_api import FurhatRemoteAPI
import time
import math
import threading
import URBasic

from furhat_functions import Pose, say, listen, listen_for, look, run_parallel_looking, set_pose, set_pose_relative, \
    set_led, gesture, listen_and_say_back, listen_for_and_retry
from Move_Robot import MoveToPositionCommand
from Robot_Controller import move_robot
from TCP_Subscriber import TCPReceiver
from furhat_functions import Pose

# Robot data
robot_ip = "172.20.10.3"
robotModel = URBasic.robotModel.RobotModel()
robot = URBasic.urScriptExt.UrScriptExt(host=robot_ip, robotModel=robotModel)
tcp_receiver = TCPReceiver(robot_ip)
pose = Pose()



# global variables
is_parallel_looking = False
endeffector = Pose()
offset = Pose()
tcp_x, tcp_y, tcp_z = 0, 0, 0
is_parallel_cartesian = False



def is_reached(robot, target_position):
        joint_angles = target_position[:6]
        actual_position = robot.get_actual_joint_positions()
        print("Checking position: Current =", actual_position, "Target =", joint_angles)
        return all(math.isclose(t, a, abs_tol=0.01) for t, a in zip(joint_angles, actual_position))

# Definition of target positions --> false = gripper open

home = (
    math.radians(-90), math.radians(-98), math.radians(-126), 
    math.radians(-45), math.radians(90), math.radians(0), False, False
    )

pos_pick_body = (
    math.radians(-134), math.radians(-125), math.radians(-104), 
    math.radians(-45), math.radians(105), math.radians(329), False, True
    )

pos_pick_body_h = (
    math.radians(-134), math.radians(-95), math.radians(-104), 
    math.radians(-45), math.radians(91), math.radians(20), False, False
    )

pos_place_body = (
    math.radians(-30), math.radians(-116), math.radians(-116), 
    math.radians(-45), math.radians(90), math.radians(321), False, False
    )

pos_place_body_h = (
    math.radians(-30), math.radians(-116), math.radians(-104), 
    math.radians(-45), math.radians(90), math.radians(321), False, True
    )

pos_pick_top = (
    math.radians(-114), math.radians(-95), math.radians(-104), 
    math.radians(-45), math.radians(91), math.radians(20), False, True
    )
pos_pick_top_h = (
    math.radians(-114), math.radians(-95), math.radians(-104), 
    math.radians(-45), math.radians(91), math.radians(20), False, False
    )

pos_place_top = (
    math.radians(-30), math.radians(-130), math.radians(-104), 
    math.radians(-45), math.radians(90), math.radians(321), False, False
    )

pos_place_top_h = (
    math.radians(-30), math.radians(-120), math.radians(-104), 
    math.radians(-45), math.radians(90), math.radians(321), False, True
    )


def main():
    print("init start")
    global endeffector, offset, holder, human, body_rack, top_rack, finished_bin, human_name
    fh = FurhatRemoteAPI("localhost")
    fh.set_voice(name="Matthew")
    fh.set_face(character="Jamie", mask="default")
    fh.set_led_color_name(fh, "none")
    set_pose(offset, 0.3, 0.35, -1.0)
    set_pose(holder, 0.2, 0.15, 0.4)
    set_pose(human, 0.2, 0.4, 0.65)
    set_pose(body_rack, -0.2, 0.1, -0.3)
    set_pose(top_rack, -0.35, 0.1, -0.3)
    set_pose(finished_bin, 0.6, -0.2, 1.0)
    look(fh, human, offset)
    print("init done")
    say(fh, "init done", 1.5)
    welcome_message = True


    # colors and parameters of parts:
    #         body,     balls,      top,        knobs       parameters
    parts = [["red",    "white",    "blue",     "yellow"],
             ["blue",   "yellow",   "red",      "red"]]#,
             #["blue",   "white",    "blue",     "red"],
             #["red",    "white",    "red",      "yellow"],
             #["blue",   "yellow",   "blue",     "yellow"]]


    input("--- Press enter to start! ---")
    time.sleep(1.0)


    # Start thread to get live feed of TCP position
    tcp_receiver.run_parallel_get_cartesian_coordinates(pose, True)
    #looking_thread = run_parallel_looking(fh, True, pose, offset)
    
    # Start teqaching user name
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
        move_robot(robot, home)
        

        # Loop through process
        # Loop over all controllers
    for p in parts:
        # Before next controller is started, robot is in body rack position
        look(fh, human, offset)
        say(fh, "Say next when we can continue with the next controller!", 3.0)
        fh.listen_for_and_retry_silent(fh, ["next"], 2, is_print=True)
        gesture(fh, "BrowRaise")
        time.sleep(1)

        # Robot grabs bottom and moves it to holder
        move_robot(robot, pos_pick_body_h)
        move_robot(robot, pos_pick_body)
        fh.set_led_color_name(fh, p[0])
        look(fh, body_rack, offset)
        say(fh, f"I bring you a {p[0]} body part")

        """wait for robot in position: holder body"""
        time.sleep(5)
        fh.set_led_color_name(fh, "none")

        # Robot puts body in holder and goes to top rack
        move_robot(robot, pos_place_body_h)
        move_robot(robot, pos_place_body)

        look(fh, human, offset)
        fh.set_led_color_name(fh, p[1])
        say(fh, f"Please mount two {p[1]} ball parts", 3.0)
        say(fh, "Say ok when you are done!", 3.0)
        gesture(fh, "Smile")
        look(fh, holder, offset)
        fh.listen_for_and_retry_silent(fh, ["ok", "okay", "OK", "Ok", "Okay"], 2.2, is_print=True)
        look(fh, human, offset)
        fh.set_led_color_name(fh, "none")


        # Robot places top on body in holder
        move_robot(robot, pos_pick_top_h)
        move_robot(robot, pos_pick_top)
        """wait for robot in position: holder (with top in gripper)"""
        look(fh, holder, offset)
        gesture(fh, "Smile")
        time.sleep(2.0)

        # Robot placed the top on the body in holder
        move_robot(robot, pos_place_top_h)
        move_robot(robot, pos_place_top)
        look(fh, human, offset)
        fh.set_led_color_name(fh, p[2])
        say(fh, f"Screw down the {p[2]} top with four screws", 4.0)
        say(fh, "Say ok when done!", 2.0)
        look(fh, holder, offset)
        gesture(fh, "Smile")
        fh.listen_for_and_retry_silent(fh, ["ok", "okay", "OK", "Ok", "Okay"], 2.2, is_print=True)
        look(fh, human, offset)
        fh.set_led_color_name(fh, "none")

        # Top is already screwed to bottom
        time.sleep(1.0)
        look(fh, human, offset)
        fh.set_led_color_name(fh, p[3])
        say(fh, f"Mount two {p[3]} knobs", 3.0)
        say(fh, "Say ok when finished!", 2.5)
        look(fh, holder, offset)
        gesture(fh, "BigSmile")
        fh.listen_for_and_retry_silent(fh, ["ok", "okay", "OK", "Ok", "Okay"], 2.2, is_print=True)
        look(fh, human, offset)
        fh.set_led_color_name(fh, "none")

        # Robot goes to body rack again (part inspection doesn't have to wait for robot to reach its position
        move_robot(robot, home)
     

        # Part inspection
        look(fh, human, offset)
        fh.set_led_color_name(fh, "none")
        say(fh, f"Please inspect the controller", 3.0)
        look(fh, holder, offset)
        fh.set_led_color_name(fh, p[0])
        say(fh, f"{p[0]} body", 2.0)
        fh.set_led_color_name(fh, p[1])
        say(fh, f"{p[1]} ball parts", 2.5)
        fh.set_led_color_name(fh, p[2])
        say(fh, f"{p[2]} top", 2.0)
        fh.set_led_color_name(fh, p[3])
        say(fh, f"{p[3]} knobs", 2.5)
        look(fh, human, offset)
        say(fh, "Say ok when you inspected it!", 3.0)
        fh.set_led_color_name(fh, "none")
        fh.listen_for_and_retry_silent(fh, ["ok", "okay", "OK", "Ok", "Okay"], 2.2, is_print=True)

        # Humans puts finished controller in bin for finished controllers
        gesture(fh, "BigSmile")
        time.sleep(1.0)
        say(fh, f"Well done {human_name}! Please take the controller and move it to the finished bin!", 4.0)
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
    main()



