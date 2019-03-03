from __future__ import print_function
import os
import cv2
from .fire_finder import FireFinder
from .shooter import Shooter
from .driver import Driver
from . import geometry


def prioritize(fire_coords, fire_cnts):
    return fire_coords[0]


video_device = int(os.environ.get('video_device', 1))
video_capture = cv2.VideoCapture(video_device)
fire_finder = FireFinder()
shooter = Shooter()
driver = Driver()
while True:
        ret, frame = video_capture.read() #Capture frame-by-frame
        if not ret: #Invalid
                print(ret)
                print(frame)

        proc, fire_px_coords, fire_cnts = fire_finder.get_fires(frame)
        fire_coords = list(map(px_coords_to_space_coords, fire_px_coords))

        angles = geometry.px_coords_to_angles(fire_coords)

        fire_coord = prioritize(fire_coords, fire_cnts)

        print(f'shooting at {fire_coord}')
        shooter.aim_and_shoot(fire_coord):


#release the capture
temp = video_capture.release() #if frame read correctly == True
