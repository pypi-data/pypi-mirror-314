"""Tests for .helper functions."""

import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory
from typing import Any

import geopandas as gpd  # type: ignore
import numpy as np
import pandas as pd  # type: ignore
import pytest
import xarray as xr

from gdptools import AggGen
from gdptools import ClimRCatData
from gdptools import UserCatData
from gdptools import WeightGen

gm_vars = ["tmmn", "tmmx", "pr"]
gldas_vars = ["tair_f_inst", "rainf_f_tavg"]


# Adding catalog entry with toptobottom false
@pytest.fixture
def climr_dict_1(vars: list[str] = gldas_vars) -> dict[str, Any]:
    """Return parameter json."""
    climater_cat = "https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet"
    cat = pd.read_parquet(climater_cat)

    _id = "GLDAS"  # noqa
    var_params = [
        cat.query("id == @_id & variable == @_var", local_dict={"_id": _id, "_var": _var}).to_dict(orient="records")[0]
        for _var in vars
    ]
    return dict(zip(vars, var_params))  # noqa B905


# Adding catalog entry with toptobottom true
@pytest.fixture
def climr_dict(vars: list[str] = gm_vars) -> dict[str, Any]:
    """Return parameter json."""
    climater_cat = "https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet"
    cat = pd.read_parquet(climater_cat)

    _id = "gridmet"  # noqa
    var_params = [
        cat.query("id == @_id & variable == @_var", local_dict={"_id": _id, "_var": _var}).to_dict(orient="records")[0]
        for _var in vars
    ]
    return dict(zip(vars, var_params))  # noqa B905


@pytest.fixture()
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    return gpd.read_file("./tests/data/DRB/DRB_4326.shp")


@pytest.fixture()
def get_xarray() -> xr.Dataset:
    """Create xarray Dataset."""
    return xr.open_dataset("./tests/data/DRB/o_of_b_test.nc")


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
sdate = pd.Timestamp("2021-01-01")
edate = pd.Timestamp("2021-01-31")
var = ["Tair"]
shp_crs = 4326
shp_poly_idx = "huc12"
wght_gen_crs = 6931


def test_serial_climrcatdata(climr_dict, get_gdf, get_out_path):
    """Test Serial versions."""
    user_data = ClimRCatData(
        cat_dict=climr_dict,
        f_feature=get_gdf,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )
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
        file_prefix="gm_drb_test",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # np.savez(
    #     "./tests/data/DRB/gm_drb.npz",
    #     tmin=_df.daily_minimum_temperature.values,
    #     tmax=_df.daily_maximum_temperature.values,
    #     pr=_df.precipitation_amount.values,
    # )

    test_data = np.load("./tests/data/DRB/gm_drb.npz")

    np.testing.assert_allclose(
        _df.daily_maximum_temperature.values,
        test_data["tmax"],
        rtol=1e-4,
        verbose=True,
    )

    np.testing.assert_allclose(
        _df.daily_minimum_temperature.values,
        test_data["tmin"],
        rtol=1e-4,
        verbose=True,
    )

    np.testing.assert_allclose(
        _df.precipitation_amount.values,
        test_data["pr"],
        rtol=1e-4,
        verbose=True,
    )
    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_df, xr.Dataset)

    ofile = get_out_path / tempfile.name
    assert ofile.exists()

    # Test that the proper feature ids get written to the generated .csv file.
    pdf = pd.read_csv(tmpdir.name + "/gm_drb_test.csv")
    columns_out = pdf.columns[4:]
    columns_in = _ngdf[shp_poly_idx]
    assert columns_out.to_list() == columns_in.to_list()

    # additional check a HUC12 values - tests column order in output
    csv_vals = pdf.query('varname == "daily_minimum_temperature"')["020402010201"].values
    df_vals = _df.daily_minimum_temperature.sel(huc12="020402010201").values
    np.testing.assert_allclose(df_vals, csv_vals, rtol=1e-4, verbose=True)


# def test_serial_usercatdata_with_error(get_xarray, get_gdf, get_out_path):
#     """Test bad time formatting.

