"""Testing ancillary functions."""

import datetime
import gc
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import pytest
import xarray as xr
from pyproj import CRS
from pyproj.exceptions import CRSError

from gdptools.data.odap_cat_data import CatClimRItem
from gdptools.utils import _buffer_line
from gdptools.utils import _cal_point_stats
from gdptools.utils import _check_for_intersection
from gdptools.utils import _get_cells_poly
from gdptools.utils import _get_crs
from gdptools.utils import _get_data_via_catalog
from gdptools.utils import _get_line_vertices
from gdptools.utils import _get_rxr_dataset
from gdptools.utils import _get_shp_file
from gdptools.utils import _get_xr_dataset
from gdptools.utils import _interpolate_sample_points
from gdptools.utils import _process_period


@pytest.mark.parametrize(
    "crs",
    [
        "epsg:4326",
        4326,
        "+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs",
    ],
)
def test__get_crs(crs: Any) -> None:
    """Test the get_crs function."""
    crs = _get_crs(crs)
    assert isinstance(crs, CRS)


@pytest.mark.parametrize(
    "crs",
    [
        "espg:4326",
        43,
        "+a=6378137 +f=0.00335281066474748 +pm=0 +no_defs",
    ],
)
def test__get_bad_crs(crs: Any) -> None:
    """Test the get_crs function."""
    with pytest.raises(CRSError):
        crs = _get_crs(crs)


@pytest.fixture(scope="function")
def cat_data() -> CatClimRItem:
    """Create a CatClimRItem object from OpenDAP data."""
    _id = "gridmet"  # noqa
    _varname = "daily_maximum_temperature"  # noqa
    cat_url = "https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet"
    climr: pd.DataFrame = pd.read_parquet(cat_url)
    data_dict: dict[str, Any] = climr.query("id == @_id & varname == @_varname").to_dict("records")[0]
    cat_cr = CatClimRItem(
        URL=data_dict["URL"],
        varname=data_dict["varname"],
        T_name=data_dict["T_name"],
        units=str(data_dict["units"]),
        X_name=data_dict["X_name"],
        Y_name=data_dict["Y_name"],
        proj=data_dict["crs"],
        resX=data_dict["resX"],
        resY=data_dict["resY"],
        toptobottom=data_dict["toptobottom"],
        crs=data_dict["crs"],
    )
    yield cat_cr
    del cat_cr
    gc.collect()


@pytest.fixture(scope="function")
def gdf() -> gpd.GeoDataFrame:
    """Create xarray dataset."""
    return gpd.read_file("./tests/data/hru_1210_epsg5070.shp")


@pytest.fixture(scope="function")
def is_degrees(gdf, cat_data) -> bool:  # type: ignore
    """Check if coords are in degrees."""
    is_degrees: bool
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(cat_cr=cat_data, gdf=gdf)
    return is_degrees


@pytest.fixture(scope="function")
def bounds(gdf, cat_data, is_degrees) -> npt.NDArray[np.double]:  # type: ignore
    """Get bounds."""
    bounds: npt.NDArray[np.double]
    gdf, bounds = _get_shp_file(gdf, cat_data, is_degrees)
    return bounds


@pytest.fixture(scope="function")
def xarray(cat_data, bounds) -> xr.DataArray:  # type: ignore
    """Create xarray dataset."""
    data: xr.DataArray = _get_data_via_catalog(cat_data, bounds, "2020-01-01")
    yield data
    del data
    gc.collect()


def test_get_cells_poly(cat_data, bounds) -> None:  # type: ignore
    """Test _get_cells_poly."""
    ds: xr.DataArray = _get_data_via_catalog(cat_data, bounds, "2020-01-01")
    print(ds)
    assert isinstance(ds, xr.DataArray)
    gdf = _get_cells_poly(xr_a=ds, x="lon", y="lat", crs_in=4326)
    assert isinstance(gdf, gpd.GeoDataFrame)


def test_interpolate_sample_points() -> None:
    """Test the interpolate function."""
    lines = gpd.read_file("./tests/data/test_lines.json")
    line = lines.loc[[1]].geometry.copy()
    test_geom = line.geometry.to_crs(5070)
    x, y, dist = _interpolate_sample_points(test_geom, 500, 6933, 5070)
    assert x[1] == pytest.approx(244728.49925291, 0.001)
    assert y[2] == pytest.approx(2090852.4680706703, 0.001)
    assert dist[1] == 500.0


