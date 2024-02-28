import cv2
from cvzone.PoseModule import PoseDetector

detector = PoseDetector()
cap = cv2.VideoCapture(0)

# video_path = 'vid.mp4'

# Create a VideoCapture object
# cap = cv2.VideoCapture(video_path)

i = 0
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmlist, bbox = detector.findPosition(img)

    i = i + 1 
    if i == 10000:
       print(lmlist)
       break
    # Draw bounding box if it exists
    if bbox:
        center_bbox = bbox["center"]
        frame_height, frame_width, _ = img.shape
        center_frame = (frame_width // 2, frame_height // 2)  # Center of the frame
        
        # Calculate the displacement of the bounding box center from the frame center
        displacement_x = center_bbox[0] - center_frame[0]
        displacement_y = center_bbox[1] - center_frame[1]
        
        print("Displacement from center of frame (x, y):", (displacement_x, displacement_y))
        
        cv2.circle(img, center_frame, 5, (0, 255, 0), cv2.FILLED)  # Draw center of frame
        cv2.circle(img, center_bbox, 5, (255, 0, 0), cv2.FILLED)  # Draw center of bounding box 
        
    cv2.imshow("MYresult", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
