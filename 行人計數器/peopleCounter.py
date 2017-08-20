# python 3.6
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import time
import datetime


def peopleCounter() :
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
	cap = cv2.VideoCapture("test.mp4") # 指定影片
	# cap = cv2.VideoCapture(0) # 使用Cam
	temp = 0
	temp2 = 0
	state = 0
	while(1):
		ret, frame = cap.read()
		frame = imutils.resize(frame, width=min(400, frame.shape[1]))
		(rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),padding=(8, 8), scale=1.05)
		for (x, y, w, h) in rects:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.circle(frame, ((x+x+w)//2, (y+y+h)//2), 7, (255, 255, 255), -1)
			if state != 1  and 0 < (x+x+w)//2 < 175 :
				if state != 0 :
					state = 1	
			elif state != 2  and 400 > (x+x+w)//2 > 225 :
				if state != 0 :
					state = 2
			elif state != 3  and 175 < (x+x+w)//2 < 200 :
				if state != 0 and state != 1 and state != 2:
					temp = temp + len(rects)
				state = 3
			elif state != 4  and 225 > (x+x+w)//2 > 200 :
				if state != 0 and state != 1 and state != 2 :
					temp2 = temp2 + len(rects)
				state = 4	
		cv2.line(frame,(175,0),(175,400),(127, 255, 255), 2)
		cv2.line(frame,(200,0),(200,400),(0,0, 255), 2)
		cv2.line(frame,(225,0),(225,400),(127, 255, 255), 2)
		
		
		cv2.putText(frame, "In: {}".format(temp2), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.putText(frame, "Out: {}".format(temp), (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == 27:
			break
	cv2.destroyAllWindows()

if __name__ == '__main__':
	peopleCounter()


