import os
import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from matplotlib.colors import LightSource
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from datetime import datetime
from datetime import timedelta
from rasterio.plot import plotting_extent
import geopandas as gpd
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
import matplotlib.patches as mpatches
try:
    import preProcessing as pre
except ImportError:
    from . import preProcessing as pre

def inundation_depth(file_path, title, 
                    outline = None, 
                    basemap = None,
                    cmap='Blues', legend_kw=None, **imshow_kwargs):

    with rio.open(file_path) as src:
        dataMasked = src.read(1, masked=True)  # Automatically handle no-data
        data = dataMasked.filled(-9999.)  # Fill no-data for visualization
        mask = ~dataMasked.mask  # Invert mask to identify valid data region

        # Define color bins and normalization
        breaks = [0.1, 0.3, 0.5, 1.0, 2.0, np.max(data[mask]) + 1]
        norm = BoundaryNorm(breaks, ncolors=len(breaks), clip=True)
        colors = plt.cm.Blues(np.linspace(0.2, 1, len(breaks)))
        colors[0, 3] = 0  # Make lowest values transparent
        custom_cmap = ListedColormap(colors)

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 8))

        _base_map(basemap, ax)

        ax.imshow(data, cmap=custom_cmap, norm=norm, extent=rio.plot.plotting_extent(src), zorder=2, **imshow_kwargs)

        # Add legend
        labels = ['< 0.1', '0.1 - 0.3', '0.3 - 0.5', '0.5 - 1.0', '1.0 - 2.0', '> 2.0']
        patches = [Patch(color=custom_cmap(norm(b)), label=label) for b, label in zip(breaks, labels)]
        
        # draw outline if needed
        _outline(outline, ax, patches)

        _add_description(ax, title, patches)

        plt.show()

def discharge(file_path, title, 
                basemap = None,
                outline = None):
    discharge_data, extent = _import_tif_file(file_path)
    fig, ax = plt.subplots(figsize=(10, 8))
    
    _base_map(basemap, ax)

    discharge_data = np.where(discharge_data == 0, np.nan, discharge_data)
    cmap = plt.cm.viridis  # 选择基础 colormap，例如 'viridis'
    cmap.set_bad(color=(1, 1, 1, 0))  # 设置无效值为透明（白色，alpha=0）

    im = ax.imshow(discharge_data, extent=extent, cmap=cmap, zorder=2 )
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Discharge')

    _outline(outline, ax)
    _add_description(ax, title)

def domain(file_path,
                title='Domain Map', 
                outline = None,
                bound_list = None,
                gauge_coords = None,
                **kwargs):
        """Show domain map
        
        Args:
            case_folder: folder path of your case
            input_filename: name of DEM file
            title: string to set the figure titile, 'Domain Map' is the defualt
            boundary: show boundary
            gauges: show gauges
        """

        with rio.open(file_path) as src:
            array = src.read(1) 

            # make nan value transparent
            extent = rio.plot.plotting_extent(src)
            nodata = src.nodata
            if nodata is not None:
                array[array == nodata] = np.nan
            array[np.isnan(array)] = np.nanmax(array)

            # use light to get hillshade
            ls = LightSource(azdeg=315, altdeg=45)
            cmap = plt.cm.gist_earth

            fig, ax = plt.subplots(figsize=(10, 8))
            rgb = ls.shade(array, cmap=cmap, blend_mode='overlay', vert_exag=1)
            img = ax.imshow(rgb, extent=extent, alpha=1)

            # add color bar
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=np.nanmin(array), vmax=np.nanmax(array)))
            sm._A = []  
            cbar = fig.colorbar(sm, ax=ax, orientation='vertical')
            cbar.set_label('Elevation (m)')

            # draw outline if needed
            _outline(outline, ax)

            # draw boundaries if needed
            if bound_list is not None:
                for i, bound in enumerate(bound_list):
                    extent = bound['extent']
                    rect = Rectangle((extent[0], extent[2]), extent[1] - extent[0], extent[3] - extent[2], 
                                        linewidth=1, edgecolor='red', facecolor='none', 
                                        label='Boundary' if i == 0 else "")
                    ax.add_patch(rect)   
                ax.legend(loc='upper right')


            if gauge_coords is not None:
                ax.scatter(gauge_coords[:, 0], gauge_coords[:, 1], color='red', s=5, label='Gauges')

                ax.legend(loc='upper right')
            
            _add_description(ax, title)

