from __future__ import print_function
import time
import os
import cv2
from fire_finder import FireFinder
import geometry
import math
from motors import Shooter, Driver
from control import Controller
from concurrent.futures import ThreadPoolExecutor

# config
video_device = int(os.environ.get('video_device', 1))

# helpers
def prioritize(fire_coords, fire_cnts):
    # return left-most fire
    if fire_coords:
        return min(fire_coords, key=lambda coords: coords[0])
    else:
        return []


# runners
def run_driver(driver, res):
    backward = False if res != 2 else True
    leftright = 0
    if res == 3:
        leftright = 1
    elif res == 4:
        leftright = 2
    elif res == 5:
        return
    driver.drive(leftright, 1, backward) # TODO pick intelligently

def get_frame():
    global frame
    while True:
        ret, frame = video_capture.read() #Capture frame-by-frame
        if not ret: #Invalid
            print('Cannot open frame from video camera')


def run_shooter(shooter):
    if frame is None:
        print('frame none')
        return
    proc, fire_px_coords, fire_cnts = fire_finder.get_fires(frame)
    # fire_px_coords = [(400, 400)]
    all_fire_angles = list(map(geometry.px_coords_to_angles, fire_px_coords))
    all_fire_angles = list(map(geometry.rad2deg, all_fire_angles))
    if all_fire_angles:
        fire_angle = prioritize(all_fire_angles, fire_cnts)
        fire_angle = (-fire_angle[0], fire_angle[1])
        print(fire_angle)
        shooter.aim_and_shoot(fire_angle[0], fire_angle[1], 2) # TODO adjust Time to Shoot

# main
frame = None
quit = False
video_capture = cv2.VideoCapture(video_device)
shooter = Shooter()
driver = Driver()
controller = Controller()
fire_finder = FireFinder()

import threading
frame_thread = threading.Thread(target=get_frame)
frame_thread.start()

try:
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            res = controller.get_control()
            if res == 0:
                break
            # curframe = None
            # while True:
            #     ret, frame = video_capture.read()
            #     if frame is not None:
            #         curframe = frame
            #     if not ret:
            #         break
            task1 = executor.submit(run_shooter, shooter)
            task2 = executor.submit(run_driver, driver, res)

            task1.result()
            task2.result()
finally:
    quit = True

video_capture.release()
