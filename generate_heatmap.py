import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import FuncFormatter
import matplotlib
matplotlib.use('Agg')
class HeatmapGenerator:
    @staticmethod
    def create_heatmap(data, ticker):
        try:
            output_folder = "static/heatmaps"
            os.makedirs(output_folder, exist_ok=True)

            def clean_column(value):
                if isinstance(value, str):
                    try:
                        return float(value.replace(",", ""))
                    except ValueError:
                        return value
                return value
            # data = data.applymap(clean_column)
            data = data.apply(lambda column: column.map(clean_column) if column.dtype == 'object' else column)
            data.fillna(0, inplace=True)
            if data.isnull().values.any():
                print("Data contains NaN values after conversion!")
                data = data.fillna(0)
            heatmap_path = os.path.join(output_folder, f"{ticker}_heatmap.png")
            heatmap_path = heatmap_path.replace("\\", "/")

            plt.figure(figsize=(26, 14))
            try:
                heatmap  = sns.heatmap(data, annot=True, fmt=".2f", cmap="viridis", cbar=True, 
                                       vmax=100_000_000_000, vmin=-10_000_000_000, 
                                       annot_kws={"size": 16})
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                plt.tight_layout(pad=5)
                plt.gca().set_frame_on(True)
                colorbar = heatmap.collections[0].colorbar
                colorbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}")) 
            except Exception as e:
                print(f"Error during heatmap generation: {e}")   
            plt.savefig(heatmap_path)
            plt.close()
            return heatmap_path
        except Exception as e:
            print(f"Error generating heatmap for {ticker}: {e}")
            return None
