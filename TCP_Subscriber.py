from rtde_receive import RTDEReceiveInterface
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class TCPReceiver:
    def __init__(self, robot_ip):
        try:
            self.rtde_receive = RTDEReceiveInterface(robot_ip)
            print("Successfully connected to the robot.")
        except Exception as e:
            print(f"Error: Could not connect to the robot at {robot_ip}. Exception: {e}")
            self.rtde_receive = None

    def get_cartesian_coordinates(self):
        """Getter method to retrieve the TCP position in Cartesian coordinates."""
        if self.rtde_receive:
            try:
                tcp_position = self.rtde_receive.getActualTCPPose()
                x, y, z = tcp_position[0], tcp_position[1], tcp_position[2]
                print(f"Cartesian Coordinates: X = {x}, Y = {y}, Z = {z}")
                return x, y, z
            except Exception as e:
                print(f"Error: Connection issue during data retrieval. Exception: {e}")
        else:
            print("No active connection to the robot.")
        return None

def update_plot(i, tcp_receiver, vector, ax):
    coords = tcp_receiver.get_cartesian_coordinates()
    if coords:
        x, y, z = coords
        # Update vector data in 3D plot with Cartesian coordinates
        vector.set_data([0, x], [0, y])
        vector.set_3d_properties([0, z])
        ax.figure.canvas.draw()

def main():
    robot_ip = '192.168.0.13'
    print("Attempting to connect to the robot for TCP position data...")
    
    tcp_receiver = TCPReceiver(robot_ip)

    # Initialize 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Set up plot limits
    max_range = 1.0
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])

    # Set up initial vector
    vector, = ax.plot([0, 0], [0, 0], [0, 0], color='b', marker='o')
    ax.quiver(0, 0, 0, 0, 0, 1, length=0.1, color="k")  # Origin arrow
    
    # Start updating the plot with the robot's TCP Cartesian coordinates
    ani = FuncAnimation(fig, update_plot, fargs=(tcp_receiver, vector, ax), interval=100)
    plt.show()

    print("Closing connection to the robot.")
    
if __name__ == "__main__":
    main()