def rain_mask(file_path,outline = None):
    
    # Load model results   
    data, extent = _import_tif_file(file_path)
    fig, ax = plt.subplots(figsize=(10, 8))
    
    cmap = plt.cm.viridis
    cmap.set_bad(color=(1, 1, 1, 0))  # 设置无效值为透明（白色，alpha=0）

    im = ax.imshow(data, extent=extent,)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Rainfall Station Index')

    _outline(outline, ax)
    _add_description(ax, 'Rainfall mask index')

def rainfall_time_series(file_path,
                            start_date = None,
                            title = None, 
                            method = 'Mean',
                            datetime_interval=24,  
                            datetime_format='%Y-%m-%d',
                            **kwargs):
    """ Plot time series of average rainfall rate inside the model domain

    Args:
        start_date: a datetime object to give the initial datetime of rain
        method: 'mean'|'max','min','mean', method to calculate gridded
            rainfall over the model domain
    """

    rainfall_array = pre._set_time_series(file_path, 3600)
    time_x, value_y = _rainfall_processing(rainfall_array, start_date, method)

    fig, ax = plt.subplots()
    ax.plot(time_x, value_y, **kwargs)
    
    if start_date is not None:
        ax.xaxis.set_major_locator(mdates.HourLocator(
                interval=datetime_interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter(datetime_format))
    ax.set_ylabel(method+' Rainfall rate (mm/h)')
    ax.grid(True)
    
    if title is None:
        title = method+' precipitation in the model domain'
    ax.set_title(title)
    
    plt.show()

def land_mask(file_path, categories, title, outline = None):
    data, extent = _import_tif_file(file_path)

    masked_data = np.ma.masked_invalid(data)
    unique_values = np.unique(masked_data.compressed()) 
    num_categories = len(unique_values)

    fig, ax = plt.subplots(figsize=(10, 8))

    cmap = plt.get_cmap('viridis', num_categories) 
    cmap.set_bad(color='none')
    norm = Normalize(vmin=unique_values.min()-0.5, vmax=unique_values.max()+0.5) 

    img = ax.imshow(data, norm=norm, extent=extent, cmap=cmap, zorder=2)

    patches = [mpatches.Patch(color=cmap(norm(val)), label=categories.get(val, 'Unknown')) for val in unique_values]
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    _outline(outline, ax)
    _add_description(ax, title)


def _rainfall_processing(rain_source, start_date, method):
    if type(start_date) is datetime:
        time_delta = np.array([timedelta(seconds=i) for i in rain_source[:,0]])
        time = start_date+time_delta
    else:
        time = rain_source[:,0]

    rainfall_intensity = rain_source[:,1:]
    if method == 'Mean':
        value = np.mean(rainfall_intensity, axis=1)
    elif method == 'Max':
        value = np.max(rainfall_intensity, axis=1)
    elif method == 'Min':
        value = np.min(rainfall_intensity, axis=1)
    elif method == 'Median':
        value = np.median(rainfall_intensity, axis=1)
    elif method == 'Sum':
        value = np.sum(rainfall_intensity, axis=1)
    return time, value

# Draw the boundary outline
def _outline(outline_path, ax, 
                legend_handles = None):
    if outline_path is not None:
        gdf = gpd.read_file(outline_path)
        gdf.boundary.plot(ax=ax, color='black', linewidth=0.5) 
        boundary_line = plt.Line2D([], [], color='black', linewidth=0.5, label='Domain outline')
        if legend_handles is not None:
            legend_handles.append(boundary_line)
    
    return ax, legend_handles

def _base_map(basemap_path, ax):
    if basemap_path is not None:
        basemap_data, extent = _import_tif_file(basemap_path)
        ls = LightSource(azdeg=315, altdeg=45)
        hillshade = ls.hillshade(basemap_data, vert_exag=1)
        ax.imshow(hillshade, extent=extent, cmap='gray', zorder=1)

def _add_description(ax, title, legend_handles = None):
    ax.set_title(title)
    ax.set_xlabel('Easting (m)')
    ax.set_ylabel('Northing (m)')
    if legend_handles is not None:
        ax.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc='upper left')

def _import_tif_file(file_path):
    with rio.open(file_path) as src:
        file_data_masked = src.read(1, masked=True)
        extent = rio.plot.plotting_extent(src)
        
    return file_data_masked, extent