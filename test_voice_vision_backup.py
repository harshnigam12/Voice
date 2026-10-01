import cv2

from vision.detect import FruitDetector
from voice.voice_listener import VoiceListener


# -------------------------------------------------
# YOLO
# -------------------------------------------------

detector = FruitDetector(
    model_path="yolov8n.pt",
    confidence=0.5
)


# -------------------------------------------------
# Webcam
# -------------------------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Could not open webcam")
    exit()


# -------------------------------------------------
# Voice
# -------------------------------------------------

voice = VoiceListener(
    model_path="models/vosk-model-small-en-us-0.15"
)

voice.start()

print("\n================================")
print(" Voice + Vision Test")
print("================================")
print("Say: get apple")
print("Say: get banana")
print("Say: get orange")
print("Press Q to quit\n")


# -------------------------------------------------
# Main Loop
# -------------------------------------------------

while True:

    ret, frame = camera.read()

    if not ret:

        print("Could not read webcam")
        break


    # ---------------------------------------------
    # YOLO detection
    # ---------------------------------------------

    detections = detector.detect(frame)

    frame = detector.draw(
        frame,
        detections
    )


    # ---------------------------------------------
    # Voice command
    # ---------------------------------------------

    command = voice.get_command()


    if command is not None:

        command = command.lower().strip()

        print("\nVoice Command:", command)


        # -----------------------------------------
        # Check "get fruit"
        # -----------------------------------------

        if command.startswith("get "):

            fruit = command.replace(
                "get ",
                "",
                1
            ).strip()


            # Find requested fruit
            matching = [

                d for d in detections

                if d["class"].lower() == fruit

            ]


            if len(matching) == 0:

                print(
                    "No",
                    fruit,
                    "detected"
                )

            else:

                # Highest-confidence requested fruit
                best = max(
                    matching,
                    key=lambda d: d["confidence"]
                )


                print(
                    "\nSELECTED FRUIT"
                )

                print(
                    "Fruit:",
                    best["class"]
                )

                print(
                    "Confidence:",
                    f"{best['confidence']:.2f}"
                )

                print(
                    "Center:",
                    best["center"]
                )

                print(
                    "Bounding Box:",
                    best["bbox"]
                )


    # ---------------------------------------------
    # Display
    # ---------------------------------------------

    cv2.imshow(
        "Voice + Vision",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# -------------------------------------------------
# Cleanup
# -------------------------------------------------

voice.stop()

camera.release()

cv2.destroyAllWindows()

print("\nTest Finished")