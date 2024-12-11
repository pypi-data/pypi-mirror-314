"""Aggregation engines."""

import contextlib
import logging
import os
import time
from abc import ABC
from abc import abstractmethod
from collections import namedtuple
from collections.abc import Generator
from typing import Any
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

import dask
import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import xarray as xr
from joblib import delayed
from joblib import Parallel
from joblib import parallel_backend

from gdptools.agg.stats_methods import Count
from gdptools.agg.stats_methods import MACount
from gdptools.agg.stats_methods import MAMax
from gdptools.agg.stats_methods import MAMin
from gdptools.agg.stats_methods import MAWeightedMean
from gdptools.agg.stats_methods import MAWeightedMedian
from gdptools.agg.stats_methods import MAWeightedStd
from gdptools.agg.stats_methods import Max
from gdptools.agg.stats_methods import Min
from gdptools.agg.stats_methods import StatsMethod
from gdptools.agg.stats_methods import WeightedMean
from gdptools.agg.stats_methods import WeightedMedian
from gdptools.agg.stats_methods import WeightedStd
from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import UserData
from gdptools.utils import _cal_point_stats
from gdptools.utils import _dataframe_to_geodataframe
from gdptools.utils import _get_default_val
from gdptools.utils import _get_interp_array
from gdptools.utils import _get_line_vertices
from gdptools.utils import _get_weight_df
from gdptools.utils import _interpolate_sample_points

logger = logging.getLogger(__name__)

AggChunk = namedtuple("AggChunk", ["ma", "wghts", "def_val", "index"])

STAT_TYPES = Union[
    Type[MAWeightedMean],
    Type[WeightedMean],
    Type[MAWeightedStd],
    Type[WeightedStd],
    Type[MAWeightedMedian],
    Type[WeightedMedian],
    Type[MACount],
    Type[Count],
    Type[MAMin],
    Type[Min],
    Type[MAMax],
    Type[Max],
]


class AggEngine(ABC):
    """Abstract aggregation class.

    Args:
        user_data (UserData): The user data.
        weights (Union[str, pd.DataFrame]): The weights.
        stat (STAT_TYPES): The statistic type.
        jobs (int, optional): The number of jobs. Defaults to -1.

    Returns:
        Tuple[dict[str, AggData], gpd.GeoDataFrame, List[npt.NDArray[Union[np.int, np.double]]]]: The calculated
            aggregations.
    """

    def calc_agg_from_dictmeta(
        self,
        user_data: UserData,
        weights: Union[str, pd.DataFrame],
        stat: STAT_TYPES,
        jobs: int = -1,
    ) -> Tuple[dict[str, AggData], gpd.GeoDataFrame, List[npt.NDArray[Union[np.int_, np.double]]]]:
        """Abstract Base Class for calculating aggregations from dictionary metadata."""
        self.usr_data = user_data
        self.id_feature = user_data.get_feature_id()
        self.vars = user_data.get_vars()
        self.stat = stat
        self.period = None
        self.wghts = _get_weight_df(weights, self.id_feature)
        self._jobs = int(os.cpu_count() / 2) if jobs == -1 else jobs
        # logger.info(f"  ParallelWghtGenEngine using {self._jobs} jobs")

        return self.agg_w_weights()

    @abstractmethod
    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Abstract method for calculating weights."""
        pass


class SerialAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend - tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend - tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "SerialAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate the aggregation.

        Perform spatial and temporal aggregation of gridded data over geometries defined in a GeoDataFrame.

        This method:
        1. Extracts the time period to be aggregated from the provided data object.
        2. Sorts and dissolves the input GeoDataFrame features by a specified feature ID, ensuring unique geometry IDs.
        3. Retrieves and slices the associated xarray DataArray based on the time period.
        4. Attempts to load the selected data into memory; if too large, a ValueError is raised, prompting the user to
           request a smaller subset.
        5. Prepares and chunks weight data for parallel computation.
        6. Uses Dask-based parallel computation to calculate statistics (defined by `self.stat`) on the weighted
           subsets of data.
        7. Returns a GeoDataFrame in the same sorted order as input, along with an array of aggregated values for each
            geometry and time step.

        Args:
            key (str): A reference key, typically associated with the variable or process being aggregated.
            data (AggData): An object containing:
                - `da` (xarray.DataArray): The gridded dataset (e.g., climate variable) to be aggregated.
                - `feature` (gpd.GeoDataFrame): The spatial geometries over which to aggregate.
                - `cat_cr` (CategoricalCoords): Metadata for temporal/spatial indexing.
                It is expected that `cat_cr` contains a time coordinate name (T_name) among others.

        Returns:
            Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
                - The GeoDataFrame (`gdf`) with dissolved features (one row per unique geometry ID).
                - A NumPy array (`val_interp`) with the aggregated values for each geometry over the specified time
                  period. The shape of this array is (number_of_time_steps, number_of_geometries).

        Raises:
            ValueError: If the requested data subset is too large to be retrieved from the remote server. The user is
                        prompted to reduce the time period or work on a smaller subset.
        """
        cp = data.cat_cr
        gdf = data.feature
        gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(data.id_feature).dissolve(by=data.id_feature, as_index=False)
        geo_index = np.asarray(gdf[data.id_feature].values, dtype=type(gdf[data.id_feature].values[0]))
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature)
        t_name = cp.T_name
        da = data.da
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval)
        try:
            mdata = da.values  # type: ignore
        except Exception as e:
            raise ValueError(
                "This error likely arrises when the data requested to aggregate is too large to be retrieved from,"
                " a remote server."
                "Please try to reduce the time-period, or work on a smaller subset."
            ) from e

        for i in np.arange(len(geo_index)):
            try:
                weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
            except KeyError:
                continue
            tw = weight_id_rows.wght.values
            i_ind = np.array(weight_id_rows.i.values).astype(int)
            j_ind = np.array(weight_id_rows.j.values).astype(int)

            val_interp[:, i] = self.stat(array=mdata[:, i_ind, j_ind], weights=tw, def_val=dfval).get_stat()

        return gdf, val_interp


class ParallelAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend - tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend - tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "ParallelAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate the aggregation.

        Perform spatial and temporal aggregation of gridded data over geometries defined in a GeoDataFrame using
        parallel processing.

        This method:
        1. Extracts the time period to be aggregated from the provided data object.
        2. Sorts and dissolves the input GeoDataFrame features by a specified feature ID, ensuring unique geometry IDs.
        3. Retrieves and slices the associated xarray DataArray based on the time period.
        4. Attempts to load the selected data into memory; if too large, a ValueError is raised, prompting the user to
           request a smaller subset.
        5. Prepares and chunks weight data for parallel computation.
        6. Uses parallel processing to calculate statistics (defined by `self.stat`) on the weighted subsets of data.
        7. Returns a GeoDataFrame in the same sorted order as input, along with an array of aggregated values for each
           geometry and time step.

        Args:
            key (str): A reference key, typically associated with the variable or process being aggregated.
            data (AggData): An object containing:
                - `da` (xarray.DataArray): The gridded dataset (e.g., climate variable) to be aggregated.
                - `feature` (gpd.GeoDataFrame): The spatial geometries over which to aggregate.
                - `cat_cr` (CategoricalCoords): Metadata for temporal/spatial indexing.
                It is expected that `cat_cr` contains a time coordinate name (T_name) among others.

        Returns:
            Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
                - The GeoDataFrame (`gdf`) with dissolved features (one row per unique geometry ID).
                - A NumPy array (`val_interp`) with the aggregated values for each geometry over the specified time
                  period. The shape of this array is (number_of_time_steps, number_of_geometries).

        Raises:
            ValueError: If the requested data subset is too large to be retrieved from the remote server. The user is
                        prompted to reduce the time period or work on a smaller subset.
        """
        cp = data.cat_cr
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        # gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(self.id_feature, axis=0).dissolve(self.id_feature, as_index=False)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        # geo_index_chunk = np.array_split(geo_index, self._jobs)
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature, sort=True)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval)

        # mdata = np.ma.masked_array(da.values, np.isnan(da.values))  # type: ignore
        try:
            mdata = da.values  # type: ignore
        except Exception as e:
            raise ValueError(
                "This error likely arrises when the data requested to aggregate is too large to be retrieved from,"
                " a remote server."
                "Please try to reduce the time-period, or work on a smaller subset."
            ) from e

        chunks = get_weight_chunks(
            unique_geom_ids=unique_geom_ids,
            feature=gdf,
            id_feature=self.id_feature,
            mdata=mdata,
            dfval=dfval,
        )

        worker_out = get_stats_parallel(
            n_jobs=self._jobs,
            stat=self.stat,
            bag=bag_generator(jobs=self._jobs, chunks=chunks),
        )

        for index, val in worker_out:
            val_interp[:, index] = val

        return gdf, val_interp


def _stats(
    bag: List[AggChunk], method: StatsMethod
) -> Tuple[npt.NDArray[np.int_], npt.NDArray[Union[np.int_, np.double]]]:
    vals = np.zeros((bag[0].ma.shape[0], len(bag)), dtype=bag[0].ma.dtype)
    index = np.zeros(len(bag), dtype=np.int_)
    for idx, b in enumerate(bag):
        index[idx] = b.index
        vals[:, idx] = method(array=b.ma, weights=b.wghts, def_val=b.def_val).get_stat()  # type: ignore
    return (index, vals)


def get_stats_parallel(
    n_jobs: int,
    stat: STAT_TYPES,
    bag: Generator[List[AggChunk], None, None],
) -> Any:
    """Get stats values."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(delayed(_stats)(chunk, method=stat) for chunk in bag)
    return worker_out


