import cv2
from vision.detect import FruitDetector

# Load your trained YOLO model
detector = FruitDetector(
    model_path="yolov8n.pt",
    confidence=0.5
)

# Open webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open webcam")
    exit()

print("Webcam started")
print("Put the apple in front of the camera")
print("Press Q to quit")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Could not read webcam")
        break

    # Run YOLO detection
    detections = detector.detect(frame)

    # Draw bounding boxes
    frame = detector.draw(frame, detections)

    # Print detections
    for obj in detections:

        print(
            "Detected:",
            obj["class"],
            "| Confidence:",
            round(obj["confidence"], 2),
            "| Center:",
            obj["center"]
        )

    # Show webcam
    cv2.imshow(
        "YOLO Webcam Test",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()