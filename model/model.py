import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.models import load_model, Sequential
import scipy as sc
import scipy.stats


class EMGModel:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        # self.model = Sequential(self.model.layers)

    def prep(self, input_data, rec):
        # Rectification the EMG data
        if(rec==True):
            input = abs(input_data)
        else:
            input = input_data

        # sliding windows for 1s  --> 1 sec = 200 row
        time = 200
        nRow, nCol = input.shape
        row = 0
        windows = []

        for row in range(nRow // time-1):
            windows.append(input.iloc[row*time : (row+1)*time, 1:9])
        
        # pad or cut
        time = 96
        pad_windows = np.zeros((time, 200, 8))
        if len(windows) < time:
            for i in range(len(windows)):
                pad_windows[i] = windows[i]
        else:
            for i in range(len(pad_windows)):
                pad_windows[len(pad_windows)-(i+1)] = windows[len(windows)-(i+1)]

        # Extract the feature
        windows = np.array(pad_windows)
        time, feat, channels = windows.shape

        final_windows_feature = []
        for window in windows:
            windows_feature = []
            for ch in range(channels):
                window_feature = []
                data = window[:,ch]

                # Mean and Standard deviation of the wave
                window_feature.append(data.mean())
                window_feature.append(data.std())
                # print(f'Mean: {data.mean()}, STD: {data.std()}')

                # Skewness and Kurtosis
                # window_feature.append(window[ch].skew())
                window_feature.append(sc.stats.skew(data))
                window_feature.append(sc.stats.kurtosis(data))
                # print(f'Skew: {sc.stats.skew(data)}, Kurtosis: {sc.stats.kurtosis(data)}')

                # Maximum and minimum values
                window_feature.append(data.max())
                window_feature.append(data.min())
                # print(f'Max: {data.max()}, Min: {data.min()}')

                # Sample variances of each wave, plus the sample covariances of all pairs of the waves
                cov = np.cov(data, bias=False)
                window_feature.append(data.var())
                window_feature.append(cov)
                # print(f'Variance: {data.var()}, Covariance: {cov}')

                # The eigenvalues of the covariance matrix
                # e_val, e_vec = np.linalg.eig(cov)
                # window_feature.append(e_val)
                # print(f'Eigenvalues: {e_val}')

                # The upper triangular elements of the matrix logarithm of the covariance matrix
                # window_feature.append(np.triu(cov))
                # print(f'Upper triangular: {np.triu(cov)}')
                
                # The magnitude of frequency components of each signal, obtained using a Fast Fourier Transform (FFT)
                fft_ch = np.fft.rfft(data)
                magnitude = np.abs(fft_ch)
                window_feature += list(np.concatenate([window_feature, magnitude]))
                # print(f'FFT: {list(np.concatenate([window_feature, magnitude]))}')

                windows_feature.append(window_feature)
            final_windows_feature.append(np.array(windows_feature).transpose())

        # print(f'Feature size: {np.shape(final_windows_feature)}')

        # Normalize the data
        X = np.array(final_windows_feature)
        X = X.reshape((X.shape[0], X.shape[1]*X.shape[2]))
        # print(f'X: {X.shape}')

        if(rec==True):
            scaler = MinMaxScaler(feature_range=(0, 1))
        else:
            scaler = MinMaxScaler(feature_range=(-1, 1))
        
        X_scaler = scaler.fit_transform(X.reshape(X.shape[0], -1)).reshape(X.shape)
        X_scaler = np.expand_dims(X_scaler, axis=0)

        # print(f'Feature shape: {X_scaler.shape}')

        return X_scaler

    def predict(self, input_data):
        # input_data = tf.convert_to_tensor(input_data, dtype=tf.float32)
        output = self.model.predict(input_data)
        
        return output

if __name__ == '__main__':
    print(tf.__version__)
    model_path = 'D:\\4_KULIAH_S2\Semester 4\myo-project\model\model_lstm.h5'
    # model_path = 'D:\\4_KULIAH_S2\Semester 4\myo-project\model\model_lstm_rec.h5'
    # model_path = 'D:\\4_KULIAH_S2\Semester 4\myo-project\model\model_cnn_rec.h5'
    model = EMGModel(model_path)
    # model = load_model(model_path)
    input_data = pd.read_csv('D:\\4_KULIAH_S2\Semester 4\myo-project\data\me-fist-1.csv')
    prep_data = model.prep(input_data, rec=False)
    output = model.predict(prep_data)
    print(output)


    input_data = pd.read_csv('D:\\4_KULIAH_S2\Semester 4\myo-project\data\me-open-1.csv')
    prep_data = model.prep(input_data, rec=False)
    output = model.predict(prep_data)
    print(output)


    input_data = pd.read_csv('D:\\4_KULIAH_S2\Semester 4\myo-project\data\me-wavein-1.csv')
    prep_data = model.prep(input_data, rec=False)
    output = model.predict(prep_data)
    print(output)


    input_data = pd.read_csv('D:\\4_KULIAH_S2\Semester 4\myo-project\data\me-waveout-1.csv')
    prep_data = model.prep(input_data, rec=False)
    output = model.predict(prep_data)
    print(output)

