import threading
import time
from rtde_receive import RTDEReceiveInterface  # Make sure rtde_receive package is imported

class TCPPositionPublisher:
    def __init__(self, robot_ip, frequency=10):
        self.rtde_receive = RTDEReceiveInterface(robot_ip)
        self.frequency = frequency
        self.running = False

    def start_publishing(self):
        self.running = True
        threading.Thread(target=self.publish_position, daemon=True).start()

    def stop_publishing(self):
        self.running = False

    def publish_position(self):
        while self.running:
            tcp_position = self.rtde_receive.getActualTCPPose()
            print("Publishing TCP Position:", tcp_position)
            # ToDo: You could add logic to send data over a network socket, write to a shared file, etc.
            time.sleep(1 / self.frequency)
