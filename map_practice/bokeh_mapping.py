"""
This file is to visualize lat,lon in Bokeh

"""


import pyproj
import json
import numpy as np

from toolz import curry, get, compose, mapcat

from bokeh.tile_providers import CARTODBPOSITRON_RETINA
from bokeh.io import show
from bokeh.plotting import figure as bokeh_figure

from shapely.geometry import Point, Polygon, MultiPolygon, MultiPoint, shape
from shapely.ops import transform
from shapely.wkt import loads as wkt_loads

listmap = compose(list, map)
listfilter = compose(list, filter)
listmapcat = compose(list, mapcat)

get_shape = curry(get)("shape")

lonlat = pyproj.Proj(init='epsg:4326')
tmerc = pyproj.Proj(init='epsg:3857')
lonlat2tmerc_proj = curry(pyproj.transform)(lonlat)(tmerc)
lonlat2tmerc = curry(transform)(lonlat2tmerc_proj)

def strip_geometries(map_data):
    map_shapes = listmap(lambda x: wkt_loads(get_shape(x)), map_list)
    points = listfilter(lambda x: x.type == "Point", map_shapes)
    polygons = listfilter(lambda x: x.type == "Polygon", map_shapes)

    multipoints = listfilter(lambda x: x.type == "MultiPoint", map_shapes)
    multipolygons = listfilter(lambda x: x.type == "MultiPolygon", map_shapes)

    return points+multipoints, polygons+multipolygons


def get_circles(points):

    points_x = listmap(lambda x: x.coords[0][0], points)
    points_y = listmap(lambda y: y.coords[0][1], points)

    return points_x, points_y

def get_patches(polygons):

    polygon_x = listmap(lambda x: listmap(curry(get)(0), x.exterior.coords), polygons)
    polygon_y = listmap(lambda x: listmap(curry(get)(1), x.exterior.coords), polygons)

    return polygon_x, polygon_y

def map_plot(map_data):

    points, polygons = trip_geometries(map_data)

    tmerc_points = listmap(lonlat2tmerc, points)
    tmerc_polygons = listmap(lonlat2tmerc, polygons)

    points_x, points_y = listmapcat(get_circles, tmerc_points)
    polygons_x, polygons_y = listmapcat(get_patches, tmerc_polygons)

    max_x = max(points_x + listmap(max, polygons_x))
    max_y = max(points_y + listmap(max, polygons_y))
    min_x = min(points_x + listmap(min, polygons_x))
    min_y = min(points_y + listmap(min, polygons_y))

    map_figure = bokeh_figure(
        tools="pan,wheelzoom, reset",
        plot_width=plot_width,
        plot_height=plot_height,
        x_range=[min_x, max_x],
        y_range=[min_y, max_y],

    )

    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # Now add the map tiles.
    map_figure.add_tile(tiles)

    map_figure.circle(x=points_x,
                      y=points_y,
                      alpha=listmapcat(curry(get)("alpha", 0.1), points),
                      color=listmapcat(curry(get)("color", "black"), points)
                      )

    map_figure.patches(x=polygons_x,
                       y=polygons_y,
                       alpha=listmapcat(curry(get)("alpha", 0.1), polygons_x),
                       color=listmapcat(curry(get)("color", "blue"), polygons_y)
                      )

    return map_figure
