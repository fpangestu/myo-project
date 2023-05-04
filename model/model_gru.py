import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.optimizers import Adam
import scipy as sc
from scipy.signal import butter, lfilter, filtfilt, sosfiltfilt


class EMGModel:
    def __init__(self, model_path):
        self.model = load_model(model_path, compile=False)
        self.model.compile(optimizer=Adam(learning_rate=0.001),loss='categorical_crossentropy',metrics=['accuracy'])
        # self.model = Sequential(self.model.layers)
    
    def overlap(self, X, window_size, window_step):
        """
        Create an overlapped version of X
        Parameters
        ----------
        X : ndarray, shape=(n_samples,)
            Input signal to window and overlap
        window_size : int
            Size of windows to take
        window_step : int
            Step size between windows
        Returns
        -------
        X_strided : shape=(n_windows, window_size)
            2D array of overlapped X
        """
        if window_size % 2 != 0:
            raise ValueError("Window size must be even!")
        # Make sure there are an even number of windows before stridetricks
        append = np.zeros((window_size - len(X) % window_size))
        X = np.hstack((X, append))

        ws = window_size
        ss = window_step
        a = X

        valid = len(a) - ws
        nw = int((valid) // ss)
        # print(nw, ws)
        out = np.ndarray((nw, ws), dtype=a.dtype)

        for i in np.arange(nw):
            # "slide" the window along the samples
            start = int(i * ss)
            stop = int(start + ws)
            out[i] = a[start:stop]

        return out


    def stft(self, X, fftsize=128, step=65, mean_normalize=True, real=False, compute_onesided=True):
        """
        Compute STFT for 1D real valued input X
        """
        if real:
            local_fft = np.fft.rfft
            cut = -1
        else:
            local_fft = np.fft.fft
            cut = None
        if compute_onesided:
            cut = fftsize // 2
        if mean_normalize:
            X -= X.mean()
        # print(X)
        X = self.overlap(X, fftsize, step)

        size = fftsize
        win = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(size) / (size - 1))
        X = X * win[None]
        X = local_fft(X)[:, :cut]
        return X

    def pretty_spectrogram(self, d, log=True, thresh=5, fft_size=512, step_size=64):
        """
        creates a spectrogram
        log: take the log of the spectrgram
        thresh: threshold minimum power for log spectrogram
        """
        specgram = np.abs(
            self.stft(d, fftsize=fft_size, step=step_size, real=False, compute_onesided=True)
        )

        if log == True:
            specgram /= specgram.max()  # volume normalize to max 1
            specgram = np.log10(specgram)  # take log
            specgram[
                specgram < -thresh
            ] = -thresh  # set anything less than the threshold as the threshold

            specgram[np.isnan(specgram)] = -thresh
        else:
            specgram[
                specgram < thresh
            ] = thresh  # set anything less than the threshold as the threshold

        return specgram

    def prep(self, input_data):
        signal = np.array(input_data)

        # Pad or Cut
        data = np.zeros((200, 8))
        if signal.shape[0] > 200:
            data[:200, :] = signal[:200, :]
        else:
            data[:signal.shape[0], :] = signal

        # Filter Signal Using High-pass Filter
        signal_filter = np.zeros((200, 8))
        sampling_freq  = 254             # Nyquist theorem (the sampling rate should be at least twice the highest frequency component in the signal)
        filter_order = 5
        cutoff_freq = 20
        for ch in range(8):
            # cutoff_freq  = (sampling_freq*0.5)*0.2
            coefficients = cutoff_freq/(sampling_freq*0.5)              # filter coefficients
            b, a = sc.signal.butter(filter_order, coefficients, btype='highpass')
            filter = filtfilt(b, a, data[:, ch])  
            signal_filter[:, ch] = filter

        # Extract Feature
        feature = np.zeros((1, 15, 240))
        fft_size = 60
        step_size = fft_size - (0.8 * fft_size) # window size - (20% of window size)
        thresh = 3

        for i in range(1):
            wav_spectrogram_1 = self.pretty_spectrogram(signal_filter[:, 0], fft_size=fft_size, step_size=step_size, log=True, thresh=thresh)
            wav_spectrogram_2 = self.pretty_spectrogram(signal_filter[:, 1], fft_size=fft_size, step_size=step_size, log=True, thresh=thresh)
            wav_spectrogram_3 = self.pretty_spectrogram(signal_filter[:, 2], fft_size=fft_size, step_size=step_size, log=True, thresh=thresh)
            wav_spectrogram_4 = self.pretty_spectrogram(signal_filter[:, 3], fft_size=fft_size, step_size=step_size, log=True, thresh=thresh)
            wav_spectrogram_5 = self.pretty_spectrogram(signal_filter[:, 4], fft_size=fft_size, step_size=step_size, log=True, thresh=thresh)
            wav_spectrogram_6 = self.pretty_spectrogram(signal_filter[:, 5], fft_size=fft_size, step_size=step_size, log=True, thresh=thresh)
            wav_spectrogram_7 = self.pretty_spectrogram(signal_filter[:, 6], fft_size=fft_size, step_size=step_size, log=True, thresh=thresh)
            wav_spectrogram_8 = self.pretty_spectrogram(signal_filter[:, 7], fft_size=fft_size, step_size=step_size, log=True, thresh=thresh)
            
            feature[i, :, :] = np.hstack((wav_spectrogram_1, wav_spectrogram_2, wav_spectrogram_3, wav_spectrogram_4, wav_spectrogram_5, wav_spectrogram_6, wav_spectrogram_7, wav_spectrogram_8))

        # print(f'File name: {gesture} No: {test_data} Shape: {data.shape} Filter: {signal_filter.shape} Feature: {feature.shape}')
        # Normalize EMG dataset
        X = (feature-feature.min())/(feature.max()-feature.min())

        return X

    def predict(self, input_data):
        # input_data = tf.convert_to_tensor(input_data, dtype=tf.float32)
        output = self.model.predict(input_data)
        
        return output
    
    def main(self, signal):
        # model_path = 'D:\\4_KULIAH_S2\Semester 4\myo-project\model\gru_model_wo_null.h5'
        # self.model = load_model(model_path)
        prep_data = self.prep(signal)
        output = self.predict(prep_data)

        return np.argmax(output)

if __name__ == '__main__':
    model_path = 'D:\\4_KULIAH_S2\Semester 4\myo-project\model\gru_model.h5'
    # model_path = 'D:\\4_KULIAH_S2\Semester 4\myo-project\model\model_lstm_rec.h5'
    # model_path = 'D:\\4_KULIAH_S2\Semester 4\myo-project\model\model_cnn_rec.h5'
    model = EMGModel(model_path)
    # model = load_model(model_path)
    input_data = pd.read_csv('D:\\4_KULIAH_S2\Semester 4\myo-project\data\me-fist-1.csv')
    prep_data = model.prep(input_data)
    output = model.predict(prep_data)
    print(output)

