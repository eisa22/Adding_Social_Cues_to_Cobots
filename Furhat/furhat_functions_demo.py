from furhat_remote_api import FurhatRemoteAPI
import time
import math
import threading

from furhat_functions import Pose, say, listen, listen_for, look, run_parallel_looking, set_pose, set_pose_relative, \
    set_led, gesture, listen_and_say_back, listen_for_and_retry

# global variables
is_parallel_looking = False
endeffector = Pose()
offset = Pose()

# only for demo
circular_motion_run = True

def circular_motion(radius=0.5, speed=1.0, update_interval=0.02, duration=1000):
    """
    Function just for demo purposes of parallel_looking in a second thread
    """
    global endeffector, circular_motion_run
    start_time = time.time()

    while (time.time() - start_time) < duration and circular_motion_run:
        # Get the current time in seconds
        current_time = time.time()

        # Calculate the angle in radians based on the time and speed
        angle = current_time * speed

        # Calculate x and y coordinates based on circular motion formula
        endeffector.x = radius * math.cos(angle)
        endeffector.y = radius * math.sin(angle)

        # Print the current coordinates
        #print(f"x: {endeffector.x:.2f}, y: {endeffector.y:.2f}")

        # Wait for the specified interval before updating
        time.sleep(update_interval)


def main():
    global endeffector, offset
    global circular_motion_run

    # Create an instance of the FurhatRemoteAPI class, providing the address of the robot or the SDK running the virtual robot
    fh = FurhatRemoteAPI("localhost")
    fh.set_voice(name="Matthew")
    fh.set_face(character="Titan", mask="default")
    set_led(fh, 0, 0, 0)
    set_pose(endeffector, 0, 0, 0)
    set_pose(offset, 0, 0, -2)
    look(fh, endeffector, offset)

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
    # circular function is just used for demo, endeffector position should be defined by real robot
    circle_thread = threading.Thread(target=circular_motion, args=(0.5, 2.0))
    circle_thread.start()
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

    # end the circle_thread
    circular_motion_run = False
    circle_thread.join()

    print("End of demo")

if __name__ == "__main__":
    main()