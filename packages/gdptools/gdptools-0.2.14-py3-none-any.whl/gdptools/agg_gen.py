"""Calculate aggregation methods."""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

import geopandas as gpd
import netCDF4
import numpy as np
import numpy.typing as npt
import pandas as pd
import xarray as xr

from gdptools.agg.agg_data_writers import CSVWriter
from gdptools.agg.agg_data_writers import JSONWriter
from gdptools.agg.agg_data_writers import NetCDFWriter
from gdptools.agg.agg_data_writers import ParquetWriter
from gdptools.agg.agg_engines import DaskAgg
from gdptools.agg.agg_engines import DaskInterp
from gdptools.agg.agg_engines import ParallelAgg
from gdptools.agg.agg_engines import ParallelInterp
from gdptools.agg.agg_engines import SerialAgg
from gdptools.agg.agg_engines import SerialInterp
from gdptools.agg.stats_methods import Count
from gdptools.agg.stats_methods import MACount
from gdptools.agg.stats_methods import MAMax
from gdptools.agg.stats_methods import MAMin
from gdptools.agg.stats_methods import Sum
from gdptools.agg.stats_methods import MASum
from gdptools.agg.stats_methods import MAWeightedMean
from gdptools.agg.stats_methods import MAWeightedMedian
from gdptools.agg.stats_methods import MAWeightedStd
from gdptools.agg.stats_methods import Max
from gdptools.agg.stats_methods import Min
from gdptools.agg.stats_methods import WeightedMean
from gdptools.agg.stats_methods import WeightedMedian
from gdptools.agg.stats_methods import WeightedStd
from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import UserData

# write a docstring for STATSMETHODS below

STATSMETHODS = Literal[
    "masked_mean",
    "mean",
    "masked_std",
    "std",
    "masked_median",
    "median",
    "masked_count",
    "count",
    "masked_sum",
    "sum",
    "masked_min",
    "min",
    "masked_max",
    "max",
]
"""List of available aggregation methods.

- `masked_mean`: Masked mean of the data.
- `mean`: Mean of the data.
- `masked_std`: Masked standard deviation of the data.
- `std`: Standard deviation of the data.
- `masked_median`: Masked median of the data.
- `median`: Median of the data.
- `masked_count`: Masked count of the data.
- `count`: Count of the data.
- `masked_sum`: Masked sum of the data.
- `sum`: Sum of the data.
- `masked_min`: Masked minimum of the data.
- `min`: Minimum of the data.
- `masked_max`: Masked maximum of the data.
- `max`: Maximum of the data.

Raises:
    TypeError: If supplied attribute is not one of STATSMETHODS.
"""

AGGENGINES = Literal["serial", "parallel", "dask"]
""" List of aggregation methods.

- `serial`: performes weighted-area aggregation by iterating through polygons.
- `parallel`: performes weighted-area aggregation by number of jobs.
- `dask`: performs weighted-area aggregation in the presence of a dask client, the
        number of jobs should be specified.

Raises:
    TypeError: If supplied attribute is not one of AGGENGINES.
"""

AGGWRITERS = Literal["none", "csv", "parquet", "netcdf", "json"]
""" List of available writers applied to the aggregation.

- `none`: Output not written to a file.
- `csv`: Output data in csv format.
- `parquet`: Output data to parquet.gzip file.
- `netcdf`: Output data in netcdf format.
- `json`: Output data as json.

Raises:
    TypeError: If supplied attribute is not one of AGGWRITERS.
"""

WRITER_TYPES = Union[
    Type[None],
    Type[CSVWriter],
    Type[ParquetWriter],
    Type[NetCDFWriter],
    Type[JSONWriter],
]

AGG_ENGINE_TYPES = Union[Type[SerialAgg], Type[ParallelAgg], Type[DaskAgg]]

LINEITERPENGINES = Literal["serial", "parallel", "dask"]
""" List of aggregation methods.

- `serial`: performes weighted-area aggregation by iterating through polygons.
- `parallel`: performes weighted-area aggregation by number of jobs.
- `dask`: performs weighted-area aggregation in the presence of a dask client, the
        number of jobs should be specified.

Raises:
    TypeError: If supplied attribute is not one of AGGENGINES.
"""


