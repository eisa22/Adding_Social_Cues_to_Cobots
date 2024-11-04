from furhat_remote_api import FurhatRemoteAPI
import time
import math
import threading


class Pose:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Pose(x={self.x}, y={self.y}, z={self.z})"
    



def set_pose(pose: Pose, x, y, z):
    pose.x = x
    pose.y = y
    pose.z = z

def set_pose_relative(pose: Pose, x, y, z):
    pose.x += x
    pose.y += y
    pose.z += z

def look(furhat: FurhatRemoteAPI, target: Pose, offset: Pose):
    location = f"{target.x - offset.x},{target.y - offset.y},{target.z - offset.z}"
    furhat.attend(location=location)
    return location

def parallel_looking(furhat: FurhatRemoteAPI, target: Pose, offset: Pose, parallel_looking_hz: float = 20.0):
    while is_parallel_looking:
        look(furhat, target, offset)
        time.sleep(1 / parallel_looking_hz)

def run_parallel_looking(furhat: FurhatRemoteAPI, is_running: bool, target: Pose, offset: Pose,
                         parallel_looking_hz: float = 20.0) -> threading.Thread | None:
    global is_parallel_looking
    is_parallel_looking = is_running

    if is_running:
        looking_thread = threading.Thread(target=parallel_looking, args=(furhat, target, offset, parallel_looking_hz))
        looking_thread.start()
        return looking_thread
    else:
        is_parallel_looking = False
        return None

def set_led(furhat: FurhatRemoteAPI, red, green, blue):
    # Set the LED lights between 0 and 255
    furhat.set_led(red=red, green=green, blue=blue)

def gesture(furhat: FurhatRemoteAPI, gesture_name):
    # Perform a named gesture
    # gesture_name is string
    furhat.gesture(name=gesture_name)

    # Possible gestures
    """
    BigSmile
    Blink
    BrowFrown
    BrowRaise
    CloseEyes
    ExpressAnger
    ExpressDisgust
    ExpressFear
    ExpressSad
    GazeAway
    Nod
    Oh
    OpenEyes
    Roll
    Shake
    Smile
    Surprise
    Thoughtful
    Wink
    """

def say(furhat: FurhatRemoteAPI, text, sleeptime: float = 0.0):
    # text is string
    furhat.say(text=text)
    time.sleep(sleeptime)

def listen(furhat: FurhatRemoteAPI):
    speech = furhat.listen()
    return speech.message

def listen_and_say_back(furhat: FurhatRemoteAPI, text_before):
    speech = listen(furhat)
    text = f"{text_before} {speech}"
    say(furhat, text, 0.0)
    return speech

def listen_for(furhat: FurhatRemoteAPI, texts: list[str], is_print=False):
    speech = furhat.listen()
    if is_print:
        print(speech.message)
    if speech.message in texts:
        return True
    return False

def listen_for_and_retry(furhat: FurhatRemoteAPI, texts: list[str], sleeptime_text, sleeptime_retry = 0.0, max_tries: int = 10, is_print=False):
    tries = 0
    result = False
    while not result and tries < max_tries:
        result = listen_for(furhat, texts, is_print)
        if not result:
            tries += 1
            if tries >= max_tries:
                # Print fail and return False after reaching max_tries
                print("Too many tries!")
                return False
            time.sleep(sleeptime_retry)
            say_again_text = f"Please say {texts[0]} again!"
            say(furhat, say_again_text, sleeptime_text)
    return True