def get_weight_chunks(
    unique_geom_ids: gpd.GeoDataFrame.groupby,
    feature: gpd.GeoDataFrame,
    id_feature: str,
    # mdata: np.ma.MaskedArray,  # type: ignore
    mdata: npt.NDArray,  # type: ignore
    dfval: Union[np.int_, np.double],
) -> List[AggChunk]:
    """Chunk data for parallel aggregation."""
    # keys = list(unique_geom_ids.groups.keys())
    keys = feature[id_feature].values
    chunks = []
    # for idx, (name, group) in enumerate(unique_geom_ids):
    for idx, key in enumerate(keys):
        with contextlib.suppress(Exception):
            weight_id_rows = unique_geom_ids.get_group(str(key))
            chunks.append(
                AggChunk(
                    mdata[
                        :,
                        np.array(weight_id_rows.i.values).astype(int),
                        np.array(weight_id_rows.j.values).astype(int),
                    ],
                    weight_id_rows.wght.values,
                    dfval,
                    idx,
                )
            )
    return chunks


def bag_generator(jobs: int, chunks: List[AggChunk]) -> Generator[List[AggChunk], None, None]:
    """Function to generate chunks."""
    chunk_size = len(chunks) // jobs + 1
    for i in range(0, len(chunks), chunk_size):
        yield chunks[i : i + chunk_size]


class DaskAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend - tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend - tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "DaskAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate the aggregation.

        Perform spatial and temporal aggregation of gridded data over geometries defined in a GeoDataFrame using Dask.

        This method:
        1. Extracts the time period to be aggregated from the provided data object.
        2. Sorts and dissolves the input GeoDataFrame features by a specified feature ID, ensuring unique geometry IDs.
        3. Retrieves and slices the associated xarray DataArray based on the time period.
        4. Attempts to load the selected data into memory; if too large, a ValueError is raised, prompting the user to
            request a smaller subset.
        5. Prepares and chunks weight data for parallel computation.
        6. Uses Dask-based parallel computation to calculate statistics (defined by `self.stat`) on the weighted subsets
            of data.
        7. Returns a GeoDataFrame in the same sorted order as input, along with an array of aggregated values for each
            geometry and time step.

        Args:
            key (str): A reference key, typically associated with the variable or process being aggregated.
            data (AggData): An object containing:
                - `da` (xarray.DataArray): The gridded dataset (e.g., climate variable) to be aggregated.
                - `feature` (gpd.GeoDataFrame): The spatial geometries over which to aggregate.
                - `cat_cr` (CategoricalCoords): Metadata for temporal/spatial indexing.
                It is expected that `cat_cr` contains a time coordinate name (T_name) among others.

        Returns:
            Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
                - The GeoDataFrame (`gdf`) with dissolved features (one row per unique geometry ID).
                - A NumPy array (`val_interp`) with the aggregated values for each geometry over the specified time
                    period.
                The shape of this array is (number_of_time_steps, number_of_geometries).

        Raises:
            ValueError: If the requested data subset is too large to be retrieved from the remote server. The user is
                prompted to reduce the time period or work on a smaller subset.
        """
        cp = data.cat_cr
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        gdf = gdf.sort_values(self.id_feature, axis=0).dissolve(self.id_feature, as_index=False)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        # geo_index_chunk = np.array_split(geo_index, self._jobs)
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature, sort=True)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval)

        try:
            mdata = da.values  # type: ignore
        except Exception as e:
            raise ValueError(
                "This error likely arrises when the data requested to aggregate is too large to be retrieved from,"
                " a remote server."
                "Please try to reduce the time-period, or work on a smaller subset."
            ) from e

        chunks = get_weight_chunks(
            unique_geom_ids=unique_geom_ids,
            feature=gdf,
            id_feature=self.id_feature,
            mdata=mdata,
            dfval=dfval,
        )

        worker_out = get_stats_dask(
            n_jobs=self._jobs,
            stat=self.stat,
            bag=bag_generator(jobs=self._jobs, chunks=chunks),
        )

        for index, val in worker_out[0]:
            val_interp[:, index] = val

        return gdf, val_interp


def get_stats_dask(
    n_jobs: int,
    stat: STAT_TYPES,
    bag: Generator[List[AggChunk], None, None],
) -> List[Any]:
    """Get stats values."""
    worker_out = [dask.delayed(_stats)(chunk, method=stat) for chunk in bag]  # type: ignore
    return dask.compute(worker_out)  # type: ignore


class InterpEngine(ABC):
    """Abstract class for interpolation."""

    def run(
        self,
        *,
        user_data: UserData,
        pt_spacing: Union[float, int, None],
        stat: str,
        interp_method: str,
        calc_crs: Any,
        mask_data: Union[float, int, None],
        output_file: Union[str, None] = None,
        jobs: int = -1,
    ) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Run InterpEngine Class.

        _extended_summary_

        Args:
            user_data (UserData): Data Class for input data
            pt_spacing (Union[float, int, None]): Numerical value in meters for the
                spacing of the interpolated sample points (default is 50)
            stat (str):  A string indicating which statistics to calculate during
                the query. Options: 'all', 'mean', 'median', 'std', 'max', 'min'
                (default is 'all')
            interp_method (str): Optional; String indicating the xarray interpolation method.
                Default method in 'linear'. Options: "linear", "nearest", "zero", "slinear",
                "quadratic", "cubic", "polynomial".
            calc_crs (Any): OGC WKT string, Proj.4 string or int EPSG code.
                Determines which projection is used for the area weighted calculations
            mask_data (bool or None): Optional; When True, nodata values are removed from
                statistical calculations.
            output_file (str or None): Optional; When a file path is specified, a CSV
                of the statistics will be written to that file path. Must end with .csv
                file ending.
            jobs (int): _description_. Defaults to -1.

        Returns:
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: Returns a DataFrame of the
                statistics and a GeoDataFrame of the point geometries
        """
        self._user_data = user_data
        self._pt_spacing = pt_spacing
        self._stat = stat
        self._interp_method = interp_method
        self._calc_crs = calc_crs
        self._mask_data = mask_data
        self._output_file = output_file
        if jobs == -1:
            self._jobs = int(os.cpu_count() / 2)  # type: ignore
            logger.info(" ParallelWghtGenEngine getting jobs from os.cpu_count()")
        else:
            self._jobs = jobs
        logger.info(f"  ParallelWghtGenEngine using {self._jobs} jobs")

        return self.interp()

    @abstractmethod
    def interp(self) -> None:
        """Abstract method for interpolating point values."""
        pass

    def get_variables(self, key) -> dict:
        """Returns a dictionary of values needed for interpolation processing."""
        # Get crs and coord names for gridded data
        user_data_type = self._user_data.get_class_type()

        if user_data_type == "ClimRCatData":
            grid_proj = self._user_data.cat_dict[key]["crs"]
            x_coord = self._user_data.cat_dict[key]["X_name"]
            y_coord = self._user_data.cat_dict[key]["Y_name"]
            t_coord = self._user_data.cat_dict[key]["T_name"]
            varname = self._user_data.cat_dict[key]["varname"]

        elif user_data_type in ["UserCatData", "NHGFStacData"]:
            grid_proj = self._user_data.proj_ds
            x_coord = self._user_data.x_coord
            y_coord = self._user_data.y_coord
            t_coord = self._user_data.t_coord
            varname = key

        elif user_data_type == "UserTiffData":
            grid_proj = self._user_data.proj_ds
            x_coord = self._user_data.x_coord
            y_coord = self._user_data.y_coord
            t_coord = None
            varname = key

        return {
            "key": key,
            "varname": varname,
            "spacing": self._pt_spacing,
            "grid_proj": grid_proj,
            "calc_crs": self._calc_crs,
            "x_coord": x_coord,
            "y_coord": y_coord,
            "t_coord": t_coord,
            "id_feature": self._user_data.id_feature,
            "class_type": user_data_type,
            "stat": self._stat,
            "mask_data": self._mask_data,
        }


