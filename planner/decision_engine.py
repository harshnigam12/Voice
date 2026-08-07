"""
decision_engine.py

High-Level Decision Engine

Responsibilities
----------------
1. Robot Mode Management
2. Voice Command Processing
3. Automatic Picking
4. Manual Mode Support

Modes
-----
AUTO
VOICE
MANUAL
"""

class DecisionEngine:

    def __init__(self, planner):

        self.planner = planner

        # Default Mode
        self.mode = "AUTO"

    # ------------------------------------------------
    # Change Robot Mode
    # ------------------------------------------------

    def set_mode(self, mode):

        mode = mode.upper()

        if mode not in ["AUTO", "VOICE", "MANUAL"]:

            print("Invalid Mode")
            return

        if mode != self.mode:

            self.mode = mode

            print(f"\nRobot Mode Changed -> {self.mode}")

    # ------------------------------------------------
    # Process Voice Commands
    # ------------------------------------------------

    def process_voice(self, command, target):

        if command is None:
            return

        command = command.lower().strip()

        print(f"\nVoice Command Received : {command}")

        # -----------------------------
        # Mode Switching
        # -----------------------------

        if command == "automatic mode":

            self.set_mode("AUTO")
            return

        elif command == "voice mode":

            self.set_mode("VOICE")
            return

        elif command == "manual mode":

            self.set_mode("MANUAL")
            return

        # -----------------------------
        # Commands only in Voice Mode
        # -----------------------------

        if self.mode != "VOICE":

            return

        if command == "pick fruit":

            if target is None:

                print("No Fruit Detected")
                return

            self.planner.execute(target)

        elif command == "home":

            self.planner.go_home()

        elif command == "place":

            self.planner.place()

        elif command == "stop":

            print("Emergency Stop Requested")

            # Future:
            # self.planner.stop()

        elif command == "release":

            print("Release Command")

            # Future:
            # self.planner.release()

        else:

            print("Unknown Command")

    # ------------------------------------------------
    # Automatic Mode
    # ------------------------------------------------

    def automatic(self, target):

        if self.mode != "AUTO":

            return

        if target is None:

            return

        print("\nAUTO : Fruit Detected")

        self.planner.execute(target)

    # ------------------------------------------------
    # Manual Mode
    # ------------------------------------------------

    def manual(self):

        if self.mode != "MANUAL":

            return

        print("\nManual Mode Active")

        # Joystick Control
        # Future Implementation

    # ------------------------------------------------
    # Main Decision Function
    # ------------------------------------------------

    def run(

        self,

        target=None,

        voice_command=None

    ):

        # Voice commands are always checked
        self.process_voice(

            voice_command,

            target

        )

        # Current mode decides behaviour
        if self.mode == "AUTO":

            self.automatic(target)

        elif self.mode == "MANUAL":

            self.manual()


# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    print("Decision Engine Ready")