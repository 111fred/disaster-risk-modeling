'''
Reads a geojson and geotiff file, extracts relevant information for one
randomly selected rooftop, and displays the single rooftop as an image.
'''

import json
import random
from matplotlib import pyplot
import rasterio
from pyproj import Proj
from rasterio.mask import mask
from rasterio.plot import show
import file_names as file

# Run this magic command in ipython to print out roof: %matplotlib osx

proj = Proj(init=file.crs)


def load_geojson(file_path):
    '''
    Given path to geojson file returns the geojson, which is of type
    dictionary that stores the building id, roof material (for training
    purposes), and cooridinates of the building.

    Input:
        file_path (str): local path to geojson file

    Output:
        geojson (dict): dictionary containing building id, roof material,
                        and coordinates for all buildings in a single file
    '''

    with open(file_path) as gj:
        geojson = json.load(gj)

    return geojson
    
def make_polygons(geojson):
    '''
    Given a full geojson dictionary, extracts relevant information for each
    building, including type, building id, roof material, and coordinates.
    Returns a list of dictionaries, where each dictionary maps a building by
    these features.

    Input:
        geojson (dict): full geojson dictionary

    Output:
        polygons (lst): a list of dictionaries (one per building)
    '''

    polygons = []

    for feature in geojson['features']:
        polygon = {}
        polygon['type'] = feature['geometry']['type']
        polygon['bid'] = feature['id']
        polygon['roof_material'] = feature['properties']['roof_material']
        polygon['coordinates'] = feature['geometry']['coordinates']
        polygons.append(polygon)

    return polygons

def transform_coordinates(coordinates_lists, transform):
    '''
    Given a list of lists of coordinates for a single building (extracted
    from a geojson), executes an affine transformation on each coordinate pair
    to output a new coordinate pair based on a provided coordinate reference
    system (crs) from the corresponding geotiff file.

    Input:
        coordinates_list (lst of lsts): a list of lists of coordinate pairs
        transform (class instance): an initialized Proj class instance that
                                    performs cartographic transformations

    Output:
        transformed_coordinate_lists (lst of lsts): a transformed list of lists
                                                    of coordinate pairs
    '''
    
    transformed_coordinates_lists = []
    
    for coordinates_list in coordinates_lists:
        inner_coord_list = []
        for coordinate in coordinates_list:
            transformed_coordinate = list(transform(coordinate[0],
                                                    coordinate[1]))
            inner_coord_list.append(transformed_coordinate)
        transformed_coordinates_lists.append(inner_coord_list)
    
    return transformed_coordinates_lists

def get_rooftop_array_after_mask(tiff_path, polygon, projection):
    '''
    Given a dictionary containing transformed coordinates for one roof and a
    initialized Proj class instance to perform cartographic transformations,
    returns an array of arrays, each one providing a numeric value for each
    pixel in the image for a specific band (in this case, 4 matrices for 4
    bands).

    Eg. Values from 0-255 correspond with the color scale.

    Input:
        tiff_path (str): path to the tif file
        polygon (dict): a dictionary of features including coordinates for a
                        single building
        projection (class instance): an initialized Proj class instance that
                                     performs cartographic transformations

    Output:
        out_image (numpy array): a numpy of values per pixel for each
                                 band (one per image layer)
    '''

    with rasterio.open(tiff_path) as tiff:
        out_image, out_transform = mask(tiff, [polygon], crop=True)

    return out_image
    
def display_single_roof(out_image):
    '''
    Given a numpy array for a single roof, displays the image using matplot.

    Input:
        out_image (array): array of array of pixel values (one per band)
    '''

    show(out_image)

def go(return_polygon_and_image=False):
    '''
    Script that reads a geojson and geotiff file, extracts relevant information
    for one randomly selected rooftop, and displays the single rooftop as a
    complete image.
    '''

    geojson = load_geojson(file.fpath_geojson)
    polygons = make_polygons(geojson)

    idx = random.randint(0,len(polygons))
    polygon = polygons[idx] # gets single rooftop at random

    polygon['coordinates'] = transform_coordinates(polygon['coordinates'],
                                                   proj)
    out_image = get_rooftop_array_after_mask(file.fpath_tiff, polygon, proj)
    
    if not return_polygon_and_image:
        display_single_roof(out_image)
    else:
        return polygon, out_image
        

if __name__ == "__main__":
    '''
    Script that reads a geojson and geotiff file, extracts relevant information
    for one randomly selected rooftop, and displays the single rooftop as a
    complete image.
    '''
    go()
