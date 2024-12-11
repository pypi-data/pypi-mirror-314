"""Test WghtGen and AggGen classes."""

import gc
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory
from typing import Any

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import pystac
import pytest
import xarray as xr
from pandas.testing import assert_frame_equal
from dask.distributed import Client, LocalCluster
from gdptools import AggGen
from gdptools import ClimRCatData
from gdptools import InterpGen
from gdptools import NHGFStacData

from gdptools import UserCatData
from gdptools import WeightGen


gm_vars = ["aet", "pet", "PDSI"]


cluster = LocalCluster(n_workers=os.cpu_count())
client = Client(cluster)  # type: ignore


@pytest.fixture
def aet_ma_mean() -> npt.NDArray[np.double]:
    """Test values for masked-mean calculation."""
    return np.asarray(
        [
            [3.1605408],
            [0.0121277],
            [41.983784],
            [68.91504],
            [81.72351],
            [92.60617],
            [48.96107],
            [37.30392],
            [27.883911],
            [64.65818],
            [52.897045],
            [1.6390916],
        ]
    )


@pytest.fixture
def aet_mean() -> npt.NDArray[np.double]:
    """Test values for mean calculation."""
    return np.asarray(
        [
            [3.1551743],
            [0.0121071],
            [41.9124973],
            [68.7980207],
            [81.5847434],
            [92.4489252],
            [48.8779355],
            [37.2405776],
            [27.8365651],
            [64.5483926],
            [52.8072282],
            [1.63630845],
        ]
    )


@pytest.fixture
def aet_nan_mean() -> npt.NDArray[np.double]:
    """Test values for mean calculation."""
    return np.asarray(
        [
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
            [9.969209968386869e36],
        ]
    )


# @pytest.fixture(scope="function")
# def param_dict(vars: list[str] = gm_vars) -> dict[str, Any]:
#     """Return parameter json."""
#     cat_params = "https://raw.githubusercontent.com/mikejohnson51/opendap.catalog/master/docs/cat_params.json"
#     params = pd.read_json(cat_params)
#     _id = "terraclim"  # noqa
#     var_params = [
#         params.query("id == @_id & variable == @_var", local_dict={"_id": _id, "_var": _var}).to_dict(orient="records")[
#             0
#         ]
#         for _var in vars
#     ]
#     data = dict(zip(vars, var_params))  # noqa B905
#     yield data
#     del data
#     gc.collect()


# @pytest.fixture(scope="function")
# def grid_dict(vars: list[str] = gm_vars) -> dict[str, Any]:
#     """Return grid json."""
#     cat_grid = "https://raw.githubusercontent.com/mikejohnson51/opendap.catalog/master/docs/cat_grids.json"
#     grids = pd.read_json(cat_grid)
#     _gridid = 116  # noqa
#     var_grid = [
#         grids.query("grid_id == @_gridid", local_dict={"_gridid": _gridid, "_var": _var}).to_dict(orient="records")[0]
#         for _var in vars
#     ]
#     data = dict(zip(vars, var_grid))  # noqa B905
#     yield data
#     del data
#     gc.collect()


@pytest.fixture(scope="function")
def climr_cat_data() -> dict[str, Any]:
    """Return dictionary of ClimateR Catalog data."""
    climater_cat = "https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet"
    cat = pd.read_parquet(climater_cat)

    # Create a dictionary of parameter dataframes for each variable
    _id = "terraclim"
    tvars = ["aet", "pet", "PDSI"]
    select_params = [
        cat.query("id == @_id & variable == @_var", local_dict={"_id": _id, "_var": _var}).to_dict(orient="records")[0]
        for _var in tvars
    ]
    data = dict(zip(tvars, select_params))  # noqa B905
    yield data
    del data
    gc.collect()


@pytest.fixture(scope="function")
def gdf() -> gpd.GeoDataFrame:
    """Create xarray dataset."""
    gdf = gpd.read_file("./tests/data/hru_1210_epsg5070.shp")
    yield gdf
    del gdf
    gc.collect()


@pytest.fixture
def poly_idx() -> str:
    """Return poly_idx."""
    return "hru_id_nat"


@pytest.fixture
def wght_gen_proj() -> int:
    """Return wght gen projection."""
    return 6931


