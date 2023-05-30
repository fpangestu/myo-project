from uarm.wrapper import SwiftAPI
import time
import numpy as np
from msvcrt import getch
import keyboard

class Robot:
    def __init__(self):
        self.swift = 0 
        self.x = 0
        self.y = 0
        self.z = 0

    def status(self):
        try:
            self.swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})                        # Robot serial number
            self.swift.waiting_ready(timeout=3)
            # print(swift.get_device_info())
            robot_status = self.swift.get_device_info()            
            return "Connected", robot_status['device_type'], robot_status['hardware_version']                                            
        except:
            return "Not Connected", "---", "---"

    def get_position(self):
        self.x, self.y, self.z = self.swift.get_position()
        return self.swift.get_position()

    def default_position(self):
        self.swift.reset(speed = 1300)
    
    def detact_robot(self):
        self.swift.set_servo_detach()

    def attach_robot(self):
        self.swift.set_servo_attach()

    def move_robot(self, x, y, z, speed=1000, wait=True):
        self.swift.set_position(x=x, y=y, z=z, speed=speed, wait=wait) 

    def pump(self, status=False):
        self.swift.set_pump(on=status)
    
    def limit_switch(self):
        return self.swift.get_limit_switch()

    def transformation_matrix(self, cube_point_robot, cube_point_sensor):
        print('calculate transformation matrix')
    
    def main(self, command, value=0):
        # print(command)
        if(command == 0):
            self.pump(status=True)
        elif(command == 1):
            self.pump(status=False)
        elif(command == 2):
            self.y = self.y + 1 
            self.move_robot(self.x, self.y, self.z, speed=1000+(value*300))
        elif(command == 3):
            self.y = self.y - 1
            self.move_robot(self.x, self.y, self.z, speed=1000+(value*300))
        elif(command == 4):
            status = self.limit_switch()
            # print(status)
            if (status == False):
                self.z = self.z - 1 
                self.move_robot(self.x, self.y, self.z, speed=1000+(value*300))
        elif(command == 5):
            self.z = self.z + 1
            self.move_robot(self.x, self.y, self.z, speed=1000+(value*300))
        elif(command == 6):
            self.x = self.x + 1 
            self.move_robot(self.x, self.y, self.z, speed=1000+(value*300))
        elif(command == 7):
            self.x = self.x - 1
            self.move_robot(self.x, self.y, self.z, speed=1000+(value*300))
    

if __name__ == '__main__':
    robot = Robot()
    status, device_info, hardware_version = robot.status()
    print(f'Status: {status}, Device info: {device_info}, Hardware version: {hardware_version}')
    time.sleep(1)
    robot.default_position()
    x, y, z = robot.get_position()
    speed = 1000
    print(f'X: {x}, Y: {y}, Z: {z}')
    
    # move robot using arrow
    while True:
        if keyboard.is_pressed('a'):
            y = y + 1
            robot.move_robot(x, y, z, speed=speed)
        elif keyboard.is_pressed('s'):
            x = x + 1
            robot.move_robot(x, y, z, speed=speed)
        elif keyboard.is_pressed('w'):
            x = x - 1
            robot.move_robot(x, y, z, speed=speed)
        elif keyboard.is_pressed('d'):
            y = y - 1
            robot.move_robot(x, y, z, speed=speed)
        elif keyboard.is_pressed('e'):
            status = robot.limit_switch()
            print(status)
            # print(status)
            if (status == False):
                z = z - 1
                robot.move_robot(x, y, z, speed=speed)
        elif keyboard.is_pressed('r'):
            z = z + 1
            robot.move_robot(x, y, z, speed=speed)
        elif keyboard.is_pressed('z'):
            robot.pump(status=True)
        elif keyboard.is_pressed('x'):
            robot.pump(status=False)
        
        print(f'X: {x}, Y: {y}, Z: {z}')



