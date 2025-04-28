
class SentimentFromPredictions:
    def __init__(self, historical_price, predicted_price_lstm, predicted_price_xgb):
        self.historical_price = historical_price
        self.predicted_price_lstm = predicted_price_lstm
        self.predicted_price_xgb = predicted_price_xgb

    def analyze_trend(self):
        """Calculates sentiment based on predicted stock movement."""
        lstm_change = ((self.predicted_price_lstm - self.historical_price) / self.historical_price) * 100
        xgb_change = ((self.predicted_price_xgb - self.historical_price) / self.historical_price) * 100

        price_change = (lstm_change + xgb_change) / 2
        if price_change > 5:
            sentiment = "Positive Outlook 📈 – Strong upward trend expected."
        elif price_change < -5:
            sentiment = "Negative Outlook 📉 – Potential bearish movement."
        else:
            sentiment = "Neutral Outlook 🔄 – Stable conditions, minimal change."

        return {
            "Price Change LSTM (%)": round(lstm_change, 2),
            "Price Change XGBoost (%)": round(xgb_change, 2),
            "Average Change (%)": round(price_change, 2),
            "Sentiment Conclusion": sentiment
        }
