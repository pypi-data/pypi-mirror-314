"""Engines for calculated zonal stats based on non-area-weighted statistics."""

import time
import warnings
from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import Any
from typing import Tuple

import dask
import dask.dataframe as dd
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import xarray as xr
from dask.distributed import Client
from dask.distributed import get_client
from dask.distributed import LocalCluster
from joblib import delayed
from joblib import Parallel
from joblib import parallel_backend
from rioxarray.exceptions import OneDimensionalRaster
from shapely.geometry import Polygon
from statsmodels.stats.weightstats import DescrStatsW
from tqdm import tqdm

from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import UserData
from gdptools.helpers import build_subset_tiff_da
from gdptools.utils import _get_shp_bounds_w_buffer
from gdptools.utils import _make_valid


def _calculate_stats(
    row: pd.Series,
    target_gdf: gpd.GeoDataFrame,
    source_ds: xr.Dataset,
    source_ds_proj: Any,
    var_name: str,
    categorical: bool,
    stats_columns: list,
    weights_proj: Any,
):
    zone = gpd.GeoDataFrame([row], columns=target_gdf.columns, crs=target_gdf.crs)
    polys, i_pixel, j_pixel, data = _intersecting_pixels_with_shape(
        raster=source_ds,
        raster_proj=source_ds_proj,
        shape=zone,
    )
    # Check if the returned arrays are empty indicating no intersecting pixels
    if len(polys) == 0:
        # Return zero values for all statistics
        print(f"Target Polygon has no values: {row.index}")
        if categorical:
            return {cat: None for cat in stats_columns}
        else:
            return {
                "median": None,
                "mean": None,
                "count": None,
                "sum": None,
                "stddev": None,
                "sum_weights": None,
                "masked_mean": None,
            }
    # if polys.crs is not zone.crs:
    #     print("this is an error") #  Check this
    if weights_proj is not None:
        weights = _pixel_spatial_weights_in_shape(polys.to_crs(weights_proj), zone.to_crs(weights_proj))
    else:
        weights = _pixel_spatial_weights_in_shape(polys, zone)
    sub_data = data[var_name].values
    sub_data_values = sub_data[i_pixel, j_pixel]
    if categorical:
        cat_data = pd.DataFrame({"Value": sub_data_values, "Weight": weights})
        weighted_counts = cat_data.groupby("Value")["Weight"].sum().to_dict()

        # Initialize all categories with zero count
        stats = {cat: None for cat in stats_columns}

        # Update counts for categories present in the zone
        for cat, count in weighted_counts.items():
            if cat in stats:
                stats[cat] = count
        stats["top"] = max(weighted_counts, key=weighted_counts.get)

        return stats
    else:
        stats = DescrStatsW(data=sub_data_values, weights=weights)
        masked_sdv = np.ma.masked_array(sub_data_values, np.isnan(sub_data_values))
        ma_mean = np.ma.average(masked_sdv, weights=weights)
        return {
            "median": stats.quantile(0.5, return_pandas=False)[0],
            "mean": stats.mean,
            "count": len(weights),
            "sum": stats.sum,
            "stddev": stats.std_mean,
            "sum_weights": stats.sum_weights,
            "masked_mean": ma_mean,
        }


