from __future__ import print_function
import math

'''
positive x is right of center-of-view and positive y is below center-of-view
px_coord is a pixel-number
angle is an angle offset from the center in radians
floor_coords are coordinages on the floor in centimeters
'''

px_max = (480, 640) # in px
cm2in = 2.54
ruler_offset = 3.125
across = 54.75 - ruler_offset
away = 64.5 - ruler_offset
hfov = 2 * math.atan(across / 2 / away)
fov = (hfov, hfov / px_max[0] * px_max[1]) # in radians
height = 5.625 * cm2in # in cm


def px_coords_to_angles(coords):
    return (
        coords[0] / px_max[0] * fov[0] - fov[0] / 2,
        coords[1] / px_max[1] * fov[1] - fov[1] / 2,
    )

def angles_to_space_coords(angle):
    y = height / math.tan(angles[0])
    x = y * math.tan(angles[1])
    return (x, y)

def rad2deg(angle):
    return tuple(map(math.degrees, angle))


if __name__ == '__main__':
    hfov_calc = math.degrees(px_coords_to_angles(px_max)[0]) - math.degrees(px_coords_to_angles((0,0))[0])
    print('horizontal field of vision is {hfov_calc:.1f} degrees'.format(**locals()))
