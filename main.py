from flask import Flask, render_template, request
from import_data import ImportedData
from clean_data import CleanedData
from eda import EDA
from generate_heatmap import HeatmapGenerator
from predict_stock import StockPredictor

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
            predicted_price = predictor.predict_next_value()
            raw_data[ticker]["Predictions"] = predicted_price

        if financials is not None and not financials.empty and financials.any(axis=None):
            raw_data[ticker]["Financials"] = cleaner.format_financials(financials)
            # if metrics:  # Filter financials by selected metrics
            #     financials = financials[metrics]
            # key_metrics = eda.generate_summary_statistics(historical_data)  # Generate Key Metrics table
            # raw_data[ticker]["Key Metrics"] = key_metrics
            # Generate heatmap 
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

