"""Tests for .helper functions."""

import gc
from typing import Any

import geopandas as gpd
import pandas as pd
import pytest
import xarray as xr
import numpy as np

from gdptools.helpers import check_gridded_data_for_dimensions
from gdptools.helpers import build_subset


@pytest.fixture(scope="function")
def get_var() -> str:
    """Get variable string."""
    return "aet"


@pytest.fixture(scope="function")
def climrcat() -> dict[str, dict[str, Any]]:
    """Return climr catalog json."""
    cat = "https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet"
    climr: pd.DataFrame = pd.read_parquet(cat)
    _id = "terraclim"  # noqa
    _varname = "aet"  # noqa
    cat_d: dict[str, Any] = climr.query("id == @_id & varname == @_varname").to_dict("records")[0]
    data = dict(zip([_varname], [cat_d]))  # noqa
    yield data
    del data
    gc.collect()


@pytest.fixture(scope="function")
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    return gpd.read_file("./tests/data/hru_1210_epsg5070.shp")  # type: ignore


@pytest.fixture(scope="function")
def get_begin_date() -> str:
    """Get begin date."""
    return "2005-01-01"


@pytest.fixture(scope="function")
def get_end_date() -> str:
    """Get end date."""
    return "2005-02-01"


@pytest.fixture(scope="function")
def get_toptobottom() -> str:
    """Get end date."""
    return "True"


@pytest.fixture(scope="function")
def get_xcoord() -> str:
    """Get end date."""
    return "lon"


@pytest.fixture(scope="function")
def get_ycoord() -> str:
    """Get end date."""
    return "lat"


@pytest.fixture(scope="function")
def get_tcoord() -> str:
    """Get end date."""
    return "day"


@pytest.fixture(scope="function")
def get_xarray(climrcat, get_var) -> xr.Dataset:
    """Create xarray Dataset."""
    ds = xr.open_dataset(climrcat[get_var]["URL"])
    yield ds
    del ds
    gc.collect()


def test_check_gridded_data_for_dimensions(get_xarray, get_var):
    """Test function check_gridded_data_for_dimensions."""
    output = check_gridded_data_for_dimensions(get_xarray, [get_var])
    assert isinstance(output, type(None))


def test_build_subset(
    get_gdf,
    get_xcoord,
    get_ycoord,
    get_tcoord,
    get_toptobottom,
    get_begin_date,
    get_end_date,
):
    """Test function build_subset."""
    subset = build_subset(
        bounds=np.asarray(get_gdf.bounds.loc[0]),
        xname=get_xcoord,
        yname=get_ycoord,
        tname=get_tcoord,
        toptobottom=get_toptobottom,
        date_min=get_begin_date,
        date_max=get_end_date,
    )

    real_subset = {
        "lon": slice(2054594.7771999985, 2127645.084399998, None),
        "lat": slice(2358794.8389, 2406615.137599999, None),
        "day": slice("2005-01-01", "2005-02-01", None),
    }

    assert subset == real_subset
