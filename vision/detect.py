"""
detect.py

YOLO Object Detection Module

Detects fruits and returns
their center coordinates.

Author:
    Your Name
"""

import cv2
from ultralytics import YOLO


class FruitDetector:

    def __init__(self,
                 model_path="models/best.pt",
                 confidence=0.50):

        self.model = YOLO(model_path)

        self.confidence = confidence

    # -----------------------------------------

    def detect(self, frame):

        detections = []

        results = self.model.predict(

            source=frame,

            conf=self.confidence,

            verbose=False

        )

        for result in results:

            boxes = result.boxes

            for box in boxes:

                x1, y1, x2, y2 = box.xyxy[0]

                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)

                confidence = float(box.conf[0])

                class_id = int(box.cls[0])

                class_name = self.model.names[class_id]

                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                detections.append({

                    "class": class_name,

                    "confidence": confidence,

                    "bbox": (x1, y1, x2, y2),

                    "center": (center_x, center_y)

                })

        return detections

    # -----------------------------------------

    def draw(self, frame, detections):

        for obj in detections:

            x1, y1, x2, y2 = obj["bbox"]

            cx, cy = obj["center"]

            label = "{} {:.2f}".format(

                obj["class"],

                obj["confidence"]

            )

            cv2.rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                (0,255,0),

                2

            )

            cv2.circle(

                frame,

                (cx,cy),

                5,

                (0,0,255),

                -1

            )

            cv2.putText(

                frame,

                label,

                (x1,y1-10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (255,0,0),

                2

            )

        return frame


# ---------------------------------------------------

if __name__ == "__main__":

    detector = FruitDetector(

        model_path="models/best.pt",

        confidence=0.5

    )

    image = cv2.imread("test.jpg")

    detections = detector.detect(image)

    image = detector.draw(

        image,

        detections

    )

    cv2.imshow(

        "Detection",

        image

    )

    cv2.waitKey(0)

    cv2.destroyAllWindows()