class AggGen:
    """Class for aggregating grid-to-polygons.

    This class provides methods for aggregating gridded data to polygons using
    area-weighted statistics. The class is initialized with various parameters
    including user data, statistical methods, aggregation engine, and more.
    """

    def __init__(
        self,
        user_data: UserData,
        stat_method: STATSMETHODS,
        agg_engine: AGGENGINES,
        agg_writer: AGGWRITERS,
        weights: Union[str, pd.DataFrame],
        out_path: Optional[Union[str, None]] = None,
        file_prefix: Optional[Union[str, None]] = None,
        append_date: Optional[bool] = False,
        precision: Optional[int] = None,
        jobs: Optional[int] = -1,
    ) -> None:
        """Initialize AggGen.

        AggGen is a class for aggregating gridded datasets to polygons using
        area-weighted statistics. The class takes various parameters including
        user data, statistical methods, aggregation engine, and more.

        Args:
            user_data (UserData): Data object, one of UserCatData, ClimateCatData.
            stat_method (STATSMETHODS): Statistical method, one of STATSMETHODS.
            agg_engine (AGGENGINES): Aggregation engine, one of AGGENGINES.
            agg_writer (AGGWRITERS): Aggregation writer, one of AGGWRITERS.
            weights (Union[str, pd.DataFrame]): Path to CSV or DataFrame containing weights.
            out_path (Optional[str], default=None): Optional output path.
            file_prefix (Optional[str], default=None): Optional file prefix.
            append_date (Optional[bool], default=False): Append date to file name if True.
            precision (Optional[int], defualt=None): The precision of the output if specified.
            jobs (Optional[int], default=-1): Number of processors for parallel or dask methods.
        """
        self._user_data = user_data
        self._stat_method = stat_method
        self._agg_engine = agg_engine
        self._agg_writer = agg_writer
        self._weights = weights
        self._out_path = out_path
        self._file_prefix = file_prefix
        self._append_date = append_date
        self._precision = precision
        self._jobs: int = jobs
        self._agg_data: Dict[str, AggData]
        self._set_stats_method()
        self._set_agg_engine()
        self._set_writer()

    def _set_writer(self):
        if self._agg_writer != "none" and ((self._out_path is None) or (self._file_prefix is None)):
            raise ValueError(
                f"If agg_writer not none, then out_path: {self._out_path}"
                f" and file_prefix: {self._file_prefix} must be set."
            )
        self.__writer: WRITER_TYPES

        if self._agg_writer == "none":
            self.__writer = None
        else:
            writers = {
                "csv": CSVWriter,
                "parquet": ParquetWriter,
                "netcdf": NetCDFWriter,
                "json": JSONWriter,
            }
            try:
                self.__writer = writers[self._agg_writer]
            except Exception as exc:
                raise TypeError(f"agg_writer: {self._agg_writer} not in {AGGWRITERS}") from exc

    def _set_agg_engine(self):
        self.agg: AGG_ENGINE_TYPES

        engines = {"serial": SerialAgg, "parallel": ParallelAgg, "dask": DaskAgg}
        try:
            self.agg = engines[self._agg_engine]
        except Exception as exc:
            raise TypeError(f"agg_engine: {self._agg_engine} not in {AGGENGINES}") from exc

    def _set_stats_method(self):
        methods = {
            "masked_mean": MAWeightedMean,
            "masked_std": MAWeightedStd,
            "masked_median": MAWeightedMedian,
            "masked_count": MACount,
            "masked_sum": MASum,
            "masked_min": MAMin,
            "masked_max": MAMax,
            "mean": WeightedMean,
            "std": WeightedStd,
            "median": WeightedMedian,
            "count": Count,
            "sum": Sum,
            "min": Min,
            "max": Max,
        }
        self._stat = methods.get(self._stat_method)
        if self._stat is None:
            raise TypeError(f"stat_method: {self._stat_method} not in {STATSMETHODS}")

    def calculate_agg(
        self,
    ) -> Tuple[gpd.GeoDataFrame, xr.Dataset]:
        """Calculate and return aggregations for target polygon data based on source gridded data.

        Interpolates source gridded data to target polygon data for a specified period.
        The output format is determined by the `agg_writer` method.

        Returns:
            Tuple[gpd.GeoDataFrame, xr.Dataset]: Calculated aggregations.

            - **gpd.GeoDataFrame**: Sorted and dissolved target GeoDataFrame. Multiple features with the same
                `id_feature` are merged into a single MultiPolygon.

            - **xr.Dataset**: Dataset containing all variables from the `UserData` class, dimensioned by time and
                `id_feature`.

        Example:
            >>> obj = AggGen()  # Initialize the AggGen class
            >>> gdf, ds = obj.calculate_agg()
        """
        self._agg_data, new_gdf, agg_vals = self.agg().calc_agg_from_dictmeta(
            user_data=self._user_data,
            weights=self._weights,
            stat=self._stat,
            jobs=self._jobs,
        )
        if self._agg_writer != "none":
            self.__writer().save_file(
                agg_data=self._agg_data,
                feature=new_gdf,
                vals=agg_vals,
                p_out=self._out_path,
                file_prefix=self._file_prefix,
                append_date=self._append_date,
                precision=self._precision,
            )

        return new_gdf, self._gen_xarray_return(feature=new_gdf, vals=agg_vals)

    @property
    def agg_data(self) -> dict[str, AggData]:
        """Return agg_data."""
        return self._agg_data

    def _gen_xarray_return(
        self,
        feature: gpd.GeoDataFrame,
        vals: List[npt.NDArray[Union[np.int_, np.double]]],
    ) -> xr.Dataset:
        """Generate xarray return."""
        dataset = []
        for idx, (_key, value) in enumerate(self._agg_data.items()):
            gdf = feature
            gdf_idx = value.id_feature
            param_values = value.cat_cr
            t_coord = param_values.T_name
            v_units = param_values.units
            v_varname = param_values.varname
            v_long_name = param_values.long_name
            time = value.da.coords[t_coord].values
            # locs = gdf.index.values
            locs = gdf[gdf_idx].values
            if self._precision is not None:
                data_vals = np.round(vals[idx], self._precision)
            else:
                data_vals = vals[idx]
            dsn = xr.Dataset(
                data_vars={
                    v_varname: (
                        ["time", gdf_idx],
                        data_vals,
                        dict(units=v_units, long_name=v_long_name, coordinates="time", grid_mapping="crs"),
                    ),
                },
                coords={
                    "time": time,
                    gdf_idx: ([gdf_idx], locs, {"feature_id": gdf_idx}),
                },
            )
            if vals[idx].dtype.str == "<f8":
                dsn[v_varname].encoding.update({"_FillValue": netCDF4.default_fillvals["f8"]})
            elif vals[idx].dtype.str == "<i8":
                dsn[v_varname].encoding.update({"_FillValue": netCDF4.default_fillvals["i8"]})

            dataset.append(dsn)
        if len(dataset) > 1:
            ds = xr.merge(dataset)
        else:
            ds = dsn
        ds.encoding["time"] = {"unlimited": True}
        fdate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        ds.attrs = {
            "Conventions": "CF-1.8",
            "featureType": "timeSeries",
            "history": (
                f"{fdate} Original filec created  by gdptools package: "
                "https://code.usgs.gov/wma/nhgf/toolsteam/gdptools \n"
            ),
        }
        return ds


