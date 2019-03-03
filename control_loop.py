from __future__ import print_function
import cv2
from .fire_finder import FireFinder
from .shooter import Shooter
from .driver import Driver


def px_coords_to_space_coords(coords):
    return (0, 0)


def prioritize(fire_coords, fire_cnts):
    return fire_coords[0]


fire_finder = FireFinder()
shooter = Shooter()
driver = Driver()
while True:
        ret, frame = fire_finder.cap.read() #Capture frame-by-frame
        if not ret: #Invalid
                print(ret)
                print(frame)

        proc, fire_px_coords, fire_cnts = fire_finder.get_fires(frame)
        fire_coords = list(map(px_coords_to_space_coords, fire_px_coords))

        fire_coord = prioritize(fire_coords, fire_cnts)

        driver.go(fire_coord)

        shooter.aim_and_shoot(fire_coord):


#release the capture
temp = cap.release() #if frame read correctly == True
cv2.destroyAllWindows()
