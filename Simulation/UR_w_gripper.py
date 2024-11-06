import pybullet as p
import pybullet_data

# Start PyBullet simulation
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Enable gravity
p.setGravity(0, 0, -9.81)

# Add a ground plane for stability
plane_id = p.loadURDF("plane.urdf")

# Load the UR3e robot
ur3e_robot = p.loadURDF(
    "/home/samuel/Workspace/UR_RobotChallenge/Simulation/urdf/ur3e.urdf",
    basePosition=[0, 0, 0],
    useFixedBase=True  # Fix the robot base
)

# Load the Robotiq gripper
robotiq_gripper = p.loadURDF(
    "/home/samuel/Workspace/UR_RobotChallenge/Simulation/urdf/robotiq_arg85_description/robots/robotiq_arg85_description.URDF",
    basePosition=[0, 0, 0.1]  # Align closer to the robot
)

# Debug tool link index
num_links = p.getNumJoints(ur3e_robot)
for i in range(num_links):
    print(f"Link {i}: {p.getJointInfo(ur3e_robot, i)[12].decode('utf-8')}")

# Attach the gripper to the robot (adjust link index)
tool_link_index = 6  # Replace with the correct link index for 'tool0' or equivalent
p.createConstraint(
    parentBodyUniqueId=ur3e_robot,
    parentLinkIndex=tool_link_index,
    childBodyUniqueId=robotiq_gripper,
    childLinkIndex=-1,
    jointType=p.JOINT_FIXED,
    jointAxis=[0, 0, 0],
    parentFramePosition=[0, 0, 0.1],  # Adjust based on actual link state
    childFramePosition=[0, 0, 0]
)

# Reduce physics step size for stability
p.setPhysicsEngineParameter(fixedTimeStep=0.01, numSolverIterations=150)

# Run the simulation
while True:
    p.stepSimulation()