@pytest.fixture
def collection() -> pystac.collection.Collection:
    """Read in NHGF Stac and selection one collection."""
    # Read in the NHGF STAC catalog
    catalog_url = "https://code.usgs.gov/wma/nhgf/stac/-/raw/main/catalog/catalog.json"
    catalog = pystac.Catalog.from_file(catalog_url)
    collection = catalog.get_child("conus404-daily")
    yield collection
    del collection
    gc.collect()


def test_nhgfstacdata(
    collection: pystac.collection.Collection,
    gdf: gpd.GeoDataFrame,
    poly_idx: str,
    wght_gen_proj: Any,
) -> None:
    """Test NHGFStacData class."""
    import xarray

    sdate = "1999-01-01"
    edate = "1999-01-07"
    var = ["PWAT"]

    user_data = NHGFStacData(collection=collection, var=var, f_feature=gdf, id_feature=poly_idx, period=[sdate, edate])

    assert type(user_data.get_source_subset(var)) == xarray.core.dataset.Dataset

    wght_gen = WeightGen(
        user_data=user_data,
        method="serial",
        weight_gen_crs=wght_gen_proj,
    )

    wdf = wght_gen.calculate_weights()

    tmpdir = TemporaryDirectory()
    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="netcdf",
        weights=wdf,
        out_path=tmpdir.name,
        file_prefix="test_agg_gen",
    )
    _, ds_out = agg_gen.calculate_agg()
    file = Path(tmpdir.name) / "test_agg_gen.nc"
    assert len(ds_out.PWAT.values) == 7
    assert file.exists()

    out_vals = np.array(
        [
            [0.00401879703815237],
            [0.0031412627954946525],
            [0.01929362081285548],
            [0.007870086363094596],
            [0.002731339138255073],
            [0.003829836307700267],
            [0.006657779295235535],
        ]
    )
    np.testing.assert_allclose(ds_out.PWAT.values, out_vals, rtol=1e-6, verbose=True)  # type: ignore

    tmpdir2 = TemporaryDirectory()
    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_max",
        agg_engine="serial",
        agg_writer="netcdf",
        weights=wdf,
        out_path=tmpdir2.name,
        file_prefix="test_agg_gen2",
    )

    _, ds_out2 = agg_gen.calculate_agg()
    file = Path(tmpdir2.name) / "test_agg_gen2.nc"
    assert len(ds_out2.PWAT.values) == 7
    assert file.exists()

    out_vals2 = np.array(
        [
            [0.004320567939430475],
            [0.00347911030985415],
            [0.019824696704745293],
            [0.009076088666915894],
            [0.0030801023822277784],
            [0.004013265948742628],
            [0.007297412026673555],
        ]
    )
    np.testing.assert_allclose(ds_out2.PWAT.values, out_vals2, rtol=1e-6, verbose=True)  # type: ignore


@pytest.fixture(scope="function")
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    gdf = gpd.read_file("./tests/data/hru_1210_epsg5070.shp")
    yield gdf
    del gdf
    gc.collect()


@pytest.fixture(scope="function")
def get_xarray() -> xr.Dataset:
    """Create xarray Dataset."""
    # return xr.open_dataset("./tests/data/cape_cod_tmax.nc")
    ds = xr.open_mfdataset(
        [
            "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_met_tmmx_1979_CurrentYear_CONUS.nc",
            "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_met_tmmn_1979_CurrentYear_CONUS.nc",
        ]
    )
    yield ds
    del ds
    gc.collect()


@pytest.fixture(scope="function")
def get_file_path(tmp_path: Path) -> Path:
    """Get temp file path."""
    return tmp_path / "test.csv"


@pytest.fixture(scope="function")
def get_out_path(tmp_path: Path) -> Path:
    """Get temp file output path."""
    return tmp_path


data_crs = 4326  # "crs84"
x_coord = "lon"
y_coord = "lat"
t_coord = "day"
sdate = "1979-01-01"
edate = "1979-01-07"
tvar = ["daily_maximum_temperature", "daily_minimum_temperature"]
shp_crs = 5070
shp_poly_idx = "hru_id_nat"
wght_gen_crs = 6931


