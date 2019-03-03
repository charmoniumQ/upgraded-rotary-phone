import keyboard
import time

class Controller(object):

	def get_control(self):
		forward = 0
		direction = 0
		if keyboard.is_pressed('w'):
			forward = 1
		if keyboard.is_pressed('s'):
			forward = 2
		if keyboard.is_pressed('a'):
			direction = 1
		if keyboard.is_pressed('d'):
			direction = 2

		return (forward, direction)
