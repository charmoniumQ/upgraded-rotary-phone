'''
positive x is right of center-of-view and positive y is below center-of-view
px_coord is a pixel-number
angle is an angle offset from the center in radians
floor_coords are coordinages on the floor in centimeters
'''

from scipy.optimize import minimize

fov = (np.deg2rad(60), np.deg2rad(60)) # in radians
px_max = (480, 640) # in px
height = 10 # in cm
def px_coords_to_angles(coords):
    return (
        coords[0] / px_max[0] * fov[0] - fov[0] / 2,
        coords[1] / px_max[1] * fov[1] - fov[1] / 2,
    )

def angles_to_space_coords(angle):
    y = height / np.tan(angles[0])
    x = y * np.tan(angles[1])
    return (x, y)