def test_buffer_line() -> None:
    """Test the buffer line function."""
    lines = gpd.read_file("./tests/data/test_lines.json")
    buffered_lines = _buffer_line(lines.geometry, 500, lines.crs, 5070)
    assert buffered_lines[0].area == pytest.approx(0.0014776797476285766, 0.0001)
    assert buffered_lines[0].length == pytest.approx(0.269159, 0.0001)
    assert buffered_lines[1].area == pytest.approx(0.00024249232348514231, 0.0001)
    assert buffered_lines[1].length == pytest.approx(0.066633, 0.0001)


def test_get_line_vertices() -> None:
    """Test the get line vertices function."""
    lines = gpd.read_file("./tests/data/test_lines.json")
    x, y, dist = _get_line_vertices(lines.loc[[1]], 6933, 4269)
    assert len(x) == 133
    assert y[10] == pytest.approx(41.78631166847265, 0.0001)
    assert dist[20] == pytest.approx(196.86121507146711, 0.0001)


def test_cal_point_stats() -> None:
    """Test the calculate point stats function."""
    pts_ds = xr.open_dataset("./tests/data/test_points.nc")
    pts_stats = _cal_point_stats(pts_ds, "all", "None")
    assert len(pts_stats) == 5
    assert pts_stats["mean"].daily_minimum_temperature[0] == pytest.approx(250.44398161, 0.0001)
    assert pts_stats["median"].daily_minimum_temperature[0] == pytest.approx(250.44887729826468, 0.0001)
    assert pts_stats["std"].daily_minimum_temperature[0] == pytest.approx(0.01882221687947004, 0.0001)
    assert pts_stats["min"].daily_minimum_temperature[0] == pytest.approx(250.40337893675422, 0.0001)
    assert pts_stats["max"].daily_minimum_temperature[0] == pytest.approx(250.46755475563168, 0.0001)


# Define a fixture for creating a temporary NetCDF file
def is_opendap_url_available(url):
    """Is testing url available."""
    try:
        xr.open_dataset(url)
        return True
    except Exception as e:
        print(f"Error accessing OpenDAP URL: {e}")
        return False


@pytest.fixture
def temp_netcdf(tmp_path):
    """Create temp netcdf file for testing."""
    data = xr.Dataset({"var1": (("x", "y"), [[1, 2], [3, 4]])})
    netcdf_file = tmp_path / "test.nc"
    data.to_netcdf(netcdf_file)
    return str(netcdf_file)


@pytest.mark.parametrize(
    "input_value, expected_type, test_id",
    [
        (
            "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_met_pr_1979_CurrentYear_CONUS.nc",
            xr.Dataset,
            "happy_path_url",
        ),
        (temp_netcdf, xr.Dataset, "happy_path_file_path"),
        (xr.Dataset(), xr.Dataset, "happy_path_xr_dataset"),
        (xr.DataArray([[1, 2], [3, 4]]), TypeError, "error_data_array"),
        (123, TypeError, "error_invalid_type"),
    ],
    ids=lambda x: x if isinstance(x, str) else None,
)
def test_get_xr_dataset(input_value, expected_type, test_id, temp_netcdf):
    """Testing _get_xr_dataset."""
    if test_id == "happy_path_file_path":
        input_value = Path(temp_netcdf)
    elif test_id == "happy_path_url":
        # Check if OpenDAP URL is available
        if not is_opendap_url_available(input_value):
            pytest.skip("OpenDAP URL is not available")
    # Act
    if isinstance(expected_type, type) and issubclass(expected_type, Exception):
        with pytest.raises(expected_type):
            _get_xr_dataset(input_value)
    else:
        result = _get_xr_dataset(input_value)

    # Assert
    if not isinstance(expected_type, type) or not issubclass(expected_type, Exception):
        assert isinstance(result, expected_type), f"Test {test_id} failed: result type mismatch"


def test_with_xr_dataset():
    """Testing valid dataset."""
    dataset = xr.Dataset({"var1": (("x", "y"), [[1, 2], [3, 4]])})
    assert _get_rxr_dataset(dataset) is dataset


def test_with_xr_dataarray():
    """Testing valid Dataarray."""
    dataarray = xr.DataArray([[1, 2], [3, 4]])
    assert _get_rxr_dataset(dataarray) is dataarray