def test_weightgen_nofile(get_xarray: xr.Dataset, get_gdf: gpd.GeoDataFrame) -> None:
    """Test WeightGen."""
    user_data = UserCatData(
        ds=get_xarray,
        proj_ds=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        var=tvar,
        f_feature=get_gdf,
        proj_feature=shp_crs,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )

    wghtgen1 = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=None,
        weight_gen_crs=wght_gen_crs,
    )

    wghts1 = wghtgen1.calculate_weights()

    wghtgen2 = WeightGen(
        user_data=user_data,
        method="serial",
        weight_gen_crs=wght_gen_crs,
    )

    wghts2 = wghtgen2.calculate_weights()

    assert_frame_equal(wghts1, wghts2)

    wghtgen3 = WeightGen(
        user_data=user_data,
        method="serial",
        weight_gen_crs=wght_gen_crs,
        output_file="",
    )

    wghts3 = wghtgen3.calculate_weights()
    assert_frame_equal(wghts1, wghts3)


def test_usercatdata(
    get_xarray: xr.Dataset,
    get_gdf: gpd.GeoDataFrame,
    get_file_path: Path,
    get_out_path: Path,
) -> None:
    """Test UserCatData."""
    user_data = UserCatData(
        ds=get_xarray,
        proj_ds=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        var=tvar,
        f_feature=get_gdf,
        proj_feature=shp_crs,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )

    tmpfile = NamedTemporaryFile()
    weight_gen = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tmpfile.name,
        weight_gen_crs=wght_gen_crs,
    )

    wghts = weight_gen.calculate_weights()

    user_data2 = UserCatData(
        ds=get_xarray,
        proj_ds=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        var=tvar,
        f_feature=get_gdf,
        proj_feature=shp_crs,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )

    weight_gen2 = WeightGen(
        user_data=user_data2,
        method="parallel",
        output_file=tmpfile.name,
        weight_gen_crs=wght_gen_crs,
    )

    _wghts2 = weight_gen2.calculate_weights()  # noqa: F841

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data2,
        stat_method="mean",
        agg_engine="serial",
        agg_writer="csv",
        weights=_wghts2,
        out_path=tmpdir.name,
        file_prefix="test_agg_gen_2",
    )

    _ngdf, _nvals = agg_gen.calculate_agg()

    outfile = Path(tmpdir.name) / "test_agg_gen_2.csv"

    assert outfile.exists()
    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_nvals, xr.Dataset)
    del _nvals, _ngdf, outfile

    user_data3 = UserCatData(
        ds=get_xarray,
        proj_ds=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        var=tvar,
        f_feature=get_gdf,
        proj_feature=shp_crs,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )
    tmpdir2 = TemporaryDirectory()
    agg_gen = AggGen(
        user_data=user_data3,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="netcdf",
        weights=wghts,
        out_path=tmpdir2.name,
        file_prefix="test_agg_gen_3",
    )

    _ngdf, _nvals = agg_gen.calculate_agg()

    outfile = Path(tmpdir2.name) / "test_agg_gen_3.nc"

    assert outfile.exists()
    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_nvals, xr.Dataset)


def test_interp_gen_with_stac(
    collection: pystac.collection.Collection,
) -> None:
    """Test InterpGen: uses the linear interpolation method and the actual line points."""
    lines = gpd.read_file("./tests/data/test_lines.json")
    sdate = "1999-01-01"
    edate = "1999-01-07"
    var = ["PWAT"]
    shp_line_idx = "Permanent_Identifier"

    user_data = NHGFStacData(
        collection=collection, var=var, f_feature=lines, id_feature=shp_line_idx, period=[sdate, edate]
    )

    interp_object = InterpGen(user_data, pt_spacing=100, stat="all")

    stats, pts = interp_object.calc_interp()
    assert isinstance(stats, pd.DataFrame)
    assert isinstance(pts, gpd.GeoDataFrame)

    stats = stats[
        (stats["date"] == "1999-01-02") & (stats["Permanent_Identifier"] == "154309038") & (stats["varname"] == var[0])
    ]
    assert stats["mean"][1] == pytest.approx(0.010689812686360156, 0.000001)
    assert stats["median"][1] == pytest.approx(0.010696031665920279, 0.000001)
    assert stats["std"][1] == pytest.approx(4.246133670338439e-05, 0.000001)
    assert stats["max"][1] == pytest.approx(0.010746015539967901, 0.000001)
    assert stats["min"][1] == pytest.approx(0.010608248067669431, 0.000001)

    pts = pts.loc["1999-01-01"][
        (pts.loc["1999-01-01"]["Permanent_Identifier"] == "154309038") & (pts.loc["1999-01-01"]["varname"] == var[0])
    ]

    assert pts.loc[[0]]["values"][0] == pytest.approx(0.008165945155717, 0.00001)
    assert pts.loc[[1]]["dist"][1] == pytest.approx(100, 0.001)
    assert pts.loc[[1]]["geometry"][1].coords[0][0] == pytest.approx(-91.35099994145847, 0.00001)
    assert pts.loc[[1]]["geometry"][1].coords[0][1] == pytest.approx(41.429287499605856, 0.00001)


