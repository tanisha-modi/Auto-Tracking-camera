# import tkinter as tk
# import json
# import math

# class RobotArmGUI:
#     def _init_(self, master):
#         self.master = master
#         self.master.title("Robot Arm GUI")

#         # Entry fields for XYZ coordinates and arm lengths
#         tk.Label(master, text="X-coordinate:").grid(row=0, column=0)
#         tk.Label(master, text="Y-coordinate:").grid(row=1, column=0)
#         tk.Label(master, text="Z-coordinate:").grid(row=2, column=0)
#         tk.Label(master, text="Length of l1:").grid(row=3, column=0)
#         tk.Label(master, text="Length of l2:").grid(row=4, column=0)

#         self.x_entry = tk.Entry(master)
#         self.y_entry = tk.Entry(master)
#         self.z_entry = tk.Entry(master)
#         self.l1_entry = tk.Entry(master)
#         self.l2_entry = tk.Entry(master)

#         self.x_entry.grid(row=0, column=1)
#         self.y_entry.grid(row=1, column=1)
#         self.z_entry.grid(row=2, column=1)
#         self.l1_entry.grid(row=3, column=1)
#         self.l2_entry.grid(row=4, column=1)

#         # Button to calculate joint angles and generate JSON file
#         tk.Button(master, text="Calculate Angles", command=self.calculate_angles).grid(row=5, column=0, columnspan=2)

#     def calculate_angles(self):
#         try:
#             # Get XYZ coordinates and arm lengths from entry fields
#             x = float(self.x_entry.get())
#             y = float(self.y_entry.get())
#             z = float(self.z_entry.get())
#             l1 = float(self.l1_entry.get())
#             l2 = float(self.l2_entry.get())

#             # Calculate joint angles
#             angles = calculate_joint_angles(x, y, z, l1, l2)

#             # Display joint angles
#             print("Joint Angles:", angles)

#             # Generate JSON file
#             json_data = {
#                 "angle_1": angles[0],
#                 "angle_2": angles[1],
#                 "angle_3": angles[2]
#             }

#             with open("input_and_angles.json", "w") as json_file:
#                 json.dump(json_data, json_file, indent=2)

#             print("JSON file generated: input_and_angles.json")

#         except ValueError:
#             print("Invalid input. Please enter valid numerical values for XYZ coordinates and arm lengths.")

# def calculate_joint_angles(x, y, z, l1, l2):
#     # Calculate angle for first joint (rotation in xy plane around y axis)
#     theta1 = (math.atan2(y, x)*180)/math.pi
#     if theta1<-90 or theta1>90:
#         return 0,0,0
    
#     # print(theta1)
#     # Project the arm's position onto the xy plane for further calculations
#     X = math.sqrt(x*x + y*y)

#     # print("hello",X)
#     # X=3
#     Y=z
#     root=math.sqrt(X*X+Y*Y)
#     a1=(X*X+Y*Y+l1*l1-l2*l2)/(2*l1*root)
#     theta21=math.atan(Y/X)+math.acos(a1)
#     theta22=math.atan(Y/X)+math.acos(a1)
#     if theta21*180/math.pi>-90 and theta21*180/math.pi<90:
#         theta2=theta21
#     elif theta22*180/math.pi>-90 and theta22*180/math.pi<90:
#         theta2=theta22
#     else:
#         return theta1,0,0
    
#     # print(a2)
#     a2=(Y-l1*math.sin(theta2))/(X-l1*math.cos(theta2))
#     theta3=math.atan(a2)
#     # print(theta3)
#     theta3-=theta2
#     theta2=theta2*180/math.pi
#     theta3=theta3*180/math.pi
#     if theta3<-90 or theta3>90:
#         return theta1,theta2,0
#     # Using law of cosines to calculate angles for the second and third joints
#     # Convert angles to degrees
#     # theta1 = math.degrees(theta1)
#     # theta2 = math.degrees(theta2)
#     # theta3 = math.degrees(theta3)
#     return theta1, theta2, theta3
# if _name_ == "_main_":
#     root = tk.Tk()
#     app = RobotArmGUI(root)
#     root.mainloop()
import cv2

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the video file or use the webcam (0 for default webcam)
video_capture = cv2.VideoCapture(0)


# Variables for storing the previous frame's center coordinates
prev_center_x, prev_center_y = 0, 0

while True:
    # Read a frame from the video
    ret, frame = video_capture.read()
    
    # Break the loop if video has ended
    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw boundary box around the face and calculate center coordinates
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        center_x = x + w // 2
        center_y = y + h // 2

        # Calculate the change in x and y coordinates
        delta_x = center_x - prev_center_x
        delta_y = center_y - prev_center_y

        # Display the change in x and y coordinates to the console
        print(f"Change in x: {delta_x}, Change in y: {delta_y}")
    

        # Update the previous center coordinates
        prev_center_x, prev_center_y = center_x, center_y

    # Display the frame with the bounding box
    cv2.imshow('Face Detection', frame)
    cv2.waitKey(1000)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV window
video_capture.release()
cv2.destroyAllWindows()