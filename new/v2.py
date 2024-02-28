import cv2
from cvzone.PoseModule import PoseDetector

detector = PoseDetector()
cap = cv2.VideoCapture(0)

i = 0
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmlist, bbox = detector.findPosition(img)

    i = i + 1 
    if i == 100:
       print(lmlist)
       break
    # Draw bounding box if it exists
    if bbox:
        # x, y, w, h = bbox
        # # Calculate center of bounding box
        # center_x = x + w // 2
        # center_y = y + h // 2
        # center = (center_x, center_y)
        # # Draw a circle at the center of the bounding box
        center = bbox["center"]
        # left = lmlist[11]
        cv2.circle(img, center, 5, (255, 0, 0), cv2.FILLED)
        print(center)

    cv2.imshow("MYresult", img)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
