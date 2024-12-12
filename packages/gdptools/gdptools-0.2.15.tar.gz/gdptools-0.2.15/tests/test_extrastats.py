"""Test scripts for stats methods."""

import gc
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
import xarray as xr
from dask.distributed import Client
from dask.distributed import LocalCluster

from gdptools import AggGen
from gdptools import UserCatData
from gdptools import WeightGen

gm_vars = ["aet"]

# Boot up a dask client
cluster = LocalCluster(threads_per_worker=os.cpu_count())
client = Client(cluster)  # type: ignore


@pytest.fixture(scope="function")
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    gdf = gpd.read_file("./tests/data/capecod_huc12.shp").dissolve(
        by=["huc12", "tohuc", "name", "hutype", "humod", "noncontrib", "states"],
        aggfunc="sum",
        as_index=False,
        dropna=False,
    )
    yield gdf
    del gdf
    gc.collect()


@pytest.fixture(scope="function")
def get_xarray() -> xr.Dataset:
    """Create xarray dataset."""
    ds = xr.open_dataset("./tests/data/rasters/climate/terraclim_aet_capecod.nc")
    yield ds
    del ds
    gc.collect()


@pytest.fixture(scope="function")
def get_out_path(tmp_path: Path) -> Path:
    """Get temp file path."""
    return tmp_path


data_crs = 4326
x_coord = "lon"
y_coord = "lat"
t_coord = "time"
sdate = "1980-01-01"
edate = "1980-12-01"
var = ["aet"]
shp_crs = 4326
shp_poly_idx = "huc12"
wght_gen_crs = 6931
stats_agg_file_prefix = "extra_stats_test"

