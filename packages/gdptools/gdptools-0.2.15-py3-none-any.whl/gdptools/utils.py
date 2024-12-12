"""Ancillary function to support core functions in helper.py."""

from __future__ import annotations

import datetime
import json
import logging
import math
import sys
import time
import warnings
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import geopandas as gpd
import geopandas.sindex
import netCDF4
import numpy as np
import numpy.typing as npt
import pandas as pd
import rioxarray as rxr
import xarray as xr
from pyproj import CRS, Transformer
from shapely import centroid
from shapely import get_coordinates
from shapely.geometry import box
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon
from typing import Literal

from pyproj.exceptions import ProjError
from gdptools.data.odap_cat_data import CatClimRItem


logger = logging.getLogger(__name__)

SOURCE_ORIGIN = Literal["source", "target"]


class ReprojectionError(Exception):
    """Custom exception for errors during reprojection."""

    pass


def _check_empty_geometries(gdf: gpd.GeoDataFrame, source_type: SOURCE_ORIGIN) -> None:
    """Checks if the GeoDataFrame contains empty geometries.

    Args:
        gdf (gpd.GeoDataFrame): The GeoDataFrame to be checked.
        source_type (SOURCE_ORIGIN): Indicates the origin of the data, either "source" or "target".

    Raises:
        ReprojectionError: If the GeoDataFrame contains empty geometries.
    """
    print(f"     - checking {source_type} for empty polygons")
    if gdf.is_empty.any():
        raise ReprojectionError(f"{source_type} GeoDataFrame contains empty geometries after reprojection.")


def _check_invalid_geometries(gdf: gpd.GeoDataFrame, source_type: SOURCE_ORIGIN) -> None:
    """Checks if the GeoDataFrame contains invalid geometries.

    Args:
        gdf (gpd.GeoDataFrame): The GeoDataFrame to be checked.
        source_type (SOURCE_ORIGIN): Indicates the origin of the data, either "source" or "target".
    """
    print(f"     - checking the {source_type} polygons for invalid polygons")
    invalid_geoms = gdf[~gdf.is_valid]
    if not invalid_geoms.empty:
        print(f"     - validating reprojected {source_type} polygons")
        _make_valid(gdf)
        # raise ReprojectionError("GeoDataFrame contains invalid geometries after reprojection.")


def _check_grid_file_availability(
    source_crs: Union[int, str, CRS], new_crs: Union[int, str, CRS], source_type: SOURCE_ORIGIN
) -> None:
    """Checks the availability of required grid files for transforming geospatial data.

    This function verifies whether the necessary grid files are accessible for the specified source and target
    coordinate reference systems (CRS). If the required files are not available, it raises a `ReprojectionError` with
    detailed information about the issue.

    Args:
        source_crs (Union[int, str, CRS]): Source CRS as an integer EPSG code, string representation, or pyproj CRS
                                           object.
        new_crs (Union[int, str, CRS]): Target CRS as an integer EPSG code, string representation, or pyproj CRS object.
        source_type (SOURCE_ORIGIN): Indicates the origin of the data, either "source" or "target".

    Raises:
        ReprojectionError: If the required grid files are not available for accurate transformation or if there is a
                           projection error.
    """
    error_message = (
        f"Reprojecting the {source_type} polygons resulted in an error that suggests the user, "
        f"may be behind a firewall that is preventing pyproj for correctly reprojecting the polygons."
        f"The user might try setting PROJ_CURL_CA_BUNDLE env variable, or setting PROJ_NETWORK to OFF."
        f"See PROJ documentation <https://proj.org/en/latest/index.html>"
    )
    try:
        source_crs = CRS.from_user_input(source_crs)
        target_crs = CRS.from_user_input(new_crs)
        transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

        # Attempt a transformation on a sample coordinate
        x, y = transformer.transform(0, 0)
        if x == float("inf") or y == float("inf"):
            raise ReprojectionError(
                f"Required grid files are not available for accurate transformation: {error_message}"
            )
    except ProjError as e:
        error_message = (
            f"Projection error while reprojecting {source_type} polygons: {e}. "
            "Please check the CRS and ensure that the required grid files are available."
        )
        logger.error(error_message)
        raise ReprojectionError(error_message) from e


def _check_reprojection(
    gdf: gpd.GeoDataFrame, new_crs: Union[int, str, CRS], source_crs: Union[int, str, CRS], source_type: SOURCE_ORIGIN
) -> None:
    """Validates the reprojection of a GeoDataFrame by checking for necessary conditions.

    This function ensures that the provided GeoDataFrame is valid for reprojection by checking for grid file
    availability (which leads to inf coordinates if not available), invalid geometries, and empty geometries.
    If any issues are detected, it logs an error and raises a `RuntimeError` with a descriptive message.

    Args:
        gdf (gpd.GeoDataFrame): The GeoDataFrame to be checked for reprojection validity.
        new_crs (Union[int, str, CRS]): Target CRS as an integer EPSG code, string representation, or pyproj CRS object.
        source_crs (Union[int, str, CRS]): Source CRS as an integer EPSG code, string representation, or pyproj CRS
                                           object.
        source_type (SOURCE_ORIGIN): Indicates the origin of the data, either "source" or "target".

    Raises:
        RuntimeError: If there are issues with the reprojection, such as invalid geometries or missing grid files.
    """
    try:
        _check_grid_file_availability(source_crs, new_crs, source_type=source_type)
        _check_invalid_geometries(gdf, source_type=source_type)
        _check_empty_geometries(gdf, source_type=source_type)
    except Exception as e:
        error_message = (
            f"Error during reprojection of the {source_type} polygons."
            f"This can occur when the {source_type} polygons are invalid, or the reprojection failed."
        )
        logger.error(error_message)
        raise RuntimeError(error_message) from e


