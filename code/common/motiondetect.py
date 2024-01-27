import cv2
import mediapipe as mp
from datetime import datetime
import json
import os


# Initialize VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

def save_pose_data_to_file(landmarks, image):
    # Create a dictionary to store pose data
    pose_data = {
        'person': {'landmarks': []}
    }

    # Iterate through the landmarks
    for idx, landmark in enumerate(landmarks.landmark):
        # Get the coordinates of each landmark
        h, w, c = image.shape
        cx, cy = int(landmark.x * w), int(landmark.y * h)

        # Append landmark data to the dictionary
        pose_data['person']['landmarks'].append({
            f'Landmark {idx}': {'x': cx, 'y': cy, 'timestamp': str(datetime.now())}
        })

    # Save the data to a JSON file
    with open('record.json', 'w') as f:
        json.dump(pose_data, f)

def pose_recognition_vision():
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)

    # Create the "videos" folder if it doesn't exist
    output_folder = 'videos'
    os.makedirs(output_folder, exist_ok=True)

    # Initialize VideoWriter object outside the loop
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = os.path.join(output_folder, f'output_{current_datetime}.avi')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640, 480))

# Generate a dynamic filename based on the current date and time
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{current_datetime}.avi'

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )
            save_pose_data_to_file(results.pose_landmarks, image)

        # Write the annotated frame to the output video
        out.write(image)

        image = cv2.flip(image, 1)
        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pose_recognition_vision()
