""" Identify and locate fire in the environment. """

import cv2
import numpy as np

class findFire(object):
	def __init__(self):
		self.cap = cv2.VideoCapture(1)
		self.flag = 0
		self.min_area = 10
		self.fire_coords = []
		self.fire_cnts = []

	def getLight(self, frame):
		self.fire_coords = []
		self.fire_cnts = []

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (11, 11), 0)
		thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.erode(thresh, None, iterations=2)
		thresh = cv2.dilate(thresh, None, iterations=4)

		return thresh

	def getColor(self, frame, val):
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		blurred = cv2.GaussianBlur(hsv, (11, 11), 0)
		mask = cv2.inRange(hsv, (0, 0, 245), (42, 120, 255))
		thresh = cv2.erode(mask, None, iterations=10)

		return mask

	def process_image(self, frame):
		val = 40
		light = self.getLight(frame)
		color = self.getColor(frame, val)

		output = cv2.bitwise_and(light, color)
		im2, contours, hierarchy = cv2.findContours(output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		for contour in contours:
			M = cv2.moments(contour)
			area = cv2.contourArea(contour)
			if area >= self.min_area:
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				self.fire_coords.append((cx, cy))
				self.fire_cnts.append(contour)

		return output

	def run(self):
		while(cv2.waitKey(1) != 27):
			ret, frame = ff.cap.read() #Capture frame-by-frame
			if not ret: #Invalid
				print ret
				print frame

			proc = self.process_image(frame)
			cv2.imshow('proc', proc) #Display the resulting frame
			# self.

		#release the capture
		temp = cap.release() #if frame read correctly == True
		cv2.destroyAllWindows()

if __name__ == '__main__':
	ff = findFire()
	ff.run()