def process_chunk(
    chunk: gpd.GeoDataFrame,
    source_ds: xr.Dataset,
    source_ds_proj: Any,
    var: str,
    categorical: bool,
    stats_columns: list,
    weights_proj: Any,
    chunk_id: int,
) -> gpd.GeoDataFrame:
    """Process a chunk of data by calculating statistics for each zone.

    Args:
        chunk: A GeoDataFrame representing a chunk of data.
        source_ds: An xarray Dataset containing the source data.
        source_ds_proj: Projection of source_ds Dataset.
        var: Name of variable in source_ds.
        categorical: True if data are categorical.
        stats_columns: List of calculated statistics
        weights_proj: Projection used to calculate weights - equal area projection.
        chunk_id: The id of the chunk.

    Returns:
        A GeoDataFrame with calculated statistics for each zone.

    """
    warnings.simplefilter("ignore", FutureWarning)
    warnings.simplefilter("ignore", RuntimeWarning)
    ngdf_chunk = chunk.copy()
    # for col in stats_columns:
    #     ngdf_chunk[col] = np.nan
    result_dict = {}
    partition_index = chunk.iloc[0]["partition_index"]
    for i, row in tqdm(chunk.iterrows(), total=chunk.shape[0], desc=f"Processing chunk: {partition_index}"):
        zone = gpd.GeoDataFrame([row], columns=chunk.columns, crs=chunk.crs)
        polys, i_pixel, j_pixel, data = _intersecting_pixels_with_shape(
            raster=source_ds, raster_proj=source_ds_proj, shape=zone
        )
        # Check if the returned arrays are empty indicating no intersecting pixels
        if len(polys) == 0:
            print(f"skipping: {i}")
            for col in stats_columns:
                ngdf_chunk.at[i, col] = None
            continue
        if source_ds_proj is not None:
            weights = _pixel_spatial_weights_in_shape(polys.to_crs(weights_proj), zone.to_crs(weights_proj))
        else:
            weights = _pixel_spatial_weights_in_shape(polys, zone)
        sub_data = data[var].values
        sub_data_values = sub_data[i_pixel, j_pixel]

        if categorical:
            cat_data = pd.DataFrame({"Value": sub_data_values, "Weight": weights})
            weighted_counts = cat_data.groupby("Value")["Weight"].sum()
            weighted_counts_dict = weighted_counts.to_dict()

            # Initialize all categories with zero count
            stats = {cat: None for cat in stats_columns}

            # Update counts for categories present in the zone
            for cat, count in weighted_counts_dict.items():
                if cat in stats_columns:
                    stats[cat] = count
            stats["top"] = weighted_counts.idxmax()

        else:
            dstats = DescrStatsW(data=sub_data_values, weights=weights)
            masked_sdv = np.ma.masked_array(sub_data_values, np.isnan(sub_data_values))
            ma_mean = np.ma.average(masked_sdv, weights=weights)
            stats = {
                "median": dstats.quantile(0.5, return_pandas=False)[0],
                "mean": dstats.mean,
                "count": len(weights),
                "sum": dstats.sum,
                "stddev": dstats.std_mean,
                "sum_weights": dstats.sum_weights,
                "masked_mean": ma_mean,
            }
        result_dict[i] = stats

    return result_dict


def _intersecting_pixels_with_shape(
    raster: xr.Dataset,
    raster_proj: Any,
    shape: gpd.GeoDataFrame,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, xr.Dataset]:
    """Get the intersecting pixels between a raster and a shape.

    Args:
        raster: An xarray Dataset representing the raster data.
        raster_proj: Projection of raster dataset.
        shape: A GeoDataFrame representing the shape data.

    Returns:
        A tuple containing the intersecting pixels as a numpy array of geometries,
        the indices of the intersecting pixels in the raster grid,
        and the clipped raster as an xarray Dataset.

    """
    # Clip the raster to the shape.
    # If bounds are not in the correct format (floats), convert them
    # Reproject shape into raster projection
    shape = shape.to_crs(raster_proj)
    try:
        bounds = shape.iloc[0].geometry.bounds
        box = raster.rio.clip_box(*bounds)
    except OneDimensionalRaster as e:
        # Handle the exception
        print(f"Target Polygon has no intersections: {e}")
        # You can choose to return a default value or raise a custom exception
        # For example, return an empty dataset or handle it as per your use case
        return np.array([]), np.array([]), np.array([]), xr.Dataset()
    tlon = box["x"]  # These are cell centre coordinates
    tlat = box["y"]  # These are cell centre coordinates

    # Work with fractions of integer cell indices to get node locations.
    # i.e. -0.5 and 0.5 are first cells nodes using the transform of the CRS
    lon, lat = np.meshgrid(np.arange(-0.5, tlon.size + 0.5), np.arange(-0.5, tlat.size + 0.5))

    # These are 2D arrays to handle non-uniformly increasing projections on cell sizes.
    xs, ys = rasterio.transform.xy(box.rio.transform(), lat, lon)
    ys = np.asarray(ys)  # These are cell nodal coordinates
    xs = np.asarray(xs)  # These are cell nodal coordinates

    # Create the numpy array of the rasterized polygon's pixels
    # I dont like this double loop.  But we are stuck with this granularity
    # due to how shapely is written.
    polys = np.empty(tlat.size * tlon.size, dtype=object)
    k = 0
    for i in range(tlat.size):
        for j in range(tlon.size):
            polys[k] = Polygon(
                [
                    [xs[i, j], ys[i, j]],
                    [xs[i + 1, j], ys[i + 1, j]],
                    [xs[i + 1, j + 1], ys[i + 1, j + 1]],
                    [xs[i, j + 1], ys[i, j + 1]],
                ]
            )
            k += 1

    # Create the dataframe.  No need for pixel i,j
    # since we can use unravel_index later using the tgt indices
    df = gpd.GeoDataFrame(geometry=polys, crs=raster_proj)
    i_pixels_in_zone, _ = shape.sindex.query(polys, predicate="intersects")

    # we have the global index into the pixels of the zone,
    # unravel them using the size of the bounding box of the zone.
    i_pixel, j_pixel = np.unravel_index(i_pixels_in_zone, (tlat.size, tlon.size))
    return df.geometry.values[i_pixels_in_zone], i_pixel, j_pixel, box


