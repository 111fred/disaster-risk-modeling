'''
Extracts the pixel matrix for of a single roof in a given tif file and creates 
a new tif file for the single roof, processes the raster bands of the new
tif file, and displays each band with a corresponding colorbar.
'''

import json
import random
import pandas as pd
import rasterio
from pyproj import Proj
import numpy as np
from matplotlib import pyplot
from rasterio.plot import show
import raster_brick
import file_names as file

dataset = rasterio.open(file.fpath_tiff)


def write_building_footprint_to_raster(dataset, out_image, polygon, name):
     '''
     Given a numpy array with the pixel values for a given building footprint,
     writes the array back into a raster file so that we can work with each 
     individual frequency band.

     Input:
          dataset (opened dataset object): opened tiff file from which
                                           out_image was extracted from
          out_image (numpy array): an array whose coordinates align with the
                                   polygon building footprint and whose cell
                                   values are the image pixels.
          polygon (dict): a dictionary for a building, containing coordinates
          name (str): name of the output raster file, saved as .tif
     '''

     if len(out_image.shape) > 2:
          c = out_image.shape[0]
          h = out_image.shape[1]
          w = out_image.shape[2]
     else:
          c = 1
          h = out_image.shape[0]
          w = out_image.shape[1]

     with rasterio.Env():
          profile = dataset.profile 
          profile.update( 
              dtype=rasterio.uint8, 
              count=c, 
              height=h, 
              width=w, 
              compress='lzw') 

          with rasterio.open(name, 'w', **profile) as dst:
               dst.update_tags(roof_material=polygon['roof_material'])
               dst.update_tags(bid=polygon['bid'])
               dst.write(out_image.astype(rasterio.uint8))

def open_and_plot_tif(tif_file):
     '''
     Opens the tif file for a single building and plots all color bands.

     Input:
          tif_file(str): file name for a single building
     '''

     tif = rasterio.open(tif_file)

     # to see the entire image
     # show(tif.read())4
     fig, (axr, axg, axb) = pyplot.subplots(1, 3, figsize=(21,7))

     bands = [axr, axg, axb]
     colors = ['inferno', 'gist_earth', 'Blues']
     mapping = dict(zip(bands, colors))
     print(mapping)

     for i, (k, v) in enumerate(mapping.items()):
          im = k.imshow(tif.read(i + 1), cmap=v)
          fig.colorbar(im, ax=k)
          k.title.set_text(v)
     
     pyplot.show()


if __name__ == "__main__":
     '''
     Script that uses a polygon dictionary (with coordinates) and array of
     band pixels, and writes and displays a new tif file for that roof.
     '''

     polygon, out_image = raster_brick.go(return_polygon_and_image=True)

     write_building_footprint_to_raster(dataset, out_image, polygon,
                                        file.building_tif)
     open_and_plot_tif(file.building_tif)
