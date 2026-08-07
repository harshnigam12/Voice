import cv2
import numpy as np

# 🔴 Replace these with YOUR calibration values
fx, fy = 729.54232691 ,728.80795106
cx, cy = 340.95019522 ,239.40823975

camera_matrix = np.array([[fx,0,cx],
                          [0,fy,cy],
                          [0,0,1]])
dist_coeffs = np.zeros((5,1))

cap = cv2.VideoCapture(1)

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

while True:
    ret, frame = cap.read()

    corners, ids, _ = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    if ids is not None:
        marker_length = 0.05  # meters

        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, dist_coeffs)

        R, _ = cv2.Rodrigues(rvec[0])
        T = tvec[0].T

        print("R:\n", R)
        print("T:\n", T)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()