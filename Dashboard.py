import tkinter as tk
from queue import Queue
import threading
import time
from datetime import datetime


class Dashboard:
    def __init__(self):
        """Initialize the Dashboard class."""
        self.queue = Queue()
        self.root = None
        self.running = False
        self.current_instruction_label = None
        self.history_frame = None
        self.instructions_history = []  # List to keep track of past instructions

    def _dashboard_loop(self):
        """Private method to create and run the GUI."""
        self.root = tk.Tk()
        self.root.title("Robot Controller Dashboard")
        
        # Set window size (not fullscreen)
        self.root.geometry("800x600")  # Width x Height

        # Create static elements
        tk.Label(self.root, text="Instruction Guide", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text="===========================", font=("Helvetica", 12)).pack()
        tk.Label(self.root, text="Task: RC-Assembly", font=("Helvetica", 12)).pack(pady=10)
        
        # Live date and time
        self.date_label = tk.Label(self.root, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}", font=("Helvetica", 10))
        self.date_label.pack()
        
        self.time_label = tk.Label(self.root, text=f"Time: {datetime.now().strftime('%H:%M:%S')}", font=("Helvetica", 10))
        self.time_label.pack()

        # Instruction History
        tk.Label(self.root, text="History:", font=("Helvetica", 12, "bold")).pack(pady=10)
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollable history
        history_canvas = tk.Canvas(self.history_frame)
        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=history_canvas.yview)
        self.history_content = tk.Frame(history_canvas)

        self.history_content.bind(
            "<Configure>",
            lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all")),
        )

        history_canvas.create_window((0, 0), window=self.history_content, anchor="n")
        history_canvas.configure(yscrollcommand=scrollbar.set)

        # Center history content
        history_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Current Instruction (centered)
        tk.Label(self.root, text="Current Instruction:", font=("Helvetica", 12, "bold")).pack(pady=10)
        self.current_instruction_label = tk.Label(self.root, text="No instructions yet.", font=("Helvetica", 16), fg="blue")
        self.current_instruction_label.pack(pady=20, expand=True)

        # Start update loops
        self._update_time()

        # Run the Tkinter main loop
        self.root.mainloop()

    def _update_time(self):
        """Update the date and time dynamically."""
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        self.date_label.config(text=f"Date: {current_date}")
        self.time_label.config(text=f"Time: {current_time}")
        
        # Schedule the next update
        self.root.after(1000, self._update_time)  # Update every second

    def _add_to_history(self, instruction):
        """Add the instruction to the history section."""
        label = tk.Label(
            self.history_content, text=instruction, font=("Helvetica", 10), fg="black", anchor="center"
        )
        label.pack(pady=2, padx=5)
        self.instructions_history.append(label)

    def pop_dashboard(self, message):
        """Update the dashboard with a new message."""
        if self.current_instruction_label:
            # Move the current instruction to the history
            current_text = self.current_instruction_label.cget("text")
            if current_text != "No instructions yet.":
                self._add_to_history(current_text)

            # Update the current instruction
            self.current_instruction_label.config(text=message, fg="blue", font=("Helvetica", 20))  # Larger font

    def start_dashboard(self):
        """Start the dashboard in a separate thread."""
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._dashboard_loop)
            thread.daemon = True  # Ensure it exits with the main program
            thread.start()

    def stop_dashboard(self):
        """Stop the dashboard by closing the GUI."""
        self.running = False
        if self.root:
            self.root.quit()


# Example Usage
if __name__ == "__main__":
    import time

    # Initialize the Dashboard instance
    dashboard = Dashboard()

    def robot_controller():
        """Simulated robot controller with dashboard updates."""
        instructions = [
            "Move to position A",
            "Pick up the object",
            "Move to position B",
            "Release the object",
            "Return to home position",
        ]
        for i, instruction in enumerate(instructions):
            print(f"Executing: {instruction}")
            dashboard.pop_dashboard(instruction)  # Send instruction to the dashboard
            time.sleep(3)  # Simulate some robot operation

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
