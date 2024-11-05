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


def is_reached(robot, target_position):
        joint_angles = target_position[:6]
        actual_position = robot.get_actual_joint_positions()
        print("Checking position: Current =", actual_position, "Target =", joint_angles)
        return all(math.isclose(t, a, abs_tol=0.01) for t, a in zip(joint_angles, actual_position))


def main():
    print("init start")
    global endeffector, offset
    #global tcp_x, tcp_y, tcp_z


    # Create an instance of the FurhatRemoteAPI class, providing the address of the robot or the SDK running the virtual robot
    fh = FurhatRemoteAPI("localhost")
    fh.set_voice(name="Matthew")
    fh.set_face(character="Titan", mask="default")
    set_led(fh, 0, 0, 0)
    set_pose(offset, 0, 0, -2)
    print("init done")
    say(fh, "Init done")
    time.sleep(3)

    tcp_receiver.run_parallel_get_cartesian_coordinates(pose, True)
    looking_thread = run_parallel_looking(fh, True, pose, offset)
    
    move_robot(robot, initial_position)
    set_led(fh, 255, 0, 0)
    while not is_reached(robot, initial_position):
        print("TCP_Position", pose.x, pose.y, pose.z)
        print("Moving towards initial position...")
        time.sleep(0.5)
    print("Initial position reached.")
    set_led(fh, 0, 255, 0)

    time.sleep(3)

    move_robot(robot, target_position)
    set_led(fh, 255, 0, 0)
    while not is_reached(robot, target_position):
        print("TCP_Position", pose.x, pose.y, pose.z)
        print("Moving towards initial position...")
        time.sleep(0.5)
    print("Initial position reached.")
    set_led(fh, 0, 255, 0)



   
    say(fh, "Hi, i am a virtual furhat robot head.")
    say(fh, "Should I move to next position?", 5.0)
    listen_for_and_retry(fh, ["okay", "ok", "Okay", "OK", "Ok"], 1.5, 0.0, 10, is_print=True)
    move_robot(robot, initial_position)
    time.sleep(3)






    """

    #Last working stand'____________________________________________________________
    say(fh, "Hi, i am a virtual furhat robot head. This is a quick demonstration of how to work with me.", 7.5)
    say(fh, "You already experienced the say function. Sadly, a wait time has to be manually configured, so i dont mess stuff up.", 8.0)
    say(fh, "First we will check the look function. I can rotate my head to a target and also take some offset into account.", 8.0)

    set_pose(endeffector, 0.5, 0.2, 0)
    set_pose(offset, 0, 0, -2)
    look(fh, endeffector, offset)
    say(fh, "I am turning my head", 4.0)

    set_pose_relative(endeffector, -1, -0.2, 0)
    look(fh, endeffector, offset)
    say(fh, "And again!", 5)

    say(fh, "Now I will demonstrate that I can turn my head while doing other stuff. I wanna do circles!", 7.0)
    looking_thread = run_parallel_looking(fh, True, endeffector, offset)

    time.sleep(5.0)
    say(fh, "I'm getting dizzy.", 5.0)
    say(fh, "Now i will turn my LEDs to red!", 2.0)
    set_led(fh, 255, 0, 0)
    time.sleep(2)
    say(fh, "Now dim green")
    set_led(fh, 0, 50, 0)
    time.sleep(3)
    set_led(fh, 0, 0, 0)

    say(fh, "Lets show some gestures!", 3.0)
    gesture(fh, "Shake")
    time.sleep(2)
    gesture(fh, "BigSmile")
    time.sleep(2)
    gesture(fh, "ExpressAnger")
    time.sleep(2)
    gesture(fh, "Roll")
    time.sleep(2)
    
    say(fh, "Lets check the listen function. Say something and i will print it out.", 4.0)
    print(listen(fh))
    time.sleep(2)

    say(fh, "Say something an I will say it back and print it!", 2.5)
    print(listen_and_say_back(fh, "You said "))
    time.sleep(3)

    say(fh, "I stop circling", 2)
    run_parallel_looking(fh, False, endeffector, offset)
    if looking_thread:
        looking_thread.join()

    set_pose(endeffector, 0, 0, 0)
    look(fh, endeffector, offset)
    time.sleep(3.5)

    say(fh, "Now lets check the listen for an retry function. You can only proceed, if you say okay. But please also try something else first.", 8.2)
    listen_for_and_retry(fh, ["okay", "ok, Okay, OK, Ok"], 1.5, 0.0, 10, is_print=True)
    say(fh, "Wow, you actually managed to say okay!", 3)
    gesture(fh, "BigSmile")
    time.sleep(2)

    say(fh, "The function we just used uses the listen for function internally, that just checks whether you said what i want you to.", 7.0)
    say(fh, "Say goodbye!", 1.5)
    print(listen_for(fh, ["goodbye", "good bye"], True))


    """






if __name__ == "__main__":
    main()