def test_interp_gen_with_climater(climr_cat_data: dict[str, Any]) -> None:
    """Test InterpGen: uses ClimateR source data, both Linear interpolation and Nearest \
    Neighbor methods and 1000 meter point spacing."""
    lines = gpd.read_file("./tests/data/test_lines.json")

    user_data = ClimRCatData(
        cat_dict=climr_cat_data,
        f_feature=lines,
        id_feature="Permanent_Identifier",
        period=["1980-10-01", "1980-10-01"],
    )

    interp_object = InterpGen(user_data, pt_spacing=100, stat="all")

    stats, pts = interp_object.calc_interp()
    assert isinstance(stats, pd.DataFrame)
    assert isinstance(pts, gpd.GeoDataFrame)

    stats = stats[
        (stats["date"] == "1980-10-01") & (stats["Permanent_Identifier"] == "154309038") & (stats["varname"] == "aet")
    ]
    assert stats["mean"][0] == pytest.approx(68.81906163977756, 0.0001)
    assert stats["median"][0] == pytest.approx(68.72597484153565, 0.0001)
    assert stats["std"][0] == pytest.approx(0.2442380929434198, 0.0001)
    assert stats["max"][0] == pytest.approx(69.3176096763355, 0.0001)
    assert stats["min"][0] == pytest.approx(68.44078166220153, 0.0001)

    pts = pts.loc["1980-10-01"][
        (pts.loc["1980-10-01"]["Permanent_Identifier"] == "154309038") & (pts.loc["1980-10-01"]["varname"] == "aet")
    ]

    assert pts.loc[[10]]["values"][10] == pytest.approx(68.51718977984109, 0.00001)
    assert pts.loc[[10]]["dist"][10] == pytest.approx(1000.0, 0.001)
    assert pts.loc[[10]]["geometry"][10].coords[0][0] == pytest.approx(-91.3547850586887, 0.00001)
    assert pts.loc[[10]]["geometry"][10].coords[0][1] == pytest.approx(41.42160652972089, 0.00001)

    # Run again with nearest sampling method
    interp_object2 = InterpGen(user_data, pt_spacing=100, interp_method="nearest", stat="all")
    stats2, pts2 = interp_object2.calc_interp()

    stats = stats2[
        (stats2["date"] == "1980-10-01")
        & (stats2["Permanent_Identifier"] == "154309038")
        & (stats2["varname"] == "aet")
    ]
    assert stats["mean"][0] == pytest.approx(68.77481, 0.0001)
    assert stats["median"][0] == pytest.approx(68.700005, 0.0001)
    assert stats["std"][0] == pytest.approx(0.3603098, 0.0001)
    assert stats["min"][0] == pytest.approx(68.400002, 0.0001)
    assert stats["max"][0] == pytest.approx(69.599998, 0.0001)

    pts = pts2.loc["1980-10-01"][
        (pts2.loc["1980-10-01"]["Permanent_Identifier"] == "154309038") & (pts2.loc["1980-10-01"]["varname"] == "aet")
    ]

    assert pts.loc[[10]]["values"][10] == pytest.approx(68.4, 0.001)
    assert pts.loc[[10]]["dist"][10] == pytest.approx(1000.0, 0.001)
    assert pts.loc[[10]]["geometry"][10].coords[0][0] == pytest.approx(-91.3547850586887, 0.00001)
    assert pts.loc[[10]]["geometry"][10].coords[0][1] == pytest.approx(41.42160652972089, 0.00001)


client.close()
del client
cluster.close()
del cluster
