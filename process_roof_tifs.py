'''
DESCRIPTION HERE
'''
import json
import random
import pandas as pd
import numpy as np
from matplotlib import pyplot
import rasterio
import rasterstats
from pyproj import Proj
from rasterio.mask import mask
from rasterio.plot import show
import raster_brick
import raster_bands
import file_names as file


proj = Proj(init=file.crs)
dataset = rasterio.open(file.fpath_tiff_t)


def get_zonal_stats_JJ_TEST(roof_tif_file):
     ''' 
     Given a single roof tif file return the corresponding feature matrix
     
     This is james' test version. I'm recreating the functionality of the zonal_stats function
     to see what it actually does -- by comparing the output of this function and that of 
     get_zonal_stats() you can see that the zonal_stats method from rasterstats package drops NO DATA,
     which is represented as a 0 in the array. 
     '''

     df = pd.DataFrame()
     tif = rasterio.open(roof_tif_file)

     for i in range(len(tif.colorinterp)):
          
          raster = tif.read(i+1)
          min = raster.min()
          max = raster.max()
          avg = np.mean(raster)
          med = np.median(raster)

          df[i] = pd.Series(med)

     df['roof'] = tif.tags()['roof_material']
     df.set_index('roof', inplace=True)

     return df



def get_zonal_stats(polygon, tif_file):
     ''' 
     Given a single polygon and the path to the corresponding tif file,
     calculates zonal stats for the shape outlined by the polygon and returns
     them as a dataframe.
     '''

     df = pd.DataFrame()

     for i in range(1,4):
     
          tats = rasterstats.zonal_stats(polygon,
               tif_file,
               stats=['min', 'max', 'median', 'majority', 'sum'],
               band=i)

          df[i] = pd.Series(tats[0]['median'])

     df['roof'] = polygon['roof_material']
     df.set_index('roof', inplace=True)

     return df



def go(limit=1):
     '''
     Returns a feature matrix where a row represents a single roof and the columns
     represent the zonal statistic for each raster band. The zonal stats for a given
     polygon are calcualted by calling get_zonal_stats(). The limit determines the number
     of roofs to include in the matrix.
     '''

     geojson = raster_brick.load_geojson(file.fpath_geojson_t)
     polygons = raster_brick.make_polgyons(geojson)
     rv = pd.DataFrame()

     for i, polygon in enumerate(polygons):
          if i < limit:
               polygon['coordinates'] = raster_brick.transform_coordinates(polygon['coordinates'], proj)
               df = get_zonal_stats(polygon, file.fpath_tiff_t)
               frames = [rv, df]
               rv = pd.concat(frames)

     return rv


