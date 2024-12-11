"""Tests for weighted zonal stats."""

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
from dask.distributed import Client, LocalCluster
from pytest import FixtureRequest

from gdptools import WeightedZonalGen
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
def get_tiff_slope() -> xr.DataArray:  # type: ignore
    """Get tiff slope file."""
    ds = rxr.open_rasterio("./tests/data/rasters/slope/slope.tif")  # type: ignore
    yield ds
    del ds
    gc.collect()


@pytest.fixture(scope="function")
def get_tiff_text() -> xr.DataArray:  # type: ignore
    """Get tiff text_prms file."""
    ds = rxr.open_rasterio("./tests/data/rasters/TEXT_PRMS/TEXT_PRMS.tif")  # type: ignore
    yield ds
    del ds
    gc.collect()


@pytest.fixture(scope="function")
def get_gdf() -> gpd.GeoDataFrame:  # type: ignore
    """Get gdf file."""
    gdf = gpd.read_file("./tests/data/Oahu.shp")
    yield gdf
    del gdf
    gc.collect()


def save_test_results(df: pd.DataFrame, file_path: str, columns: list) -> None:
    """Save test results."""
    # Save only the specified columns
    df[columns].to_csv(file_path)


def load_baseline_results(file_path: str) -> pd.DataFrame:
    """Load baseline results."""
    return pd.read_csv(file_path, header=0)


def load_current_results(file_path: str) -> pd.DataFrame:
    """Load current results."""
    return pd.read_csv(file_path, header=0)


def compare_test_results(current_df: pd.DataFrame, baseline_df: pd.DataFrame, columns: list) -> None:
    """Compare test results."""
    # Compare only the specified columns
    current_subset = current_df[columns]
    baseline_subset = baseline_df[columns]

    pd.testing.assert_frame_equal(current_subset, baseline_subset, check_dtype=True)