def _pixel_spatial_weights_in_shape(polygons: gpd.array.GeometryArray, shape: gpd.GeoDataFrame):
    """Calculate the spatial weights of pixels within a shape.

    Args:
        polygons: A GeometryArray representing the polygons to calculate weights for.
        shape: A GeoDataFrame representing the shape.

    Returns:
        The normalized intersection weights of the polygons within the shape.

    """
    # Normalized intersection weights
    return (polygons.intersection(shape.iloc[0].geometry).area) / shape.iloc[0].geometry.area


class ZonalEngine(ABC):
    """Base class for zonal stats engines."""

    def calc_zonal_from_aggdata(
        self,
        user_data: UserData,
        categorical: bool = False,
        jobs: int = 1,
    ) -> pd.DataFrame:
        """calc_zonal_from_aggdata Template method for calculated zonal stats.

        _extended_summary_

        Args:
            user_data (UserData): _description_
            categorical (bool): _description_. Defaults to False.
            jobs (int): _description_. Defaults to 1.

        Returns:
            pd.DataFrame: _description_
        """
        self._user_data = user_data
        self._categorical = categorical
        self._jobs = jobs

        return self.zonal_stats()

    def calc_weights_zonal_from_aggdata(
        self,
        user_data: UserData,
        crs: Any = 6931,
        categorical: bool = False,
        jobs: int = 1,
    ) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics from raster data.

        Args:
            user_data: The UserData object containing the subsetted raster data.
            crs: CRS used to re-project source and target into before calculating weights.
            categorical: A boolean indicating if the data is categorical. Defaults to False.
            jobs: The number of parallel jobs. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the weighted zonal statistics.

        """
        self._user_data = user_data
        self._weight_gen_crs = crs
        self._categorical = categorical
        self._jobs = jobs

        return self.weighted_zonal_stats()

    @abstractmethod
    def zonal_stats(self) -> pd.DataFrame:
        """Abstract method for calculating zonal stats."""
        pass

    @abstractmethod
    def weighted_zonal_stats(self) -> gpd.GeoDataFrame:
        """Abstract method for calculating weighted zonal stats."""
        pass


class ZonalEngineSerial(ZonalEngine):
    """Serial zonal stats engine."""

    def weighted_zonal_stats(self) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics for each zone in the GeoDataFrame.

        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing the zonal statistics for each zone.

        """
        tqdm.pandas(desc="Applying zonal stats")
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        var_name = zvars[0]
        source_ds = agg_data.da.to_dataset(name=var_name)  # .rio.reproject(self._weight_gen_crs)
        # Reproject target to source projection
        target_gdf = agg_data.feature  # .to_crs(self._user_data.proj_ds)
        if self._categorical:
            data_array = agg_data.da.values
            filtered_data_array = data_array[~np.isnan(data_array)]
            unique_categories = np.unique(filtered_data_array)
            stats_columns = unique_categories.tolist() + ["top"]
        else:
            stats_columns = ["median", "mean", "count", "sum", "stddev", "sum_weights", "masked_mean"]
        target_gdf[stats_columns] = target_gdf.progress_apply(
            lambda row: _calculate_stats(
                row=row,
                target_gdf=target_gdf,
                source_ds=source_ds,
                source_ds_proj=self._user_data.proj_ds,
                var_name=var_name,
                categorical=self._categorical,
                stats_columns=stats_columns,
                weights_proj=self._weight_gen_crs,
            ),
            axis=1,
            result_type="expand",
        )
        return target_gdf

    def zonal_stats(self) -> pd.DataFrame:
        """zonal_stats Calculate zonal stats serially.

        _extended_summary_

        Returns:
            pd.DataFrame: _description_
        """
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        ds_ss = agg_data.da

        if self._categorical:
            d_categories = list(pd.Categorical(ds_ss.values.flatten()).categories)

        tstrt = time.perf_counter()
        lon, lat = np.meshgrid(
            ds_ss[agg_data.cat_cr.X_name].values,
            ds_ss[agg_data.cat_cr.Y_name].values,
        )
        lat_flat = lat.flatten()
        lon_flat = lon.flatten()
        ds_vals = ds_ss.values.flatten()
        df_points = pd.DataFrame(
            {
                "index": np.arange(len(lat_flat)),
                "vals": ds_vals,
                "lat": lat_flat,
                "lon": lon_flat,
            }
        )
        try:
            fill_val = ds_ss._FillValue
            df_points_filt = df_points[df_points.vals != fill_val]
        except Exception:
            df_points_filt = df_points

        source_df = gpd.GeoDataFrame(
            df_points_filt,
            geometry=gpd.points_from_xy(df_points_filt.lon, df_points_filt.lat),
        )
        tend = time.perf_counter()
        print(f"converted tiff to points in {tend - tstrt:0.4f} seconds")
        source_df.set_crs(agg_data.cat_cr.proj, inplace=True)
        target_df = agg_data.feature.to_crs(agg_data.cat_cr.proj)
        target_df = _make_valid(target_df)
        target_df.reset_index()
        target_df_keys = target_df[agg_data.id_feature].values
        tstrt = time.perf_counter()
        ids_tgt, ids_src = source_df.sindex.query(target_df.geometry, predicate="contains")
        tend = time.perf_counter()
        print(f"overlaps calculated in {tend - tstrt:0.4f} seconds")
        if self._categorical:
            val_series = pd.Categorical(source_df["vals"].iloc[ids_src], categories=d_categories)
            agg_df = pd.DataFrame({agg_data.id_feature: target_df[agg_data.id_feature].iloc[ids_tgt].values})
            agg_df["vals"] = val_series
            unique_vals = np.unique(ds_vals)
            del val_series
            tstrt = time.perf_counter()
            vals_dict = agg_df.groupby(agg_data.id_feature)["vals"].apply(list).to_dict()

            comp_stats = []
            for key in vals_dict.keys():
                unique, frequency = np.unique(np.array(vals_dict[key]), return_counts=True)
                total_count = frequency.sum()
                # Loop through each category and calculate the percentage
                zonal_dict = {}
                # for u,f in zip(unique, frequency):
                #     zonal_dict[u]=[f / total_count]
                # flake8: noqa: B905
                zonal_dict = {unique_value: f / total_count for unique_value, f in zip(unique, frequency)}

                stat = pd.DataFrame(zonal_dict, dtype=float, columns=unique_vals, index=["0"]).fillna(0.0)
                stat["count"] = total_count
                stat[agg_data.id_feature] = key
                comp_stats.append(stat)

            stats = pd.concat(comp_stats)
            stats = stats.set_index(agg_data.id_feature)
            tend = time.perf_counter()
            print(f"categorical zonal stats calculated in {tend - tstrt:0.4f} seconds")

        else:
            agg_df = pd.DataFrame(
                {
                    agg_data.id_feature: target_df[agg_data.id_feature].iloc[ids_tgt].values,
                    "vals": source_df["vals"].iloc[ids_src],
                }
            )
            tstrt = time.perf_counter()
            # Group the values by the polygon, run Pandas descibe() on each group of values, and round to 10 decimals
            stats = agg_df.groupby(agg_data.id_feature)["vals"].describe()  # .map(lambda x: np.float64(f"{x:0.10f}"))
            stats["sum"] = agg_df.groupby(agg_data.id_feature).sum()
            tend = time.perf_counter()
            print(f"zonal stats calculated in {tend - tstrt:0.4f} seconds")

        tstrt = time.perf_counter()
        stats_inds = stats.index

        missing = np.setdiff1d(target_df_keys, stats_inds)
        target_df_stats = target_df.loc[target_df[agg_data.id_feature].isin(list(stats_inds))]
        target_df_missing = target_df.loc[target_df[agg_data.id_feature].isin(list(missing))]
        nearest = target_df_stats.sindex.nearest(target_df_missing.geometry, return_all=False)
        print(nearest)
        print(f"number of missing values: {len(missing)}")
        stats_missing = stats.iloc[nearest[1]]
        stats_missing.index = missing
        stats_tot = pd.concat([stats, stats_missing])
        stats_tot.index.name = agg_data.id_feature
        tend = time.perf_counter()
        print(f"fill missing values with nearest neighbors in {tend - tstrt:0.4f} seconds")

        return stats_tot


