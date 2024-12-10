import rasterio
import numpy as np
import pandas as pd
import rasterio as rio
from rasterio.features import shapes
import fiona
from shapely.geometry import shape, mapping

def remap_rain_mask_and_extract_source(rain_mask, rain_source, 
                                       remapped_rainmask, remapped_rain_source):
    # Step 1: Read the rainMask.tif and find unique station indexes
    with rasterio.open(rain_mask) as src:
        rain_mask = src.read(1)  # Read the first band
        profile = src.profile  # Get profile for writing output later

    # Find unique station indexes (ignoring NoData values)
    unique_indexes = np.unique(rain_mask[rain_mask != src.nodata])
    # Remap these indexes to start from 0
    remap_dict = {old_idx: new_idx for new_idx, old_idx in enumerate(sorted(unique_indexes))}

    # Create a new rain mask with remapped indexes
    remapped_rain_mask = np.copy(rain_mask)
    for old_idx, new_idx in remap_dict.items():
        remapped_rain_mask[rain_mask == old_idx] = new_idx

    # Step 2: Read the rainfall source data without interpreting headers
    rainfall_data = pd.read_csv(rain_source, delim_whitespace=True, header=None)

    # Set the first column as the index (time series)
    rainfall_data.set_index(0, inplace=True)

    # Assign column names manually, assuming the rest are station indexes
    rainfall_data.columns = [str(col) for col in range(1, len(rainfall_data.columns) + 1)]

    # Extract columns that correspond to valid station indexes
    station_indexes = [col for col in rainfall_data.columns if col.isdigit()]

    # Remap the corresponding station columns
    remapped_columns = []
    valid_columns = []

    for col in station_indexes:
        col = col.strip()  # Remove any leading/trailing whitespace
        if int(col) in remap_dict:
            remapped_columns.append(f'station_{remap_dict[int(col)]}')
            valid_columns.append(col)

    # Subset the DataFrame to include only valid columns
    rainfall_data = rainfall_data[valid_columns]

    # Check again to ensure column length matches the DataFrame columns length
    if len(rainfall_data.columns) == len(remapped_columns):
        rainfall_data.columns = remapped_columns
    else:
        print("Warning: The number of remapped columns does not match the DataFrame columns length.")
        print(f"DataFrame has {len(rainfall_data.columns)} columns, but {len(remapped_columns)} column names were generated.")

    # Step 3: Save the remapped rain mask to a new GeoTIFF file
    with rasterio.open(remapped_rainmask, 'w', **profile) as dst:
        dst.write(remapped_rain_mask.astype(np.int16), 1)

    # Output the remapped rainfall data to a new text file
    rainfall_data.to_csv(remapped_rain_source, sep='\t', index=True)

    print("Remapping complete. Remapped rain mask and rainfall source data saved.")

def geotiff_to_shapefile(geotiff_path, output_shapefile_path):
    # 打开 GeoTIFF 文件
    with rio.open(geotiff_path) as src:
        # 读取第一个波段的数据
        dataMasked = src.read(1, masked=True)  # 使用 masked=True 自动处理无效数据
        mask = ~dataMasked.mask  # 反转掩膜以标识有效数据区域

        # 将掩膜转换为矢量形状
        transform = src.transform
        shapes_generator = shapes(mask.astype(np.uint8), transform=transform)

        # 创建 shapefile schema (字段定义)
        schema = {
            'geometry': 'Polygon',
            'properties': {'value': 'int'}
        }

        # 使用 fiona 打开 shapefile 进行写入
        with fiona.open(output_shapefile_path, mode='w', driver='ESRI Shapefile',
                        crs=src.crs.to_dict(), schema=schema) as output:
            for geom, value in shapes_generator:
                if value == 1:  # 只提取有效区域的形状
                    output.write({
                        'geometry': mapping(shape(geom)),
                        'properties': {'value': int(value)}
                    })
