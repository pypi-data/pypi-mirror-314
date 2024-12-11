"""Tests for reprojection method."""

import pytest
from shapely.geometry import Polygon, Point, LineString
import geopandas as gpd
from gdptools.utils import _reproject_for_weight_calc, ReprojectionError, _check_reprojection


def test_reproject_for_weight_calc_valid():
    """Test valid reprojection of target and source polygons."""
    target_poly = gpd.GeoDataFrame({"geometry": [Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])]}, crs="EPSG:4326")
    source_poly = gpd.GeoDataFrame({"geometry": [Polygon([(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)])]}, crs="EPSG:4326")
    wght_gen_crs = "EPSG:3857"
    try:
        target_poly_reprojected, source_poly_reprojected = _reproject_for_weight_calc(
            target_poly, source_poly, wght_gen_crs
        )
        assert not target_poly_reprojected.empty and not source_poly_reprojected.empty
    except ReprojectionError:
        pytest.fail("ReprojectionError raised unexpectedly!")


def test_check_reprojection_valid_polygon():
    """Test checking of valid reprojected polygon geometry."""
    geom = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")
    new_crs = "EPSG:3857"
    try:
        _check_reprojection(gdf, new_crs, gdf.crs, "source")
    except ReprojectionError:
        pytest.fail("ReprojectionError raised unexpectedly!")


def test_check_reprojection_valid_point():
    """Test checking of valid reprojected point geometry."""
    geom = Point(0, 0)
    gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")
    new_crs = "EPSG:3857"
    try:
        _check_reprojection(gdf, new_crs, gdf.crs, "source")
    except ReprojectionError:
        pytest.fail("ReprojectionError raised unexpectedly!")


def test_check_reprojection_valid_linestring():
    """Test checking of valid reprojected LineString geometry."""
    geom = LineString([(0, 0), (1, 1)])
    gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")
    new_crs = "EPSG:3857"
    try:
        _check_reprojection(gdf, new_crs, gdf.crs, "source")
    except ReprojectionError:
        pytest.fail("ReprojectionError raised unexpectedly!")


def test_check_reprojection_empty_geometries():
    """Test checking of empty geometries should raise ReprojectionError."""
    geom = Polygon([])
    gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")
    new_crs = "EPSG:3857"
    with pytest.raises(RuntimeError):
        _check_reprojection(gdf, new_crs, gdf.crs, "source")


def test_check_reprojection_missing_grids():
    """Test checking of geometries with missing grid files should raise ReprojectionError."""
    # This test assumes that the necessary grid files are not available, which might be difficult to simulate.
    # Instead, we can simulate the exception.
    geom = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")
    new_crs = "+proj=unknown"
    with pytest.raises(RuntimeError):
        _check_reprojection(gdf, new_crs, gdf.crs, "source")
