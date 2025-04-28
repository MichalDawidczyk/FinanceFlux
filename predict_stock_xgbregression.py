import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler

class XGBRegressorStockPredictor:
    def __init__(self, historical_data):
        self.data = historical_data
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def prepare_data(self, time_steps=10):
        """Prepares stock data for training."""
        self.scaled_data = self.scaler.fit_transform(self.data["Close"].values.reshape(-1, 1))

        x, y = [], []
        for i in range(len(self.scaled_data) - time_steps):
            x.append(self.scaled_data[i:i + time_steps])
            y.append(self.scaled_data[i + time_steps])

        return np.array(x).reshape(-1, time_steps, 1), np.array(y)

    def predict_next_value(self):
        """Predicts next closing price using XGBoost."""
        x_train, y_train = self.prepare_data()
        
        model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1)
        model.fit(x_train.reshape(x_train.shape[0], -1), y_train)

        last_days = self.scaled_data[-10:].reshape(1, -1)
        prediction = model.predict(last_days)

        return self.scaler.inverse_transform(prediction.reshape(-1, 1))[0, 0]

