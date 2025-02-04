import cv2
import numpy as np
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('./model/theftSurvModel')

# Define the labels
lb = tf.keras.preprocessing.image_dataset_from_directory(
    './data/',
    labels='inferred',
    label_mode='binary',
    batch_size=32,
    image_size=(244, 244),
)

# Initialize the video capture
capture_video = cv2.VideoCapture(0)

# Initialize the video writer
writer = None

# Create a queue to store the predictions
Queue = []

# Start the video loop
while True:

    # Capture the next frame
    ret, frame = capture_video.read()

    # If the frame is empty, break the loop
    if not ret:
        break

    # If the width and height of the video are unknown, get them from the first frame
    if writer is None:
        (Width, Height) = frame.shape[:2]
        writer = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'MJPG'), 30, (Width, Height), True)

    # Convert the frame to RGB and resize it
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (244, 244)).astype('float32')

    # Subtract the mean from the frame
    frame -= np.array([0.485, 0.456, 0.406])

    # Expand the dimensions of the frame
    frame = np.expand_dims(frame, axis=0)

    # Predict the probability of theft
    preds = model.predict(frame)[0]

    # Append the prediction to the queue
    Queue.append(preds)

    # Get the mean of the predictions in the queue
    results = np.array(Queue).mean(axis=0)

    # Get the index of the most likely class
    i = np.argmax(results)

    # Get the label of the most likely class
    label = lb.class_names[-2]

    # Add the label to the frame
    cv2.putText(frame, 'Theft classified : {}'.format(label), (45, 60), cv2.FONT_HERSHEY_PLAIN, 1.25, (255, 0, 0), 5)

    # Write the frame to the video file
    writer.write(frame)

    # Display the frame
    cv2.imshow('In progress', frame)

    # Check if the user pressed the 'q' key
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the video capture and writer
capture_video.release()
writer.release()

# Close all windows
cv2.destroyAllWindows()