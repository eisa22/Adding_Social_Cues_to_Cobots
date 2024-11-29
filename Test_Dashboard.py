from Dashboard import Dashboard  # Ensure the Dashboard class is correctly imported
import time

# Instructions for testing
instructions = [
    "This is the instruction guide for the RC-Assembly task.",
    "Assemble the cardboard box according to the provided guide.",
    "Careful, now I am going to place the body into the holder.",
    "Mount two white ball parts, meanwhile I get you the top plate.",
    "Careful, I will now put the top plate on the remote control.",
    "Screw down the blue top with four screws.",
    "Mount two red knobs.",
    "Please inspect the controller:",
    "Red body",
    "White ball parts",
    "Blue top",
    "Yellow knobs",
    "Take the controller and put it into the box. Then close the box and put it aside.",
    "Task finished. Thank you!"
]

# Initialize the Dashboard
dashboard = Dashboard()

def test_dashboard():
    """Test displaying instructions on the dashboard."""
    print("Starting the Dashboard...")
    dashboard.start_dashboard()  # Start the Dashboard UI

    for instruction in instructions:
        print(f"Displaying instruction: {instruction}")  # Debug: Print to console
        dashboard.pop_dashboard(instruction)  # Update the dashboard with the instruction
        input("Press Enter to show the next instruction...")  # Wait for user interaction

    print("End of test. Showing final message...")
    dashboard.pop_dashboard("End of test instructions. Thank you!")  # Final message
    time.sleep(3)  # Allow time for the final message
    dashboard.stop_dashboard()  # Gracefully stop the dashboard
    print("Dashboard stopped.")

if __name__ == "__main__":
    try:
        test_dashboard()
    except KeyboardInterrupt:
        print("Exiting the test due to keyboard interrupt.")
        dashboard.stop_dashboard()