def create_dummy_netcdf_file(file_path):
    """Create dummy netcdf file for testing."""
    # Create some sample data
    data = np.random.rand(100, 100)
    x = np.linspace(0, 10, data.shape[1])
    y = np.linspace(0, 10, data.shape[0])

    # Create a DataArray
    da = xr.DataArray(data, coords=[y, x], dims=["y", "x"])
    da.rio.set_spatial_dims(x_dim="x", y_dim="y", inplace=True)
    da.rio.write_crs("epsg:4326", inplace=True)

    # Convert to Dataset and save as NetCDF
    ds = da.to_dataset(name="test_var")
    ds.to_netcdf(file_path)


def test_with_dummy_dataset(tmp_path):
    """Test valid netcdf file."""
    # Create a dummy NetCDF file
    file_path = tmp_path / "dummy.nc"
    create_dummy_netcdf_file(file_path)

    # Test the _get_rxr_dataset function
    result = _get_rxr_dataset(str(file_path))
    assert isinstance(result, xr.DataArray), "Result is not an xarray.Dataset"


def test_with_invalid_file_path():
    """Test invalid file path."""
    invalid_path = "non_existent_file.nc"
    result = _get_rxr_dataset(invalid_path)
    assert "Failed to open dataset" in result


def test_with_unsupported_type():
    """Test unsupported type."""
    result = _get_rxr_dataset(123)
    assert "Unsupported type for ds" in result


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (pytest.param(["2022-01-01"], ["2022-01-01"], id="single_string_date")),
        (
            pytest.param(
                [datetime.datetime(2022, 1, 1)], [pd.Timestamp("2022-01-01").isoformat()], id="single_datetime_object"
            )
        ),
        (
            pytest.param(
                [pd.Timestamp("2022-01-01")], [pd.Timestamp("2022-01-01").isoformat()], id="single_pd_timestamp"
            )
        ),
        (pytest.param(["2022-01-01", "2022-01-31"], ["2022-01-01", "2022-01-31"], id="two_string_dates")),
        (
            pytest.param(
                [datetime.datetime(2022, 1, 1), datetime.datetime(2022, 1, 31)],
                [pd.Timestamp("2022-01-01").isoformat(), pd.Timestamp("2022-01-31").isoformat()],
                id="two_datetime_objects",
            )
        ),
        (
            pytest.param(
                [pd.Timestamp("2022-01-01"), pd.Timestamp("2022-01-31")],
                [pd.Timestamp("2022-01-01").isoformat(), pd.Timestamp("2022-01-31").isoformat()],
                id="two_pd_timestamps",
            )
        ),
    ],
)
def test_process_period_happy_path(test_input, expected):
    """Test _process_period function."""
    # Act
    result = _process_period(test_input)

    # Assert
    assert result == expected, f"Expected {expected}, got {result}"


# Edge cases
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (pytest.param(["2022-01-01T00:00:00Z"], ["2022-01-01T00:00:00Z"], id="iso_format_string")),
        (pytest.param([pd.Timestamp("2022-01-01T00:00:00")], ["2022-01-01T00:00:00"], id="iso_format_timestamp")),
    ],
)
def test_process_period_edge_cases(test_input, expected):
    """Test _process_period edge cases."""
    # Act
    result = _process_period(test_input)

    # Assert
    assert [s[:-5] for s in result] == [s[:-5] for s in expected], f"Expected {expected}, got {result}"


# Error cases
@pytest.mark.parametrize(
    "test_input, exception_message",
    [
        (pytest.param(123, "period must be a list", id="non_list_input")),
        (pytest.param([], "period must contain 1 or 2 elements", id="empty_list")),
        (
            pytest.param(
                ["2022-01-01", "2022-01-31", "2022-02-28"],
                "period must contain 1 or 2 elements",
                id="three_element_list",
            )
        ),
        (
            pytest.param(
                [123],
                "Elements of period must be string, pd.Timestamp, datetime.datetime, or None",
                id="invalid_element_type",
            )
        ),
        (
            pytest.param(
                [datetime.datetime(2022, 1, 1), 123],
                "Elements of period must be string, pd.Timestamp, datetime.datetime, or None",
                id="mixed_invalid_element_type",
            )
        ),
    ],
)
def test_process_period_error_cases(test_input, exception_message):
    """Test _process_period error cases."""
    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        _process_period(test_input)
    assert str(exc_info.value) == exception_message, f"Expected ValueError with message '{exception_message}'"
