
# imports 
import cv2
from cvzone.PoseModule import PoseDetector
detector = PoseDetector()


# Create a VideoCapture object
cap = cv2.VideoCapture(0)


# If we use already saved video
# video_path = 'vid.mp4'
# cap = cv2.VideoCapture(video_path)


# created this variable to break/terminate after a few loops 
i = 0 


while True:
    success, img = cap.read()
    img = detector.findPose(img)

    # findPosition return 2 things :
    # 1. a list containing the coordinates of key points on the human body
    # 2. bounding box containing 4 coordinates -> (x,y) coordinates of top-left corner, w - width, h - height
    lmlist, bbox = detector.findPosition(img)



    if lmlist :
        angle1, img = detector.findAngle(lmlist[11][0:2], lmlist[13][0:2], lmlist[15][0:2], img)


    # to terminate the loop
    i = i + 1 
    if i == 10000:
    #    print(lmlist) 
       break



    # Draw bounding box if it exists
    if bbox:
        # bbox further contains 2 things -> center points, bbox of 4 coordinates
        coor = bbox["bbox"]
        x, y, w, h = coor
        center_bbox = (x + w // 2, y + h // 2)  # Center of the bounding box
        # center_bbox = (x, y)  
        




        # frame parameters
        frame_height, frame_width, _ = img.shape
        center_frame = (frame_width // 2, frame_height // 2)  # Center of the frame




        
        # Calculate the adjusted center of the bounding box in case the bounding box going beyond the edge of frame
        if x < 0 and x + w > frame_width:
            center_bbox = (frame_width // 2, center_bbox[1])
        elif x < 0:
            center_bbox = ((x + w) // 2, center_bbox[1])  
            print("x < 0")
        elif x + w > frame_width:
            center_bbox = (x + ((frame_width - x)// 2), center_bbox[1])
            print("x + w > 0")
        if y < 0 and y + h > frame_height:
            center_bbox = (center_bbox[0], frame_height//2)
        elif y < 0:
            center_bbox = (center_bbox[0], (y + h)// 2)
            print("y < 0")
        elif y + h > frame_height:
            center_bbox = (center_bbox[0], y +  ((frame_height - y) // 2))
            print("y + h > 0")
        
        print("Adjusted center of bounding box:", center_bbox)



        # Calculate the displacement of the adjusted bounding box center from the frame center
        displacement_x = center_bbox[0] - center_frame[0]
        displacement_y = center_bbox[1] - center_frame[1]
        
        print("Displacement from center of frame (x, y):", (displacement_x, displacement_y))

        



        # frame center rectangle 
        f_center_box_x = center_frame[0] - 30
        f_center_box_y = center_frame[1] - 30
        f_center_box_w = 60
        f_center_box_h = 60



        # determining if the center of bbox lie inside frame's center box - move/don't move  
        if(f_center_box_x < center_bbox[0] and f_center_box_x + f_center_box_w > center_bbox[0] and f_center_box_y < center_bbox[1] and f_center_box_y + f_center_box_h > center_bbox[1]):
            print("LOW") # dont move
        else:
            print("HIGH") # move

            # determining the direction 
            if(displacement_x > 30):    # 30 coz mene frame's center box 60 width and height liya hai 
                print("Right")
            elif(displacement_x < -30):
                print("left")
            if(displacement_y > 30):
                print("down")
            elif(displacement_y < -30):
                print("Up")
        



        # draw on screen
        cv2.rectangle(img, (f_center_box_x, f_center_box_y, f_center_box_w, f_center_box_h), (0, 255, 0), 2)  # Draw center of frame
        cv2.circle(img, center_bbox, 10, (0, 0, 255), cv2.FILLED)  # Draw center of bounding box 




    cv2.imshow("MYresult", img)
    if cv2.waitKey(100) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
