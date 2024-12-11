"""Tests for .helper functions."""

import gc
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory

import geopandas as gpd  # type: ignore
import pandas as pd  # type: ignore
import pytest
import xarray as xr

from gdptools import AggGen
from gdptools import UserCatData
from gdptools import WeightGen


@pytest.fixture(scope="function")
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    gdf = gpd.read_file("./tests/data/DRB/DRB_4326.shp")
    yield gdf
    del gdf
    gc.collect()


@pytest.fixture(scope="function")
def get_xarray() -> xr.Dataset:
    """Create xarray Dataset."""
    ds = xr.open_dataset("./tests/data/DRB/o_of_b_test.nc")
    yield ds
    del ds
    gc.collect()


@pytest.fixture()
def get_file_path(tmp_path: Path) -> Path:
    """Get temp file path."""
    return tmp_path / "test.csv"


@pytest.fixture()
def get_out_path(tmp_path: Path) -> Path:
    """Get temp file output path."""
    return tmp_path


data_crs = 4326
x_coord = "lon"
y_coord = "lat"
t_coord = "time"
sdate = "2021-01-01T00:00"
edate = "2021-01-01T02:00"
var = ["Tair"]
shp_crs = 4326
shp_poly_idx = "huc12"
wght_gen_crs = 6931


def test_calculate_weights(get_xarray, get_gdf, get_out_path):  # type: ignore
    """Test calculate weights."""
    user_data = UserCatData(
        ds=get_xarray,
        proj_ds=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        var=var,
        f_feature=get_gdf,
        proj_feature=shp_crs,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )  # type: ignore

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tempfile.name,  # type: ignore
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        file_prefix="gm_tmax",
    )

    _ngdf, _vals = agg_gen.calculate_agg()

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_vals, xr.Dataset)

    ofile = get_out_path / tempfile.name
    assert ofile.exists()

    outfile = pd.read_csv(ofile)
    print(outfile.head())
