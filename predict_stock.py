import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping

class StockPredictor:
    def __init__(self, historical_data):
        self.data = historical_data

    def prepare_data(self, time_steps=10):
        """Scales and formats data for LSTM."""
        scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = scaler.fit_transform(self.data["Close"].values.reshape(-1, 1))
        self.scaler = scaler

        x, y = [], []
        for i in range(len(self.scaled_data) - time_steps):
            x.append(self.scaled_data[i:i + time_steps])
            y.append(self.scaled_data[i + time_steps])
        
        return np.array(x), np.array(y)

    def build_model(self):
        """Defines and compiles the LSTM model."""
        model = Sequential([
            Input(shape=(10, 1)),
            LSTM(100, return_sequences=True),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def predict_next_value(self):
        """Trains model and predicts next closing price."""
        self.prepare_data()

        x_train, y_train = self.prepare_data(time_steps=30)
        model = self.build_model()
        early_stop = EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)
        model.fit(x_train, y_train, epochs=50, batch_size=5, verbose=0, callbacks=[early_stop])
        # model.fit(x_train, y_train, epochs=5, batch_size=1, verbose=0)
        last_days = self.scaled_data[-10:].reshape(1, 10, 1)
        prediction = model.predict(last_days)

        return self.scaler.inverse_transform(prediction)[0, 0]
