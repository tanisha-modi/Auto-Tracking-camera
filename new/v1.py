import cv2
from cvzone.PoseModule import PoseDetector
detector = PoseDetector()
cap = cv2.VideoCapture(0)
while True : 
    success, img = cap.read()
    img = detector.findPose(img)
    lmlist, bbox = detector.findPosition(img)
    cv2.imshow("MYresult", img)
    cv2.waitKey(1)