stats_test_dict = {
    "mean": np.array(
        [
            101.16062306991417,
            101.89667307594982,
            101.2733032241714,
            9.969209968386869e36,
            100.9036416305431,
            101.91529811292946,
            101.03068109986368,
            98.46565574058324,
            93.07121115331904,
            92.45570806658066,
            90.48008765075167,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            101.40248301493793,
            101.8873294510659,
            99.50107851056474,
            100.4309934822545,
            100.62063622592113,
            9.969209968386869e36,
            9.969209968386869e36,
            101.69107103850423,
            102.24948948225652,
            100.47079170743466,
            98.34781450367866,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            101.68587686693002,
            101.56572558541157,
            102.0937536384102,
            101.76418440396608,
            102.42196633387192,
            101.6329372224863,
            98.96916760272836,
        ]
    ),
    "masked_mean": np.array(
        [
            101.16062306991417,
            101.8966730759498,
            101.2733032241714,
            100.05816974966501,
            100.9036416305431,
            101.91529811292946,
            101.03068109986368,
            98.46565574058326,
            93.07121115331904,
            92.45570806658064,
            90.48008765075167,
            78.49760907203974,
            89.34413144809446,
            96.99061669351724,
            101.40248301493793,
            101.88732945106588,
            99.50107851056474,
            100.4309934822545,
            100.62063622592113,
            101.78268552575857,
            102.62499140614398,
            101.69107103850423,
            102.24948948225654,
            100.47079170743463,
            98.34781450367868,
            94.55486649072155,
            94.7903818181858,
            95.65744527770667,
            82.02395986050959,
            101.68587686693002,
            101.56572558541158,
            102.0937536384102,
            101.76418440396608,
            102.4219663338719,
            101.6329372224863,
            98.96916760272835,
        ]
    ),
    "std": np.array(
        [
            1.0003892091786877,
            0.7911563045720997,
            0.4080304233840606,
            9.969209968386869e36,
            1.0277142628879288,
            0.2986934885356372,
            0.785698687017503,
            1.6931545704992268,
            0.33980162501226735,
            0.12425810081148257,
            5.242918161308443,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            0.3387121300010567,
            0.36494767602363687,
            0.3573982816668527,
            0.7416486484984715,
            0.40021744002823045,
            9.969209968386869e36,
            9.969209968386869e36,
            1.3413452046562988,
            0.31630355993647824,
            0.9006479322725042,
            0.7652429313689281,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            0.4111362583884137,
            0.35439110939858265,
            0.35941018152546117,
            0.23746710411094515,
            0.30436852468370656,
            0.644496557408004,
            0.9845920100477381,
        ]
    ),
    "masked_std": np.array(
        [
            1.0003892091786877,
            0.7911563045720997,
            0.40803042338406065,
            0.4671860532554067,
            1.0277142628879288,
            0.2986934885356372,
            0.785698687017503,
            1.6931545704992266,
            0.33980162501226735,
            0.12425810081148257,
            5.242918161308443,
            4.839172437349917,
            6.940672409870688,
            1.2336661663479385,
            0.3387121300010567,
            0.3649476760236368,
            0.3573982816668527,
            0.7416486484984716,
            0.40021744002823045,
            0.6866778538007787,
            0.9851531167641697,
            1.3413452046562986,
            0.31630355993647824,
            0.9006479322725042,
            0.7652429313689281,
            0.9256468704805688,
            0.7061713502404676,
            0.668180555414047,
            7.396964065744921,
            0.4111362583884137,
            0.35439110939858265,
            0.3594101815254612,
            0.23746710411094518,
            0.3043685246837065,
            0.644496557408004,
            0.9845920100477382,
        ]
    ),
    "median": np.array(
        [
            101.10537131764697,
            101.48510789710312,
            101.22466385452995,
            9.969209968386869e36,
            101.0,
            102.01741256698185,
            101.15604005047945,
            98.98601240869728,
            93.06418297794386,
            92.5,
            92.59287203005034,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            101.43751981564013,
            101.99884887421094,
            99.5,
            100.45869944074289,
            100.48416231907657,
            9.969209968386869e36,
            9.969209968386869e36,
            101.59732979273177,
            102.23963178743178,
            100.36835267411982,
            98.41374240472904,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            101.5,
            101.52421925155595,
            101.99409926614607,
            101.70000457763672,
            102.5,
            101.76145088744256,
            99.18132200288065,
        ]
    ),
    "masked_median": np.array(
        [
            101.10537131764697,
            101.48510789710312,
            101.22466385452995,
            100.01632482293296,
            101.0,
            102.01741256698185,
            101.15604005047945,
            98.98601240869728,
            93.06418297794386,
            92.5,
            92.59287203005034,
            76.80000305175781,
            92.70000457763672,
            97.20000457763672,
            101.43751981564013,
            101.99884887421094,
            99.5,
            100.45869944074289,
            100.48416231907657,
            101.70000457763672,
            102.61069426119117,
            101.59732979273177,
            102.23963178743178,
            100.36835267411982,
            98.41374240472904,
            94.6028114712023,
            94.84716934734533,
            95.71593896988016,
            85.13760159877924,
            101.5,
            101.52421925155595,
            101.99409926614607,
            101.70000457763672,
            102.5,
            101.76145088744256,
            99.18132200288065,
        ]
    ),
    "count": np.array(
        [
            18.0,
            11.0,
            19.0,
            16.0,
            17.0,
            13.0,
            14.0,
            16.0,
            6.0,
            8.0,
            10.0,
            10.0,
            32.0,
            58.0,
            14.0,
            21.0,
            11.0,
            19.0,
            7.0,
            18.0,
            20.0,
            20.0,
            12.0,
            23.0,
            8.0,
            16.0,
            17.0,
            15.0,
            22.0,
            17.0,
            19.0,
            18.0,
            9.0,
            15.0,
            12.0,
            19.0,
        ]
    ),
    "masked_count": np.array(
        [
            18.0,
            11.0,
            19.0,
            15.0,
            17.0,
            13.0,
            14.0,
            16.0,
            6.0,
            8.0,
            10.0,
            9.0,
            31.0,
            56.0,
            14.0,
            21.0,
            11.0,
            19.0,
            7.0,
            16.0,
            19.0,
            20.0,
            12.0,
            23.0,
            8.0,
            14.0,
            16.0,
            13.0,
            18.0,
            17.0,
            19.0,
            18.0,
            9.0,
            15.0,
            12.0,
            19.0,
        ]
    ),
    "min": np.array(
        [
            98.5999984741211,
            101.0,
            99.5,
            9.969209968386869e36,
            93.20000457763672,
            101.0,
            98.80000305175781,
            90.5,
            92.30000305175781,
            92.30000305175781,
            76.70000457763672,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            100.4000015258789,
            100.5999984741211,
            98.70000457763672,
            98.5,
            100.20000457763672,
            9.969209968386869e36,
            9.969209968386869e36,
            98.9000015258789,
            101.4000015258789,
            98.4000015258789,
            94.9000015258789,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            101.20000457763672,
            101.20000457763672,
            101.4000015258789,
            101.30000305175781,
            101.80000305175781,
            100.5,
            94.9000015258789,
        ]
    ),
    "masked_min": np.array(
        [
            98.5999984741211,
            101.0,
            99.5,
            98.5999984741211,
            93.20000457763672,
            101.0,
            98.80000305175781,
            90.5,
            92.30000305175781,
            92.30000305175781,
            76.70000457763672,
            76.70000457763672,
            75.80000305175781,
            94.0999984741211,
            100.4000015258789,
            100.5999984741211,
            98.70000457763672,
            98.5,
            100.20000457763672,
            100.20000457763672,
            99.70000457763672,
            98.9000015258789,
            101.4000015258789,
            98.4000015258789,
            94.9000015258789,
            92.80000305175781,
            93.70000457763672,
            92.70000457763672,
            66.80000305175781,
            101.20000457763672,
            101.20000457763672,
            101.4000015258789,
            101.30000305175781,
            101.80000305175781,
            100.5,
            94.9000015258789,
        ]
    ),
    "max": np.array(
        [
            103.0999984741211,
            103.0999984741211,
            101.80000305175781,
            9.969209968386869e36,
            102.0999984741211,
            102.5,
            102.5,
            100.0999984741211,
            93.5999984741211,
            93.5999984741211,
            92.9000015258789,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            102.0999984741211,
            102.5,
            100.30000305175781,
            101.9000015258789,
            101.4000015258789,
            9.969209968386869e36,
            9.969209968386869e36,
            103.9000015258789,
            103.0,
            102.5,
            99.5999984741211,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            9.969209968386869e36,
            103.0999984741211,
            102.5,
            102.9000015258789,
            102.20000457763672,
            102.9000015258789,
            102.9000015258789,
            101.0,
        ]
    ),
    "masked_max": np.array(
        [
            103.0999984741211,
            103.0999984741211,
            101.80000305175781,
            101.30000305175781,
            102.0999984741211,
            102.5,
            102.5,
            100.0999984741211,
            93.5999984741211,
            93.5999984741211,
            92.9000015258789,
            92.20000457763672,
            94.9000015258789,
            99.5,
            102.0999984741211,
            102.5,
            100.30000305175781,
            101.9000015258789,
            101.4000015258789,
            103.5,
            103.9000015258789,
            103.9000015258789,
            103.0,
            102.5,
            99.5999984741211,
            96.5,
            96.70000457763672,
            96.70000457763672,
            88.0,
            103.0999984741211,
            102.5,
            102.9000015258789,
            102.20000457763672,
            102.9000015258789,
            102.9000015258789,
            101.0,
        ]
    ),
    "sum": np.array(
        [
            1.81600000e03,
            1.12000000e03,
            1.92190002e03,
            9.96920997e36,
            1.70689990e03,
            1.32399988e03,
            1.40969995e03,
            1.56140002e03,
            5.57599976e02,
            7.40899963e02,
            8.76800049e02,
            9.96920997e36,
            9.96920997e36,
            9.96920997e36,
            1.41959985e03,
            2.13659985e03,
            1.09380005e03,
            1.90480017e03,
            7.05000000e02,
            9.96920997e36,
            9.96920997e36,
            2.02659985e03,
            1.22800000e03,
            2.31119995e03,
            7.84299988e02,
            9.96920997e36,
            9.96920997e36,
            9.96920997e36,
            9.96920997e36,
            1.72920007e03,
            1.93219995e03,
            1.83870007e03,
            9.16100037e02,
            1.53469983e03,
            1.21970007e03,
            1.87909985e03,
        ]
    ),
    "masked_sum": np.array(
        [
            1816.0,
            1120.0,
            1921.90002441,
            1501.69995117,
            1706.89990234,
            1323.99987793,
            1409.69995117,
            1561.40002441,
            557.59997559,
            740.89996338,
            876.80004883,
            737.80004883,
            2730.19995117,
            5421.79980469,
            1419.59985352,
            2136.59985352,
            1093.80004883,
            1904.8001709,
            705.0,
            1626.79980469,
            1939.69995117,
            2026.59985352,
            1228.0,
            2311.19995117,
            784.29998779,
            1323.29992676,
            1519.20007324,
            1241.29992676,
            1483.40002441,
            1729.20007324,
            1932.19995117,
            1838.70007324,
            916.10003662,
            1534.6998291,
            1219.70007324,
            1879.09985352,
        ]
    ),
}


