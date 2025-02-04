import sys
import os
from twilio.rest import Client
import cv2
from keras.models import load_model
import numpy as np
from PyQt5.QtWidgets import QApplication, QFileDialog

# from gunDetection import detect_gun


def resource_path(relative_path):
    """Get absolute path to resources, works for dev and PyInstaler"""
    try:
        # PyInstaller creates a temp folder and store path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class VideoClassification:
    def __init__(self):
        # Load the trained model
        self.model = load_model(resource_path("./model/theftSurvModel/"))

        # Load the Haar cascade file for face detection
        face_cascade = cv2.CascadeClassifier(
            resource_path(
                cv2.data.haarcascades + "./haarcascade_frontalface_default.xml"
            )
        )

        # Define your class labels
        self.class_labels = [
            "gun_theft",
            "pick_pocketing_theft",
            "shoplifting_theft",
            "snitching_theft",
            "theft",
        ]  #  labels in ./data

        # Define your camera name or ID
        self.camera_name = "ESP32 Cam 1"  # Replace with your actual camera name or ID

        # Twilio account SID and Auth Token
        account_sid = "your-sid"
        auth_token = "your-token"
        client = Client(account_sid, auth_token)

        # Capture the camera feed
        cap = cv2.VideoCapture(
            0
        )  # to use ESP32-CAM replace 0 with the IP address of your ESP32-CAM
        ret, frame = cap.read()

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter("output/output.avi", fourcc, 20.0, (640, 480))

        # If camera is not available, open a file dialog to select a video file
        if not cap.isOpened():
            app = QApplication(sys.argv)
            video_path, _ = (
                QFileDialog.getOpenFileName()
            )  # show an "Open" dialog box and return the path to the selected file
            cap = cv2.VideoCapture(video_path)

        frame_counter = 0

        # Load YOLO
        # net = cv2.dnn.readNet("./yolo/yolov3.weights", "./yolo/yolov3.cfg")
        # layer_names = net.getLayerNames()
        # output_layers_indices = net.getUnconnectedOutLayers()
        # output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        # output_layers = [layer_names[i[0] - 1] for i in output_layers_indices]
        # output_layers = [layer_names[i - 1] for i in output_layers_indices.flatten()]

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Use the detect_gun function
            # detect_gun(frame, net, output_layers)

            for _ in range(10):
                (taken, frame) = cap.read()
                frame_counter += 1

            if not taken:
                break

            # If the frame was not read successfully, break from the loop
            if not ret:
                break
            # Convert the frame to grayscale (required for the detectMultiScale function)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            # Draw rectangles around the faces
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            out.write(frame)

            # Preprocess the frame
            preprocessed_frame = self.preprocess_frame(
                frame
            )  # frame preprocessing function

            # Make a prediction
            prediction = self.model.predict(np.array([preprocessed_frame]))
            predicted_class = np.argmax(prediction)

            # Set a threshold
            threshold = 0.8

            # Get the label of the predicted class
            if prediction[0][predicted_class] > threshold:
                predicted_label = self.class_labels[predicted_class]
            else:
                predicted_label = "Normal"

            # Get the label of the predicted class
            # predicted_label = self.class_labels[predicted_class]

            # Check if the predicted label is in the list of class labels
            # if predicted_label not in ['gun_theft', 'pick_pocketing_theft', 'shoplifting_theft', 'snitching_theft', 'theft']:
            # predicted_label = 'Normal'

            # If the predicted label is not 'Normal Video', send an SMS alert
            """ if predicted_label != 'Normal':
                message = client.messages.create(
                    body='Message from Smart City Surveillance System: Alert! Theft detected: ' + predicted_label + ' on ' + self.camera_name,
                    from_='+12058787379',
                    to ='+263772936474'
                ) """

            # Calculate the position of the text
            text_x = int(frame.shape[1] * 0.1)
            text_y = int(frame.shape[0] * 0.1)

            # Display the prediction on the frame
            cv2.putText(
                frame,
                "Predicted class: " + predicted_label,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            # Show the frame
            cv2.imshow("Video", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release the VideoCapture object
        cap.release()
        out.release()

        # Close all OpenCV windows
        cv2.destroyAllWindows()

    def preprocess_frame(self, frame):
        frame_resized = cv2.resize(
            frame, (244, 244)
        )  # Replace (64, 64) with your actual input size

        # Convert the frame to an array
        frame_array = np.array(frame_resized)

        # Normalize the pixel values (this assumes your model expects pixel values between 0 and 1)
        frame_normalized = frame_array / 255.0

        return frame_normalized
