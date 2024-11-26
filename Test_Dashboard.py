import time
from Dashboard import Dashboard

# Initialize the Dashboard instance
dashboard = Dashboard()

def robot_controller():
    """Simulated robot controller with dashboard updates."""
    for i in range(20):
        print(f"Running step {i}")
        dashboard.pop_dashboard(f"Robot is at step {i}")  # Update the dashboard
        time.sleep(2)  # Simulate some robot operation

if __name__ == "__main__":
    try:
        # Start the dashboard
        dashboard.start_dashboard()

        # Run the robot controller
        robot_controller()

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Stop the dashboard gracefully
        dashboard.stop_dashboard()
