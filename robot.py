from uarm.wrapper import SwiftAPI
import time
import numpy as np
from msvcrt import getch


class Robot:
    def __init__(self):
        self.swift = 0 

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
        return self.swift.get_position()

    def default_position(self):
        self.swift.reset(speed=800)
    
    def detact_robot(self):
        self.swift.set_servo_detach()

    def attach_robot(self):
        self.swift.set_servo_attach()

    def move_robot(self, x, y, z, speed=30, wait=True):
        self.swift.set_position(x=x, y=y, z=z, speed=speed, wait=wait) 

    def pump(self, status=False):
        self.swift.set_pump(on=status)

    def transformation_matrix(self, cube_point_robot, cube_point_sensor):
        print('calculate transformation matrix')

    
    
if __name__ == '__main__':
    robot = Robot()
    status, device_info, hardware_version = robot.status()
    print(f'Status: {status}, Device info: {device_info}, Hardware version: {hardware_version}')
    time.sleep(2)
    robot.default_position()
    print(f'Posotion: {robot.get_position()}')
    # time.sleep(5)
    # robot.detact_robot()
    # time.sleep(3)
    # # robot.attach_robot()
    # print(f'Position: {robot.get_position()}')
    # robot.test_robot()