def test_calculate_weights_serial(get_xarray, get_gdf, get_out_path) -> None:
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
    )

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tempfile.name,
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    for stat in ["mean", "std", "min", "max", "sum"]:
        tmpdir = TemporaryDirectory()
        reference_array = stats_test_dict[stat]
        agg_gen = AggGen(
            user_data=user_data,
            stat_method=stat,
            agg_engine="serial",
            agg_writer="csv",
            weights=tempfile.name,
            out_path=tmpdir.name,
            file_prefix=stats_agg_file_prefix,
        )

        _ngdf, _vals = agg_gen.calculate_agg()

        assert isinstance(_ngdf, gpd.GeoDataFrame)
        assert isinstance(_vals, xr.Dataset)

        _testvals = _vals[var[0]].isel(time=5).values

        # assert (
        #     len(reference_array[np.isnan(reference_array)])
        #     == len(_testvals[np.isnan(_testvals)])
        #     == 10
        # )
        np.testing.assert_allclose(
            _testvals[~np.isnan(_testvals)],
            reference_array[~np.isnan(reference_array)],
            rtol=1e-4,
            verbose=True,
        )

        ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
        assert ofile.exists()

        outfile = pd.read_csv(ofile)
        print(outfile.head())

    for stat in [
        "masked_mean",
        "masked_std",
        "masked_median",
        "masked_min",
        "masked_max",
        "masked_count",
        "count",
        "masked_sum",
    ]:
        tmpdir = TemporaryDirectory()
        reference_array = stats_test_dict[stat]
        agg_gen = AggGen(
            user_data=user_data,
            stat_method=stat,
            agg_engine="serial",
            agg_writer="csv",
            weights=tempfile.name,
            out_path=tmpdir.name,
            file_prefix=stats_agg_file_prefix,
        )

        _ngdf, _vals = agg_gen.calculate_agg()

        assert isinstance(_ngdf, gpd.GeoDataFrame)
        assert isinstance(_vals, xr.Dataset)

        _testvals = _vals[var[0]].isel(time=5).values

        assert len(reference_array[np.isnan(reference_array)]) == len(_testvals[np.isnan(_testvals)]) == 0
        np.testing.assert_allclose(
            _testvals[~np.isnan(_testvals)],
            reference_array[~np.isnan(reference_array)],
            rtol=1e-2,
            verbose=True,
        )

        ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
        assert ofile.exists()

        outfile = pd.read_csv(ofile)
        print(outfile.head())


