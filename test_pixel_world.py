import numpy as np

from vision.pixel_to_world import PixelToWorld


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


converter = PixelToWorld(K, R, T)


# Apple center from our webcam test
u = 921
v = 564


world = converter.convert(u, v)


print("Pixel:")
print("u =", u)
print("v =", v)

print("\nWorld Coordinate:")
print("X =", world[0])
print("Y =", world[1])
print("Z =", world[2])