#     NOTE: pd.Timestamp("2021-01-01T00:00") returns "2021-01-01T00:00:00" when converted to isoformat() which
#     _process_period() returns.  When subsetting this dataset, it will fail.
#     """
#     def test_serial_usercatdata_with_error(get_xarray, get_gdf):
#         """Test Serial versions."""
#         sdate = pd.Timestamp("2021-01-01T00:00")
#         edate = pd.Timestamp("2021-01-01T02:00")
#         user_data = UserCatData(
#             ds=get_xarray,
#             proj_ds=data_crs,
#             x_coord=x_coord,
#             y_coord=y_coord,
#             t_coord=t_coord,
#             var=var,
#             f_feature=get_gdf,
#             proj_feature=shp_crs,
#             id_feature=shp_poly_idx,
#             period=[sdate, edate],
#         )  # type: ignore

#         tempfile = NamedTemporaryFile()

#         wght_gen = WeightGen(
#             user_data=user_data,
#             method="serial",
#             output_file=tempfile.name,  # type: ignore
#             weight_gen_crs=wght_gen_crs,
#         )

#         _wghts = wght_gen.calculate_weights()
#     with pytest.raises(KeyError) as excinfo:
#         test_serial_usercatdata_with_error(get_xarray, get_gdf)
#         assert "The source data time coordinate is formatted as" in str(excinfo.value)


def test_serial_usercatdata_timestamp(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = pd.Timestamp("2020-12-31T00:00")
    edate = pd.Timestamp("2021-01-01T02:00")
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
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # np.savez(
    #     "./tests/data/DRB/user_drb_usercatdata.npz",
    #     Tair=_df.Tair.values
    # )

    test_data = np.load("./tests/data/DRB/user_drb_usercatdata.npz")

    np.testing.assert_allclose(
        _df.Tair.values,
        test_data["Tair"],
        rtol=1e-4,
        verbose=True,
    )

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_df, xr.Dataset)

    ofile = get_out_path / tempfile.name
    assert ofile.exists()

    # Test that the proper feature ids get written to the generated .csv file.
    pdf = pd.read_csv(tmpdir.name + "/tair.csv")
    columns_out = pdf.columns[4:]
    columns_in = _ngdf[shp_poly_idx]
    assert columns_out.to_list() == columns_in.to_list()

    # additional check a HUC12 values - tests column order in output
    csv_vals = pdf["020402010201"].values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, csv_vals)


def test_serial_usercatdata_datetime(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = datetime.datetime(2020, 12, 31, 0, 0)
    edate = datetime.datetime(2021, 1, 1, 2, 0)
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
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # np.savez(
    #     "./tests/data/DRB/user_drb_usercatdata.npz",
    #     Tair=_df.Tair.values
    # )

    test_data = np.load("./tests/data/DRB/user_drb_usercatdata.npz")

    np.testing.assert_allclose(
        _df.Tair.values,
        test_data["Tair"],
        rtol=1e-4,
        verbose=True,
    )

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_df, xr.Dataset)

    ofile = get_out_path / tempfile.name
    assert ofile.exists()

    # Test that the proper feature ids get written to the generated .csv file.
    pdf = pd.read_csv(tmpdir.name + "/tair.csv")
    columns_out = pdf.columns[4:]
    columns_in = _ngdf[shp_poly_idx]
    assert columns_out.to_list() == columns_in.to_list()

    # additional check a HUC12 values - tests column order in output
    csv_vals = pdf["020402010201"].values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, csv_vals)


def test_serial_usercatdata(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
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
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # np.savez(
    #     "./tests/data/DRB/user_drb_usercatdata.npz",
    #     Tair=_df.Tair.values
    # )

    test_data = np.load("./tests/data/DRB/user_drb_usercatdata.npz")

    np.testing.assert_allclose(
        _df.Tair.values,
        test_data["Tair"],
        rtol=1e-4,
        verbose=True,
    )

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_df, xr.Dataset)

    ofile = get_out_path / tempfile.name
    assert ofile.exists()

    # Test that the proper feature ids get written to the generated .csv file.
    pdf = pd.read_csv(tmpdir.name + "/tair.csv")
    columns_out = pdf.columns[4:]
    columns_in = _ngdf[shp_poly_idx]
    assert columns_out.to_list() == columns_in.to_list()

    # additional check a HUC12 values - tests column order in output
    csv_vals = pdf["020402010201"].values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, csv_vals)


