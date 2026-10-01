from vision.pixel_to_world import PixelToWorld
from robotics.inverse_kinematics import InverseKinematics

print("FULL PIPELINE TEST")
print("==================")

# Apple center from our YOLO webcam test
u = 921
v = 564

print("\nApple pixel:")
print("u =", u)
print("v =", v)
import numpy as np

# Camera calibration
K = np.array([
    [729.54232691, 0, 340.95019522],
    [0, 728.80795106, 239.40823975],
    [0, 0, 1]
])

R = np.array([
    [5.55055848e-04, 9.99696883e-01, 2.46137102e-02],
    [8.10554094e-01, 1.39655899e-02, -5.85497244e-01],
    [-5.85663515e-01, 2.02757272e-02, -8.10300650e-01]
])

T = np.array([
    [0.09251071],
    [-0.0079242],
    [0.35281046]
])

# Convert pixel → world
converter = PixelToWorld(K, R, T)

world = converter.convert(u, v)

print("\nWorld coordinates:")
print("X =", world[0])
print("Y =", world[1])
print("Z =", world[2])
# Convert metres → millimetres
x_mm = world[0] * 1000
y_mm = world[1] * 1000
z_mm = world[2] * 1000

print("\nWorld coordinates in mm:")
print("X =", x_mm)
print("Y =", y_mm)
print("Z =", z_mm)
# Inverse Kinematics
ik = InverseKinematics()

angles = ik.solve(
    x_mm,
    y_mm,
    z_mm
)

print("\nJoint angles:")

if angles is None:

    print("IK FAILED")

else:

    print("Base     =", angles["base"])
    print("Shoulder =", angles["shoulder"])
    print("Elbow    =", angles["elbow"])
    print("Wrist    =", angles["wrist"])