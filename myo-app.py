import os
import threading
import time
import queue
import myo
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from matplotlib.figure import Figure
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import random
import numpy as np
import sys
sys.path.insert(0, 'D:/4_KULIAH_S2/Semester 4/myo-project/')
from myo_sensor import Listener
from robot import Robot
sys.path.insert(0, 'D:/4_KULIAH_S2/Semester 4/myo-project/model')
from model import EMGModel
event = None

class View(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.size = (1650, 700)
        self.file_name = ''
        self.cube_point_robot = []
        self.transformation_matrix = []

        # Sensor & model
        myo.init(sdk_path='D:\\4_KULIAH_S2\Semester 4\myo-project\myo-sdk-win-0.9.0')
        self.hub = myo.Hub()
        self.listener = Listener()
        # self.robot = Robot()
        # self.model = EMGModel(model_path = 'D:\\4_KULIAH_S2\Semester 4\myo-project\model\gru_model.h5')
        self.my_queue1 = queue.Queue()
        self.my_queue2 = queue.Queue()
        
        # create a Matplotlib figure
        x_lim = 200
        y_lim = 170

        self.fig1 = Figure()
        self.ax1 = self.fig1.add_subplot(1, 1, 1)
        self.ax1.tick_params(axis='both', which='major', labelsize=7)
        self.ax1.set_xlim(0, x_lim)
        self.ax1.set_ylim(-y_lim, y_lim)
        for line_y in [-100, 0, 100]:
            self.ax1.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot(1, 1, 1)
        self.ax2.tick_params(axis='both', which='major', labelsize=7)
        self.ax2.set_xlim(0, x_lim)
        self.ax2.set_ylim(-y_lim, y_lim)
        for line_y in [-100, 0, 100]:
            self.ax2.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig3 = Figure()
        self.ax3 = self.fig3.add_subplot(1, 1, 1)
        self.ax3.tick_params(axis='both', which='major', labelsize=7)
        self.ax3.set_xlim(0, x_lim)
        self.ax3.set_ylim(-y_lim, y_lim)
        for line_y in [-100, 0, 100]:
            self.ax3.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig4 = Figure()
        self.ax4 = self.fig4.add_subplot(1, 1, 1)
        self.ax4.tick_params(axis='both', which='major', labelsize=7)
        self.ax4.set_xlim(0, x_lim)
        self.ax4.set_ylim(-y_lim, y_lim)
        for line_y in [-100, 0, 100]:
            self.ax4.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig5 = Figure()
        self.ax5 = self.fig5.add_subplot(1, 1, 1)
        self.ax5.tick_params(axis='both', which='major', labelsize=7)
        self.ax5.set_xlim(0, x_lim)
        self.ax5.set_ylim(-y_lim, y_lim)
        for line_y in [-100, 0, 100]:
            self.ax5.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig6 = Figure()
        self.ax6 = self.fig6.add_subplot(1, 1, 1)
        self.ax6.tick_params(axis='both', which='major', labelsize=7)
        self.ax6.set_xlim(0, x_lim)
        self.ax6.set_ylim(-y_lim, y_lim)
        for line_y in [-100, 0, 100]:
            self.ax6.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig7 = Figure()
        self.ax7 = self.fig7.add_subplot(1, 1, 1)
        self.ax7.tick_params(axis='both', which='major', labelsize=7)
        self.ax7.set_xlim(0, x_lim)
        self.ax7.set_ylim(-y_lim, y_lim)
        for line_y in [-100, 0, 100]:
            self.ax7.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig8 = Figure()
        self.ax8 = self.fig8.add_subplot(1, 1, 1)
        self.ax8.tick_params(axis='both', which='major', labelsize=7)
        self.ax8.set_xlim(0, x_lim)
        self.ax8.set_ylim(-y_lim, y_lim)
        for line_y in [-100, 0, 100]:
            self.ax8.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig_gyro = Figure()
        self.ax_gyro = self.fig_gyro.add_subplot(1, 1, 1)
        self.ax_gyro.tick_params(axis='both', which='major', labelsize=7)
        self.ax_gyro.set_xlim(0, 120)
        self.ax_gyro.set_ylim(-120, 120)
        for line_y in [-50, 0, 50]:
            self.ax_gyro.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig_acc = Figure()
        self.ax_acc = self.fig_acc.add_subplot(1, 1, 1)
        self.ax_acc.tick_params(axis='both', which='major', labelsize=7)
        self.ax_acc.set_xlim(0, 120)
        self.ax_acc.set_ylim(-5, 5)
        for line_y in [-3, 0, 3]:
            self.ax_acc.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        self.fig_ori = Figure()
        self.ax_ori = self.fig_ori.add_subplot(1, 1, 1)
        self.ax_ori.tick_params(axis='both', which='major', labelsize=7)
        self.ax_ori.set_xlim(0, 120)
        self.ax_ori.set_ylim(-1.3, 1.3)
        for line_y in [-0.5, 0, 0.5]:
            self.ax_ori.axhline(line_y, color='gray', linestyle='--', alpha=0.5)

        # create initial line
        self.x1 = np.arange(x_lim)
        self.y1 = np.zeros((len(self.x1)))
        self.line1, = self.ax1.plot(self.x1, self.y1)
        
        self.x2 = np.arange(x_lim)
        self.y2 = np.zeros((len(self.x2)))
        self.line2, = self.ax2.plot(self.x2, self.y2)

        self.x3 = np.arange(x_lim)
        self.y3 = np.zeros((len(self.x3)))
        self.line3, = self.ax3.plot(self.x3, self.y3)

        self.x4 = np.arange(x_lim)
        self.y4 = np.zeros((len(self.x4)))
        self.line4, = self.ax4.plot(self.x4, self.y4)

        self.x5 = np.arange(x_lim)
        self.y5 = np.zeros((len(self.x5)))
        self.line5, = self.ax5.plot(self.x5, self.y5)

        self.x6 = np.arange(x_lim)
        self.y6 = np.zeros((len(self.x6)))
        self.line6, = self.ax6.plot(self.x6, self.y6)

        self.x7 = np.arange(x_lim)
        self.y7 = np.zeros((len(self.x7)))
        self.line7, = self.ax7.plot(self.x7, self.y7)

        self.x8 = np.arange(x_lim)
        self.y8 = np.zeros((len(self.x8)))
        self.line8, = self.ax8.plot(self.x8, self.y8)

        self.x_gyro = np.arange(120)
        self.y_gyro_1 = np.zeros((len(self.x_gyro)))
        self.y_gyro_2 = np.zeros((len(self.x_gyro)))
        self.y_gyro_3 = np.zeros((len(self.x_gyro)))
        self.line_gyro_1, = self.ax_gyro.plot(self.x_gyro, self.y_gyro_1)
        self.line_gyro_2, = self.ax_gyro.plot(self.x_gyro, self.y_gyro_2)
        self.line_gyro_3, = self.ax_gyro.plot(self.x_gyro, self.y_gyro_3)
        self.ax_gyro.legend(handles=[self.line_gyro_1, self.line_gyro_2, self.line_gyro_3],
                    labels=['X', 'Y', 'Z'], loc='right', fontsize=7)

        self.x_acc = np.arange(120)
        self.y_acc_1 = np.zeros((len(self.x_acc)))
        self.y_acc_2 = np.zeros((len(self.x_acc)))
        self.y_acc_3 = np.zeros((len(self.x_acc)))
        self.line_acc_1, = self.ax_acc.plot(self.x_acc, self.y_acc_1)
        self.line_acc_2, = self.ax_acc.plot(self.x_acc, self.y_acc_2)
        self.line_acc_3, = self.ax_acc.plot(self.x_acc, self.y_acc_3)
        self.ax_acc.legend(handles=[self.line_acc_1, self.line_acc_2, self.line_acc_3],
                    labels=['X', 'Y', 'Z'], loc='right', fontsize=7)

        self.x_ori = np.arange(120)
        self.y_ori_1 = np.zeros((len(self.x_ori)))
        self.y_ori_2 = np.zeros((len(self.x_ori)))
        self.y_ori_3 = np.zeros((len(self.x_ori)))
        self.y_ori_4 = np.zeros((len(self.x_ori)))
        self.line_ori_1, = self.ax_ori.plot(self.x_ori, self.y_ori_1)
        self.line_ori_2, = self.ax_ori.plot(self.x_ori, self.y_ori_2)
        self.line_ori_3, = self.ax_ori.plot(self.x_ori, self.y_ori_3)
        self.line_ori_4, = self.ax_ori.plot(self.x_ori, self.y_ori_4)
        self.ax_ori.legend(handles=[self.line_ori_1, self.line_ori_2, self.line_ori_3, self.line_ori_4],
                    labels=['X', 'Y', 'Z', 'W'], loc='right', fontsize=6)

        box = self.ids.box0
        box.add_widget(FigureCanvasKivyAgg(self.fig1))
        box = self.ids.box1
        box.add_widget(FigureCanvasKivyAgg(self.fig2))
        box = self.ids.box2
        box.add_widget(FigureCanvasKivyAgg(self.fig3))
        box = self.ids.box3
        box.add_widget(FigureCanvasKivyAgg(self.fig4))
        box = self.ids.box4
        box.add_widget(FigureCanvasKivyAgg(self.fig5))
        box = self.ids.box5
        box.add_widget(FigureCanvasKivyAgg(self.fig6))
        box = self.ids.box6
        box.add_widget(FigureCanvasKivyAgg(self.fig7))
        box = self.ids.box7
        box.add_widget(FigureCanvasKivyAgg(self.fig8))
        box = self.ids.box_gyro
        box.add_widget(FigureCanvasKivyAgg(self.fig_gyro))
        box = self.ids.box_acc
        box.add_widget(FigureCanvasKivyAgg(self.fig_acc))
        box = self.ids.box_ori
        box.add_widget(FigureCanvasKivyAgg(self.fig_ori))
        self.txt_hist = self.ids.txt_hist
        self.status = 'Ready!!!'
        self.txt_hist.text = self.status

        # check cube point        
        self.zero_position_sensor = self.read_coor_from_file("zero_position_sensor")
        if(len(self.zero_position_sensor) == 0):
            self.zero_position_sensor = []
        
        self.cube_point_sensor = self.read_coor_from_file("cube_point_sensor")
        if(len(self.cube_point_sensor) == 0):
            self.cube_point_sensor = []
        else:
            print(self.cube_point_sensor)
            self.ids.txt_sensor_1.text = 'Done'
            self.ids.txt_sensor_2.text = 'Done'
            self.ids.txt_sensor_3.text = 'Done'
            self.ids.txt_sensor_4.text = 'Done'
            self.ids.txt_sensor_5.text = 'Done'
            self.ids.txt_sensor_6.text = 'Done'
            self.ids.txt_sensor_7.text = 'Done'
            self.ids.txt_sensor_8.text = 'Done'


        # start a thread to read sensor data and update the plot
        self.running = True
        self.record = False
        self.sensor_thread = threading.Thread(target=self.read_sensor)
        self.sensor_thread.start()
        
        # update the plot with the new data in the main thread
        Clock.schedule_interval(self.update_plot, 0.01)        

    def read_sensor(self):
        # read sensor data in a loop
        # while self.running:
        # Read sensor data
        sec = 0.005
        emg_ = []
        imu_ = []
        sec_ = []

        with self.hub.run_in_background(self.listener.on_event):
            while True:
                time.sleep(0.003)
                emg, imu = self.listener.emg_data, self.listener.stream
                self.my_queue1.put(emg)
                self.my_queue2.put(imu)
                if self.record == True:
                    sec_.append(sec)
                    emg_.append(emg)
                    if len(imu) != 0:
                        imu_.append(imu)
                        sec = sec + 0.005
                    else:
                        if len(imu_) == 0:
                            imu_.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                        elif len(imu_) != 0:
                            imu_.append(imu_[-1])
                        sec = sec + 0.005
                elif self.record == False and len(emg_) != 0:
                    tm = np.array(sec_)
                    emg = np.vstack(emg_)
                    imu = np.vstack(imu_)
                    print(np.shape(tm), np.shape(emg), np.shape(imu))
                    self.listener.write_to_csv(tm, emg, imu, self.file_name)
                    sec = 0.005
                    emg_ = []
                    imu_ = []
                    sec_ = []
                        
    def update_plot(self, dt):
        self.ids.device_status.text, self.ids.battery_status.text, self.ids.stream_status.text = str(self.listener.device_name), str(self.listener.battery), str(self.listener.stream_status)
        
        # calculate transformation matrix if all sensor and robot coordinate already full
        if len(self.cube_point_sensor) == 8 and len(self.cube_point_robot) == 8 and len(self.transformation_matrix) == 0:
            self.transformation_matrix = self.robot.transformation_matrix(self.cube_point_robot, self.cube_point_sensor)

        # kalman filter
        # if len(self.zero_position_sensor) > 0 and len(self.listener.stream) != 0:
        #     x, y, z = self.listener.kalman_filter(self.zero_position_sensor, self.listener.stream)
        #     print(f'X: {np.round(x[0], 10)}, Y: {np.round(y[0], 10)}, Z: {np.round(z[0], 10)}')

        # update the plot with the new data
        emg_ = []
        imu_ = []
        while not self.my_queue1.empty():
            if len(self.my_queue1.get()) != 0:
                emg_.append(self.my_queue1.get())
            else:
                _ = self.my_queue1.get()
        if (len(emg_) == 0):
            emg = np.vstack([[0, 0, 0, 0, 0, 0, 0, 0]])
        else:        
            emg = np.vstack(emg_)
        # print(emg.shape)
        
        while not self.my_queue2.empty():
            if len(self.my_queue2.get()) != 0:
                imu_.append(self.my_queue2.get())
            else:
                _ = self.my_queue2.get()
        if (len(imu_) == 0):
            imu = np.vstack([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        else:
            imu = np.vstack(imu_)
        # print(imu.shape)

        # emg, stream = self.my_queue1.get, self.my_queue2.get
        # print(emg)

        self.y1 = np.append(self.y1[len(emg[:, 0]):], emg[:, 0])
        self.line1.set_ydata(self.y1)
        
        self.y2 = np.append(self.y2[len(emg[:, 1]):], emg[:, 1])
        self.line2.set_ydata(self.y2)
        
        self.y3 = np.append(self.y3[len(emg[:, 2]):], emg[:, 2])
        self.line3.set_ydata(self.y3)
        
        self.y4 = np.append(self.y4[len(emg[:, 3]):], emg[:, 3])
        self.line4.set_ydata(self.y4)
        
        self.y5 = np.append(self.y5[len(emg[:, 4]):], emg[:, 4])
        self.line5.set_ydata(self.y5)
        
        self.y6 = np.append(self.y6[len(emg[:, 5]):], emg[:, 5])
        self.line6.set_ydata(self.y6)
        
        self.y7 = np.append(self.y7[len(emg[:, 6]):], emg[:, 6])
        self.line7.set_ydata(self.y7)
        
        self.y8 = np.append(self.y8[len(emg[:, 7]):], emg[:, 7])
        self.line8.set_ydata(self.y8)

        self.y_ori_1 = np.append(self.y_ori_1[len(imu[:, 0]):], imu[:, 0])
        self.y_ori_2 = np.append(self.y_ori_2[len(imu[:, 1]):], imu[:, 1])
        self.y_ori_3 = np.append(self.y_ori_3[len(imu[:, 2]):], imu[:, 2])
        self.y_ori_4 = np.append(self.y_ori_4[len(imu[:, 3]):], imu[:, 3])
        self.line_ori_1.set_ydata(self.y_ori_1)
        self.line_ori_2.set_ydata(self.y_ori_2)
        self.line_ori_3.set_ydata(self.y_ori_3)
        self.line_ori_4.set_ydata(self.y_ori_4)

        self.y_acc_1 = np.append(self.y_acc_1[len(imu[:, 4]):], imu[:, 4])
        self.y_acc_2 = np.append(self.y_acc_2[len(imu[:, 5]):], imu[:, 5])
        self.y_acc_3 = np.append(self.y_acc_3[len(imu[:, 6]):], imu[:, 6])
        self.line_acc_1.set_ydata(self.y_acc_1)
        self.line_acc_2.set_ydata(self.y_acc_2)
        self.line_acc_3.set_ydata(self.y_acc_3)

        self.y_gyro_1 = np.append(self.y_gyro_1[len(imu[:, 7]):], imu[:, 7])
        self.y_gyro_2 = np.append(self.y_gyro_2[len(imu[:, 8]):], imu[:, 8])
        self.y_gyro_3 = np.append(self.y_gyro_3[len(imu[:, 9]):], imu[:, 9])
        self.line_gyro_1.set_ydata(self.y_gyro_1)
        self.line_gyro_2.set_ydata(self.y_gyro_2)
        self.line_gyro_3.set_ydata(self.y_gyro_3)

        # # redraw the canvas
        self.fig1.canvas.draw()
        self.fig2.canvas.draw()
        self.fig3.canvas.draw()
        self.fig4.canvas.draw()
        self.fig5.canvas.draw()
        self.fig6.canvas.draw()
        self.fig7.canvas.draw()
        self.fig8.canvas.draw()
        self.fig_gyro.canvas.draw()
        self.fig_acc.canvas.draw()
        self.fig_ori.canvas.draw()

        #empty queue

    def on_stop(self):
        # stop the thread when the app is closed
        self.running = False
        self.sensor_thread.join()
        
    def text_popup(self, name_file): 
        if len(name_file) != 0:
            self.status = self.status +"\nFile Name: " + name_file
            self.txt_hist.text = self.status
            self.file_name = name_file + ".csv"

    def start_record(self): 
        if self.ids.btn_start.text == 'Start':
            if  len(self.file_name) == 0:
                self.status = self.status +"\nFile Name is Empty!!!"
                self.txt_hist.text = self.status
            else:    
                self.record = True
                self.ids.btn_start.text = 'Stop'
                self.status = self.status +"\n"+ self.file_name +" Recording Start!!!"
                self.txt_hist.text = self.status
        else:
            self.record = False
            self.ids.btn_start.text = 'Start'
            self.status = self.status +"\n"+ self.file_name +" Recording Stop!!!"
            self.txt_hist.text = self.status
    
    def release_robot(self):
        if self.ids.btn_release_robot.text == 'Release':
            self.ids.btn_release_robot.text = 'Lock'
            # self.robot.detact_robot()
            print('robot detact')
        else:
            self.ids.btn_release_robot.text = 'Release'
            # self.robot.attach_robot()
            print('robot attach')

            time.sleep(1)
            # self.robot.default_position()
            print('robot default position')
    
    def reset_robot(self):
        self.ids.txt_robot_1.text = ''
        self.ids.txt_robot_2.text = ''
        self.ids.txt_robot_3.text = ''
        self.ids.txt_robot_4.text = ''
        self.ids.txt_robot_5.text = ''
        self.ids.txt_robot_6.text = ''
        self.ids.txt_robot_7.text = ''
        self.ids.txt_robot_8.text = ''

        # reset coordinate
        self.cube_point_robot = []
        print('position robot reset')

    def save_robot (self):
        #save coordinate
        if len(self.cube_point_robot) < 9:
            # self.cube_point_robot.append(self.robot.get_position())
            print('position robot save')

        # change status ui
        if self.ids.txt_robot_1.text == '':
            self.ids.txt_robot_1.text = 'Done'
        elif self.ids.txt_robot_2.text == '':
            self.ids.txt_robot_2.text = 'Done'
        elif self.ids.txt_robot_3.text == '':
            self.ids.txt_robot_3.text = 'Done'
        elif self.ids.txt_robot_4.text == '':
            self.ids.txt_robot_4.text = 'Done'
        elif self.ids.txt_robot_5.text == '':
            self.ids.txt_robot_5.text = 'Done'
        elif self.ids.txt_robot_6.text == '':
            self.ids.txt_robot_6.text = 'Done'
        elif self.ids.txt_robot_7.text == '':
            self.ids.txt_robot_7.text = 'Done'
        elif self.ids.txt_robot_8.text == '':
            self.ids.txt_robot_8.text = 'Done'
        else:
            pass

    def zero_position(self):
        # take sensor zero position
        imu = self.listener.stream
        self.zero_position_sensor = imu[4:7]
        self.save_coor_to_file(self.zero_position_sensor, "zero_position_sensor")

        # make it vibrating
        self.listener.vibrate()
        print(f'zero position save: {self.zero_position_sensor}')
    
    def reset_sensor(self):
        self.ids.txt_sensor_1.text = ''
        self.ids.txt_sensor_2.text = ''
        self.ids.txt_sensor_3.text = ''
        self.ids.txt_sensor_4.text = ''
        self.ids.txt_sensor_5.text = ''
        self.ids.txt_sensor_6.text = ''
        self.ids.txt_sensor_7.text = ''
        self.ids.txt_sensor_8.text = ''

        # reset coordinate
        self.cube_point_sensor = []
        print('position sensor reset')

    def save_sensor (self):
        # save coordinate
        imu = self.listener.stream
        if len(self.cube_point_sensor) < 8:
            # kalman = self.listener.kalman_filter(self.zero_position_sensor, imu)
            self.cube_point_sensor.append(imu)              # orientation x acceleration x gyroscope (4, 3, 3)
            print(f'position: {imu}, shape: {np.shape(self.cube_point_sensor)}')
        
        if len(self.cube_point_sensor) == 8:
            self.save_coor_to_file(self.cube_point_sensor, "cube_point_sensor")

        # change status ui
        if self.ids.txt_sensor_1.text == '':
            self.ids.txt_sensor_1.text = 'Done'
        elif self.ids.txt_sensor_2.text == '':
            self.ids.txt_sensor_2.text = 'Done'
        elif self.ids.txt_sensor_3.text == '':
            self.ids.txt_sensor_3.text = 'Done'
        elif self.ids.txt_sensor_4.text == '':
            self.ids.txt_sensor_4.text = 'Done'
        elif self.ids.txt_sensor_5.text == '':
            self.ids.txt_sensor_5.text = 'Done'
        elif self.ids.txt_sensor_6.text == '':
            self.ids.txt_sensor_6.text = 'Done'
        elif self.ids.txt_sensor_7.text == '':
            self.ids.txt_sensor_7.text = 'Done'
        elif self.ids.txt_sensor_8.text == '':
            self.ids.txt_sensor_8.text = 'Done'
        else:
            pass
    
    def save_coor_to_file(self, data, name):
        """
        Save value into file

        Args:
            data (list) : value to save
            name (str) : name of file

        Returns:
            -
        """
        path_file = "D:/4_KULIAH_S2/Semester 4/myo-project/file/"
        isExist = os.path.exists(path_file)
        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(path_file)
            # print("Folder Created")
        
        np.savetxt(path_file + "/" + name + ".txt", data)

    def read_coor_from_file(self, name, *args):
        """
        Read value from file

        Args:
            name (str) : name of file

        Returns:
            -
        """
        path_file = "D:/4_KULIAH_S2/Semester 4/myo-project/file/" + name + ".txt"
        isExist = os.path.exists(path_file)
        if not isExist:
            return []
        
        return np.loadtxt(path_file)

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file("view.kv")
        return View()

if __name__ == '__main__':
    MainApp().run()