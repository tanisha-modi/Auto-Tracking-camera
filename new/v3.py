import cv2
from cvzone.PoseModule import PoseDetector

detector = PoseDetector()
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmlist, bbox = detector.findPosition(img)

    if lmlist:
        # Extract shoulder coordinates

        left_shoulder = lmlist[5]  # Left shoulder coordinates
        right_shoulder = lmlist[6]  # Right shoulder coordinates
        print("Left Shoulder Coordinates:", left_shoulder)
        print("Right Shoulder Coordinates:", right_shoulder)

    cv2.imshow("MYresult", img)
    if cv2.waitKey(1000) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
