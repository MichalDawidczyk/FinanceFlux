import yfinance as yf
import pandas as pd

class ImportedData:
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = {}

    def fetch_data(self):
        columns_date = ["2024-12-31 00:00:00", "2023-12-31 00:00:00", "2022-12-31 00:00:00", "2021-12-31 00:00:00",
                        "2024-09-30 00:00:00", "2023-09-30 00:00:00", "2022-09-30 00:00:00", "2021-09-30 00:00:00"]
        for ticker in self.tickers:
            try:
                print(f"\nFetching data for {ticker}...")
                stock = yf.Ticker(ticker)

                historical_data = stock.history(start=self.start_date, end=self.end_date)
                financials = stock.financials
                key_stats = stock.info

                if financials is not None:
                    financials.columns = financials.columns.map(str)
                    financials = financials.loc[:, financials.columns.intersection(columns_date)]
                    financials.columns = financials.columns.str.replace(' 00:00:00', '')

                key_metrics = {
                    "Ticker": ticker,
                    "P/E Ratio": key_stats.get("forwardPE"),
                    "EPS": key_stats.get("trailingEps"),
                    "Market Cap": key_stats.get("marketCap"),
                    "Website": key_stats.get("website")
                }

                self.data[ticker] = {
                    "Historical Data": historical_data,
                    "Financials": financials,
                    "Key Metrics": key_metrics
                }

                print(f"Data fetched successfully for {ticker}.")

            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")

        return self.data
