"""Tests for raster functions."""

import gc
import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import geopandas as gpd
import pandas as pd
import pytest
import rioxarray as rxr
import xarray as xr
from dask.distributed import Client
from dask.distributed import LocalCluster
from pytest import FixtureRequest

from gdptools import ZonalGen
from gdptools.data.user_data import UserTiffData


@contextmanager
def get_dask_client():
    """Get dask cluster."""
    cluster = LocalCluster(n_workers=os.cpu_count())
    client = Client(cluster)
    try:
        yield client
    finally:
        cluster.close()
        client.close()


@pytest.fixture(scope="function")
def get_tiff_slope() -> xr.DataArray:
    """Get tiff slope file."""
    ds = rxr.open_rasterio("./tests/data/rasters/slope/slope.tif")  # type: ignore
    yield ds
    del ds
    gc.collect()


@pytest.fixture(scope="function")
def get_tiff_text() -> xr.DataArray:
    """Get tiff text_prms file."""
    ds = rxr.open_rasterio("./tests/data/rasters/TEXT_PRMS/TEXT_PRMS.tif")  # type: ignore
    yield ds
    del ds
    gc.collect()


@pytest.fixture(scope="function")
def get_gdf() -> gpd.GeoDataFrame:
    """Get gdf file."""
    gdf = gpd.read_file("./tests/data/Oahu.shp")
    yield gdf
    del gdf
    gc.collect()


slope_output = [1587.0, 7.981096408317581, 13.067518737687127, 0.0, 1.5, 3.0, 6.0, 61.0, 12666.0]

text_output = [0.0, 0.0, 0.9416666666666667, 0.058333333333333334, 120]

inputs = [
    ("slope", "x", "y", 1, "band", 26904, False, "get_tiff_slope", "get_gdf", "fid", slope_output),
    ("TEXT_PRMS", "x", "y", 1, "band", 26904, True, "get_tiff_text", "get_gdf", "fid", text_output),
]


@pytest.mark.parametrize("vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid,expected", inputs)
def test_cat_tiff_intersection(
    vn: str,
    xn: str,
    yn: str,
    bd: int,
    bn: str,
    crs: Any,
    cat: bool,
    ds: str,
    gdf: str,
    fid: str,
    expected: list,
    request: FixtureRequest,
) -> None:
    """Test tiff intersection function."""
    data = UserTiffData(
        var=vn,
        ds=request.getfixturevalue(ds),
        proj_ds=crs,
        x_coord=xn,
        y_coord=yn,
        bname=bn,
        band=bd,
        f_feature=request.getfixturevalue(gdf),
        id_feature=fid,
    )
    tmpdir = TemporaryDirectory()
    zonal_gen = ZonalGen(
        user_data=data,
        zonal_engine="serial",
        zonal_writer="csv",
        out_path=tmpdir.name,
        file_prefix="tmpzonal",
    )
    stats = zonal_gen.calculate_zonal(categorical=cat)
    stat_list = list(stats.values[50])

    assert stat_list[0] == expected[0]
    assert stat_list[1] == pytest.approx(expected[1], 0.00000000001)
    assert stat_list[2] == pytest.approx(expected[2], 0.00000000001)
    assert stat_list[3:9] == expected[3:9]
    assert isinstance(stats, pd.DataFrame)
    file = Path(tmpdir.name) / "tmpzonal.csv"
    assert file.exists()


