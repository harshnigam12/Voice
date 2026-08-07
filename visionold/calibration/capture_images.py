import cv2

cap = cv2.VideoCapture(1)
count = 0

while True:
    ret, frame = cap.read()
    cv2.imshow("Capture", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        cv2.imwrite(f"../../images/img{count}.jpg", frame)
        print("Saved:", count)
        count += 1

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()