class ZonalEngineParallel(ZonalEngine):
    """Parallel zonal stats engine."""

    def weighted_zonal_stats(self) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics for each zone in the GeoDataFrame.

        Returns:
            ngdf: A GeoDataFrame containing the zonal statistics for each zone.
        """
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        source_ds = agg_data.da.to_dataset(name=self._user_data.get_vars()[0])
        # source_ds = source_ds.rio.reproject(self._weight_gen_crs)
        target_gdf = agg_data.feature  # .to_crs(self._weight_gen_crs)
        target_gdf["partition_index"] = [i // (len(target_gdf) // self._jobs) for i in range(len(target_gdf))]
        if self._categorical:
            data_array = agg_data.da.values
            filtered_data_array = data_array[~np.isnan(data_array)]
            unique_categories = np.unique(filtered_data_array)
            stats_columns = unique_categories.tolist() + ["top"]
        else:
            stats_columns = ["median", "mean", "count", "sum", "stddev", "sum_weights", "masked_mean"]
        chunk_size = len(target_gdf) // self._jobs + 1
        # Split target_gdf into chunks
        chunks = [target_gdf.iloc[i : i + chunk_size] for i in range(0, len(target_gdf), chunk_size)]

        # Process each chunk in parallel
        results = Parallel(n_jobs=self._jobs)(
            delayed(process_chunk)(
                chunk,
                source_ds,
                self._user_data.proj_ds,
                zvars[0],
                self._categorical,
                stats_columns,
                self._weight_gen_crs,
                chunk_id=i,
            )
            for i, chunk in enumerate(chunks)
        )
        for d in results:
            for index, row_data in d.items():
                for col, value in row_data.items():
                    target_gdf.at[index, col] = value
        return pd.DataFrame(target_gdf)

    def zonal_stats(self) -> pd.DataFrame:
        """Calculate zonal statistics serially.

        This function calculates zonal statistics based on the provided input data.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated zonal statistics.

        """
        n_jobs: int = self._jobs
        # n_jobs = 2
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for parallel zonal stats in {tend - tstrt:0.4f} seconds")
        ds_ss = agg_data.da

        target_df = agg_data.feature.to_crs(agg_data.cat_cr.proj)
        target_df = _make_valid(target_df)
        target_df_keys = target_df[agg_data.id_feature].values
        to_workers = _chunk_dfs(
            geoms_to_chunk=target_df,
            df=ds_ss,
            x_name=agg_data.cat_cr.X_name,
            y_name=agg_data.cat_cr.Y_name,
            proj=agg_data.cat_cr.proj,
            ttb=agg_data.cat_cr.toptobottom,
            id_feature=agg_data.id_feature,
            categorical=self._categorical,
            n_jobs=n_jobs,
        )

        tstrt = time.perf_counter()
        worker_out = self.get_stats_parallel(n_jobs, to_workers)
        for i in range(len(worker_out)):
            if i == 0:
                stats = worker_out[i]
                print(type(stats))
            else:
                stats = pd.concat([stats, worker_out[i]])
        stats.set_index(agg_data.id_feature, inplace=True)
        # stats = pd.concat(worker_out)
        tend = time.perf_counter()
        print(f"Parallel calculation of zonal stats in {tend - tstrt:0.04} seconds")

        tstrt = time.perf_counter()
        stats_inds = stats.index

        missing = np.setdiff1d(target_df_keys, stats_inds)
        if len(missing) <= 0:
            return stats
        target_df_stats = target_df.loc[target_df[agg_data.id_feature].isin(list(stats_inds))]
        target_df_missing = target_df.loc[target_df[agg_data.id_feature].isin(list(missing))]
        nearest = target_df_stats.sindex.nearest(target_df_missing.geometry, return_all=False)
        print(nearest)
        print(f"number of missing values: {len(missing)}")
        stats_missing = stats.iloc[nearest[1]]
        stats_missing.index = missing
        stats_tot = pd.concat([stats, stats_missing])
        stats_tot.index.name = agg_data.id_feature
        tend = time.perf_counter()
        print(f"fill missing values with nearest neighbors in {tend - tstrt:0.4f} seconds")

        return stats_tot

    def get_stats_parallel(
        self,
        n_jobs: int,
        to_workers: Generator[
            Tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str],
            None,
            None,
        ],
    ) -> Any:
        """Perform parallel computation of statistics using a parallel engine.

        Args:
            n_jobs: An integer representing the number of parallel jobs.
            to_workers: A generator yielding tuples of input data for each worker.

        Returns:
            Any: The output of the parallel computation.

        """
        with parallel_backend("loky", inner_max_num_threads=1):
            worker_out = Parallel(n_jobs=n_jobs)(delayed(_get_stats_on_chunk)(*chunk_pair) for chunk_pair in to_workers)
        return worker_out


class ZonalEngineDask(ZonalEngine):
    """Parallel zonal stats engine."""

    def weighted_zonal_stats(self) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics for each zone in the GeoDataFrame.

        Returns:
            ngdf: A GeoDataFrame containing the zonal statistics for each zone.
        """
        dask_create = False
        try:
            client = get_client()
        except ValueError:
            # If no client exists, you can either create a new one or handle it accordingly
            cluster = LocalCluster(n_workers=self._jobs)
            client = Client(cluster)  # This line creates a new client, which might not be desirable in all cases
            dask_create = True

        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        source_ds = agg_data.da.to_dataset(name=self._user_data.get_vars()[0])
        # source_ds_scat = client.scatter(source_ds, broadcast=True)
        # source_ds = source_ds.rio.reproject(self._weight_gen_crs)
        target_gdf = agg_data.feature  # .to_crs(self._weight_gen_crs)
        target_gdf["partition_index"] = [i // (len(target_gdf) // self._jobs) for i in range(len(target_gdf))]
        ddf = dd.from_pandas(target_gdf, npartitions=self._jobs)
        # Extract unique categories if categorical data
        if self._categorical:
            data_array = agg_data.da.values
            filtered_data_array = data_array[~np.isnan(data_array)]
            unique_categories = np.unique(filtered_data_array)
            stats_columns = unique_categories.tolist() + ["top"]
        else:
            stats_columns = ["median", "mean", "count", "sum", "stddev", "sum_weights", "masked_mean"]

        result = ddf.map_partitions(
            process_chunk,
            source_ds,
            self._user_data.proj_ds,
            zvars[0],
            self._categorical,
            stats_columns,
            self._weight_gen_crs,
            1,
            meta=dict,
        )
        compute_result = result.compute()
        print("Finished Compute", flush=True)
        # Update the main DataFrame with the processed values
        ngdf = target_gdf.copy()
        for d in compute_result:
            for index, row_data in d.items():
                for col, value in row_data.items():
                    ngdf.at[index, col] = value
        if dask_create:
            cluster.close()
            client.close()
        return pd.DataFrame(ngdf)

    def zonal_stats(self) -> pd.DataFrame:
        """Calculate zonal statistics serially.

        This method calculates zonal statistics based on the provided input data.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated zonal statistics.

        """
        n_jobs: int = self._jobs
        # n_jobs = 2
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        ds_ss = agg_data.da

        target_df = agg_data.feature.to_crs(agg_data.cat_cr.proj)
        target_df = _make_valid(target_df)
        # target_df.reset_index(inplace=True)
        target_df_keys = target_df[agg_data.id_feature].values
        to_workers = _chunk_dfs(
            geoms_to_chunk=target_df,
            df=ds_ss,
            x_name=agg_data.cat_cr.X_name,
            y_name=agg_data.cat_cr.Y_name,
            proj=agg_data.cat_cr.proj,
            ttb=agg_data.cat_cr.toptobottom,
            id_feature=agg_data.id_feature,
            categorical=self._categorical,
            n_jobs=n_jobs,
        )

        tstrt = time.perf_counter()
        worker_out = _get_stats_dask(to_workers)
        for i in range(len(worker_out[0])):
            if i == 0:
                stats = worker_out[0][i]
                print(type(stats))
            else:
                stats = pd.concat([stats, worker_out[0][i]])
        stats.set_index(agg_data.id_feature, inplace=True)
        # stats = pd.concat(worker_out)
        tend = time.perf_counter()
        print(f"Parallel calculation of zonal stats in {tend - tstrt:0.04} seconds")

        tstrt = time.perf_counter()
        stats_inds = stats.index

        missing = np.setdiff1d(target_df_keys, stats_inds)
        if len(missing) <= 0:
            return stats
        target_df_stats = target_df.loc[target_df[agg_data.id_feature].isin(list(stats_inds))]
        target_df_missing = target_df.loc[target_df[agg_data.id_feature].isin(list(missing))]
        nearest = target_df_stats.sindex.nearest(target_df_missing.geometry, return_all=False)
        print(nearest)
        print(f"number of missing values: {len(missing)}")
        stats_missing = stats.iloc[nearest[1]]
        stats_missing.index = missing
        stats_tot = pd.concat([stats, stats_missing])
        stats_tot.index.name = agg_data.id_feature
        tend = time.perf_counter()
        print(f"fill missing values with nearest neighbors in {tend - tstrt:0.4f} seconds")

        return stats_tot


def _get_stats_dask(
    to_workers: Generator[
        Tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str],
        None,
        None,
    ]
) -> pd.DataFrame:
    """Calculate statistics using Dask parallel processing.

    Args:
        to_workers: A generator of tuples containing the data for each worker.

    Returns:
        Any: The computed statistics.

    """
    worker_out = [dask.delayed(_get_stats_on_chunk)(*worker) for worker in to_workers]  # type: ignore
    return dask.compute(worker_out)  # type: ignore