def test_calculate_weights_serial_median(get_xarray, get_gdf, get_out_path) -> None:
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
    )

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tempfile.name,
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    stat = "median"
    tmpdir = TemporaryDirectory()
    reference_array = stats_test_dict[stat]
    agg_gen = AggGen(
        user_data=user_data,
        stat_method=stat,
        agg_engine="serial",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        file_prefix=stats_agg_file_prefix,
    )

    _ngdf, _vals = agg_gen.calculate_agg()

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_vals, xr.Dataset)

    # _testvals = _vals[0][5, :]
    _testvals = _vals[gm_vars[0]][5, :]

    # assert (
    #     len(reference_array[np.isnan(reference_array)])
    #     == len(_testvals[np.isnan(_testvals)])
    #     == 10
    # )
    np.testing.assert_allclose(
        _testvals[~np.isnan(_testvals)],
        reference_array[~np.isnan(reference_array)],
        rtol=1e-2,
        verbose=True,
    )

    ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
    assert ofile.exists()

    outfile = pd.read_csv(ofile)
    print(outfile.head())

    stat = "masked_median"
    tmpdir = TemporaryDirectory()
    reference_array = stats_test_dict[stat]
    agg_gen = AggGen(
        user_data=user_data,
        stat_method=stat,
        agg_engine="serial",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        file_prefix=stats_agg_file_prefix,
    )

    _ngdf, _vals = agg_gen.calculate_agg()

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_vals, xr.Dataset)

    _testvals = _vals[gm_vars[0]][5, :]

    # assert (
    #     len(reference_array[np.isnan(reference_array)])
    #     == len(_testvals[np.isnan(_testvals)])
    #     == 0
    # )
    np.testing.assert_allclose(
        _testvals[~np.isnan(_testvals)],
        reference_array[~np.isnan(reference_array)],
        rtol=1e-2,
        verbose=True,
    )

    ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
    assert ofile.exists()

    outfile = pd.read_csv(ofile)
    print(outfile.head())


