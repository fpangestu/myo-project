from __future__ import print_function
import myo
import time
import csv
import keyboard
import numpy as np

class Listener(myo.DeviceListener):
    def __init__(self) -> None:
        super().__init__()
        self.is_recording = False
        self.filename = 'me-open-short.csv'
        self.header_written = False
        self.stream = []
        self.emg_data = []
        self.battery = 0
        self.stream_status = True 
        self.device_name = 0

    
    def on_connected(self, event):
        # print("Hello, '{}'! Double tap to exit.".format(event.device_name))
        event.device.vibrate(myo.VibrationType.short)
        event.device.request_battery_level()
        event.device.stream_emg(True)
        self.device_name = event.device_name
        # self.battery = event.battery_level
        # self.stream_status = True
        # print(self.device_name, self.battery, self.stream_status)

    def on_battery_level(self, event):
        # print("Your battery level is:", event.battery_level)
        self.battery = event.battery_level

    def on_pose(self, event):
        # if event.pose == myo.Pose.double_tap:
        #     return False
        pass
    
    def on_unpaired(self, event):
        return False  # Stop the hub
    
    def on_orientation(self, event):
        orientation = event.orientation
        acceleration = event.acceleration
        gyroscope = event.gyroscope

        self.stream = np.array([orientation.x, orientation.y, orientation.z, orientation.w, acceleration.x, acceleration.y, acceleration.z, gyroscope.x, gyroscope.y, gyroscope.z])
        
        # return [orientation, acceleration, gyroscope] 

    def on_emg(self, event):
        emg = event.emg
        self.emg_data = np.array(emg)
        
        # return emg

    def write_to_csv(self, tm, emg, stream, name_file):
        with open(name_file, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not self.header_written:
                writer.writerow(['time', 'channel_1', 'channel_2', 'channel_3', 'channel_4', 'channel_5', 'channel_6', 'channel_7', 'channel_8', 'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w', 'acceleration_x', 'acceleration_y', 'acceleration_z', 'gyroscope_x', 'gyroscope_y', 'gyroscope_z'])
                self.header_written = True
            
            for i in range(len(tm)):
                data = np.concatenate([tm[i], emg[i], stream[i]])
                writer.writerow(data)

    def reset_stream(self):
        self.emg_data = []
        self.stream = []

    def main(self):
        myo.init(sdk_path='D:\\4_KULIAH_S2\Semester 4\myo-project\myo-sdk-win-0.9.0')
        hub = myo.Hub()
        listener = Listener()

        if hub.run(listener, 100):
            return listener.emg_data, listener.stream


if __name__ == '__main__':
    pass
    # myo.init(sdk_path='D:\\4_KULIAH_S2\Semester 4\myo-project\myo-sdk-win-0.9.0')
    # hub = myo.Hub()
    # listener = Listener()
    # sec = 0.005
    # emg_ = []
    # imu_ = []
    # sec_ = []

    # try:
    #     while hub.run(listener, 5):
    #         if keyboard.is_pressed('s'):
    #             if listener.is_recording == False:
    #                 listener.is_recording = True
    #             else:
    #                 listener.is_recording = False
            
            
    #         while listener.is_recording == True:
    #             print(f'EMG: {listener.emg_data}')
    #             print(f'IMU: {listener.stream}')
                
    #             if len(listener.emg_data) != 0 and len(listener.stream) != 0:
    #                 sec_.append(sec)
    #                 emg_.append(listener.emg_data)
    #                 imu_.append(listener.stream)
    #                 sec = sec + 0.005
    #             elif len(listener.emg_data) != 0 and len(listener.stream) == 0:
    #                 sec_.append(sec)
    #                 emg_.append(listener.emg_data)
    #                 if len(imu_) == 0:
    #                     imu_.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #                 elif len(imu_) != 0:
    #                     imu_.append(imu_[-1])
    #                 sec = sec + 0.005
    #             else:
    #                 pass

    #             if keyboard.is_pressed('s'):
    #                 if listener.is_recording == False:
    #                     listener.is_recording = True
    #                 else:
    #                     listener.is_recording = False
      
    #         if keyboard.is_pressed('a'):
    #             tm = np.vstack(sec_)
    #             emg = np.vstack(emg_)
    #             imu = np.vstack(imu_)
    #             listener.write_to_csv(tm, emg, imu)
    #             listener.reset_stream()
    #             sec = 0.005
    #             emg_ = []
    #             imu_ = []
    #             sec_ = []
    # except KeyboardInterrupt:
    #     pass
    
    # print('Bye, bye!')
