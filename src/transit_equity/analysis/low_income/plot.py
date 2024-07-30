import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx

def plot_multiple_histograms_by_column_group(data: pd.DataFrame, column: str = 'low_income_population', group_column: str = 'county',
                    figsize: tuple = (10, 10), title: str = 'Histogram', bins: int = 10):
    """
    Plot multiple histograms of the same column grouped by another column.

    Parameters
    ----------
    data : pd.DataFrame
        The data to plot
    
    column : str
        The column to plot
    
    group_column : str
        The column to group by
    
    figsize : tuple
        The size of the plot
    
    title : str
        The title of the plot
        (Note: Currently, the title is not used)
    
    bins : int
        The number of bins to use for the histogram
    
    Returns
    -------
    None
    """
    all_heights, all_bins = np.histogram(data[column], bins = bins)

    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize = figsize)

    width = (all_bins[1] - all_bins[0])/(len(data[group_column].unique()) + 1)

    # Plot data
    index = 0
    for group, group_data in data.groupby(group_column):
        heights, bins = np.histogram(group_data[column], bins = all_bins)
        ax.bar(bins[:-1] + index*width, heights, label = group, width=width)
        index += 1
    
    plt.legend()

def plot_gdf(gdf: gpd.GeoDataFrame, column: str, cmap: str = 'viridis', title: str = 'Map', 
    figsize: tuple = (10, 10), **kwargs):
    """
    Plot a GeoDataFrame with a specified column and colormap

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        The GeoDataFrame to plot
    
    column : str
        The column to plot
    
    cmap : str
        The colormap to use
    
    title : str
        The title of the plot
    
    figsize : tuple
        The size of the plot
    
    **kwargs
        Additional keyword arguments to pass to the plot function
        **kwargs
            Additional keyword arguments to pass to the plot function.
            Possible kwargs for this function include:
            - legend_kwds: Additional keyword arguments for customizing the legend
            - classification_kwds: Additional keyword arguments for customizing the classification
    """
    gdf_crs = gdf.to_crs(epsg=3857)
    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize = figsize)

    # Plot data
    ax = gdf_crs.plot(figsize=figsize, alpha=0.9, column = column,
        ax = ax,
        cmap = cmap,
        legend = True,
        legend_kwds = kwargs['legend_kwds'] if 'legend_kwds' in kwargs else {},
        scheme=None if 'classification_kwds' not in kwargs else "User_Defined",
        classification_kwds = kwargs['classification_kwds'] if 'classification_kwds' in kwargs else {})

    cx.add_basemap(ax)

    # Stylize plots
    # plt.style.use('bmh')

    # Set title
    ax.set_title(title, fontdict = {'fontsize': '20', 'fontweight' : '4'})

    return fig, ax
