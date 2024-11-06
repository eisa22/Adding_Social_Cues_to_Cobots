import pybullet as p
import pybullet_data
import time
import math
import os
import numpy as np

# Connect to PyBullet in GUI mode
p.connect(p.GUI)

# Set up search path for PyBullet data (for the ground plane)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load the ground plane
# plane_id = p.loadURDF("plane.urdf")

# Set gravity in the environment
p.setGravity(0, 0, -9.81)

# Path to your UR3 URDF model (adjust this path as needed)
ur3_path = "Simulation/urdf/ur3e.urdf"  # Replace with the actual path to your UR3 URDF
print("Loading UR3 URDF from:", os.path.abspath(ur3_path))

# Load the UR3 robot into the simulation
ur3_start_position = [0, 0, 0]
ur3_start_orientation = p.getQuaternionFromEuler([0, 0, 0])
try:
    ur3_id = p.loadURDF(ur3_path, ur3_start_position, ur3_start_orientation, useFixedBase=True)
except p.error as e:
    print("Error loading URDF:", e)
    p.disconnect()
    exit()

# Get the number of joints
num_joints = p.getNumJoints(ur3_id)
print("UR3 has {} joints.".format(num_joints))

# Define the move_sim_robot function
def move_sim_robot(position, steps=240):
    # Extract joint angles and gripper state from the position tuple
    joint_angles = position[:6]  # First six elements are joint angles
    gripper_open = position[7]   # Last boolean for gripper state

    # Get current joint positions
    current_positions = [p.getJointState(ur3_id, joint_index)[0] for joint_index in range(num_joints)]

    # Calculate incremental movement per step
    increments = [(target - current) / steps for target, current in zip(joint_angles, current_positions)]

    for step in range(steps):
        # Update each joint position gradually
        for joint_index, increment in enumerate(increments):
            if joint_index < num_joints:  # Ensure we're within joint limits
                target_position = current_positions[joint_index] + increment * step
                p.setJointMotorControl2(
                    bodyIndex=ur3_id,
                    jointIndex=joint_index,
                    controlMode=p.POSITION_CONTROL,
                    targetPosition=target_position
                )

        # Control gripper state (dummy code since gripper setup may vary)
        gripper_joint_index = num_joints - 1  # Adjust based on actual gripper joint index
        if gripper_open:
            p.setJointMotorControl2(
                bodyIndex=ur3_id,
                jointIndex=gripper_joint_index,
                controlMode=p.POSITION_CONTROL,
                targetPosition=0.04  # Open position
            )
        else:
            p.setJointMotorControl2(
                bodyIndex=ur3_id,
                jointIndex=gripper_joint_index,
                controlMode=p.POSITION_CONTROL,
                targetPosition=0.0  # Closed position
            )

        # Step the simulation
        p.stepSimulation()
        time.sleep(1 / 240)  # Slow down the simulation for viewing

# Initial position
initial_position = (
    math.radians(0), math.radians(-90), math.radians(0), 
    math.radians(-90), math.radians(0), math.radians(0), 
    False, False
)

# Run the simulation loop indefinitely
while True:
    # Move the robot to the initial position
    move_sim_robot(initial_position, steps=240)  # Adjust steps to control speed

    # Step the simulation
    p.stepSimulation()
    time.sleep(1 / 240)  # Slow down the simulation for viewing

# Disconnect from the simulation
p.disconnect()
