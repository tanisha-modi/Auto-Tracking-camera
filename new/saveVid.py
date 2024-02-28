import cv2
from cvzone.PoseModule import PoseDetector

detector = PoseDetector()
video_path = "d:/code/internship/new/vid.mp4"  # Specify the path to your video file
cap = cv2.VideoCapture(video_path)

while True:
    success, img = cap.read()
    if not success:
        break
    
    img = detector.findPose(img)
    lmlist, bbox = detector.findPosition(img)

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
