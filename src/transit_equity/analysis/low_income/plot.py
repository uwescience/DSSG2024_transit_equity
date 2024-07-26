import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_multiple_histograms_by_column_group(data: pd.DataFrame, column: str = 'low_income_population', group_column: str = 'county',
                    title: str = 'Histogram', bins: int = 10):
    all_heights, all_bins = np.histogram(data[column], bins = bins)

    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize = (10, 10))

    width = (all_bins[1] - all_bins[0])/(len(data[group_column].unique()) + 1)

    # Plot data
    index = 0
    for group, group_data in data.groupby(group_column):
        heights, bins = np.histogram(group_data[column], bins = all_bins)
        ax.bar(bins[:-1] + index*width, heights, label = group, width=width)
        index += 1
    
    plt.show()