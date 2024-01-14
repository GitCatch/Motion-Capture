import cv2
import mediapipe as mp


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Open a video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # Check if pose landmarks are detected
    if results.pose_landmarks:
        # Iterate through the landmarks
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            # Get the coordinates of each landmark
            h, w, c = image.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)

            # Print the coordinates
            print(f"Landmark {idx}: ({cx}, {cy})")

        # Draw the pose annotation on the image
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        )

    # Flip the image horizontally for a selfie-view display
    image = cv2.flip(image, 1)

    # Display the image with pose landmarks
    cv2.imshow('MediaPipe Pose', image)

    # Exit when 'Esc' key is pressed
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the video capture
cap.release()
cv2.destroyAllWindows()
