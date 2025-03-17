'''
Local file names
'''
current_user = 't'

if current_user == 't':
    fpath_tiff = '/Users/Tammy/Documents/_MSCAPP/Fall 2019/Unsupervised ML/' \
                   'Final Project/stac/colombia/borde_rural/borde_rural_' \
                   'ortho-cog.tif'
    fpath_geojson = '/Users/Tammy/Documents/_MSCAPP/Fall 2019/Unsupervised ML/' \
                    'Final Project/stac/colombia/borde_rural/train-borde_rural' \
                    '.geojson'

if current_user == 'j':
    fpath_tiff = '/Users/jamesjensen/Documents/harris/q1_20/UML/Project/stac/' \
                 'colombia/borde_rural/borde_rural_ortho-cog.tif'
    fpath_geojson = '/Users/jamesjensen/Documents/harris/q1_20/UML/Project/' \
                    'stac/colombia/borde_rural/train-borde_rural.geojson'

crs = 'epsg:32618'
building_tif = 'BIGTST.tif'