def _get_stats_on_chunk(
    geom: gpd.GeoDataFrame,
    df: xr.Dataset,
    x_name: str,
    y_name: str,
    proj: Any,
    toptobottom: int,
    categorical: bool,
    id_feature: str,
) -> pd.DataFrame:
    """Calculate statistics for a chunk of data.

    Args:
        geom: A GeoDataFrame representing the chunk of geometries.
        df: An xarray Dataset representing the data.
        x_name: The name of the x-coordinate variable.
        y_name: The name of the y-coordinate variable.
        proj: The projection of the data.
        toptobottom: The direction of top to bottom.
        categorical: A boolean indicating if the data is categorical.
        id_feature: The identifier feature.

    Returns:
        pd.DataFrame: A DataFrame containing the calculated statistics.

    """
    num_features = len(geom.index)
    comp_stats = []
    unique_vals = np.unique(df.values)
    for index in range(num_features):
        target_df = geom.iloc[[index]]
        feat_bounds = _get_shp_bounds_w_buffer(gdf=target_df, ds=df, crs=proj, lon=x_name, lat=y_name)

        subset_dict = build_subset_tiff_da(bounds=feat_bounds, xname=x_name, yname=y_name, toptobottom=toptobottom)
        ds_ss = df.sel(**subset_dict)
        lon, lat = np.meshgrid(
            ds_ss[x_name].values,
            ds_ss[y_name].values,
        )
        lat_flat = lat.flatten()
        lon_flat = lon.flatten()
        ds_vals = ds_ss.values.flatten()  # type: ignore
        df_points = pd.DataFrame(
            {
                "index": np.arange(len(lat_flat)),
                "vals": ds_vals,
                "lat": lat_flat,
                "lon": lon_flat,
            }
        )
        try:
            fill_val = ds_ss._FillValue
            df_points = df_points[df_points.vals != fill_val]
        except Exception:
            df_points = df_points

        source_df = gpd.GeoDataFrame(
            df_points,
            geometry=gpd.points_from_xy(df_points.lon, df_points.lat),
            crs=proj,
        )

        ids_src = source_df.sindex.query(target_df.geometry.values[0], predicate="contains")
        if categorical:
            # Get unique values
            cats = list(pd.Categorical(source_df["vals"].iloc[ids_src]).categories)
            # Get the list of the values within the polygon
            val_series = list(pd.Categorical(source_df["vals"].iloc[ids_src], categories=cats))
            # Count each value
            unique, frequency = np.unique(val_series, return_counts=True)
            # Sum the total number of cells within the polygon
            total_count = frequency.sum()
            # Loop through each category and calculate the percentage
            zonal_dict = {}
            # for u,f in zip(unique, frequency):
            #     zonal_dict[u]=[f / total_count]
            # flake8: noqa: B905
            zonal_dict = {u: f / total_count for u, f in zip(unique, frequency)}

            stats = pd.DataFrame(zonal_dict, dtype=float, columns=unique_vals, index=["0"]).fillna(0.0)
            stats["count"] = total_count

        else:
            agg_df = pd.DataFrame(
                data={
                    "vals": source_df["vals"].iloc[ids_src].values,
                }
            )
            # Group the values by the polygon, run Pandas descibe() on each group of values, and round to 10 decimals
            stats = agg_df.describe().T  # .map(lambda x: np.float64(f"{x:0.10f}")).T
            stats["sum"] = agg_df["vals"].sum()
        # Add the polygon ID
        stats[id_feature] = target_df[id_feature].values[0]
        if stats["count"].values[0] <= 0:
            continue

        comp_stats.append(stats)

    # Merge all the rows and return the output
    return pd.concat(comp_stats)


def _chunk_dfs(
    geoms_to_chunk: gpd.GeoDataFrame,
    df: xr.DataArray,
    x_name: str,
    y_name: str,
    proj: Any,
    ttb: int,
    id_feature: str,
    categorical: bool,
    n_jobs: int,
) -> Generator[
    Tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str],
    None,
    None,
]:
    """Chunk the dataframes for parallel processing.

    Args:
        geoms_to_chunk: A GeoDataFrame representing the geometries to chunk.
        df: An xarray DataArray representing the data.
        x_name: The name of the x-coordinate variable.
        y_name: The name of the y-coordinate variable.
        proj: The projection of the data.
        ttb: The top-to-bottom direction.
        id_feature: The identifier feature.
        categorical: A boolean indicating if the data is categorical.
        n_jobs: The number of parallel jobs.

    Yields:
        Tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str]: A tuple containing the chunked dataframes.

    """
    start = 0
    chunk_size = geoms_to_chunk.shape[0] // n_jobs + 1

    for i in range(n_jobs):
        start = i * chunk_size
        yield geoms_to_chunk.iloc[start : start + chunk_size], df, x_name, y_name, proj, ttb, categorical, id_feature
