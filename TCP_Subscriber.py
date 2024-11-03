from rtde_receive import RTDEReceiveInterface
import time

def main():
    # Define the robot's IP address
    robot_ip = '192.168.31.224'

    # Attempt to connect to the robot
    print("Attempting to connect to the robot for TCP position data...")
    try:
        rtde_receive = RTDEReceiveInterface(robot_ip)
        print("Successfully connected to the robot.")
    except Exception as e:
        print(f"Error: Could not connect to the robot at {robot_ip}. Exception: {e}")
        return

    try:
        while True:
            # Get the current TCP position
            tcp_position = rtde_receive.getActualTCPPose()
            print(f"Current TCP Position: {tcp_position}")

            # Add a small delay to avoid overwhelming the output
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Stopped TCP position subscriber.")
    except Exception as e:
        print(f"Error: Connection to the robot was lost. Exception: {e}")
    finally:
        print("Closing connection to the robot.")
        # Add any cleanup code here if necessary

if __name__ == "__main__":
    main()
