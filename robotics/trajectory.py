"""
trajectory.py

Trajectory Planning for 5-DOF Robotic Arm

Workflow:
HOME -> FRUIT -> HANDOVER -> HOME
"""

import time


class TrajectoryPlanner:

    def __init__(self, serial_controller):

        self.serial = serial_controller

        self.step = 2
        self.delay = 0.02

        self.home = {
            "base": 90,
            "shoulder": 90,
            "elbow": 90,
            "wrist": 90,
            "gripper": 20
        }

        self.current = self.home.copy()

    # -------------------------------------------------

    def interpolate(self, start, end):

        trajectory = []

        if start < end:

            while start <= end:
                trajectory.append(start)
                start += self.step

        else:

            while start >= end:
                trajectory.append(start)
                start -= self.step

        if trajectory[-1] != end:
            trajectory.append(end)

        return trajectory

    # -------------------------------------------------

    def generate(self, target):

        base = self.interpolate(
            self.current["base"],
            target["base"]
        )

        shoulder = self.interpolate(
            self.current["shoulder"],
            target["shoulder"]
        )

        elbow = self.interpolate(
            self.current["elbow"],
            target["elbow"]
        )

        wrist = self.interpolate(
            self.current["wrist"],
            target["wrist"]
        )

        gripper = self.interpolate(
            self.current["gripper"],
            target["gripper"]
        )

        max_len = max(
            len(base),
            len(shoulder),
            len(elbow),
            len(wrist),
            len(gripper)
        )

        def extend(arr):

            while len(arr) < max_len:
                arr.append(arr[-1])

            return arr

        base = extend(base)
        shoulder = extend(shoulder)
        elbow = extend(elbow)
        wrist = extend(wrist)
        gripper = extend(gripper)

        path = []

        for i in range(max_len):

            path.append({

                "base": base[i],

                "shoulder": shoulder[i],

                "elbow": elbow[i],

                "wrist": wrist[i],

                "gripper": gripper[i]

            })

        return path

    # -------------------------------------------------

    def execute(self, target):

        trajectory = self.generate(target)

        for point in trajectory:

            self.serial.send_angles(

                point["base"],
                point["shoulder"],
                point["elbow"],
                point["wrist"],
                point["gripper"]

            )

            time.sleep(self.delay)

        self.current = target.copy()

    # -------------------------------------------------

    def move_to_fruit(self, fruit_angles):

        print("Moving to fruit...")

        self.execute(fruit_angles)

    # -------------------------------------------------

    def move_to_user(self, handover_angles):

        print("Moving to user...")

        self.execute(handover_angles)

    # -------------------------------------------------

    def return_home(self):

        print("Returning Home...")

        self.execute(self.home)

        self.current = self.home.copy()

    # -------------------------------------------------

    def pick_and_place(self,
                       fruit_angles,
                       handover_angles):

        # HOME -> FRUIT
        self.move_to_fruit(fruit_angles)

        print("Close Gripper")

        time.sleep(1)

        # FRUIT -> USER
        self.move_to_user(handover_angles)

        print("Open Gripper")

        time.sleep(1)

        # USER -> HOME
        self.return_home()