def test_calculate_weights_dask(get_xarray, get_gdf, get_out_path) -> None:
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
    )

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="dask",
        output_file=tempfile.name,
        weight_gen_crs=wght_gen_crs,
        jobs=4,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    for stat in ["mean", "std", "min", "max", "sum"]:
        tmpdir = TemporaryDirectory()
        reference_array = stats_test_dict[stat]
        agg_gen = AggGen(
            user_data=user_data,
            stat_method=stat,
            agg_engine="dask",
            agg_writer="csv",
            weights=tempfile.name,
            out_path=tmpdir.name,
            file_prefix=stats_agg_file_prefix,
            jobs=4,
        )

        _ngdf, _vals = agg_gen.calculate_agg()

        assert isinstance(_ngdf, gpd.GeoDataFrame)
        assert isinstance(_vals, xr.Dataset)

        _testvals = _vals[gm_vars[0]][5, :]

        # assert (
        #     len(reference_array[np.isnan(reference_array)])
        #     == len(_testvals[np.isnan(_testvals)])
        #     == 10
        # )
        np.testing.assert_allclose(
            _testvals[~np.isnan(_testvals)],
            reference_array[~np.isnan(reference_array)],
            rtol=1e-4,
            verbose=True,
        )

        ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
        assert ofile.exists()

        outfile = pd.read_csv(ofile)
        print(outfile.head())

    for stat in ["masked_mean", "masked_std", "masked_min", "masked_max", "masked_count", "count", "masked_sum"]:
        tmpdir = TemporaryDirectory()
        reference_array = stats_test_dict[stat]
        agg_gen = AggGen(
            user_data=user_data,
            stat_method=stat,
            agg_engine="dask",
            agg_writer="csv",
            weights=tempfile.name,
            out_path=tmpdir.name,
            file_prefix=stats_agg_file_prefix,
            jobs=4,
        )

        _ngdf, _vals = agg_gen.calculate_agg()

        assert isinstance(_ngdf, gpd.GeoDataFrame)
        assert isinstance(_vals, xr.Dataset)

        _testvals = _vals[gm_vars[0]][5, :]

        # assert (
        #     len(reference_array[np.isnan(reference_array)])
        #     == len(_testvals[np.isnan(_testvals)])
        #     == 0
        # )
        np.testing.assert_allclose(
            _testvals[~np.isnan(_testvals)],
            reference_array[~np.isnan(reference_array)],
            rtol=1e-4,
            verbose=True,
        )

        ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
        assert ofile.exists()

        outfile = pd.read_csv(ofile)
        print(outfile.head())


