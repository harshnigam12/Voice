"""

Camera configuration and webcam handler.

"""

import cv2


class Camera:

    def __init__(self,
                 camera_index=1,
                 width=640,
                 height=480):

        self.camera_index = camera_index
        self.width = width
        self.height = height

        self.cap = None

    # ---------------------------------
    # Open Camera
    # ---------------------------------

    def open(self):

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():

            raise Exception(
                f"Cannot open camera {self.camera_index}"
            )

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,
                     self.width)

        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,
                     self.height)

        print("Camera Opened")

    # ---------------------------------
    # Read Frame
    # ---------------------------------

    def read(self):

        if self.cap is None:

            raise Exception(
                "Camera not initialized."
            )

        ret, frame = self.cap.read()

        if not ret:

            return None

        return frame

    # ---------------------------------
    # Release Camera
    # ---------------------------------

    def release(self):

        if self.cap:

            self.cap.release()

            cv2.destroyAllWindows()

            print("Camera Released")

    # ---------------------------------
    # Display Frame
    # ---------------------------------

    def show(self,
             window_name,
             frame):

        cv2.imshow(window_name, frame)

    # ---------------------------------
    # Wait Key
    # ---------------------------------

    def wait(self):

        return cv2.waitKey(1) & 0xFF


# -------------------------------------
# Testing
# -------------------------------------

if __name__ == "__main__":

    camera = Camera(

        camera_index=1,

        width=640,

        height=480

    )

    camera.open()

    while True:

        frame = camera.read()

        if frame is None:

            break

        camera.show(

            "Camera",

            frame

        )

        if camera.wait() == ord('q'):

            break

    camera.release()