def test_serial_usercatdata_with_precision(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
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
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
        precision=4,
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # np.savez(
    #     "./tests/data/DRB/user_drb_usercatdata.npz",
    #     Tair=_df.Tair.values
    # )

    test_data = np.load("./tests/data/DRB/user_drb_usercatdata.npz")

    np.testing.assert_allclose(
        _df.Tair.values,
        test_data["Tair"],
        rtol=1e-4,
        verbose=True,
    )

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_df, xr.Dataset)

    ofile = get_out_path / tempfile.name
    assert ofile.exists()

    # Test that the proper feature ids get written to the generated .csv file.
    pdf = pd.read_csv(tmpdir.name + "/tair.csv")
    columns_out = pdf.columns[4:]
    columns_in = _ngdf[shp_poly_idx]
    assert columns_out.to_list() == columns_in.to_list()

    # additional check a HUC12 values - tests column order in output
    csv_vals = pdf["020402010201"].values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, csv_vals)


def test_serial_usercatdata_out_netcdf(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
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
        # output_file='./tests/data/DRB/usercatdata_weights_parallel.csv',
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="netcdf",
        weights=tempfile.name,
        out_path=tmpdir.name,
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # Test that the proper feature ids get written to the generated .csv file.
    xds = xr.open_dataset(tmpdir.name + "/tair.nc")
    columns_out = xds.coords[shp_poly_idx].values
    columns_in = _ngdf[shp_poly_idx]
    assert list(columns_out) == columns_in.to_list()

    # additional check a HUC12 values - tests column order in output
    ncf_vals = xds.Tair.sel(huc12="020402010201").values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, ncf_vals)


def test_serial_usercatdata_out_netcdf_with_precision(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
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
        # output_file='./tests/data/DRB/usercatdata_weights_parallel.csv',
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="netcdf",
        weights=tempfile.name,
        out_path=tmpdir.name,
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
        precision=4,
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # Test that the proper feature ids get written to the generated .csv file.
    xds = xr.open_dataset(tmpdir.name + "/tair.nc")
    columns_out = xds.coords[shp_poly_idx].values
    columns_in = _ngdf[shp_poly_idx]
    assert list(columns_out) == columns_in.to_list()

    # additional check a HUC12 values - tests column order in output
    ncf_vals = xds.Tair.sel(huc12="020402010201").values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, ncf_vals)


def test_serial_usercatdata_out_parquet(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
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
        # output_file='./tests/data/DRB/usercatdata_weights_parallel.csv',
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="parquet",
        weights=tempfile.name,
        out_path=tmpdir.name,
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # Test that the proper feature ids get written to the generated parquet file.
    # Here we grab a set of results for a HUC12.  Parquet reorders the feature ids
    # So this is a different way of testing.
    pdf = pd.read_parquet(tmpdir.name + "/tair.parquet.gzip")
    pq_vals = pdf["020402010201"].values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, pq_vals)


def test_serial_usercatdata_out_parquet_with_precision(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
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
        # output_file='./tests/data/DRB/usercatdata_weights_parallel.csv',
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="parquet",
        weights=tempfile.name,
        out_path=tmpdir.name,
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
        precision=4,
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # Test that the proper feature ids get written to the generated parquet file.
    # Here we grab a set of results for a HUC12.  Parquet reorders the feature ids
    # So this is a different way of testing.
    pdf = pd.read_parquet(tmpdir.name + "/tair.parquet.gzip")
    pq_vals = pdf["020402010201"].values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, pq_vals)


def test_serial_usercatdata_out_json(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
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
        # output_file='./tests/data/DRB/usercatdata_weights_parallel.csv',
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="json",
        weights=tempfile.name,
        out_path=tmpdir.name,
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # Test that the proper feature ids get written to the generated parquet file.
    # Here we grab a set of results for a HUC12.  Parquet reorders the feature ids
    # So this is a different way of testing.
    pdf = pd.read_json(tmpdir.name + "/tair.json")
    pq_vals = pdf["020402010201"].values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, pq_vals)


def test_serial_usercatdata_out_json_with_precision(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
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
        # output_file='./tests/data/DRB/usercatdata_weights_parallel.csv',
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="json",
        weights=tempfile.name,
        out_path=tmpdir.name,
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
        precision=4,
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # Test that the proper feature ids get written to the generated parquet file.
    # Here we grab a set of results for a HUC12.  Parquet reorders the feature ids
    # So this is a different way of testing.
    pdf = pd.read_json(tmpdir.name + "/tair.json")
    pq_vals = pdf["020402010201"].values
    df_vals = _df.Tair.sel(huc12="020402010201").values
    np.testing.assert_equal(df_vals, pq_vals)