def _reproject_for_weight_calc(
    target_poly: gpd.GeoDataFrame,
    source_poly: gpd.GeoDataFrame,
    wght_gen_crs: Any,
) -> Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Reprojects source and target GeoDataFrames to a specified CRS and checks for reprojection errors.

    Args:
        target_poly (gpd.GeoDataFrame): The target GeoDataFrame to be reprojected.
        source_poly (gpd.GeoDataFrame): The source GeoDataFrame to be reprojected.
        wght_gen_crs (Any): The CRS to reproject the GeoDataFrames to. This can be an EPSG code, string,
                            or pyproj CRS object.

    Returns:
        Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]: The reprojected target and source GeoDataFrames.

    Raises:
        ReprojectionError: If there are any reprojection errors or issues with the CRS.
    """
    start = time.perf_counter()
    try:
        source_poly_reprojected = _reproject_and_check(
            message="     - reprojecting and validating source polygons",
            geom=source_poly,
            wght_gen_crs=wght_gen_crs,
            source_type="source",
        )
    except ReprojectionError as e:
        logger.error(f"Failed to reproject source polygons: {e}")
        raise
    try:
        target_poly_reprojected = _reproject_and_check(
            message="     - reprojecting and validating target polygons",
            geom=target_poly,
            wght_gen_crs=wght_gen_crs,
            source_type="target",
        )
    except ReprojectionError as e:
        logger.error(f"Failed to reproject target polygons: {e}")
        raise
    end = time.perf_counter()
    print(f"Reprojecting to: {wght_gen_crs} and validating polygons finished in {round(end - start, 2)} seconds")
    return target_poly_reprojected, source_poly_reprojected


def _reproject_and_check(message: str, geom: gpd.GeoDataFrame, wght_gen_crs: Any, source_type: SOURCE_ORIGIN):
    """Reprojects a GeoDataFrame to a specified CRS and checks for reprojection validity.

    This function prints a message, reprojects the provided geometry, and verifies the reprojection's integrity.
    If any issues arise during the reprojection check, an error is logged, and the exception is raised.

    Args:
        message (str): A message to be printed before the reprojection process.
        geom (gpd.GeoDataFrame): The GeoDataFrame containing the geometries to be reprojected.
        wght_gen_crs (Any): The target CRS to which the geometries will be reprojected.
        source_type (SOURCE_ORIGIN): Indicates the origin of the data, either "source" or "target".

    Raises:
        Exception: If there is an error during the reprojection process or the validity check.

    Returns:
        gpd.GeoDataFrame: The reprojected GeoDataFrame.
    """
    print(message)
    # Reproject the source geometry
    result = geom.to_crs(wght_gen_crs)
    try:
        _check_reprojection(result, wght_gen_crs, geom.crs, source_type=source_type)
    except Exception as e:
        logger.error(f"Reprojection error: {e}")
        raise

    return result


def _get_grid_cell_sindex(grid_cells: gpd.GeoDataFrame) -> geopandas.sindex:
    start = time.perf_counter()
    spatial_index = grid_cells.sindex
    # print(type(spatial_index))
    end = time.perf_counter()
    print(f"Spatial index generations finished in {round(end - start, 2)} second(s)")
    return spatial_index


# def _reproject_for_weight_calc(
#     target_poly: gpd.GeoDataFrame,
#     source_poly: gpd.GeoDataFrame,
#     wght_gen_crs: Any,
# ) -> Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
#     start = time.perf_counter()
#     source_poly = source_poly.to_crs(wght_gen_crs)
#     _check_reprojection(source_poly, wght_gen_crs)
#     target_poly = target_poly.to_crs(wght_gen_crs)
#     _check_reprojection(target_poly, wght_gen_crs)
#     end = time.perf_counter()
#     print(f"Reprojecting to epsg:{wght_gen_crs} finished in {round(end-start, 2)}" " second(s)")
#     return target_poly, source_poly


def _check_grid_cell_crs(grid_cells: gpd.GeoDataFrame) -> None:
    if not grid_cells.crs:
        error_string = f"grid_cells don't contain a valid crs: {grid_cells.crs}"
        raise ValueError(error_string)


def _check_feature_crs(poly: gpd.GeoDataFrame) -> None:
    if not poly.crs:
        error_string = f"polygons don't contain a valid crs: {poly.crs}"
        raise ValueError(error_string)


def _check_target_poly_idx(poly: gpd.GeoDataFrame, poly_idx: str) -> None:
    if poly_idx not in poly.columns:
        error_string = f"Error: target_poly_idx ({poly_idx}) is not found in the poly" f" ({poly.columns})"
        raise ValueError(error_string)


def _check_source_poly_idx(poly: gpd.GeoDataFrame, poly_idx: List[str]) -> None:
    for id in poly_idx:
        if id not in poly.columns:
            error_string = f"Error: source_poly_idx ({id}) is not found in the poly" f" ({poly.columns})"
            raise ValueError(error_string)


def _get_print_on(numrows: int) -> int:
    """Return an interval to print progress of run_weights() function.

    Args:
        numrows (int): Number of rows: as in number of polygons

    Returns:
        int: Reasonable interval to print progress statements. Prints at about 10%
    """
    if numrows <= 10:  # pragma: no cover
        print_on = 1
    elif numrows <= 100:
        print_on = 10
    elif numrows <= 1000:
        print_on = 100
    elif numrows <= 10000:
        print_on = 1000
    elif numrows <= 100000:
        print_on = 10000
    else:
        print_on = 50000
    return int(print_on)


def _get_crs(crs_in: Any) -> CRS:
    """Return pyproj.CRS given integer or string.

    Args:
        crs_in (Any): integer: epsg code or pyproj string

    Returns:
        CRS: pyproj.CRS
    """
    # if type(crs_in) == int:
    #     in_crs = CRS.from_epsg(crs_in)
    # elif type(crs_in) == str:
    #     in_crs = CRS.from_proj4(crs_in)
    return CRS.from_user_input(crs_in)


def _get_cells_poly(  # noqa
    xr_a: Union[xr.Dataset, xr.DataArray],
    x: str,
    y: str,
    crs_in: Any,
    verbose: Optional[bool] = False,
) -> gpd.GeoDataFrame:
    """Get cell polygons associated with "nodes" in xarray gridded data.

    Args:
        xr_a (Union[xr.Dataset, xr.DataArray]): _description_
        x (str): _description_
        y (str): _description_
        crs_in (Any): _description_
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Returns:
        gpd.GeoDataFrame: _description_

        grid-cell polygons are calculated as follows:

        1) The polygons surrounding each node, where for each node at
           (i, j) the 4 surrounding polygons tpoly1a, tpoly2a, tpoly3a
           tpoly4a are calculated.

        (i-1, j+1)    (i, j+1)  (i+1, j+1)
            *...........*...........*
            .           .           .
            .           .           .
            . (tpoly3a) . (tpoly2a) .
            .           .           .
            .           .           .
        (i-1, j)      (i, j)    (i+1, j)
            *...........*...........*
            .           .           .
            .           .           .
            . (tpoly4a) . (tpoly1a) .
            .           .           .
            .           .           .
            *...........*...........*
        (i-1, j-1)    (i, j-1)  (i+1, j-1)

        2) The centroid is calculated for each of the 4 polygons
           in step 1, from with the bonding polygon of the node
           is determined.
            *..........*..........*
            .          .          .
            .          .          .
            .    p3----------p2   .
            .    |     .      |   .
            .    |     .      |   .
            *....|.....*......|...*
            .    |     .      |   .
            .    |     .      |   .
            .    p4----------p1   .
            .          .          .
            .          .          .
            *..........*..........*

        The grid-cell polygon surounding the node/vertex at (i, j) is
        [p1, p2, p3, p4, p1]

        This is to account for both rectangular and non-rectangular
        grid geometries.
    """
    tlon = xr_a[x]
    tlat = xr_a[y]
    in_crs = crs_in

    lon, lat = np.meshgrid(tlon, tlat)
    poly = []
    if verbose:
        logger.info("calculating surrounding cell vertices")
    start = time.perf_counter()

    tpoly1a = [
        Polygon(
            [
                [lon[i, j], lat[i, j]],
                [lon[i, j - 1], lat[i, j - 1]],
                [lon[i + 1, j - 1], lat[i + 1, j - 1]],
                [lon[i + 1, j], lat[i + 1, j]],
            ]
        )
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    tpoly2a = [
        Polygon(
            [
                [lon[i, j], lat[i, j]],
                [lon[i + 1, j], lat[i + 1, j]],
                [lon[i + 1, j + 1], lat[i + 1, j + 1]],
                [lon[i, j + 1], lat[i, j + 1]],
            ]
        )
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    tpoly3a = [
        Polygon(
            [
                [lon[i, j], lat[i, j]],
                [lon[i, j + 1], lat[i, j + 1]],
                [lon[i - 1, j + 1], lat[i - 1, j + 1]],
                [lon[i - 1, j], lat[i - 1, j]],
            ]
        )
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    tpoly4a = [
        Polygon(
            [
                [lon[i, j], lat[i, j]],
                [lon[i - 1, j], lat[i - 1, j]],
                [lon[i - 1, j - 1], lat[i - 1, j - 1]],
                [lon[i, j - 1], lat[i, j - 1]],
            ]
        )
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    end = time.perf_counter()
    if verbose:
        logger.info("finished calculating surrounding cell vertices in" f" {round(end - start, 2)} second(s)")

    # print(len(lon_n), len(lat_n), type(lon_n), np.shape(lon_n))
    numcells = len(tpoly1a)
    index = np.array(range(numcells))
    i_index = np.empty(numcells)
    j_index = np.empty(numcells)
    count = 0
    for i in range(1, lon.shape[0] - 1):
        for j in range(1, lon.shape[1] - 1):
            i_index[count] = i
            j_index[count] = j
            count += 1

    if verbose:
        logger.info("calculating centroids")

    start = time.perf_counter()
    # tpoly1 = [Polygon(tpoly1a)]
    p1 = get_coordinates(centroid(tpoly1a))

    # tpoly2 = [Polygon(tpoly2a)]
    p2 = get_coordinates(centroid(tpoly2a))

    # tpoly3 = [Polygon(tpoly3a)]
    p3 = get_coordinates(centroid(tpoly3a))

    # tpoly4 = [Polygon(tpoly4a)]
    p4 = get_coordinates(centroid(tpoly4a))
    end = time.perf_counter()

    if verbose:
        logger.info("finished calculating surrounding cell vertices " f" in {round(end - start, 2)} second(s)")
    lon_point_list = [[p1[i][0], p2[i][0], p3[i][0], p4[i][0]] for i in range(numcells)]
    lat_point_list = [[p1[i][1], p2[i][1], p3[i][1], p4[i][1]] for i in range(numcells)]
    poly = [Polygon(zip(lon_point_list[i], lat_point_list[i])) for i in range(numcells)]  # noqa B905
    df = pd.DataFrame({"i_index": i_index, "j_index": j_index})
    return gpd.GeoDataFrame(df, index=index, geometry=poly, crs=in_crs)


def _build_subset_cat(
    cat_cr: CatClimRItem,
    bounds: Tuple[np.double, np.double, np.double, np.double],
    date_min: str,
    date_max: Optional[str] = None,
) -> Dict[Any, Any]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        cat_cr (CatClimRItem): _description_
        bounds (npt.NDArray[np.double]): _description_
        date_min (str): _description_
        date_max (str, optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """
    xname = cat_cr.X_name
    yname = cat_cr.Y_name
    # print(type(xname), type(yname))
    tname = cat_cr.T_name
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    gridorder = bool(cat_cr.toptobottom)
    if not gridorder:
        return (
            {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: date_min,
            }
            if date_max is None
            else {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: slice(date_min, date_max),
            }
        )

    elif date_max is None:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            tname: date_min,
        }

    else:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            tname: slice(date_min, date_max),
        }


