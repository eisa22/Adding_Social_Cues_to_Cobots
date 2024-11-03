from rtde_receive import RTDEReceiveInterface
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

def cartesian_to_spherical(x, y, z):
    # Convert Cartesian coordinates to spherical coordinates
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r) if r != 0 else 0  # inclination angle
    phi = np.arctan2(y, x)  # azimuthal angle
    return r, theta, phi

def update_plot(i, rtde_receive, vector, ax):
    try:
        tcp_position = rtde_receive.getActualTCPPose()
        x, y, z = tcp_position[0], tcp_position[1], tcp_position[2]
        
        # Convert to spherical coordinates
        r, theta, phi = cartesian_to_spherical(x, y, z)
        print(f"Spherical Coordinates: Radius = {r}, Theta = {theta}, Phi = {phi}")
        
        # Update vector data in 3D plot
        vector.set_data([0, r * np.sin(theta) * np.cos(phi)], [0, r * np.sin(theta) * np.sin(phi)])
        vector.set_3d_properties([0, r * np.cos(theta)])

        # Redraw the plot
        ax.figure.canvas.draw()
        
    except Exception as e:
        print(f"Error: Connection issue during data retrieval. Exception: {e}")
        return

def main():
    robot_ip = '192.168.31.224'
    print("Attempting to connect to the robot for TCP position data...")
    
    try:
        rtde_receive = RTDEReceiveInterface(robot_ip)
        print("Successfully connected to the robot.")
    except Exception as e:
        print(f"Error: Could not connect to the robot at {robot_ip}. Exception: {e}")
        return

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
    
    # Start updating the plot with the robot's TCP direction
    ani = FuncAnimation(fig, update_plot, fargs=(rtde_receive, vector, ax), interval=100)
    plt.show()

    print("Closing connection to the robot.")
    
if __name__ == "__main__":
    main()
