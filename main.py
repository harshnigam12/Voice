"""
main.py

Intelligent Robotic Arm

System Flow

Camera
    ↓
YOLO Detection
    ↓
Voice-selected Fruit
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
    # Selected Fruit
    # -------------------------------------------------

    requested_fruit = None

    # -------------------------------------------------
    # Main Loop
    # -------------------------------------------------

    while True:

        frame = camera.read()

        if frame is None:
            continue

        # ---------------------------------------------
        # Get Voice Command
        # ---------------------------------------------

        command = voice.get_command()

        if command:

            print(
                f"\nReceived Command: {command}"
            )

            if command.startswith("get "):

                requested_fruit = command.replace(
                    "get ",
                    "",
                    1
                ).strip()

                print(
                    f"Requested Fruit: {requested_fruit}"
                )

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

            # -----------------------------------------
            # Find Requested Fruit
            # -----------------------------------------

            if requested_fruit is not None:

                matching_detections = [

                    d for d in detections

                    if d["class"].lower()
                    == requested_fruit.lower()

                ]

                if len(matching_detections) > 0:

                    # If multiple requested fruits are
                    # visible, choose the highest confidence.

                    best = max(
                        matching_detections,
                        key=lambda d: d["confidence"]
                    )

                    u, v = best["center"]

                    x, y, z = converter.convert(
                        u,
                        v
                    )

                    target = (x, y, z)

                    print(
                        f"\nRequested Fruit = "
                        f"{requested_fruit}"
                    )

                    print(
                        f"Detected = {best['class']}"
                    )

                    print(
                        f"Confidence = "
                        f"{best['confidence']:.2f}"
                    )

                    print(
                        f"World = "
                        f"({x:.1f}, "
                        f"{y:.1f}, "
                        f"{z:.1f})"
                    )

                else:

                    print(
                        f"\nWaiting for "
                        f"{requested_fruit}..."
                    )

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