def _read_shp_file(shp_file: Union[str, Path, gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
    """Read shapefile.

    Args:
        shp_file (Union[str, gpd.GeoDataFrame]): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    if isinstance(shp_file, gpd.GeoDataFrame):
        return shp_file.reset_index()
    gdf = gpd.read_file(shp_file)
    return gdf.reset_index()


def _get_shp_file(
    shp_file: gpd.GeoDataFrame, cat_cr: CatClimRItem, is_degrees: bool
) -> Tuple[gpd.GeoDataFrame, Tuple[np.double, np.double, np.double, np.double]]:
    """Return GeoDataFrame and bounds of shapefile.

    Args:
        shp_file (gpd.GeoDataFrame): _description_
        cat_cr (CatClimRItem): _description_
        is_degrees (bool): _description_

    Returns:
        Union[gpd.GeoDataFrame, npt.NDArray[np.double]]: _description_
    """
    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf = shp_file.to_crs(cat_cr.proj)
    # buffer polygons bounding box by twice max resolution of grid
    bbox = box(*gdf.total_bounds)
    # if
    gdf_bounds = bbox.buffer(2.0 * max(cat_cr.resX, cat_cr.resY)).bounds  # type: ignore
    if is_degrees and (gdf_bounds[0] < -180.0) & (gdf_bounds[2] > 180.0):
        newxmax = 180.0 - (abs(gdf_bounds[0]) - 180.0)
        newxmin = -180.0 + (abs(gdf_bounds[2]) - 180.0)
        gdf_bounds = (newxmin, gdf_bounds[1], newxmax, gdf_bounds[3])
        print("Warning: The feature data crosses the anitmeridian.")

    # TODO: need to rethink buffer - leaving it out for now
    # gdf_bounds = gdf.total_bounds.buffer(2.0*buffer)
    return gdf, gdf_bounds


def _is_degrees_nc(ds: xr.Dataset, x_name: str, y_name: str) -> bool:
    """Test if "degree" or "degrees" is present in the units attribute of both X and Y coordinates.

    Args:
        ds (xr.Dataset): The dataset.
        x_name (str): The name of the X coordinate.
        y_name (str): The name of the Y coordinate.

    Returns:
        bool: True if "degree" or "degrees" is present in the units attribute of both X and Y coordinates,
            False otherwise.

    Raises:
        ValueError: If the units attribute is missing from either X or Y coordinate.
    """
    try:
        x_units = ds[x_name].attrs["units"]
        y_units = ds[y_name].attrs["units"]
        if "degree" in x_units.lower() or "degree" in y_units.lower():
            return True
        return False
    except KeyError as e:
        raise ValueError(
            f"Both {x_name} and {y_name} coordinates must have units attribute. Add units to coordinates of the dataset"
        ) from e


def _is_degrees(ds: xr.Dataset, cat_cr: CatClimRItem) -> bool:
    """Test if degrees in attributes on longitude.

    Args:
        ds (xr.Dataset): The dataset.
        cat_cr (CatClimRItem): The CatClimRItem.

    Returns:
        bool: True if "degree" or "degrees" is in the units attribute of both X and Y coordinates, False otherwise.

    Raises:
        ValueError: If the "units" attribute is missing from either X or Y coordinate.
    """
    try:
        x_units = ds[cat_cr.X_name].attrs["units"]
        y_units = ds[cat_cr.Y_name].attrs["units"]
        if "degree" in x_units.lower() or "degree" in y_units.lower():
            return True
        return False
    except KeyError as e:
        raise ValueError(
            f"Both {ds[cat_cr.X_name]} and {ds[cat_cr.Y_name]} coordinates must have units attribute."
        ) from e


def _is_lon_0_360(vals: npt.NDArray[np.double]) -> bool:
    """Test if longitude spans 0-360.

    Args:
        vals (npt.NDArray[np.double]): _description_

    Returns:
        bool: _description_
    """
    result = False
    if (vals[0] > 180.0) & (np.min(vals) > 0.0):
        result = True  # False
    elif (np.max(vals) > 180.0) & (np.min(vals) > 180.0):
        result = True  # False
    elif np.max(vals) > 180.0:
        result = True

    return result


def _get_shp_bounds_w_buffer(
    gdf: gpd.GeoDataFrame,
    ds: Union[xr.DataArray, xr.Dataset],
    crs: Any,
    lon: str,
    lat: str,
) -> npt.NDArray[np.double]:
    """_get_shp_bounds_w_buffer Return bounding box based on 2 * max(ds.dx, ds.dy).

    _extended_summary_

    Args:
        gdf (gpd.GeoDataFrame): _description_
        ds (Union[xr.DataArray, xr.Dataset]): _description_
        crs (Any): _description_
        lon (str): _description_
        lat (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        npt.NDArray[np.double]: _description_
    """
    bbox = box(*gdf.to_crs(crs).total_bounds)
    if bbox.area == np.nan:  # noqa:
        raise ValueError(f"unable to reproject f_feature's projection {gdf.crs} to proj_ds{crs}")
    return np.asarray(
        bbox.buffer(2 * max(max(np.diff(ds[lat].values)), max(np.diff(ds[lon].values)))).bounds  # type: ignore
    )


def _check_for_intersection(
    cat_cr: CatClimRItem,
    gdf: gpd.GeoDataFrame,
) -> Tuple[bool, bool, bool]:
    """Check broadly for intersection between features and grid.

    Args:
        cat_cr (CatClimRItem): _description_
        gdf (gpd.GeoDataFrame): _description_

    Returns:
        Tuple[bool, bool, bool]: _description_
    """
    is_degrees = False
    is_intersect = True
    is_0_360 = False
    ds_url = cat_cr.URL
    ds = xr.open_dataset(ds_url + "#fillmismatch", decode_coords=True, chunks={})
    xvals = ds[cat_cr.X_name]
    yvals = ds[cat_cr.Y_name]
    minx = xvals.values.min()
    maxx = xvals.values.max()
    miny = yvals.values.min()
    maxy = yvals.values.max()
    ds_bbox = box(minx, miny, maxx, maxy)
    bounds = _get_shp_bounds_w_buffer(
        gdf,
        ds,
        cat_cr.crs,
        cat_cr.X_name,
        cat_cr.Y_name,
    )
    is_degrees = _is_degrees(ds=ds, cat_cr=cat_cr)
    if is_degrees & (not ds_bbox.intersects(box(*np.asarray(bounds).tolist()))):
        is_intersect = False
        is_0_360 = _is_lon_0_360(xvals.values)
        if is_0_360:
            warning_string = (
                "0-360 longitude crossing the international date line encountered.\n"
                "Longitude coordinates will be 0-360 in output."
            )
            warnings.warn(warning_string, stacklevel=2)

    return is_intersect, is_degrees, is_0_360


def _check_for_intersection_nc(
    ds: xr.Dataset,
    x_name: str,
    y_name: str,
    proj: Any,
    gdf: gpd.GeoDataFrame,
) -> Tuple[bool, bool, bool]:
    """Check broadly for intersection between features and grid.

    Args:
        ds (xr.Dataset): _description_
        x_name (str): _description_
        y_name (str): _description_
        proj (Any): _description_
        gdf (gpd.GeoDataFrame): _description_

    Returns:
        Tuple[bool, bool, bool]: _description_
    """
    is_degrees = False
    is_intersect = True
    is_0_360 = False

    xvals = ds[x_name]
    yvals = ds[y_name]
    minx = xvals.values.min()
    maxx = xvals.values.max()
    miny = yvals.values.min()
    maxy = yvals.values.max()
    ds_bbox = box(minx, miny, maxx, maxy)
    bounds = _get_shp_bounds_w_buffer(
        gdf,
        ds,
        proj,
        x_name,
        y_name,
    )
    is_degrees = _is_degrees_nc(ds=ds, x_name=x_name, y_name=y_name)
    if is_degrees & (not ds_bbox.intersects(box(*np.asarray(bounds).tolist()))):
        is_intersect = False
        is_0_360 = _is_lon_0_360(xvals.values)
        if is_0_360:
            warning_string = (
                "0-360 longitude crossing the international date line encountered.\n"
                "Longitude coordinates will be 0-360 in output."
            )
            warnings.warn(warning_string, stacklevel=2)

    return is_intersect, is_degrees, is_0_360


def _get_data_via_catalog(
    cat_cr: CatClimRItem,
    bounds: Tuple[np.double, np.double, np.double, np.double],
    begin_date: str,
    end_date: Optional[str] = None,
    rotate_lon: Optional[bool] = False,
) -> xr.DataArray:
    """Get xarray spatial and temporal subset.

    Args:
        cat_cr (CatClimRItem): _description_
        bounds (Tuple[np.double, np.double, np.double, np.double]): _description_
        begin_date (str): _description_
        end_date (Optional[str], optional): _description_. Defaults to None.
        rotate_lon (Optional[bool], optional): _description_. Defaults to False.

    Returns:
        xr.DataArray: _description_
    """
    ds_url = cat_cr.URL
    ds = xr.open_dataset(ds_url + "#fillmismatch", decode_coords=True, chunks={})
    if rotate_lon:
        lon = cat_cr.X_name
        ds.coords[lon] = (ds.coords["lon"] + 180) % 360 - 180
        ds = ds.sortby(ds[lon])

    # get grid data subset to polygons buffered bounding box
    ss_dict = _build_subset_cat(cat_cr, bounds, begin_date, end_date)
    # gridMET requires the '#fillmismatch' see:
    # https://discourse.oceanobservatories.org/
    # t/
    # accessing-data-on-thredds-opendap-via-python-netcdf4-or-xarray
    # -dealing-with-fillvalue-type-mismatch-error/61

    varname = cat_cr.varname
    return ds[varname].sel(**ss_dict)


def _get_weight_df(wght_file: Union[str, pd.DataFrame], poly_idx: str) -> pd.DataFrame:
    if isinstance(wght_file, pd.DataFrame):
        # wghts = wght_file.copy()
        wghts = wght_file.astype({"i": int, "j": int, "wght": float, poly_idx: str})
    elif isinstance(wght_file, str):
        wghts = pd.read_csv(wght_file, dtype={"i": int, "j": int, "wght": float, poly_idx: str})
    else:
        sys.exit("wght_file must be one of string or pandas.DataFrame")
    return wghts


def _date_range(p_start: str, p_end: str, intv: int) -> Iterator[str]:
    """Return a date range.

    Args:
        p_start (str): _description_
        p_end (str): _description_
        intv (int): _description_

    Yields:
        Iterator[str]: _description_
    """
    start = datetime.strptime(p_start, "%Y-%m-%d")
    end = datetime.strptime(p_end, "%Y-%m-%d")
    diff = (end - start) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y-%m-%d")
    yield end.strftime("%Y-%m-%d")


def _get_catalog_time_increment(param: dict) -> Tuple[int, str]:  # type: ignore
    interval = str(param.get("interval")).split(" ")
    return int(interval[0]), str(interval[1])


def _get_dataframe(object: Union[str, pd.DataFrame]) -> pd.DataFrame:
    if isinstance(object, str):
        return pd.DataFrame.from_dict(json.loads(object))
    else:
        return object


def _get_default_val(native_dtype: np.dtype):  # type: ignore
    """Get default fill value based on gridded data dtype.

    Args:
        native_dtype (np.dtype): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """
    if native_dtype.kind == "i":
        dfval = netCDF4.default_fillvals["i8"]
    elif native_dtype.kind == "f":
        dfval = netCDF4.default_fillvals["f8"]
    else:
        raise TypeError(
            "gdptools currently only supports int and float types." f"The value type here is {native_dtype}"
        )

    return dfval


def _get_interp_array(
    n_geo: int,
    nts: int,
    native_dtype: Union[np.dtype[np.double], np.dtype[np.int_]],
    default_val: Any,
) -> Union[npt.NDArray[np.int_], npt.NDArray[np.double]]:
    """Get array for interpolation based on the dtype of the gridded data.

    _extended_summary_

    Args:
        n_geo (int): Number of polygons in target geometry
        nts (int): Number of time steps in gridded data
        native_dtype (np.dtype): Gridded data data type
        default_val (Any): _description_

    Raises:
        TypeError: _description_

    Returns:
        Union[npt.NDArray[np.int], npt.NDArray[np.double]]: _description_
    """
    if native_dtype.kind == "i":
        # val_interp = np.empty((nts, n_geo), dtype=np.dtype("int64"))
        val_interp = np.full((nts, n_geo), dtype=np.dtype("int64"), fill_value=default_val)
    elif native_dtype.kind == "f":
        # val_interp = np.empty((nts, n_geo), dtype=np.dtype("float64"))
        val_interp = np.full((nts, n_geo), dtype=np.dtype("float64"), fill_value=default_val)
    else:
        raise TypeError(
            "gdptools currently only supports int and float types." f"The value type here is {native_dtype}"
        )

    return val_interp


def _get_top_to_bottom(data: Union[xr.Dataset, xr.DataArray], y_coord: str) -> bool:
    """Get orientation of y-coordinate data in xarray Dataset.

    Args:
        data (xr.Dataset): _description_
        y_coord (str): _description_

    Returns:
        bool: _description_
    """
    yy = data.coords[y_coord].values
    return yy[0] <= yy[-1]


def _get_xr_dataset(ds: Union[str, xr.Dataset]) -> xr.Dataset:
    """Get xarray.Dataset."""
    if isinstance(ds, str):
        return xr.open_dataset(ds + "#fillmismatch", decode_coords=True, chunks={})
    if isinstance(ds, Path):
        return xr.open_dataset(ds, decode_coords=True, chunks={})
    elif isinstance(ds, xr.Dataset):
        return ds
    elif isinstance(ds, xr.DataArray):
        raise TypeError("Expected xarray.Dataset, not xarray.DataArray")
    else:
        raise TypeError("Invalid xarray dataset, must be a URL or xarray Dataset")


def _get_rxr_dataset(ds: Union[str, xr.DataArray, xr.Dataset]) -> Union[xr.DataArray, xr.Dataset]:
    """Get xarray.Dataset."""
    if isinstance(ds, (xr.Dataset, xr.DataArray)):
        return ds
    elif isinstance(ds, str):
        try:
            # Attempt to open the dataset
            return rxr.open_rasterio(ds)
        except Exception as e:
            # Return a useful error message
            return f"Failed to open dataset from '{ds}'. Error: {e}"
    else:
        # Handle cases where ds is neither a Dataset/DataArray nor a string
        return f"Unsupported type for ds: {type(ds)}. Expected str, xr.DataArray, or xr.Dataset."


def _interpolate_sample_points(
    geom: gpd.GeoSeries, spacing: Union[float, int], calc_crs: Any, crs: Any
) -> Tuple[npt.NDArray[np.double], npt.NDArray[np.double], npt.NDArray[np.double]]:
    """Interpolated points at equal distances along a line.

    Return the interpolated points and their distances from the initial point.

    Args:
        geom (gpd.GeoSeries): Line geometry to pull sample points from.
        spacing (Union[float, int]): The distance in meters between the sample points.
        calc_crs (Any): Coordinate system to calculate interpolated points and distance.
        crs (Any): Coordinate system to return the points in. EPSG code or Proj 4 string.

    Returns:
        Tuple[npt.NDArray[np.double], npt.NDArray[np.double], npt.NDArray[np.double]]:
        x (npt.NDArray[np.double]): Array of x coordinates of the sample points.
        y (npt.NDArray[np.double]): Array of y coordinates of the sample points.
        dist (npt.NDArray[np.double]): Array of distances from the first point to each of the sample points.

    Raises:
        Exception: For any other errors encountered during reprojection.
    """
    # Reproject twice prevents inf values
    # rp_geom: gpd.GeoSeries = geom.to_crs(calc_crs)
    rp_geom: gpd.GeoSeries = geom.to_crs(calc_crs)
    try:
        _check_reprojection(rp_geom, calc_crs, geom.crs, source_type="source")
    except Exception as e:
        logger.error(f"Reprojection error: {e}")
        raise
    # Get line length
    length = rp_geom.length.values[0]
    # Calculate the number of sample points
    num_points = int(length / spacing) + 1
    # Create empty numpy arrays for x,y coords
    x = np.zeros(num_points, dtype=np.double)
    y = np.zeros(num_points, dtype=np.double)
    dist = np.zeros(num_points, dtype=np.double)
    # Find sample points on line  # from nldi_xstools.PathGen
    d = 0.0
    index = 0
    while d < length:
        point = rp_geom.interpolate(d)
        # Project to grid crs
        point = point.to_crs(crs)
        # x[index] = point.x
        # y[index] = point.y
        # fix for FutureWarning
        x[index] = float(point.iloc[0].x)
        y[index] = float(point.iloc[0].y)
        dist[index] = d
        d += spacing
        index += 1

    return x, y, dist


def _get_line_vertices(geom: gpd.GeoDataFrame, calc_crs: Any, crs: Any) -> Tuple[list[float], list[float], list[float]]:
    """Return the vertices and the distance inbetween of a line in a GeoDataFrame.

    Args:
        geom (GeoDataFrame): A GeoDataFrame with a single line geometry
        calc_crs(Any): Coordinate system to calculate vertex distance.
        crs (Any): Coordinate system to return the points in. EPSG code or Proj 4 string.

    Returns:
        Tuple[list[float], list[float], list[float]]: Three list containing the x coords,
            y coords and distance in meters from the first vertex to each vertex

    Raises:
        Exception: For any other errors encountered during reprojection.
    """
    # project to equidistant crs to calculate distance between vertices
    rp_geom: gpd.GeoSeries = geom.to_crs(calc_crs).reset_index()
    try:
        _check_reprojection(rp_geom, calc_crs, geom.crs, "source")
    except Exception as e:
        logger.error(f"Reprojection error: {e}")
        raise
    if type(rp_geom.geometry[0]) is LineString:
        x, y = rp_geom.geometry[0].coords.xy
    else:  # If it is a multilinestring:
        x, y = rp_geom.geometry[0].geoms[0].coords.xy
    x = list(x)
    y = list(y)

    # cal distance between the first vertex and each vertex
    for i in range(len(x)):
        if i == 0:
            dist = [0.0]
        else:
            d = dist[i - 1] + math.dist([x[i - 1], y[i - 1]], [x[i], y[i]])
            dist.append(d)

    # Project line to grid crs and export vertex coords
    rp_geom: gpd.GeoSeries = geom.to_crs(crs).reset_index()
    if type(rp_geom.geometry[0]) is LineString:
        x, y = rp_geom.geometry[0].coords.xy
    else:  # If it is a multilinestring:
        x, y = rp_geom.geometry[0].geoms[0].coords.xy
    x = list(x)
    y = list(y)

    return x, y, dist


def _cal_point_stats(
    data: Union[xr.DataArray, xr.Dataset],
    stat: str,
    userdata_type: str,
    skipna: Union[bool, None] = None,
) -> dict[Any]:
    """Calculate the specified stats from a geodataframe of points.

    Args:
        data: (Union[xr.DataArray, xr.Dataset]): Xarray DataArray or Dataset of values pulled from
            a gridded dataset at interpolated points
        stat (str): A string indicating which statistics to calculated.
            Options: all, mean, median, std, min, max
        userdata_type (str): A string indicating the type of the User Data Class. Options
            are 'UserCatData', 'ClimRCatData', 'UserTiffData', 'NHGFStacData'.
        skipna (bool or None): Optional; If True, skip nodata values in the gridded
            data for the calculations of statistics. By default, only skips missing
            values for float dtypes.

    Returns:
        dict: A dictionary of statistical values
    """
    out_vals: dict[Any] = {}

    # Calculate the stats
    if userdata_type != "UserTiffData":
        userdata_type = "other"

    stat = ["mean", "median", "std", "min", "max"] if stat == "all" else [stat]

    options = {
        "UserTiffData": {
            "mean": data.mean(dim=["pt"], skipna=skipna).values,
            "median": data.median(dim=["pt"], skipna=skipna).values,
            "std": data.std(dim=["pt"], skipna=skipna).values,
            "min": data.min(dim=["pt"], skipna=skipna).values,
            "max": data.max(dim=["pt"], skipna=skipna).values,
        },
        "other": {
            "mean": data.mean(dim=["pt"], skipna=skipna),
            "median": data.median(dim=["pt"], skipna=skipna),
            "std": data.std(dim=["pt"], skipna=skipna),
            "min": data.min(dim=["pt"], skipna=skipna),
            "max": data.max(dim=["pt"], skipna=skipna),
        },
    }

    for i in stat:
        out_vals[i] = options[userdata_type][i]

    return out_vals


def _buffer_line(
    geometry: gpd.GeoSeries,
    buffer: Union[float, int],
    proj_feature: CRS,
    calc_crs: Any,
) -> gpd.GeoSeries:
    """Buffer a line segment.

    The line gets reprojected to an AEA projection, so that the buffer can be
    submitted in meters. Then the buffered geometry it reprojected back to
    a user specified crs.

    Args:
        geometry (GeoSeries): Geometry of the query line
        buffer (float): Value in meters of the diameter of the buffer
        proj_feature (CRS): Coordinate system of the returned buffer geometry
        calc_crs: Coordinate system in which to perform the statistical calculations

    Returns:
        new_geometry (GeoSeries): Geometry of the buffer
    """
    return geometry.to_crs(calc_crs).buffer(buffer).to_crs(proj_feature)


def _dataframe_to_geodataframe(df: pd.DataFrame, crs: str) -> gpd.GeoDataFrame:
    """Convert pandas Dataframe to Geodataframe."""
    geometry = [Point(xy) for xy in zip(df.x, df.y)]  # noqa: B905
    try:
        df = df.drop(["x", "y", "crs"], axis=1)
    except KeyError:
        df = df.drop(["x", "y"], axis=1)

    return gpd.GeoDataFrame(df, geometry=geometry, crs=crs)


def _process_period(period: List[Optional[Union[str, pd.Timestamp, datetime.datetime]]]) -> List[str]:
    """Process the period list and convert elements to pd.Timestamp.

    Args:
        period: A list of elements representing a time period. Each element can be a string,
            pd.Timestamp, datetime.datetime, or None.

    Returns:
        List[pd.Timestamp]: A list of pd.Timestamp objects representing the processed period.

    Raises:
        ValueError: If period is not a list or if it does not contain 1 or 2 elements.
        ValueError: If the elements of period are not of the expected types.

    Examples:
        >>> _process_period(['2022-01-01', '2022-01-31'])
        [Timestamp('2022-01-01 00:00:00'), Timestamp('2022-01-31 00:00:00')]
    """
    # Check if period is a list
    if not isinstance(period, list):
        raise ValueError("period must be a list")

    # Check if the list contains 1 or 2 elements
    if len(period) not in [1, 2]:
        raise ValueError("period must contain 1 or 2 elements")

    # Convert strings to datetime and validate elements
    result = []
    for element in period:
        if isinstance(element, str):
            result.append(element)
        elif isinstance(element, datetime.datetime):
            result.append(element.isoformat())
        elif isinstance(element, pd.Timestamp) or element is None:
            result.append(element.isoformat())
        else:
            raise ValueError("Elements of period must be string, pd.Timestamp, datetime.datetime, or None")

    return result


def _make_valid(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Convert invalid geometries in a GeoDataFrame to valid ones.

    This function checks for invalid geometries in the provided GeoDataFrame.
    For invalid geometries, it uses the buffer trick (buffering by a distance of 0)
    to attempt to convert them into valid geometries. This approach is based on
    the method in Shapely and has been adapted for this specific use case.

    Note: It's recommended to use this function with caution, as the buffer trick
    might not always produce the desired results for all types of invalid geometries.

    Adapted from Shapely:
    Copyright (c) 2007, Sean C. Gillies. 2019, Casper van der Wel. 2007-2022,
    Shapely Contributors. All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Args:
        df (gpd.GeoDataFrame): A GeoDataFrame containing the geometries to be validated.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame with invalid geometries made valid. If no
                          invalid geometries are found, the original GeoDataFrame
                          is returned unchanged.
    """
    polys = ["Polygon", "MultiPolygon"]
    if df.geom_type.isin(polys).all():
        mask = ~df.geometry.is_valid
        print(f"     - fixing {len(mask[mask])} invalid polygons.")
        col = df._geometry_column_name
        df.loc[mask, col] = df.loc[mask, col].buffer(0)
    return df
