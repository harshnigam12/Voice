"""

Estimates camera pose using ArUco Marker.

Outputs:
1. Rotation Matrix (R)
2. Translation Vector (T)

"""

import cv2
import numpy as np


class PoseEstimator:

    def __init__(self,
                 camera_matrix,
                 distortion_coeffs,
                 marker_length=0.05):

        self.camera_matrix = camera_matrix
        self.dist_coeffs = distortion_coeffs
        self.marker_length = marker_length

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )

        self.parameters = cv2.aruco.DetectorParameters()

    # -------------------------------------------------

    def estimate(self, frame):

        corners, ids, _ = cv2.aruco.detectMarkers(

            frame,

            self.aruco_dict,

            parameters=self.parameters

        )

        if ids is None:

            return None, None

        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(

            corners,

            self.marker_length,

            self.camera_matrix,

            self.dist_coeffs

        )

        # First detected marker
        rvec = rvecs[0]
        tvec = tvecs[0]

        # Convert rotation vector → rotation matrix
        rotation_matrix, _ = cv2.Rodrigues(rvec)

        # Draw marker
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Draw coordinate axes
        cv2.drawFrameAxes(

            frame,

            self.camera_matrix,

            self.dist_coeffs,

            rvec,

            tvec,

            self.marker_length

        )

        return rotation_matrix, tvec

    # -------------------------------------------------

    def show_pose(self, frame):

        R, T = self.estimate(frame)

        if R is not None:

            print("\nRotation Matrix\n")

            print(R)

            print("\nTranslation Vector\n")

            print(T)

        return frame


# ---------------------------------------------------------

if __name__ == "__main__":

    fx = 729.54232691
    fy = 728.80795106

    cx = 340.95019522
    cy = 239.40823975

    K = np.array([

        [fx,0,cx],

        [0,fy,cy],

        [0,0,1]

    ])

    dist = np.zeros((5,1))

    estimator = PoseEstimator(

        K,

        dist,

        marker_length=0.05

    )

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        estimator.show_pose(frame)

        cv2.imshow(

            "Pose Estimation",

            frame

        )

        if cv2.waitKey(1) == 27:
            break

    cap.release()

    cv2.destroyAllWindows()