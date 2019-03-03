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
    driver.drive(leftright, 0.5, backward) # TODO pick intelligently


def run_shooter(shooter):
    ret, frame = video_capture.read() #Capture frame-by-frame
    if not ret: #Invalid
        print(ret)
        print(frame)
        #raise RuntimeError()

    proc, fire_px_coords, fire_cnts = fire_finder.get_fires(frame)
    # fire_px_coords = [(400, 400)]
    all_fire_angles = list(map(geometry.px_coords_to_angles, fire_px_coords))
    all_fire_angles = list(map(geometry.rad2deg, all_fire_angles))
    if all_fire_angles:
        fire_angle = prioritize(all_fire_angles, fire_cnts)
        print(fire_angle)
        shooter.aim_and_shoot(fire_angle[0], fire_angle[1], 2) # TODO adjust Time to Shoot
    #shooter.aim_and_shoot(90, 90, .5) # TODO adjust Time to Shoot

# main
video_capture = cv2.VideoCapture(video_device)
shooter = Shooter()
driver = Driver()
controller = Controller()
fire_finder = FireFinder()
with ThreadPoolExecutor(max_workers=10) as executor:
    while True:
        res = controller.get_control()
        if res == 0:
            break
        task1 = executor.submit(run_shooter, shooter)
        task2 = executor.submit(run_driver, driver, res)

        task1.result()
        task2.result()

video_capture.release()
