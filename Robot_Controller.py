import URBasic
import math
import time
import math3d as m3d

"""SETTINGS AND VARIABLES ________________________________________________________________"""

ROBOT_IP = '192.168.31.224'
ACCELERATION = 0.4  # Robot acceleration value
VELOCITY = 0.4  # Robot speed value

# The Joint position the robot starts at
robot_startposition = (math.radians(0.0),
                       math.radians(-90),
                       math.radians(0),
                       math.radians(-90),
                       math.radians(0),
                       math.radians(0))

# Define the target position (x, y, z, rx, ry, rz) in meters and radians
target_position = [0.1, 0.2, 0.3, 0, math.radians(45), 0]  # Modify these values as needed

"""FUNCTIONS _____________________________________________________________________________"""

def move_to_point(robot, position):
    """
    Function to move the robot to a specific target position.
    
    Inputs:
        position: A list representing the target pose in the format [x, y, z, rx, ry, rz]
    """
    robot.set_realtime_pose(position)
    print("Moved robot to position:", position)

"""MAIN SCRIPT ____________________________________________________________________________"""

# Initialise robot with URBasic
print("Initialising robot")
robotModel = URBasic.robotModel.RobotModel()
robot = URBasic.urScriptExt.UrScriptExt(host=ROBOT_IP, robotModel=robotModel)

robot.reset_error()
print("Robot initialised")
time.sleep(1)

# Move Robot to the starting position
robot.movej(q=robot_startposition, a=ACCELERATION, v=VELOCITY)
print("Robot moved to start position")

# Move Robot to the target point
robot.init_realtime_control()  # Starts the realtime control loop on the Universal-Robot Controller
time.sleep(1)  # Wait to ensure everything is initialised

try:
    print("Moving to target point")
    move_to_point(robot, target_position)
    time.sleep(2)  # Wait to allow movement to complete

except KeyboardInterrupt:
    print("Closing robot connection")
    robot.close()

except Exception as e:
    print("An error occurred:", e)
    robot.close()

finally:
    # Remember to always close the robot connection, otherwise it is not possible to reconnect
    robot.close()
