
"""
Test script to verify SO-100 arm setup with Bionix API
"""

import numpy as np
import pybullet as pb
import pybullet_data
from pathlib import Path
import time

# Configuration
FREQUENCY = 30
URDF_PATH = str(Path(__file__).parent / "SO-100-arm-main/urdf/so_100_arm.urdf")

# Connect to PyBullet
pb.connect(pb.GUI)
pb.setAdditionalSearchPath(pybullet_data.getDataPath())
pb.setGravity(0, 0, -9.81)
pb.loadURDF("plane.urdf")

# Load SO-100 robot
robot_id = pb.loadURDF(URDF_PATH, useFixedBase=True)

# Print joint information to identify correct indices
print("SO-100 Joint Information:")
print("-" * 50)
for j in range(pb.getNumJoints(robot_id)):
    info = pb.getJointInfo(robot_id, j)
    joint_name = info[1].decode()
    joint_type = info[2]
    joint_type_str = "REVOLUTE" if joint_type == pb.JOINT_REVOLUTE else "PRISMATIC" if joint_type == pb.JOINT_PRISMATIC else "FIXED"
    print(f"Index {j}: {joint_name} - Type: {joint_type_str}")

# Test joint control
print("\nTesting joint control...")
num_joints = pb.getNumJoints(robot_id)

# Simple test movement
test_positions = [0.0] * num_joints
test_positions[0] = 0.5  # Move first joint
test_positions[1] = 0.3  # Move second joint

for _ in range(100):
    for i in range(len(test_positions)):
        pb.setJointMotorControl2(
            robot_id,
            i,
            pb.POSITION_CONTROL,
            test_positions[i],
            force=5 * 240.0
        )
    pb.stepSimulation()
    time.sleep(1/FREQUENCY)

print("\nTest complete! Check the joint indices printed above.")
print("Update EEF_IDX and GRIPPER_IDX in your code accordingly.")

# Keep simulation open
input("Press Enter to close...")
pb.disconnect()