
# imports 
import math
import cv2
from cvzone.PoseModule import PoseDetector
detector = PoseDetector()


# Create a VideoCapture object
cap = cv2.VideoCapture(0)


# If we use already saved video
# video_path = 'vid.mp4'
# cap = cv2.VideoCapture(video_path)



def calculate_waist_angle_z(lmlist):
    # Assuming the indices of the relevant landmarks representing the waist or hip points
    # Adjust these indices based on your specific pose detection model
    left_hip_index = 11
    right_hip_index = 12

    # Extracting the 3D coordinates of the left and right hip points
    left_hip = lmlist[left_hip_index]
    right_hip = lmlist[right_hip_index]

    if left_hip and right_hip:
        # Calculate the vector components
        vector_z = right_hip[2] - left_hip[2]
        vector_hip = math.sqrt((right_hip[0] - left_hip[0])**2 + (right_hip[1] - left_hip[1])**2)

        # Calculate the angle with the Z-axis
        waist_angle_z = math.degrees(math.atan2(vector_hip, vector_z))
        return waist_angle_z
    else:
        return None

# Example usage:
# lmlist = [[418, 291, -877], [439, 259, -812], [451, 262, -812], [464, 265, -812], [397, 254, -823], [380, 254, -823], [366, 253, -823], [478, 287, -448], [338, 273, -487], [435, 337, -741], [382, 329, -754], [561, 470, -238], [210, 467, -330], [650, 648, -406], [132, 674, -397], [588, 763, -967], [206, 816, -905], [594, 807, -1106], [207, 877, -1045], [560, 778, -1128], [244, 856, -1072], [551, 728, -1004], [248, 832, -934], [486, 891, -24], [248, 885, 29], [473, 1246, -167], [266, 1230, -264], [478, 1565, 203], [269, 1551, -26], [481, 1621, 208], [264, 1608, -25], [436, 1664, -316], [307, 1646, -581]]










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
        # print(lmlist[24][0:2])

        # print(lmlist[12][2])
        # print(lmlist[24][2])
        # print(lmlist[26][2])
        # print("ok")
        
        angle1, img = detector.findAngle(lmlist[12][1:3], lmlist[24][1:3], lmlist[26][1:3], img)
        # angle2, img = detector.findAngle(lmlist[11][0:2], lmlist[23][0:2], lmlist[25][0:2], img)
        waist_angle_z = calculate_waist_angle_z(lmlist)
        if waist_angle_z is not None:
             print("Angle of waist in Z-axis:", waist_angle_z)
        else:
             print("Waist landmarks not detected.")


    # to terminate the loop
    i = i + 1 
    if i == 1000:
       if lmlist :
           print(len(lmlist)) 
           print(lmlist) 
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
            # print("x < 0")
        elif x + w > frame_width:
            center_bbox = (x + ((frame_width - x)// 2), center_bbox[1])
            # print("x + w > 0")
        if y < 0 and y + h > frame_height:
            center_bbox = (center_bbox[0], frame_height//2)
        elif y < 0:
            center_bbox = (center_bbox[0], (y + h)// 2)
            # print("y < 0")
        elif y + h > frame_height:
            center_bbox = (center_bbox[0], y +  ((frame_height - y) // 2))
            # print("y + h > 0")
        
        # print("Adjusted center of bounding box:", center_bbox)



        # Calculate the displacement of the adjusted bounding box center from the frame center
        displacement_x = center_bbox[0] - center_frame[0]
        displacement_y = center_bbox[1] - center_frame[1]
        
        # print("Displacement from center of frame (x, y):", (displacement_x, displacement_y))

        



        # frame center rectangle 
        f_center_box_x = center_frame[0] - 30
        f_center_box_y = center_frame[1] - 30
        f_center_box_w = 60
        f_center_box_h = 60



        # determining if the center of bbox lie inside frame's center box - move/don't move  
        # if(f_center_box_x < center_bbox[0] and f_center_box_x + f_center_box_w > center_bbox[0] and f_center_box_y < center_bbox[1] and f_center_box_y + f_center_box_h > center_bbox[1]):
        #     print("LOW") # dont move
        # else:
        #     print("HIGH") # move

        #     # determining the direction 
        #     if(displacement_x > 30):    # 30 coz mene frame's center box 60 width and height liya hai 
        #         print("Right")
        #     elif(displacement_x < -30):
        #         print("left")
        #     if(displacement_y > 30):
        #         print("down")
        #     elif(displacement_y > -30):
        #         print("Up")
        



        # draw on screen
        cv2.rectangle(img, (f_center_box_x, f_center_box_y, f_center_box_w, f_center_box_h), (0, 255, 0), 2)  # Draw center of frame
        cv2.circle(img, center_bbox, 10, (0, 0, 255), cv2.FILLED)  # Draw center of bounding box 




    cv2.imshow("MYresult", img)
    if cv2.waitKey(100) == ord('q'):
        break







cap.release()
cv2.destroyAllWindows()


