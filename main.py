import cv2
import numpy as np
from ultralytics import YOLO
from vision.utils.pixel_to_world import pixel_to_world

# 🔴 Replace with YOUR values
fx, fy = 729.54232691 ,728.80795106
cx, cy = 340.95019522 ,239.40823975

# ✅ Rotation matrix
R = np.array([
    [ 5.55055848e-04,  9.99696883e-01,  2.46137102e-02],
    [ 8.10554094e-01,  1.39655899e-02, -5.85497244e-01],
    [-5.85663515e-01,  2.02757272e-02, -8.10300650e-01]
])

# ✅ Translation vector
T = np.array([
    [ 0.09251071],
    [-0.0079242 ],
    [ 0.35281046]
])
K = np.mat([[fx,0,cx],
            [0,fy,cy],
            [0,0,1]])

model = YOLO("models/best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    results = model(frame)

    for r in results:
        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = box

            u = (x1 + x2) / 2
            v = (y1 + y2) / 2

            img_points = np.array([[u, v]], dtype=np.double)

            world = pixel_to_world(K, R, T, img_points)

            print("World Coordinate:", world)

            cv2.circle(frame, (int(u), int(v)), 5, (0,255,0), -1)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()