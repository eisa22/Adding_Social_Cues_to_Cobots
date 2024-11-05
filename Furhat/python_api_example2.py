from furhat_remote_api import FurhatRemoteAPI

# Create an instance of the FurhatRemoteAPI class, providing the address of the robot or the SDK running the virtual robot
furhat = FurhatRemoteAPI("localhost")

# Set voice to Matthew (English)
furhat.set_voice(name='Matthew')

# Get the list of users
users = furhat.get_users()

if len(users) > 0:
    # Attend the nearest user
    furhat.attend(user="CLOSEST")
    furhat.say(text="Oh, hello there", blocking=True)

furhat.say(text="Let me show you my cool LED lights", blocking=True)
# Set the LED lights
furhat.set_led(red=255, green=0, blue=0)

furhat.say(text="And a nice gesture", blocking=True)
# Perform a named gesture
furhat.gesture(name="ExpressDisgust", blocking=True)

furhat.say(text="Please say something", blocking=True)

# Listen for speech
answer = furhat.listen()

if answer.message != "":
    furhat.say(text="I think you said, " + answer.message, blocking=True)
else:
    furhat.say(text="I don't think you said anything", blocking=True)