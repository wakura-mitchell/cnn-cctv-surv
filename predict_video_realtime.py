# USAGE
# python predict_video.py --model model/activity.model --label-bin model/lb.pickle --input example_clips/lifting.mp4 --output output/lifting_128avg.avi --size 64

# python predict_video.py --model model/activity_gpu.model --label-bin model/lb.pickle --input example_clips/clip5.mp4 --output output/lifting_128avg.avi --size 64

#python predict_video_realtime.py --model model/activity_gpu.model --label-bin model/lb.pickle --output output/xxx_128avg.avi --size 64

# import the necessary packages
from keras.models import load_model
from imutils.video import VideoStream
from collections import deque
import numpy as np
import argparse
import time
import pickle
import cv2
#from twilio.rest import Client
camid = 0   #upadte as per your requirements
location = 'GZU Campus' 


path_to_model = './model/theftSurvModel'
path_to_labels = ('./model/theftSurvLB.pickle')
input = './input/pic.mp4'
path_to_output = './output/demo_output.avi'
size = 128

# load the trained model and label binarizer from disk
print("[INFO] loading model and label binarizer...")
model = load_model(path_to_model)
lb = pickle.loads(open(path_to_labels, "rb").read())

# initialize the image mean for mean subtraction along with the
# predictions queue
mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")
Q = deque(maxlen = size)

# initialize the video stream, pointer to output video file, and
#------------------# frame dimensions
# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src = "0").start()
writer = None
time.sleep(2.0)
#-------------------
(W, H) = (None, None)
#client = Client("ACea4cecca40ebb1bf4594098d5cef3XXX", "32789639585561088d5937514694eXXX") # copy from twilio
prelabel = ''
prelabel = ''
ok = 'Normal'
fi_label = []
framecount = 0
# loop over frames from the video file stream
while True:
	# read the next frame from the file
	frame = vs.read()

	# if the frame was not grabbed, then we have reached the end
	# of the stream


	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(W, H) = frame.shape[:2]

	# clone the output frame, then convert it from BGR to RGB
	# ordering, resize the frame to a fixed 224x224, and then
	# perform mean subtraction
	output = frame.copy()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame = cv2.resize(frame, (244, 244)).astype("float32")
	frame -= mean

	# make predictions on the frame and then update the predictions
	# queue
	preds = model.predict(np.expand_dims(frame, axis=0))[0]
	#proba = model.predict(frame)[0]
	#print('new prob', proba)
	prediction = preds.argmax(axis=0)
	Q.append(preds)

	# perform prediction averaging over the current history of
	# previous predictions
	results = np.array(Q).mean(axis=0)
	print('Results = ', results)
	maxprob = np.max(results)
	print('Maximun Probability = ', maxprob)
	i = np.argmax(results)
	label = lb.classes_[i]
#	labelnew = lb.classes_[i]
	rest = 1 - maxprob
    
	diff = (maxprob) - (rest)
	print('Difference of prob ', diff)
	th = 100
	if diff > .80:
		th = diff
      
        
        
        
	if (preds[prediction]) < th:
		text = "Alert : {} - {:.2f}%".format((ok), 100 - (maxprob * 100))
		cv2.putText(output, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 255, 0), 5)
	else:
		fi_label = np.append(fi_label, label)
		text = "Alert : {} - {:.2f}%".format((label), maxprob * 100)
		cv2.putText(output, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 255, 0), 5) 
#		if label != prelabel: #update to get alert on your mobile number
#			client.messages.create(to="countrycode and mobile number", #for example +918XXXXXXXXX
#                       from_="Sender number from twilio", #example +1808400XXXX
#                       body='\n'+ str(text) +'\n Satellite: ' + str(camid) + '\n Orbit: ' + location)
		prelabel = label


# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number

	# check if the video writer is None
	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(path_to_output, fourcc, 30,
			(W, H), True)

	# write the output frame to disk
	writer.write(output)

	# show the output image
	cv2.imshow("Output", output)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# release the file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()
