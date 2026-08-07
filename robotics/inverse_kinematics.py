"""

Converts world coordinates (X,Y,Z) into robot joint angles.

Input:
    X, Y, Z (mm)

Output:
    Base
    Shoulder
    Elbow
    Wrist

"""

import math

from config.robot import (
    BASE_HEIGHT,
    UPPER_ARM,
    FOREARM,
    WRIST
)


class InverseKinematics:

    def __init__(self):

        self.L1 = BASE_HEIGHT
        self.L2 = UPPER_ARM
        self.L3 = FOREARM
        self.L4 = WRIST

    def solve(self, x, y, z):
      
        try:

            # -----------------------------------------
            # Base Rotation
            # -----------------------------------------

            theta1 = math.degrees(
                math.atan2(y, x)
            )

            # -----------------------------------------
            # Horizontal Distance
            # -----------------------------------------

            r = math.sqrt(x ** 2 + y ** 2)

            # -----------------------------------------
            # Vertical Distance
            # -----------------------------------------

            z = z - self.L1

            # -----------------------------------------
            # Wrist Compensation
            # -----------------------------------------

            wrist_angle = 0

            r = r - self.L4 * math.cos(
                math.radians(wrist_angle)
            )

            z = z - self.L4 * math.sin(
                math.radians(wrist_angle)
            )

            # -----------------------------------------
            # Shoulder to Target Distance
            # -----------------------------------------

            d = math.sqrt(
                r ** 2 +
                z ** 2
            )

            # -----------------------------------------
            # Workspace Check
            # -----------------------------------------

            if d > (self.L2 + self.L3):

                raise ValueError(
                    "Target is outside robot workspace."
                )

            # -----------------------------------------
            # Elbow Angle
            # -----------------------------------------

            cos_theta3 = (

                self.L2 ** 2 +
                self.L3 ** 2 -
                d ** 2

            ) / (

                2 *
                self.L2 *
                self.L3

            )

            cos_theta3 = max(
                -1,
                min(
                    1,
                    cos_theta3
                )
            )

            theta3 = math.degrees(
                math.acos(
                    cos_theta3
                )
            )

            # -----------------------------------------
            # Shoulder Angle
            # -----------------------------------------

            alpha = math.atan2(
                z,
                r
            )

            cos_beta = (

                self.L2 ** 2 +
                d ** 2 -
                self.L3 ** 2

            ) / (

                2 *
                self.L2 *
                d

            )

            cos_beta = max(
                -1,
                min(
                    1,
                    cos_beta
                )
            )

            beta = math.acos(
                cos_beta
            )

            theta2 = math.degrees(
                alpha + beta
            )

            # -----------------------------------------
            # Wrist Angle
            # -----------------------------------------

            theta4 = -(

                theta2 +
                theta3

            )

            # -----------------------------------------
            # Return
            # -----------------------------------------

            return {

                "base": theta1,

                "shoulder": theta2,

                "elbow": theta3,

                "wrist": theta4

            }

        except Exception as e:

            print(
                "IK Error:",
                e
            )

            return None


if __name__ == "__main__":

    ik = InverseKinematics()

    target = ik.solve(

        x=220,

        y=150,

        z=50

    )

    print(target)