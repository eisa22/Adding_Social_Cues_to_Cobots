import threading
import time
import math

class BreathingMotionController:
    def __init__(self, robot):
        self.robot = robot
        self.breathing_period = 5.0
        self.breathing_amplitude = 0.02
        self.breathing = False
        self.base_joint_positions = None

    def start_breathing(selfz):
        if not self.breathing:
            print("Starting breathing motion")
            self.breathing = True
            self.base_joint_positions = self.robot.get_actual_joint_positions()
            threading.Thread(target=self.perform_breathing_motion, daemon=True).start()

    def stop_breathing(self):
        print("Stopping breathing motion")
        self.breathing = False

    def perform_breathing_motion(self):
        while self.breathing:
            current_time = time.time()
            offset = self.breathing_amplitude * math.sin(2 * math.pi * current_time / self.breathing_period)
            breathing_pose = [base + offset for base in self.base_joint_positions]
            self.robot.movej(q=breathing_pose, a=0.05, v=0.05)
            time.sleep(0.1)
