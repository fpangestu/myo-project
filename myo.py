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
    
    def on_connected(self, event):
        print("Hello, '{}'! Double tap to exit.".format(event.device_name))
        event.device.vibrate(myo.VibrationType.short)
        event.device.request_battery_level()
        event.device.stream_emg(True)

    # def on_battery_level(self, event):
    #     print("Your battery level is:", event.battery_level)
        
    def on_pose(self, event):
        if event.pose == myo.Pose.double_tap:
            return False
    
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

    def write_to_csv(self, sec, emg, stream):
        with open(self.filename, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not self.header_written:
                writer.writerow(['time', 'channel_1', 'channel_2', 'channel_3', 'channel_4', 'channel_5', 'channel_6', 'channel_7', 'channel_8', 'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w', 'acceleration_x', 'acceleration_y', 'acceleration_z', 'gyroscope_x', 'gyroscope_y', 'gyroscope_z'])
                self.header_written = True
            
            data = np.concatenate([np.array([round(sec, 3)]), np.array(emg), np.array(stream)])
            writer.writerows([data])
        
            # if keyboard.is_pressed('s'):
            #     if listener.is_recording == True:
            #         listener.is_recording = False
            #     else:
            #         listener.is_recording = True

    def reset_stream(self):
        self.emg_data = []
        self.stream = []

if __name__ == '__main__':
    myo.init(sdk_path='D:\\4_KULIAH_S2\Semester 4\myo-project\myo-sdk-win-0.9.0')
    hub = myo.Hub()
    listener = Listener()
    sec = 0.005

    try:
        while hub.run(listener, 100):
            time.sleep(0.005)
            if keyboard.is_pressed('s'):
                if listener.is_recording == False:
                    listener.is_recording = True
                else:
                    listener.is_recording = False
            
            if listener.is_recording == True:
                print(f'EMG: {listener.emg_data}, Stream: {listener.stream}')
                listener.write_to_csv(sec, listener.emg_data, listener.stream)
                listener.reset_stream()
                sec  = sec + 0.005
    except KeyboardInterrupt:
        pass
    
    print('Bye, bye!')