def test_calculate_weights_dask_median(get_xarray, get_gdf, get_out_path) -> None:
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
    )

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="dask",
        output_file=tempfile.name,
        weight_gen_crs=wght_gen_crs,
        jobs=4,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    stat = "median"
    tmpdir = TemporaryDirectory()
    reference_array = stats_test_dict[stat]
    agg_gen = AggGen(
        user_data=user_data,
        stat_method=stat,
        agg_engine="dask",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        file_prefix=stats_agg_file_prefix,
        jobs=4,
    )

    _ngdf, _vals = agg_gen.calculate_agg()

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_vals, xr.Dataset)

    _testvals = _vals[gm_vars[0]][5, :]

    # assert (
    #     len(reference_array[np.isnan(reference_array)])
    #     == len(_testvals[np.isnan(_testvals)])
    #     == 10
    # )
    np.testing.assert_allclose(
        _testvals[~np.isnan(_testvals)],
        reference_array[~np.isnan(reference_array)],
        rtol=1e-2,
        verbose=True,
    )

    ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
    assert ofile.exists()

    outfile = pd.read_csv(ofile)
    print(outfile.head())

    stat = "masked_median"
    tmpdir = TemporaryDirectory()
    reference_array = stats_test_dict[stat]
    agg_gen = AggGen(
        user_data=user_data,
        stat_method=stat,
        agg_engine="dask",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        file_prefix=stats_agg_file_prefix,
        jobs=4,
    )

    _ngdf, _vals = agg_gen.calculate_agg()

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_vals, xr.Dataset)

    _testvals = _vals[gm_vars[0]][5, :]

    # assert (
    #     len(reference_array[np.isnan(reference_array)])
    #     == len(_testvals[np.isnan(_testvals)])
    #     == 0
    # )
    np.testing.assert_allclose(
        _testvals[~np.isnan(_testvals)],
        reference_array[~np.isnan(reference_array)],
        rtol=1e-2,
        verbose=True,
    )

    ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
    assert ofile.exists()

    outfile = pd.read_csv(ofile)
    print(outfile.head())