@pytest.mark.parametrize("vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid,expected", inputs)
def test_cat_tiff_intersectio_p(
    vn: str,
    xn: str,
    yn: str,
    bd: int,
    bn: str,
    crs: Any,
    cat: bool,
    ds: str,
    gdf: str,
    fid: str,
    expected: list,
    request: FixtureRequest,
) -> None:
    """Test tiff intersection function."""
    data = UserTiffData(
        var=vn,
        ds=request.getfixturevalue(ds),
        proj_ds=crs,
        x_coord=xn,
        y_coord=yn,
        bname=bn,
        band=bd,
        f_feature=request.getfixturevalue(gdf),
        id_feature=fid,
    )
    tmpdir = TemporaryDirectory()
    zonal_gen = ZonalGen(
        user_data=data,
        zonal_engine="parallel",
        zonal_writer="csv",
        out_path=tmpdir.name,
        file_prefix="tmpzonal",
    )
    stats = zonal_gen.calculate_zonal(categorical=cat)
    stat_list = list(stats.values[50])

    assert stat_list[0] == expected[0]
    assert stat_list[1] == pytest.approx(expected[1], 0.00000000001)
    assert stat_list[2] == pytest.approx(expected[2], 0.00000000001)
    assert stat_list[3:9] == expected[3:9]
    assert isinstance(stats, pd.DataFrame)
    file = Path(tmpdir.name) / "tmpzonal.csv"
    assert file.exists()


@pytest.mark.parametrize("vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid,expected", inputs)
def test_cat_tiff_intersectio_d(
    vn: str,
    xn: str,
    yn: str,
    bd: int,
    bn: str,
    crs: Any,
    cat: bool,
    ds: str,
    gdf: str,
    fid: str,
    expected: list,
    request: FixtureRequest,
) -> None:
    """Test tiff intersection function."""
    with get_dask_client() as _client:  # noqa

        data = UserTiffData(
            var=vn,
            ds=request.getfixturevalue(ds),
            proj_ds=crs,
            x_coord=xn,
            y_coord=yn,
            bname=bn,
            band=bd,
            f_feature=request.getfixturevalue(gdf),
            id_feature=fid,
        )
        tmpdir = TemporaryDirectory()
        zonal_gen = ZonalGen(
            user_data=data,
            zonal_engine="dask",
            zonal_writer="csv",
            out_path=tmpdir.name,
            file_prefix="tmpzonal",
            jobs=4,
        )
        stats = zonal_gen.calculate_zonal(categorical=cat)
        stat_list = list(stats.values[50])

        assert stat_list[0] == expected[0]
        assert stat_list[1] == pytest.approx(expected[1], 0.00000000001)
        assert stat_list[2] == pytest.approx(expected[2], 0.00000000001)
        assert stat_list[3:9] == expected[3:9]
        assert isinstance(stats, pd.DataFrame)
        file = Path(tmpdir.name) / "tmpzonal.csv"
        assert file.exists()


@pytest.mark.parametrize(
    "vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid,precision",
    [
        (
            "slope",
            "x",
            "y",
            1,
            "band",
            26904,
            False,
            "get_tiff_slope",
            "get_gdf",
            "fid",
            2,  # Precision of 2 decimal places
        ),
        (
            "TEXT_PRMS",
            "x",
            "y",
            1,
            "band",
            26904,
            True,
            "get_tiff_text",
            "get_gdf",
            "fid",
            4,  # Precision of 4 decimal places
        ),
    ],
)
def test_zonal_gen_precision(
    vn: str,
    xn: str,
    yn: str,
    bd: int,
    bn: str,
    crs: Any,
    cat: bool,
    ds: str,
    gdf: str,
    fid: str,
    precision: int,
    request: FixtureRequest,
) -> None:
    """Test ZonalGen precision handling."""
    data = UserTiffData(
        var=vn,
        ds=request.getfixturevalue(ds),
        proj_ds=crs,
        x_coord=xn,
        y_coord=yn,
        bname=bn,
        band=bd,
        f_feature=request.getfixturevalue(gdf),
        id_feature=fid,
    )
    with TemporaryDirectory() as tmpdir:
        zonal_gen = ZonalGen(
            user_data=data,
            zonal_engine="serial",
            zonal_writer="csv",
            out_path=tmpdir,
            file_prefix="tmpzonal",
            precision=precision,
        )
        stats = zonal_gen.calculate_zonal(categorical=cat)

        assert isinstance(stats, pd.DataFrame)
        file = Path(tmpdir) / "tmpzonal.csv"
        assert file.exists()

        # Read the CSV and verify precision
        df = pd.read_csv(file)
        for col in df.select_dtypes(include=["float"]):
            assert df[col].apply(lambda x: len(str(x).split(".")[1]) if "." in str(x) else 0).max() <= precision
