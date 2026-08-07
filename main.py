"""
main.py

Intelligent Robotic Arm

System Flow

Camera
    ↓
YOLO Detection
    ↓
Highest Confidence Fruit
    ↓
Pixel -> World
    ↓
Decision Engine
    ↓
Task Planner
    ↓
Inverse Kinematics
    ↓
Servo Mapper
    ↓
Trajectory Planner
    ↓
Arduino
"""

import time
import numpy as np

from config.robot import (
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    HANDOVER_POSITION,
    SERIAL_PORT,
    BAUDRATE
)

from vision.webcam_detection import WebcamDetection
from vision.detect import FruitDetector
from vision.pose_estimation import PoseEstimator
from vision.pixel_to_world import PixelToWorld

from robotics.inverse_kinematics import InverseKinematics
from robotics.servo_mapper import ServoMapper
from robotics.trajectory import TrajectoryPlanner

from communication.serial_controller import SerialController

from planner.task_planner import TaskPlanner
from planner.decision_engine import DecisionEngine

from voice.voice_listener import VoiceListener


def main():

    print("=" * 60)
    print(" Intelligent Robotic Arm Started ")
    print("=" * 60)

    # -------------------------------------------------
    # Camera
    # -------------------------------------------------

    camera = WebcamDetection()

    camera.open()

    # -------------------------------------------------
    # Fruit Detector
    # -------------------------------------------------

    detector = FruitDetector(

        model_path=MODEL_PATH,

        confidence=CONFIDENCE_THRESHOLD

    )

    # -------------------------------------------------
    # Camera Parameters
    # (Replace with your calibration values)
    # -------------------------------------------------

    K = np.array([
        [729.54232691, 0, 340.95019522],
        [0, 728.80795106, 239.40823975],
        [0, 0, 1]
    ])

    distortion = np.zeros((5, 1))

    pose = PoseEstimator(

        K,

        distortion,

        marker_length=0.05

    )

    # -------------------------------------------------
    # Robot
    # -------------------------------------------------

    ik = InverseKinematics()

    mapper = ServoMapper()

    serial = SerialController(

        port=SERIAL_PORT,

        baudrate=BAUDRATE

    )

    if not serial.connect():

        print("Arduino Connection Failed")

        return

    trajectory = TrajectoryPlanner(serial)

    planner = TaskPlanner(

        detector,

        ik,

        mapper,

        trajectory,

        HANDOVER_POSITION

    )

    decision = DecisionEngine(planner)

    # -------------------------------------------------
    # Voice Listener
    # -------------------------------------------------

    voice = VoiceListener(

        model_path="vosk-model-small-en-us-0.15"

    )

    voice.start()

    print("\nRobot Ready\n")

    # -------------------------------------------------
    # Main Loop
    # -------------------------------------------------

    while True:

        frame = camera.read()

        if frame is None:

            continue

        # ---------------------------------------------
        # Estimate Camera Pose
        # ---------------------------------------------

        R, T = pose.estimate(frame)

        target = None

        if R is not None:

            converter = PixelToWorld(

                K,

                R,

                T

            )

            detections = detector.detect(frame)

            frame = detector.draw(

                frame,

                detections

            )

            if len(detections) > 0:

                # Highest confidence fruit

                best = max(

                    detections,

                    key=lambda d: d["confidence"]

                )

                u, v = best["center"]

                x, y, z = converter.convert(

                    u,

                    v

                )

                target = (x, y, z)

                print(

                    f"\nTarget = {best['class']}"

                )

                print(

                    f"Confidence = {best['confidence']:.2f}"

                )

                print(

                    f"World = ({x:.1f}, {y:.1f}, {z:.1f})"

                )

        # ---------------------------------------------
        # Voice Command
        # ---------------------------------------------

        command = voice.get_command()

        # ---------------------------------------------
        # Decision Engine
        # ---------------------------------------------

        decision.run(

            target=target,

            voice_command=command

        )

        # ---------------------------------------------
        # Display
        # ---------------------------------------------

        camera.show(

            "Robot Camera",

            frame

        )

        if camera.wait() == ord('q'):

            break

    # -------------------------------------------------
    # Cleanup
    # -------------------------------------------------

    voice.stop()

    camera.release()

    serial.disconnect()

    print("\nRobot Closed")


if __name__ == "__main__":

    main()