class InterpGen:
    """Class for calculating grid statistics along a polyline geometry.

    This class provides methods for interpolating gridded data to a polyline
    and calculating various statistics along the line.
    """

    def __init__(
        self,
        user_data: UserData,
        *,
        pt_spacing: Union[float, int, None] = 50,
        stat: str = "all",
        interp_method: str = "linear",
        mask_data: Union[bool, None] = False,
        output_file: Union[str, None] = None,
        calc_crs: Any = 6931,
        method: LINEITERPENGINES = "serial",
        jobs: Optional[int] = -1,
    ) -> None:
        """Initialize InterpGen class.

        Args:
            user_data (UserData): Data class for input data.
            pt_spacing (Union[float, int, None], optional): Spacing of interpolated sample points in meters. Defaults
                to 50.
            stat (str): Statistics to calculate. Options are 'all', 'mean', 'median', 'std', 'max', 'min'.
                Defaults to 'all'.
            interp_method (str): xarray interpolation method. Defaults to 'linear'.
            mask_data (Union[bool, None], optional): Remove nodata values if True. Defaults to False.
            output_file (Union[str, None], optional): File path for CSV output, must end with .csv. Defaults to None.
            calc_crs (Any): Projection for area-weighted calculations. Defaults to 6933.
            method (LINEITERPENGINES): Methodology for query. Default is 'serial'.
            jobs (Optional[int], optional): Number of processors for parallel methods. If set to -1, half of the
                available processors will be used. Defaults to -1.
        """
        self._user_data = user_data
        self._line = user_data.f_feature
        self._pt_spacing = pt_spacing
        self._stat = stat
        self._interp_method = interp_method
        self._mask_data = mask_data
        self._output_file = output_file
        self._calc_crs = calc_crs
        self._method = method
        self._jobs = jobs

    def calc_interp(self) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Run interpolation and statistical calculations along the polyline.

        This method performs the interpolation and calculates the specified statistics
        based on the method chosen during initialization.

        Raises:
            ValueError: If the interpolation method specified is not supported.

        Returns:
            Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]: The calculated statistics and points.
        """
        interp_engine = {
            "serial": SerialInterp,
            "parallel": ParallelInterp,
            "dask": DaskInterp,
        }

        # Check if the method is available
        if self._method.lower() not in interp_engine:
            raise ValueError(
                f"Invalid method: {self._method}. Available methods are: {', '.join(interp_engine.keys())}"
            )

        self._interp_data, stats, pts = interp_engine[self._method]().run(
            user_data=self._user_data,
            pt_spacing=self._pt_spacing,
            stat=self._stat,
            interp_method=self._interp_method,
            calc_crs=self._calc_crs,
            mask_data=self._mask_data,
            output_file=self._output_file,
        )

        return stats, pts
