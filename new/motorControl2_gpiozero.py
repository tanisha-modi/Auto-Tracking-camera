# imports 
import cv2
from cvzone.PoseModule import PoseDetector
from gpiozero import Motor
from time import sleep

detector = PoseDetector()

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Define the stepper motor
motor = Motor(forward=33, backward=35)

def move_stepper_motor(direction):
    if direction == 'c':
        print('motor running clockwise\n')
        motor.forward()
        sleep(0.02)
        motor.stop()
        sleep(0.02)
        motor.backward()
        sleep(0.02)
        motor.stop()
        sleep(0.02)
    elif direction == 'a':
        print('motor running anti-clockwise\n')
        motor.forward()
        sleep(0.02)
        motor.stop()
        sleep(0.02)
        motor.backward()
        sleep(0.02)
        motor.stop()
        sleep(0.02)

while True:
    success, img = cap.read()
    img = detector.findPose(img)

    lmlist, bbox = detector.findPosition(img)

    if lmlist:
        angle1, img = detector.findAngle(lmlist[11][0:2], lmlist[13][0:2], lmlist[15][0:2], img)

    if bbox:
        coor = bbox["bbox"]
        x, y, w, h = coor
        center_bbox = (x + w // 2, y + h // 2)
        frame_height, frame_width, _ = img.shape
        center_frame = (frame_width // 2, frame_height // 2)

        displacement_x = center_bbox[0] - center_frame[0]
        displacement_y = center_bbox[1] - center_frame[1]

        f_center_box_x = center_frame[0] - 30
        f_center_box_y = center_frame[1] - 30
        f_center_box_w = 60
        f_center_box_h = 60

        if f_center_box_x < center_bbox[0] and f_center_box_x + f_center_box_w > center_bbox[0] and f_center_box_y < center_bbox[1] and f_center_box_y + f_center_box_h > center_bbox[1]:
            print("LOW")  # don't move
        else:
            print("HIGH")  # move

            if displacement_x > 30:
                print("Right")
                move_stepper_motor('c')
            elif displacement_x < -30:
                print("left")
                move_stepper_motor('a')
            if displacement_y > 30:
                print("down")
            elif displacement_y < -30:
                print("Up")

        cv2.rectangle(img, (f_center_box_x, f_center_box_y, f_center_box_w, f_center_box_h), (0, 255, 0), 2)
        cv2.circle(img, center_bbox, 10, (0, 0, 255), cv2.FILLED)

    cv2.imshow("MYresult", img)
    if cv2.waitKey(100) == ord('q'):
        motor.stop()
        break

cap.release()
cv2.destroyAllWindows()
