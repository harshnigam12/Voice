"""

Main Vision Pipeline

Camera
   ↓
YOLO Detection
   ↓
Pose Estimation
   ↓
Pixel to World Conversion

"""

import cv2
import numpy as np

from config.camera import Camera
from vision.detect import FruitDetector
from vision.pose_estimation import PoseEstimator
from vision.pixel_to_world import PixelToWorld


class WebcamDetection:

    def __init__(self):

        # -------------------------
        # Camera Calibration
        # Replace with your values
        # -------------------------

        self.camera_matrix = np.array([

            [729.54232691,0,340.95019522],

            [0,728.80795106,239.40823975],

            [0,0,1]

        ])

        self.distortion = np.array(

            [[-0.42,0.23,0,0,-0.07]]

        )

        # -------------------------

        self.camera = Camera()

        self.detector = FruitDetector(

            model_path="models/best.pt",

            confidence=0.50

        )

        self.pose = PoseEstimator(

            self.camera_matrix,

            self.distortion,

            marker_length=0.05

        )

        self.converter = None

    # ----------------------------------------------------

    def start(self):

        self.camera.open()

        while True:

            frame = self.camera.read()

            if frame is None:

                break

            # --------------------------
            # Camera Pose
            # --------------------------

            R, T = self.pose.estimate(frame)

            if R is not None:

                self.converter = PixelToWorld(

                    self.camera_matrix,

                    R,

                    T

                )

            # --------------------------
            # YOLO Detection
            # --------------------------

            detections = self.detector.detect(frame)

            frame = self.detector.draw(

                frame,

                detections

            )

            # --------------------------
            # Convert Pixel → World
            # --------------------------

            if self.converter is not None:

                for obj in detections:

                    cx, cy = obj["center"]

                    X, Y, Z = self.converter.convert(

                        cx,

                        cy

                    )

                    print(

                        f"{obj['class']}"

                        f"  Pixel=({cx},{cy})"

                        f"  World=({X:.1f},{Y:.1f},{Z:.1f})"

                    )

                    cv2.putText(

                        frame,

                        f"({X:.1f},{Y:.1f})",

                        (cx+10,cy),

                        cv2.FONT_HERSHEY_SIMPLEX,

                        0.5,

                        (0,255,255),

                        2

                    )

            # --------------------------

            cv2.imshow(

                "Vision System",

                frame

            )

            key = cv2.waitKey(1)

            if key == ord('q'):

                break

        self.camera.release()

    # ----------------------------------------------------

    def get_target(self):

        """
        Returns first detected fruit.

        Used by main.py
        """

        frame = self.camera.read()

        detections = self.detector.detect(frame)

        if len(detections) == 0:

            return None

        obj = detections[0]

        cx, cy = obj["center"]

        X, Y, Z = self.converter.convert(

            cx,

            cy

        )

        return {

            "class": obj["class"],

            "world": (X,Y,Z)

        }


# -------------------------------------------------------

if __name__ == "__main__":

    system = WebcamDetection()

    system.start()