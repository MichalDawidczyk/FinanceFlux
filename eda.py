import pandas as pd

class EDA:
    @staticmethod
    def generate_summary_statistics(data):
        try:
            data = data.drop(columns=["Dividends", "Stock Splits"], errors="ignore")
            statistics = {
                "Mean": data.mean().to_dict(),
                "Median": data.median().to_dict(),
                "Standard Deviation": data.std().to_dict(),
                "Min": data.min().to_dict(),
                "Max": data.max().to_dict()
            }
            return statistics
        except Exception as e:
            print(f"Error generating summary statistics: {e}")
            return {}