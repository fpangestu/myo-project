import numpy as np
import myo
import time

class MyListener(myo.DeviceListener):

    def __init__(self):
        self.emg_data = []

    def on_connected(self, event):
        event.device.stream_emg(True)

    def on_emg(self, event):
        self.emg_data.append(event.emg)

if __name__ == '__main__':
    myo.init(sdk_path='D:\\4_KULIAH_S2\Semester 4\myo-project\myo-sdk-win-0.9.0')
    hub = myo.Hub()
    listener = MyListener()

    with hub.run_in_background(listener.on_event):
        while True:
            time.sleep(0.005)
            try:
                if len(listener.emg_data) > 0:
                    # Do something with the collected data
                    print(listener.emg_data)
            except KeyboardInterrupt:
                break
    
    # process the collected data here
    emg_data = listener.emg_data
    print(np.shape(emg_data))
