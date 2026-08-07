"""

Converts image pixel coordinates into
robot world coordinates.

Uses:
- Camera Intrinsic Matrix (K)
- Rotation Matrix (R)
- Translation Vector (T)


"""

import numpy as np


class PixelToWorld:

    def __init__(self,
                 camera_matrix,
                 rotation_matrix,
                 translation_vector):

        self.K = np.asarray(camera_matrix, dtype=np.float64)

        self.R = np.asarray(rotation_matrix, dtype=np.float64)

        self.T = np.asarray(translation_vector,
                            dtype=np.float64).reshape(3, 1)

        self.K_inv = np.linalg.inv(self.K)

        self.R_inv = np.linalg.inv(self.R)

    # --------------------------------------------------
    # Convert one pixel to world coordinate
    # --------------------------------------------------

    def convert(self, u, v):

        pixel = np.array([[u],
                          [v],
                          [1.0]])

        camera_point = self.K_inv @ pixel

        camera_point = self.R_inv @ camera_point

        scale = self.T[2][0] / camera_point[2][0]

        world = scale * camera_point

        world = world - (self.R_inv @ self.T)

        return (

            float(world[0]),

            float(world[1]),

            0.0

        )

    # --------------------------------------------------
    # Convert multiple points
    # --------------------------------------------------

    def convert_points(self, points):

        result = []

        for (u, v) in points:

            result.append(

                self.convert(u, v)

            )

        return result


# ------------------------------------------------------
# Example
# ------------------------------------------------------

if __name__ == "__main__":

    fx = 729.54232691
    fy = 728.80795106

    cx = 340.95019522
    cy = 239.40823975

    K = np.array([

        [fx, 0, cx],

        [0, fy, cy],

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

    converter = PixelToWorld(

        K,

        R,

        T

    )

    world = converter.convert(

        320,

        250

    )

    print(world)