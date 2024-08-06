import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx
import folium.folium

from matplotlib.colors import rgb2hex
from matplotlib.patches import Patch
from geopandas.explore import _categorical_legend
from folium.plugins import Geocoder
import plotly.graph_objects as go

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

def explore_gdf(gdf: gpd.GeoDataFrame, column: str, cmap: str = 'viridis', title: str = 'Map', figsize: tuple = (10, 10),
                search_bar: bool = True,
                bins: list = None, bin_labels: list = None, bin_column: str = '_bin') -> folium.Map:
    """
    Explore a GeoDataFrame with a specified column and colormap.
    If bins, bin_labels, and bin_column are provided, the data will be classified into bins, and the bins will be plotted.
    
    Warning:
    The binned column will also be added to the GeoDataFrame. Feel free to drop this column if you don't need it. 

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

    bins : list
        The bins to use for classification
    
    bin_labels : list
        The labels for the bins
    
    bin_column : str
        The column to store the bin values
    """
    if bins is None or len(bins) == 0:
        m = gdf.explore(column = column, cmap = cmap, figsize = figsize, title = title)
        return m

    if bin_labels is None or len(bin_labels) == 0:
        bin_labels = bins

    bins_true_min, bins_true_max = 0, len(bins)
    bins_true_length = bins_true_max - bins_true_min + 1

    gdf[bin_column] = np.digitize(gdf[column], bins=bins, right=False)
    cmap_listed = plt.colormaps[cmap].resampled(bins_true_length)
    # legend_elements = [Patch(facecolor=cmap_listed(i), edgecolor='black', 
    #                          label=bin_labels[i]) for i in range(len(bin_labels))]
    colors = [rgb2hex(cmap_listed(i)) for i in range(bins_true_length)]

    m = gdf.explore(bin_column, cmap=cmap, legend = False, vmin=bins_true_min, vmax=bins_true_max, figsize=figsize, title=title)
    _categorical_legend(
        m=m,
        title=title,
        categories=bin_labels,
        colors=colors
    )

    if search_bar:
        Geocoder().add_to(m)

    return m

def plot_grouped_line_chart(data_df: pd.DataFrame, x: str, y: str, group: str, title: str = 'Line Chart', figsize: tuple = (10, 10)):
    """
    Plot a grouped line chart.
    This is a very specific function, and it is better used simply as a reference for creating more general functions.

    Parameters
    ----------
    data : pd.DataFrame
        The data to plot
    
    x : str
        The x-axis column
    
    y : str
        The y-axis column
    
    group : str
        The column to group by
    
    title : str
        The title of the plot
    
    figsize : tuple
        The size of the plot
    """
    fig = go.Figure()

    # Plot data
    for key, group_df in data_df.groupby(group):
        fig.add_trace(
            go.Scatter(
                x=group_df[x]
                y=group_df[y],
                mode='lines',
                line=dict(
                    width=3
                ),
                name=key
            )
        )

    return fig