class SerialInterp(InterpEngine):
    """Serial Interpolation Class."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def interp(  # noqa: C901
        self,
    ) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Abstract method for interpolating point values.

        Returns:
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: Returns a DataFrame of the
                statistics and a GeoDataFrame of the point geometries
        """
        # Get each grid variable
        wvars = self._user_data.get_vars()
        r_interp_dict = {}

        # Loop thru each grid variable
        for index, key in enumerate(wvars):
            logger.debug(f"Starting to process {key}")
            # loop thru each line geometry
            stats_list = []
            points_list = []
            line_dict = {}
            for i in range(len(self._user_data.f_feature)):
                logger.debug("Looping through lines")
                # Pull geometry ID from geodataframe
                line_id = self._user_data.f_feature.loc[[i]][self._user_data.id_feature][i]
                # Prep the input data
                interp_data: AggData = self._user_data.prep_interp_data(key=key, poly_id=line_id)
                logger.debug("Defined interp_data")
                line_dict[line_id] = interp_data
                # Calculate statistics
                statistics, pts = self.grid_to_line_intersection(interp_data, key=key)
                logger.debug("Calculated stats and pts")
                stats_list.append(statistics)
                points_list.append(pts)

            logger.debug("Combined stats and pts into a dataframe")
            key_stats = pd.concat(stats_list)
            key_points = pd.concat(points_list)

            r_interp_dict[key] = line_dict

            if index == 0:
                stats = key_stats
                points = key_points
            else:
                stats = pd.concat([stats, key_stats])
                points = pd.concat([points, key_points])

            if self._output_file:
                stats.to_csv(self._output_file)

        # Project points back to original crs
        points = points.to_crs(self._user_data.proj_feature)
        logger.debug("Finished running serial interp")

        return r_interp_dict, stats, points

    def grid_to_line_intersection(
        self: "InterpEngine", interp_data: "AggData", key: Union[str, None] = None
    ) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Function for extracting grid values and stats for polyline geometry.

        _extended_summary_

        Args:
            interp_data (AggData): An AggData object with info about the line geometry
                and gridded data to interpolate
            key (Union[str, None], optional): Name of the variable in the xarray
                dataset. Defaults to None.

        Returns:
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: Returns a DataFrame of the
                statistics and a GeoDataFrame of the point geometries
        """
        data_array = interp_data.da
        varname = interp_data.cat_cr.varname
        spacing = self._pt_spacing
        user_data_type = self._user_data.get_class_type()

        # Get crs and coord names for gridded data
        if user_data_type in ["ClimRCatData"]:
            grid_proj = self._user_data.cat_dict[key]["crs"]
            x_coord = self._user_data.cat_dict[key]["X_name"]
            y_coord = self._user_data.cat_dict[key]["Y_name"]

        elif user_data_type in ["UserCatData", "NHGFStacData", "UserTiffData"]:
            grid_proj = self._user_data.proj_ds
            x_coord = self._user_data.x_coord
            y_coord = self._user_data.y_coord

        # Reproject line to the grid's crs
        line = interp_data.feature.copy()
        geom = line.geometry.to_crs(grid_proj)

        # Either find line vertices
        if spacing == 0:
            x, y, dist = _get_line_vertices(geom=geom, calc_crs=self._calc_crs, crs=grid_proj)

        # Or interpolate sample points
        else:
            x, y, dist = _interpolate_sample_points(geom=geom, spacing=spacing, calc_crs=self._calc_crs, crs=grid_proj)

        poly_id_array = np.full(len(dist), interp_data.feature[self._user_data.id_feature].values[0])

        # Attempt to interpolate sample points
        # This might fail for some data arrays
        try:
            logger.info("Able to interpolate points without reprojecting the data array")
            interp_dataarray: xr.DataArray = data_array.to_dataset(name=varname).interp(
                x=("pt", x), y=("pt", y), method=self._interp_method
            )  # Add distsance

        except Exception:
            logger.info("Needed to assign CRS to subsetted data array prior to point interpolation", Exception)
            # Set coordinate system
            data_array = (
                data_array.rio.write_crs(grid_proj).rio.set_spatial_dims(
                    x_dim=x_coord,
                    y_dim=y_coord,
                )
                # Drop coords that are not required
                .drop_vars([item for item in data_array.coords if item not in data_array.indexes._variables.keys()])
                # Reproject; this is necessary because interp() will not work without it
                .rio.reproject(grid_proj)
            )
            interp_dataarray: xr.DataArray = data_array.to_dataset(name=varname).interp(
                x=("pt", x), y=("pt", y), method=self._interp_method
            )  # Add distsance

        interp_dataarray = xr.merge([interp_dataarray, xr.DataArray(dist, dims=["pt"], name="dist")])  # Add polygon IDs
        interp_dataarray = xr.merge(
            [
                interp_dataarray,
                xr.DataArray(poly_id_array, dims=["pt"], name=self._user_data.id_feature),
            ]
        )

        interp_geo_df = _dataframe_to_geodataframe(interp_dataarray.to_dataframe(), crs=grid_proj)
        interp_geo_df.rename(columns={varname: "values"}, inplace=True)
        id_feature_array = np.full(len(interp_geo_df), varname)
        interp_geo_df["varname"] = id_feature_array

        # prefer date, feature id and varname, up front of dataframe.
        t_coord = interp_data.cat_cr.T_name
        if self._user_data.get_class_type() != "UserTiffData":
            out_vals: dict[str, float] = {"date": interp_dataarray[t_coord].values}
            out_vals[self._user_data.id_feature] = np.full(
                out_vals[list(out_vals.keys())[0]].shape[0],
                interp_data.feature[self._user_data.id_feature].values[0],
            )
        else:
            out_vals: dict[str, float] = {
                self._user_data.id_feature: interp_data.feature[self._user_data.id_feature].values
            }

        out_vals["varname"] = np.full(
            out_vals[list(out_vals.keys())[0]].shape[0],
            interp_data.cat_cr.varname,
        )
        out_vals |= _cal_point_stats(
            data=interp_dataarray[interp_data.cat_cr.varname],
            userdata_type=self._user_data.get_class_type(),
            stat=self._stat,
            skipna=self._mask_data,
        )
        stats_df = pd.DataFrame().from_dict(out_vals)

        return stats_df, interp_geo_df


# Todo: create parallel method
class ParallelInterp(InterpEngine):
    """Dask Interpolation Class.

    This method leverages joblib to parallelize the interpolation methods.
    """

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def interp(  # noqa: C901
        self,
    ) -> Tuple[pd.DataFrame, gpd.GeoDataFrame]:
        """Parallel method for interpolating point values.

        Returns:
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: Returns a DataFrame of the
                statistics and a GeoDataFrame of the point geometries
        """
        # Get each grid variable
        wvars = self._user_data.get_vars()

        stats = []
        points = []

        # Loop thru each grid variable
        for index, key in enumerate(wvars):
            # Chunk the geodataframe into equal parts
            gdf_list = _chunk_gdf(self._jobs, self._user_data.f_feature)

            # Clip gridded data to 2d bounds of the input gdf
            data_array: xr.DataArray = self._user_data.get_source_subset(key)

            # Comb the user_data object for variables needed for the processing
            variables: dict = self.get_variables(key)

            with parallel_backend("loky", inner_max_num_threads=1):
                worker_out = Parallel(n_jobs=self._jobs)(
                    delayed(_grid_to_line_intersection)(chunk, data_array, variables) for chunk in gdf_list
                )

            key_stats: pd.DataFrame = pd.concat(list(zip(*worker_out))[0])  # noqa B905
            key_points: gpd.GeoDataFrame = pd.concat(list(zip(*worker_out))[1])  # noqa B905
            del worker_out

            if index == 0:
                stats: pd.DataFrame = key_stats
                points: gpd.GeoDataFrame = key_points
                out_grid: dict = {key: data_array}
            else:
                stats = pd.concat([stats, key_stats])
                points = pd.concat([points, key_points])
                out_grid[key] = data_array

        if self._output_file:
            stats.to_csv(self._output_file)

        # Project points back to original crs
        points = points.to_crs(self._user_data.proj_feature)

        return out_grid, stats, points


class DaskInterp(InterpEngine):
    """Dask Interpolation Class.

    This method leverages Dask to parallelize the interpolation methods.
    """

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def interp(  # noqa: C901
        self,
    ) -> Tuple[pd.DataFrame, gpd.GeoDataFrame]:
        """Dask method for interpolating point values.

        Returns:
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: Returns a DataFrame of the
                statistics and a GeoDataFrame of the point geometries
        """
        import dask.bag as db

        # Get each grid variable
        wvars = self._user_data.get_vars()

        stats = []
        points = []

        # Loop thru each grid variable
        for index, key in enumerate(wvars):
            # Clip gridded data to 2d bounds of the gdf
            self.data_array: xr.DataArray = self._user_data.get_source_subset(key)
            # Comb the user_data object for variables needed for the processing
            self.variables: dict = self.get_variables(key)

            bag = db.from_sequence(self._user_data.f_feature.reset_index().index.to_list()).map(self.g2l)
            results = bag.compute()
            del bag

            key_stats: pd.DataFrame = pd.concat(list(zip(*results))[0])  # noqa B905
            key_points: gpd.GeoDataFrame = pd.concat(list(zip(*results))[1])  # noqa B905
            del results

            if index == 0:
                stats = key_stats
                points = key_points
                out_grid = {key: self.data_array}
            else:
                stats = pd.concat([stats, key_stats])
                points = pd.concat([points, key_points])
                out_grid[key] = self.data_array

        if self._output_file:
            stats.to_csv(self._output_file)

        # Project points back to original crs
        points = points.to_crs(self._user_data.proj_feature)

        return out_grid, stats, points

    def g2l(self, id):
        """Simplified grid to line function.

        Args:
            id (int): ID of the row for the correct geometery within a geodataframe.

        Returns:
            Tuple[pd.Dataframe, gpd.Geodataframe]: Returns a single row DataFrame of the
                statistics and a single row GeoDataFrame of the point geometries interpolated
                from one line geometry
        """
        variables = self.variables
        variables["interp_method"] = self._interp_method

        line = self._user_data.f_feature.reset_index().loc[[id]]
        geom = line.geometry.to_crs(variables["grid_proj"])

        # Either find line vertices
        if variables["spacing"] == 0:
            x, y, dist = _get_line_vertices(geom=geom, calc_crs=variables["calc_crs"], crs=variables["grid_proj"])

        # Or interpolate sample points
        else:
            x, y, dist = _interpolate_sample_points(
                geom=geom,
                spacing=variables["spacing"],
                calc_crs=variables["calc_crs"],
                crs=variables["grid_proj"],
            )

        poly_id_array = np.full(len(dist), line[variables["id_feature"]].values[0])
        # Set coordinate system
        data_array = (
            self.data_array.rio.write_crs(variables["grid_proj"])
            .rio.set_spatial_dims(
                x_dim=variables["x_coord"],
                y_dim=variables["y_coord"],
            )
            .rio.reproject(variables["grid_proj"])
        )

        interp_dataarray: xr.DataArray = data_array.to_dataset(name=variables["varname"]).interp(
            x=("pt", x), y=("pt", y)
        )  # Add distsance
        interp_dataarray = xr.merge([interp_dataarray, xr.DataArray(dist, dims=["pt"], name="dist")])  # Add polygon IDs
        interp_dataarray = xr.merge(
            [
                interp_dataarray,
                xr.DataArray(poly_id_array, dims=["pt"], name=variables["id_feature"]),
            ]
        )

        interp_geo_df = _dataframe_to_geodataframe(interp_dataarray.to_dataframe(), crs=variables["grid_proj"])
        interp_geo_df.rename(columns={variables["varname"]: "values"}, inplace=True)
        id_feature_array = np.full(len(interp_geo_df), variables["varname"])
        interp_geo_df["varname"] = id_feature_array

        # prefer date, feature id and varname, up front of dataframe.
        if variables["t_coord"] is not None:
            out_vals: dict[str, float] = {"date": interp_dataarray[variables["t_coord"]].values}
            out_vals[variables["id_feature"]] = np.full(
                out_vals[list(out_vals.keys())[0]].shape[0],
                line[variables["id_feature"]].values[0],
            )
        else:
            out_vals: dict[str, float] = {variables["id_feature"]: line[variables["id_feature"]].values}

        out_vals["varname"] = np.full(
            out_vals[list(out_vals.keys())[0]].shape[0],
            variables["varname"],
        )
        out_vals |= _cal_point_stats(
            data=interp_dataarray[variables["varname"]],
            userdata_type=variables["class_type"],
            stat=variables["stat"],
            skipna=variables["mask_data"],
        )

        stats = pd.DataFrame().from_dict(out_vals)

        return stats, interp_geo_df


def _chunk_gdf(processes, f_feature) -> List[gpd.GeoDataFrame]:
    """Divide geodataframe up into equal parts by an input number of processes.

    Args:
        processes (int): Number of chunks to create.
        f_feature (gdp.GeoDataFrame): The geodataframe to chunk up.

    Returns:
        List[gdf.GeodDataFrame]: A list of equal sizedchunks of the original
        geodataframe.
    """
    from math import ceil

    gdf_list = []
    num_feat = len(f_feature)
    batch_size = ceil(num_feat / processes)
    bottom_row = batch_size
    top_row = 0
    while top_row < num_feat:
        gdf_list.append(f_feature[top_row:bottom_row])
        top_row += batch_size
        bottom_row += batch_size
        bottom_row = min(bottom_row, num_feat)
    return gdf_list


def _grid_to_line_intersection(chunk: gpd.GeoDataFrame, data_array: xr.DataArray, variables: dict):
    """Performs the grid to line interpolation given explicit inputs.

    The functions loops thru each geometry in the geodataframe and interpolates points
    at the specified spacing long the line. Then the gridded data is queried for values
    at the generated points. Finally, statistics are calculated from the values at
    the points. A dataframe of the stats and a geodataframe of the points are returned.

    Args:
        chunk (gpd.GeoDataFrame): A geodataframe of one or more rows.
        data_array (xr.DataArray): Xarrary DataArray of one or more time steps.
        variables (dict): A dictionary of variables needed to preform the interpolations.

    Returns:
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: Returns a DataFrame of the
                statistics and a GeoDataFrame of the point geometries
    """
    stats_list = []
    interp_geo_list = []

    for i in range(len(chunk)):
        line: gpd.GeoDataFrame = chunk.reset_index().loc[[i]]
        geom: gpd.GeoSeries = line.geometry.to_crs(variables["grid_proj"])

        # Either find line vertices
        if variables["spacing"] == 0:
            x, y, dist = _get_line_vertices(geom=geom, calc_crs=variables["calc_crs"], crs=variables["grid_proj"])

        # Or interpolate sample points
        else:
            x, y, dist = _interpolate_sample_points(
                geom=geom,
                spacing=variables["spacing"],
                calc_crs=variables["calc_crs"],
                crs=variables["grid_proj"],
            )

        poly_id_array = np.full(len(dist), line[variables["id_feature"]].values[0])
        # Set coordinate system
        data_array = (
            data_array.rio.write_crs(variables["grid_proj"])
            .rio.set_spatial_dims(
                x_dim=variables["x_coord"],
                y_dim=variables["y_coord"],
            )
            .rio.reproject(variables["grid_proj"])
        )

        interp_dataarray: xr.DataArray = data_array.to_dataset(name=variables["varname"]).interp(
            x=("pt", x), y=("pt", y), method=variables["interp_method"]
        )  # Add distsance
        interp_dataarray = xr.merge([interp_dataarray, xr.DataArray(dist, dims=["pt"], name="dist")])  # Add polygon IDs
        interp_dataarray = xr.merge(
            [
                interp_dataarray,
                xr.DataArray(poly_id_array, dims=["pt"], name=variables["id_feature"]),
            ]
        )

        interp_geo_df = _dataframe_to_geodataframe(interp_dataarray.to_dataframe(), crs=variables["grid_proj"])
        interp_geo_df.rename(columns={variables["varname"]: "values"}, inplace=True)
        id_feature_array = np.full(len(interp_geo_df), variables["varname"])
        interp_geo_df["varname"] = id_feature_array

        interp_geo_list.append(interp_geo_df)

        # prefer date, feature id and varname, up front of dataframe.
        if variables["t_coord"] is not None:
            out_vals: dict[str, float] = {"date": interp_dataarray[variables["t_coord"]].values}
            out_vals[variables["id_feature"]] = np.full(
                out_vals[list(out_vals.keys())[0]].shape[0],
                line[variables["id_feature"]].values[0],
            )
        else:
            out_vals: dict[str, float] = {variables["id_feature"]: line[variables["id_feature"]].values}

        out_vals["varname"] = np.full(
            out_vals[list(out_vals.keys())[0]].shape[0],
            variables["varname"],
        )
        out_vals |= _cal_point_stats(
            data=interp_dataarray[variables["varname"]],
            userdata_type=variables["class_type"],
            stat=variables["stat"],
            skipna=variables["mask_data"],
        )

        stats_list.append(pd.DataFrame().from_dict(out_vals))

    interp_geo_df: gpd.GeoDataFrame = pd.concat(interp_geo_list)
    stats_df: pd.DataFrame = pd.concat(stats_list)

    return stats_df, interp_geo_df