@pytest.mark.parametrize(
    "vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid,precision",
    [
        # (
        #     "slope",
        #     "x",
        #     "y",
        #     1,
        #     "band",
        #     26904,
        #     False,
        #     "get_tiff_slope",
        #     "get_gdf",
        #     "fid",
        #     2,  # Precision of 2 decimal places
        # ),
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
def test_weighted_zonal_gen_precision(
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
    """Test WeightedZonalGen precision handling."""
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
        zonal_gen = WeightedZonalGen(
            user_data=data,
            weight_gen_crs=crs,
            zonal_engine="serial",
            zonal_writer="csv",
            out_path=tmpdir,
            file_prefix="tmpzonal",
            precision=precision,
        )
        stats = zonal_gen.calculate_weighted_zonal(categorical=cat)

        assert isinstance(stats, pd.DataFrame)
        file = Path(tmpdir) / "tmpzonal.csv"
        assert file.exists()

        # Read the CSV and verify precision
        df = pd.read_csv(file)
        for col in df.select_dtypes(include=["float"]):
            assert df[col].apply(lambda x: len(str(x).split(".")[1]) if "." in str(x) else 0).max() <= precision


@pytest.mark.parametrize(
    "vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid",
    [
        # (
        #     "slope",
        #     "x",
        #     "y",
        #     1,
        #     "band",
        #     26904,
        #     False,
        #     "get_tiff_slope",
        #     "get_gdf",
        #     "fid",
        # ),
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
        ),
    ],
)
def test_weighted_zonal_gen_serial(
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
    request: FixtureRequest,
) -> None:
    """Test weighted zonal statistics calculation using the serial engine."""
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
        zonal_gen = WeightedZonalGen(
            user_data=data,
            weight_gen_crs=crs,
            zonal_engine="serial",
            zonal_writer="csv",
            out_path=tmpdir,
            precision=2,
            file_prefix="tmpzonal",
        )
        stats = zonal_gen.calculate_weighted_zonal(categorical=cat)

        # Convert column names to strings (if they are integers)
        stats.columns = stats.columns.map(str)

        # Define the path to the baseline file
        baseline_file_path = "./tests/data/rasters/weighted_baseline_serial_test_results.csv"

        # Define the columns to test
        columns_to_test = ["0", "1", "2", "3", "top"]

        file = Path(tmpdir) / "tmpzonal.csv"

        # Check if the baseline file exists
        if Path(baseline_file_path).exists():
            # Load baseline results and compare
            baseline_df = load_baseline_results(baseline_file_path)
            current_df = load_current_results(file)
            compare_test_results(current_df, baseline_df, columns=columns_to_test)
        else:
            # If the baseline doesn't exist, save the current results as baseline
            save_test_results(stats, baseline_file_path, columns=columns_to_test)

        assert isinstance(stats, pd.DataFrame)
        file = Path(tmpdir) / "tmpzonal.csv"
        assert file.exists()


@pytest.mark.parametrize(
    "vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid",
    [
        # (
        #     "slope",
        #     "x",
        #     "y",
        #     1,
        #     "band",
        #     26904,
        #     False,
        #     "get_tiff_slope",
        #     "get_gdf",
        #     "fid",
        # ),
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
        ),
    ],
)
def test_weighted_zonal_gen_parallel(
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
    request: FixtureRequest,
) -> None:
    """Test weighted zonal statistics calculation using the parallel engine."""
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
        zonal_gen = WeightedZonalGen(
            user_data=data,
            weight_gen_crs=crs,
            zonal_engine="parallel",
            zonal_writer="csv",
            out_path=tmpdir,
            file_prefix="tmpzonal",
            precision=2,
            jobs=4,
        )
        stats = zonal_gen.calculate_weighted_zonal(categorical=cat)

        # Convert column names to strings (if they are integers)
        stats.columns = stats.columns.map(str)

        # Define the path to the baseline file
        baseline_file_path = "./tests/data/rasters/weighted_baseline_parallel_test_results.csv"

        # Define the columns to test
        columns_to_test = ["0", "1", "2", "3", "top"]

        file = Path(tmpdir) / "tmpzonal.csv"

        # Check if the baseline file exists
        if Path(baseline_file_path).exists():
            # Load baseline results and compare
            baseline_df = load_baseline_results(baseline_file_path)
            current_df = load_current_results(file)
            compare_test_results(current_df, baseline_df, columns=columns_to_test)
        else:
            # If the baseline doesn't exist, save the current results as baseline
            save_test_results(stats, baseline_file_path, columns=columns_to_test)

        assert isinstance(stats, pd.DataFrame)
        assert file.exists()


@pytest.mark.parametrize(
    "vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid",
    [
        # (
        #     "slope",
        #     "x",
        #     "y",
        #     1,
        #     "band",
        #     26904,
        #     False,
        #     "get_tiff_slope",
        #     "get_gdf",
        #     "fid",
        # ),
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
        ),
    ],
)
def test_weighted_zonal_gen_dask(
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
    request: FixtureRequest,
) -> None:
    """Test weighted zonal statistics calculation using the dask engine."""
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
        with TemporaryDirectory() as tmpdir:
            zonal_gen = WeightedZonalGen(
                user_data=data,
                weight_gen_crs=crs,
                zonal_engine="dask",
                zonal_writer="csv",
                out_path=tmpdir,
                file_prefix="tmpzonal",
                precision=2,
                jobs=4,
            )
            stats = zonal_gen.calculate_weighted_zonal(categorical=cat)

            # Convert column names to strings (if they are integers)
            stats.columns = stats.columns.map(str)

            # Define the path to the baseline file
            baseline_file_path = "./tests/data/rasters/weighted_baseline_dask_test_results.csv"

            # Define the columns to test
            columns_to_test = ["0", "1", "2", "3", "top"]

            file = Path(tmpdir) / "tmpzonal.csv"

            # Check if the baseline file exists
            if Path(baseline_file_path).exists():
                # Load baseline results and compare
                baseline_df = load_baseline_results(baseline_file_path)
                current_df = load_current_results(file)
                compare_test_results(current_df, baseline_df, columns=columns_to_test)
            else:
                # If the baseline doesn't exist, save the current results as baseline
                save_test_results(stats, baseline_file_path, columns=columns_to_test)

            assert isinstance(stats, pd.DataFrame)
            assert file.exists()
