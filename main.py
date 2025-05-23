from flask import Flask, render_template, request
from import_data import ImportedData
from clean_data import CleanedData
from eda import EDA
from generate_heatmap import HeatmapGenerator
from predict_stock import StockPredictor
from predict_stock_xgbregression import XGBRegressorStockPredictor
from sentiment_analysis import SentimentFromPredictions

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    # Define parameters
    # tickers = ['AMZN', 'AAPL', 'TSLA']
    ticker = request.args.get("ticker", "AMZN")
    start_date = "2024-01-01"
    end_date = "2025-01-01"

    importer = ImportedData([ticker], start_date, end_date)
    raw_data = importer.fetch_data()

    cleaner = CleanedData()
    eda = EDA()

    if ticker in raw_data:
        content = raw_data[ticker]
        historical_data = content["Historical Data"]
        financials = content["Financials"]

        if historical_data is not None and not historical_data.empty:
            raw_data[ticker]["Historical Data"] = cleaner.clean_historical_data(historical_data)
            raw_data[ticker]["EDA"] = eda.generate_summary_statistics(historical_data)

            predictor = StockPredictor(historical_data)
            predicted_price_lstm = predictor.predict_next_value()
            raw_data[ticker]["Predictions"] = predicted_price_lstm

            predictor_xgb = XGBRegressorStockPredictor(historical_data)
            predicted_price_xgb = predictor_xgb.predict_next_value()
            raw_data[ticker]["XGBoost Prediction"] = predicted_price_xgb

            historical_close = historical_data["Close"].iloc[-1] 
            sentiment_analyzer = SentimentFromPredictions(historical_close, predicted_price_lstm, predicted_price_xgb)
            sentiment_summary = sentiment_analyzer.analyze_trend()
            raw_data[ticker]["Sentiment Analysis"] = sentiment_summary

        if financials is not None and not financials.empty and financials.any(axis=None):
            raw_data[ticker]["Financials"] = cleaner.format_financials(financials)

            heatmap_path = HeatmapGenerator.create_heatmap(financials, ticker)
            if heatmap_path:
                content["Heatmap"] = f"heatmaps/{ticker}_heatmap.png"
            else:
                content["Heatmap"] = None
        else:
            raw_data[ticker]["Financials"] = None
    else:
        raw_data = None

    return render_template(
        "index.html",
        data=raw_data,
        selected_ticker=ticker
    )

if __name__ == "__main__":
    app.run(debug=True)

