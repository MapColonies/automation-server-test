""" configuration for running ingestion tests"""
from mc_automation_tools import common

ORIG_DISCRETE_PATH = common.get_environment_variable('ORIG_DISCRETE_PATH', '/home/ronenk1/dev/automation-server-test/shp/1')
SHAPES_PATH = common.get_environment_variable('SHAPES_PATH', 'Shapes')
TIFF_PATH = common.get_environment_variable('TIFF_PATH', 'tiff')
# SHAPE_FILE_LIST = ['Files.dbf', 'Product.shp', 'Product.dbf', 'ShapeMetadata.shp', 'ShapeMetadata.dbf']
SHAPE_FILE_LIST = ['Files.shp', 'Files.dbf', 'Product.shp', 'Product.dbf', 'ShapeMetadata.shp', 'ShapeMetadata.dbf']