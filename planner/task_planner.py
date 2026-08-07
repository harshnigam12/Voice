"""
High level robot task planner.

Workflow:
HOME -> PICK FRUIT -> HANDOVER POSITION -> HOME
"""

class TaskPlanner:

    def __init__(
        self,
        detector,
        ik,
        mapper,
        trajectory,
        handover_position
    ):

        self.detector = detector
        self.ik = ik
        self.mapper = mapper
        self.trajectory = trajectory
        self.handover_position = handover_position

    # ------------------------------------------
    # HOME
    # ------------------------------------------

    def go_home(self):

        print("\nGoing Home")

        self.trajectory.return_home()

    # ------------------------------------------
    # PICK
    # ------------------------------------------

    def pick(self, target):

        print("\nPicking Fruit")

        # Convert XYZ -> Joint Angles
        angles = self.ik.solve(
            target[0],
            target[1],
            target[2]
        )

        if angles is None:

            print("IK Failed")
            return False

        # Convert Joint Angles -> Servo Angles
        servo_angles = self.mapper.map_angles(angles)

        # Create target pose
        fruit_pose = {
            "base": servo_angles["base"],
            "shoulder": servo_angles["shoulder"],
            "elbow": servo_angles["elbow"],
            "wrist": servo_angles["wrist"],
            "gripper": 20
        }

        # Smooth movement to fruit
        self.trajectory.move_to_fruit(fruit_pose)

        # Close gripper
        print("Closing Gripper")

        fruit_pose["gripper"] = 70

        self.trajectory.execute(fruit_pose)

        return True

    # ------------------------------------------
    # PLACE
    # ------------------------------------------

    def place(self):

        print("\nMoving To Handover Position")

        # Handover Position XYZ -> Joint Angles
        angles = self.ik.solve(
            self.handover_position[0],
            self.handover_position[1],
            self.handover_position[2]
        )

        if angles is None:

            print("IK Failed")
            return

        # Joint -> Servo
        servo_angles = self.mapper.map_angles(angles)

        handover_pose = {
            "base": servo_angles["base"],
            "shoulder": servo_angles["shoulder"],
            "elbow": servo_angles["elbow"],
            "wrist": servo_angles["wrist"],
            "gripper": 70
        }

        # Move smoothly to handover position
        self.trajectory.move_to_user(handover_pose)

        # Open gripper
        print("Opening Gripper")

        handover_pose["gripper"] = 20

        self.trajectory.execute(handover_pose)

    # ------------------------------------------
    # COMPLETE TASK
    # ------------------------------------------

    def execute(self, target):

        self.go_home()

        success = self.pick(target)

        if success:

            self.place()

        self.go_home()

        print("\nTask Finished")