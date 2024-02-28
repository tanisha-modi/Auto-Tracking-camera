import cv2
import math

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the video file or use the webcam (0 for default webcam)
video_capture = cv2.VideoCapture(0)

# Get the center coordinates of the frame
frame_center_x, frame_center_y = int(video_capture.get(3) / 2), int(video_capture.get(4) / 2)

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

        # Calculate the change in x and y coordinates from the center of the frame
        delta_x = center_x - frame_center_x
        delta_y = center_y - frame_center_y

        # Display the change in x and y coordinates to the console
        print(f"Change in x: {delta_x}, Change in y: {delta_y}")

    # Display the frame with the bounding box
    cv2.imshow('Face Detection', frame)
    cv2.waitKey(1000)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV window
video_capture.release()
cv2.destroyAllWindows()