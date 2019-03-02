""" Identify and locate fire in the environment. """

import cv2
import numpy as np

class findFire(object):
	def __init__(self):
		self.cap = cv2.VideoCapture(1)
		self.flag = 0
		self.fire_coords = []
		self.fire_cnts = []

	def nothing(*arg):
		pass

	def getLight(self, frame):
		self.fire_coords = []
		self.fire_cnts = []

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (11, 11), 0)
		thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.erode(thresh, None, iterations=2)
		thresh = cv2.dilate(thresh, None, iterations=4)
		# im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		# for contour in contours:
		# 	M = cv.moments(contour)
		# 	area = cv.contourArea(contour)
		# 	if area >= self.min_area:
		# 		cx = int(M['m10']/M['m00'])
		# 		cy = int(M['m01']/M['m00'])
		# 		self.fire_coords.append((cx, cy))
		# 		self.fire_cnts.append(contour)

		return thresh

	def getColor(self, frame, val):
		# inverted = cv2.bitwise_not(frame)

		# lowHue = cv2.getTrackbarPos('lowHue', 'colorTest')
		# highHue = cv2.getTrackbarPos('highHue', 'colorTest')

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		blurred = cv2.GaussianBlur(hsv, (11, 11), 0)
		mask = cv2.inRange(hsv, (10, 120,220), (100, 255,255))
		thresh = cv2.erode(mask, None, iterations=10)
		# thresh = cv2.dilate(mask, None, iterations=2)
		# im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		# for contour in contours:
		# 	M = cv.moments(contour)
		# 	area = cv.contourArea(contour)
		# 	if area >= self.min_area:
		# 		cx = int(M['m10']/M['m00'])
		# 		cy = int(M['m01']/M['m00'])
		# 		self.fire_coords.append((cx, cy))
		# 		self.fire_cnts.append(contour)

		return mask

	def process_image(self, frame):
		val = 40
		light = self.getLight(frame)
		color = self.getColor(frame, val)

		return color

	def run(self):
		# cv2.namedWindow('colorTest', cv2.WINDOW_NORMAL)
		# icol = (0, 100, 80, 10, 255, 255)   # Red
		# cv2.createTrackbar('Hue_Low','colorTest',icol[0], 255, self.nothing)
		# cv2.createTrackbar('Hue_High','colorTest',icol[3], 255, self.nothing)

		while(cv2.waitKey(1) != 27):
			ret, frame = ff.cap.read() #Capture frame-by-frame
			if not ret: #Invalid
				print ret
				print frame

			proc = self.process_image(frame)
			cv2.imshow('proc', proc) #Display the resulting frame
			# if cv2.waitKey(1) & 0xFF == ord('q'):
			# 	break

		#release the capture
		temp = cap.release() #if frame read correctly == True
		cv2.destroyAllWindows()

if __name__ == '__main__':
	ff = findFire()
	ff.run()