import cv2
import numpy as np
import glob

# ======================================================
# Camera Calibration using Chessboard Images
# ======================================================

# Number of INNER corners
CHESSBOARD_SIZE = (7, 6)

# Size of one square (mm)
# Doesn't affect camera matrix if only intrinsics are needed.
SQUARE_SIZE = 25

# Folder containing calibration images
IMAGE_PATH = "images/*.jpg"


def calibrate_camera():

    # Prepare object points
    objp = np.zeros(
        (CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3),
        np.float32
    )

    objp[:, :2] = np.mgrid[
        0:CHESSBOARD_SIZE[0],
        0:CHESSBOARD_SIZE[1]
    ].T.reshape(-1, 2)

    objp *= SQUARE_SIZE

    object_points = []
    image_points = []

    images = glob.glob(IMAGE_PATH)

    if len(images) == 0:
        print("No calibration images found.")
        return

    print(f"Found {len(images)} images\n")

    criteria = (
        cv2.TERM_CRITERIA_EPS +
        cv2.TERM_CRITERIA_MAX_ITER,
        30,
        0.001
    )

    image_size = None

    for image_name in images:

        image = cv2.imread(image_name)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        image_size = gray.shape[::-1]

        found, corners = cv2.findChessboardCorners(
            gray,
            CHESSBOARD_SIZE,
            None
        )

        if found:

            refined_corners = cv2.cornerSubPix(
                gray,
                corners,
                (11, 11),
                (-1, -1),
                criteria
            )

            object_points.append(objp)
            image_points.append(refined_corners)

            cv2.drawChessboardCorners(
                image,
                CHESSBOARD_SIZE,
                refined_corners,
                found
            )

            cv2.imshow(
                "Chessboard Detection",
                image
            )

            cv2.waitKey(300)

            print(f"{image_name}  ✓")

        else:

            print(f"{image_name}  ✗ Chessboard Not Found")

    cv2.destroyAllWindows()

    if len(object_points) == 0:

        print("\nCalibration failed!")

        return

    print("\nCalculating camera parameters...\n")

    ret, camera_matrix, distortion, rvecs, tvecs = cv2.calibrateCamera(

        object_points,

        image_points,

        image_size,

        None,

        None

    )

    print("=====================================")
    print("Calibration Successful")
    print("=====================================\n")

    print("Camera Matrix:\n")
    print(camera_matrix)

    print("\nDistortion Coefficients:\n")
    print(distortion)

    print("\nRotation Vectors:")
    print(len(rvecs))

    print("\nTranslation Vectors:")
    print(len(tvecs))

    return camera_matrix, distortion


# ======================================================

if __name__ == "__main__":

    calibrate_camera()