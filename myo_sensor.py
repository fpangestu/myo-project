from __future__ import print_function
import myo
import time
import csv
import keyboard
import numpy as np
from pykalman import KalmanFilter

class Listener(myo.DeviceListener):
    def __init__(self) -> None:
        super().__init__()
        self.is_recording = False
        self.filename = 'test1111.csv'
        self.header_written = False
        self.stream = []
        self.emg_data = []
        self.battery = ''
        self.stream_status = False
        self.device_name = ''

        # kalman filter
        self.save_value = []
        self.init_kalman = False
        n_timesteps = 1
        n_dim_state = 3
        self.filtered_state_means_x = np.zeros((n_timesteps, n_dim_state))
        self.filtered_state_means_y = np.zeros((n_timesteps, n_dim_state))
        self.filtered_state_means_z = np.zeros((n_timesteps, n_dim_state))
        self.filtered_state_covariances_x = np.zeros((n_timesteps, n_dim_state, n_dim_state))
        self.filtered_state_covariances_y = np.zeros((n_timesteps, n_dim_state, n_dim_state))
        self.filtered_state_covariances_z = np.zeros((n_timesteps, n_dim_state, n_dim_state))

    def on_connected(self, event):
        # print("Hello, '{}'! Double tap to exit.".format(event.device_name))
        self.device = event.device
        event.device.vibrate(myo.VibrationType.short)
        event.device.request_battery_level()
        event.device.stream_emg(True)
        self.device_name = event.device_name
        self.stream_status = True
        print(self.device_name, self.stream_status)

    def on_battery_level(self, event):
        self.battery = event.battery_level
        print("Your battery level is:", self.battery)

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
        
        # return np.array([orientation.x, orientation.y, orientation.z, orientation.w, acceleration.x, acceleration.y, acceleration.z, gyroscope.x, gyroscope.y, gyroscope.z]) 

    def on_emg(self, event):
        self.emg_data = np.array(event.emg)
        # self.emg_data = np.array(emg)
        
        # return np.array(emg)

    def write_to_csv(self, tm, emg, stream, name_file):
        with open(name_file, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if self.header_written == 'False':
                writer.writerow(['time', 'channel_1', 'channel_2', 'channel_3', 'channel_4', 'channel_5', 'channel_6', 'channel_7', 'channel_8', 'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w', 'acceleration_x', 'acceleration_y', 'acceleration_z', 'gyroscope_x', 'gyroscope_y', 'gyroscope_z'])
                self.header_written = True
            
            for i in range(len(tm)):
                data = np.concatenate([[tm[i]], emg[i, :], stream[i, :]])
                writer.writerow(data)

    def reset_stream(self):
        self.emg_data = []
        self.stream = []

    def kalman_filter(self, zero_position, imu):
        acc = np.array(imu[4:7])
        acc_variance = 0.002**2     #variance = std**2

        if self.init_kalman == False:
            # time step
            dt = 0.01

            # transition_matrix  
            F = [[1, dt, 0.5*dt**2], 
                [0,  1,       dt],
                [0,  0,        1]]

            # observation_matrix   
            H = [0, 0, 1]

            # transition_covariance 
            Q = [[0.2,    0,      0], 
                [  0,  0.1,      0],
                [  0,    0,  10e-4]]

            # observation_covariance 
            R = acc_variance

            # initial_state_mean
            X0 = [0, 0, zero_position[0]]
            Y0 = [0, 0, zero_position[1]]
            Z0 = [0, 0, zero_position[2]]

            # initial_state_covariance
            P0 = [[  0,    0,               0], 
                [  0,    0,               0],
                [  0,    0,   acc_variance]]

            self.kf_x0 = KalmanFilter(transition_matrices = F, 
                            observation_matrices = H, 
                            transition_covariance = Q, 
                            observation_covariance = R, 
                            initial_state_mean = X0, 
                            initial_state_covariance = P0)

            self.kf_y0 = KalmanFilter(transition_matrices = F, 
                            observation_matrices = H, 
                            transition_covariance = Q, 
                            observation_covariance = R, 
                            initial_state_mean = Y0, 
                            initial_state_covariance = P0)
            
            self.kf_z0 = KalmanFilter(transition_matrices = F, 
                            observation_matrices = H, 
                            transition_covariance = Q, 
                            observation_covariance = R, 
                            initial_state_mean = Z0, 
                            initial_state_covariance = P0)
            
            self.filtered_state_means_x = X0
            self.filtered_state_means_y = Y0
            self.filtered_state_means_z = Z0
            self.filtered_state_covariances_x = P0
            self.filtered_state_covariances_y = P0
            self.filtered_state_covariances_z = P0
            self.init_kalman = True
        else:
            self.filtered_state_means_x, self.filtered_state_covariances_x = (
                self.kf_x0.filter_update(
                    self.filtered_state_means_x,
                    self.filtered_state_covariances_x,
                    acc[0]
                )
            )

            self.filtered_state_means_y, self.filtered_state_covariances_y = (
                self.kf_y0.filter_update(
                    self.filtered_state_means_y,
                    self.filtered_state_covariances_y,
                    acc[1]
                )
            )

            self.filtered_state_means_z, self.filtered_state_covariances_z = (
                self.kf_z0.filter_update(
                    self.filtered_state_means_z,
                    self.filtered_state_covariances_z,
                    acc[2]
                )
            )
        
        # iterative estimation for each new measurement
        # for t in range(n_timesteps):
        #     if t == 0:
        #         filtered_state_means[t] = X0
        #         filtered_state_covariances[t] = P0
        #     else:
        #         filtered_state_means[t], filtered_state_covariances[t] = (
        #         kf.filter_update(
        #             filtered_state_means[t-1],
        #             filtered_state_covariances[t-1],
        #             acc[t, 0]
        #         )
        #     )

            # self.save_value.append([self.filtered_state_means_x[0], self.filtered_state_means_y[0], self.filtered_state_means_z[0]])
            # if len(self.save_value) > 600:
            #     data_ = np.vstack(self.save_value)
            #     with open('kalman_drift', mode='a', newline='') as csv_file:
            #         writer = csv.writer(csv_file)
            #         if self.header_written == 'False':
            #             writer.writerow(['accX', 'accY', 'accZ'])
            #             self.header_written = True
                    
            #         for i in range(len(data_)):
            #             data = data_[i, :]
            #             writer.writerow(data)
                
        return self.filtered_state_means_x, self.filtered_state_means_y, self.filtered_state_means_z



    def vibrate(self):
        self.device.vibrate(myo.VibrationType.medium)


if __name__ == '__main__':
    # pass
    myo.init(sdk_path='D:\\4_KULIAH_S2\Semester 4\myo-project\myo-sdk-win-0.9.0')
    hub = myo.Hub()
    listener = Listener()
    sec = 0.005
    emg_ = []
    imu_ = []
    sec_ = []

    try:
        with hub.run_in_background(listener.on_event):
            time.sleep(0.005)
        # while hub.run(listener, 1):
            # print(listener.emg_data)
            if keyboard.is_pressed('s'):
                if listener.is_recording == False:
                    listener.is_recording = True
                else:
                    listener.is_recording = False
            
            
            while listener.is_recording == True:
                print(listener.emg_data)
                # print(f'EMG: {listener.time_data, listener.emg_data}')
                # print(f'IMU: {listener.stream}')
                
                sec_.append(sec)
                emg_.append(listener.emg_data)
                if len(listener.stream) != 0:
                    imu_.append(listener.stream)
                    sec = sec + 0.005
                else:
                    if len(imu_) == 0:
                        imu_.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                    elif len(imu_) != 0:
                        imu_.append(imu_[-1])
                    sec = sec + 0.005

                if keyboard.is_pressed('s'):
                    if listener.is_recording == False:
                        listener.is_recording = True
                    else:
                        listener.is_recording = False
      
            if keyboard.is_pressed('a'):
                tm = np.array(sec_)
                emg = np.vstack(emg_)
                imu = np.vstack(imu_)
                listener.write_to_csv(tm, emg, imu, 'test2.csv')
                listener.reset_stream()
                sec = 0.005
                emg_ = []
                imu_ = []
                sec_ = []
    except KeyboardInterrupt:
        pass
    
    print('Bye, bye!')
