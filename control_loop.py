from __future__ import print_function
import os
import cv2
from fire_finder import FireFinder
import geometry
from motors import Shooter, Driver
from control import Controller
from concurrent.futures import ThreadPoolExecutor

# config
video_device = int(os.environ.get('video_device', 1))

# helpers
def prioritize(fire_coords, fire_cnts):
    # TODO
    return fire_coords[0]


# runners
def run_driver(driver):
    fire_finder = FireFinder()
    controller = Controller()
    while True:
        forwardback, leftright = controller.get_control()

        if forwardback == 0:
            continue

        forward = True if forwardBack == 1 else False
        driver.drive(leftright, .25, forward) # TODO pick intelligently


def run_shooter(shooter):
    while True:
        ret, frame = video_capture.read() #Capture frame-by-frame
        if not ret: #Invalid
            print(ret)
            print(frame)
            #raise RuntimeError()

        #proc, fire_px_coords, fire_cnts = fire_finder.get_fires(frame)
        #all_fire_angles = list(map(geometry.px_coords_to_angles, fire_px_coords))
        #fire_angle = prioritize(all_fire_angles)
        #shooter.aim_and_shoot(fire_angle[0], fire_angle[1], 2) # TODO adjust Time to Shoot
        shooter.aim_and_shoot(90, 90, 2) # TODO adjust Time to Shoot
        time.sleep(1)

# main
video_capture = cv2.VideoCapture(video_device)
shooter = Shooter()
driver = Driver()
with ThreadPoolExecutor(max_workers=10) as executor:
    task1 = executor.submit(run_shooter, shooter)
    task2 = executor.submit(run_driver, driver)

    task1.result()
    task2.result()


video_capture.release()
