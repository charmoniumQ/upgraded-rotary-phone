import time
import sys, termios, tty, os

class Controller(object):

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


    # 1 = forward, 2 = backward, 3 = left, 4 = right
    def get_control(self):
        char = self.getch()

        if (char == "q"):
            exit(0)  

        if (char == "a"):
            print('Left pressed')
            return 3

        if (char == "d"):
            print('Right pressed')
            return 4

        elif (char == "w"):
            print('Up pressed')
            return 1
        
        elif (char == "s"):
            print('Down pressed')
            return 2
        




"""import keyboard
import time

class Controller(object):

    def get_control(self):
        forward = 0
        direction = 0
        if keyboard.is_pressed('w'):
            print("a")
            forward = 1
        if keyboard.is_pressed('s'):
            print("b")
            forward = 2
        if keyboard.is_pressed('a'):
            print("c")
            direction = 1
        if keyboard.is_pressed('d'):
            print("d")
            direction = 2

        print("getting control")
        return (forward, direction)"""


