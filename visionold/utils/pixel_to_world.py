import numpy as np

def pixel_to_world(camera_intrinsics, r, t, img_points):

    K_inv = camera_intrinsics.I
    R_inv = np.asmatrix(r).I
    R_inv_T = np.dot(R_inv, np.asmatrix(t))

    world_points = []
    coords = np.zeros((3, 1), dtype=np.float64)

    for img_point in img_points:
        coords[0] = img_point[0]
        coords[1] = img_point[1]
        coords[2] = 1.0

        cam_point = np.dot(K_inv, coords)
        cam_R_inv = np.dot(R_inv, cam_point)

        scale = R_inv_T[2][0] / cam_R_inv[2][0]
        scale_world = np.multiply(scale, cam_R_inv)

        world_point = np.asmatrix(scale_world) - np.asmatrix(R_inv_T)

        pt = np.zeros((3, 1), dtype=np.float64)
        pt[0] = world_point[0]
        pt[1] = world_point[1]
        pt[2] = 0

        world_points.append(pt.T.tolist())

    return world_points