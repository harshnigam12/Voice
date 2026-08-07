"""

Converts IK joint angles into servo angles.

"""
from inverse_kinematics import InverseKinematics


from config.robot import (
    SERVO_OFFSETS,
    SERVO_LIMITS
)


class ServoMapper:

    def __init__(self):

        self.offsets = SERVO_OFFSETS

        self.limits = SERVO_LIMITS

    def clamp(self, angle, minimum, maximum):

        return max(
            minimum,
            min(
                maximum,
                angle
            )
        )

    def map_angles(self, joint_angles):

        if joint_angles is None:

            return None

        base = (
            joint_angles["base"]
            +
            self.offsets["base"]
        )

        shoulder = (
            joint_angles["shoulder"]
            +
            self.offsets["shoulder"]
        )

        elbow = (
            joint_angles["elbow"]
            +
            self.offsets["elbow"]
        )

        wrist = (
            joint_angles["wrist"]
            +
            self.offsets["wrist"]
        )

        base = self.clamp(
            base,
            *self.limits["base"]
        )

        shoulder = self.clamp(
            shoulder,
            *self.limits["shoulder"]
        )

        elbow = self.clamp(
            elbow,
            *self.limits["elbow"]
        )

        wrist = self.clamp(
            wrist,
            *self.limits["wrist"]
        )

        return {

            "base": int(base),

            "shoulder": int(shoulder),

            "elbow": int(elbow),

            "wrist": int(wrist)

        }


if __name__ == "__main__":

    ik = InverseKinematics()

    # Create Servo Mapper object
    mapper = ServoMapper()

    # Target position (X, Y, Z) in mm
    x = 220
    y = 150
    z = 50

    # Step 1: Calculate joint angles using Inverse Kinematics
    joint_angles = ik.solve(x, y, z)

    print("Inverse Kinematics Output:")
    print(joint_angles)

    # Step 2: Convert joint angles into safe servo angles
    servo_angles = mapper.map_angles(joint_angles)

    print("\nServo Angles:")
    print(servo_angles)