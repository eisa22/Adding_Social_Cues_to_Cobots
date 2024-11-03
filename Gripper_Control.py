import URBasic

class ControlGripper:
    def __init__(self, robot):
        """
        Initialize the gripper control with the given robot instance.
        The robot should be an instance of URBasic.urScriptExt.UrScriptExt.
        
        Parameters:
            robot (UrScriptExt): The robot instance to control.
        """
        self.robot = robot

    def open_gripper(self):
        """
        Opens the gripper by setting the appropriate digital output to False.
        Adjust the output channel based on your configuration.
        """
        # Assuming Digital Output 0 is used for gripper control
        self.robot.set_standard_digital_out(0, False)
        print("Gripper opened.")

    def close_gripper(self):
        """
        Closes the gripper by setting the appropriate digital output to True.
        Adjust the output channel based on your configuration.
        """
        # Assuming Digital Output 0 is used for gripper control
        self.robot.set_standard_digital_out(0, True)
        print("Gripper closed.")