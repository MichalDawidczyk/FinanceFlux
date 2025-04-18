import pandas as pd

class CleanedData:
    @staticmethod
    def clean_historical_data(data):
        try:
            data = data.drop(columns=["Dividends", "Stock Splits", "Volume"], errors="ignore")
            data.dropna(inplace=True)
            data.reset_index(inplace=True)

            if "Date" in data.columns:
                data["Date"] = pd.to_datetime(data["Date"]).dt.date  # Properly format dates

            float_columns = ["Open", "High", "Low", "Close"]
            for col in float_columns:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors="coerce")  # Convert to numeric FIRST

            # Now calculate daily returns
            daily_returns = data["Close"].pct_change()
            std_dev = daily_returns.std()
            outlier_threshold = 10 * std_dev
            data = data[(daily_returns.abs() <= outlier_threshold)]

            # Finally, format numeric values as strings
            for col in float_columns:
                if col in data.columns:
                    data[col] = data[col].map(lambda x: f"{x:.2f}" if pd.notna(x) else x)

            return data
        except Exception as e:
            print(f"Error cleaning historical data: {e}")
            return data

 
    @staticmethod
    def format_financials(financials):
        try:
            for col in financials.columns:
                financials[col] = financials[col].apply(
                    lambda x: f"{float(x):,.2f}" if isinstance(x, (int, float)) else (x if pd.notna(x) else "N/A")
                )
            return financials

        except Exception as e:
            print(f"Error formatting financials: {e}")
            return financials