def test_calculate_weights_parallel(get_xarray, get_gdf, get_out_path) -> None:
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
    )

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="parallel",
        output_file=tempfile.name,
        weight_gen_crs=wght_gen_crs,
        jobs=4,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    for stat in ["mean", "std", "min", "max", "sum"]:
        tmpdir = TemporaryDirectory()
        reference_array = stats_test_dict[stat]
        agg_gen = AggGen(
            user_data=user_data,
            stat_method=stat,
            agg_engine="parallel",
            agg_writer="csv",
            weights=tempfile.name,
            out_path=tmpdir.name,
            file_prefix=stats_agg_file_prefix,
            jobs=4,
        )

        _ngdf, _vals = agg_gen.calculate_agg()

        assert isinstance(_ngdf, gpd.GeoDataFrame)
        assert isinstance(_vals, xr.Dataset)

        _testvals = _vals[gm_vars[0]][5, :]

        # assert (
        #     len(reference_array[np.isnan(reference_array)])
        #     == len(_testvals[np.isnan(_testvals)])
        #     == 10
        # )
        np.testing.assert_allclose(
            _testvals[~np.isnan(_testvals)],
            reference_array[~np.isnan(reference_array)],
            rtol=1e-4,
            verbose=True,
        )

        ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
        assert ofile.exists()

        outfile = pd.read_csv(ofile)
        print(outfile.head())

    for stat in ["masked_mean", "masked_std", "masked_min", "masked_max", "masked_count", "count", "masked_sum"]:
        tmpdir = TemporaryDirectory()
        reference_array = stats_test_dict[stat]
        agg_gen = AggGen(
            user_data=user_data,
            stat_method=stat,
            agg_engine="parallel",
            agg_writer="csv",
            weights=tempfile.name,
            out_path=tmpdir.name,
            file_prefix=stats_agg_file_prefix,
            jobs=4,
        )

        _ngdf, _vals = agg_gen.calculate_agg()

        assert isinstance(_ngdf, gpd.GeoDataFrame)
        assert isinstance(_vals, xr.Dataset)

        _testvals = _vals[gm_vars[0]][5, :]

        # assert (
        #     len(reference_array[np.isnan(reference_array)])
        #     == len(_testvals[np.isnan(_testvals)])
        #     == 0
        # )
        np.testing.assert_allclose(
            _testvals[~np.isnan(_testvals)],
            reference_array[~np.isnan(reference_array)],
            rtol=1e-4,
            verbose=True,
        )

        ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
        assert ofile.exists()

        outfile = pd.read_csv(ofile)
        print(outfile.head())


def test_calculate_weights_parallel_median(get_xarray, get_gdf, get_out_path) -> None:
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
    )

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="parallel",
        output_file=tempfile.name,
        weight_gen_crs=wght_gen_crs,
        jobs=4,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    stat = "median"
    tmpdir = TemporaryDirectory()
    reference_array = stats_test_dict[stat]
    agg_gen = AggGen(
        user_data=user_data,
        stat_method=stat,
        agg_engine="parallel",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        file_prefix=stats_agg_file_prefix,
        jobs=4,
    )

    _ngdf, _vals = agg_gen.calculate_agg()

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_vals, xr.Dataset)

    _testvals = _vals[gm_vars[0]][5, :]

    # assert (
    #     len(reference_array[np.isnan(reference_array)])
    #     == len(_testvals[np.isnan(_testvals)])
    #     == 10
    # )
    np.testing.assert_allclose(
        _testvals[~np.isnan(_testvals)],
        reference_array[~np.isnan(reference_array)],
        rtol=1e-2,
        verbose=True,
    )

    ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
    assert ofile.exists()

    outfile = pd.read_csv(ofile)
    print(outfile.head())

    stat = "masked_median"
    tmpdir = TemporaryDirectory()
    reference_array = stats_test_dict[stat]
    agg_gen = AggGen(
        user_data=user_data,
        stat_method=stat,
        agg_engine="parallel",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        file_prefix=stats_agg_file_prefix,
        jobs=4,
    )

    _ngdf, _vals = agg_gen.calculate_agg()

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_vals, xr.Dataset)

    _testvals = _vals[gm_vars[0]][5, :]

    # assert (
    #     len(reference_array[np.isnan(reference_array)])
    #     == len(_testvals[np.isnan(_testvals)])
    #     == 0
    # )
    np.testing.assert_allclose(
        _testvals[~np.isnan(_testvals)],
        reference_array[~np.isnan(reference_array)],
        rtol=1e-2,
        verbose=True,
    )

    ofile = Path(tmpdir.name) / (stats_agg_file_prefix + ".csv")
    assert ofile.exists()

    outfile = pd.read_csv(ofile)
    print(outfile.head())


cluster.close()
client.close()
del client
del cluster
