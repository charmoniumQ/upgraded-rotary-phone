from __future__ import print_function
import cv2
import numpy as np
import datetime
import random
import string

""" Identify and locate fire in the environment. """

def timestamp():
    return int((datetime.datetime.now() - datetime.datetime(year=1970, month=1, day=1)).total_seconds())

MIN_AREA = 500

class FireFinder(object):
    def getLight(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # TODO: factor out magic numbres
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)

        return thresh

    def getColor(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # TODO: factor out magic numbres
        blurred = cv2.GaussianBlur(hsv, (11, 11), 0)
        mask = cv2.inRange(hsv, (0, 0, 245), (42, 120, 255))
        thresh = cv2.erode(mask, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)

        return mask

    def get_fires(self, frame):
        height, width, channels = frame.shape
        light = np.zeros((height, width), np.uint8)
        color = np.zeros((height, width), np.uint8)
        for i in range(0,6):
            light = np.add(light, self.getLight(frame))
            color = np.add(color, self.getColor(frame))

        output = cv2.bitwise_and(light, color)
        im2, contours, hierarchy = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        fire_coords = []
        fire_cnts = []
        for contour in contours:
            M = cv2.moments(contour)
            area = cv2.contourArea(contour)
            if area >= MIN_AREA:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                fire_coords.append((cx, cy))
                fire_cnts.append(contour)
        t = timestamp()
        for point in fire_coords:
            cv2.circle(frame, point, 1, (0,255,0), thickness=3, lineType=8, shift=0)
        cv2.imwrite('/tmp/{t}_frame.jpg'.format(**locals()), frame)
        # cv2.imwrite('/tmp/{t}_light.jpg'.format(**locals()), light)
        # cv2.imwrite('/tmp/{t}_color.jpg'.format(**locals()), color)
        # cv2.imwrite('/tmp/{t}_output.jpg'.format(**locals()), output)

        return output, fire_coords, fire_cnts

def run():
    import os
    video_device = int(os.environ.get('video_device', 1))
    video_capture = cv2.VideoCapture(video_device)
    fire_finder = FireFinder()

    while cv2.waitKey(1) != 27:
        ret, frame = video_capture.read() #Capture frame-by-frame
        if not ret: #Invalid
            print(ret)
            print(frame)
            raise RuntimeError('Cannot open frame from video camera')

        proc, fire_coords, fire_cnts = fire_finder.get_fires(frame)
        for point in fire_coords:
            cv2.circle(proc, point, 1, (0,255,0), thickness=3, lineType=8, shift=0)
        cv2.imshow('proc', proc) #Display the resulting frame

    #release the capture
    temp = video_capture.release() #if frame read correctly == True
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()
