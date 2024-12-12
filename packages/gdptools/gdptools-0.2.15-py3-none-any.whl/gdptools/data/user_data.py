"""Prepare user data for weight generation."""

import datetime
import logging
import time
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional
from typing import Union

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from pyproj import CRS
from shapely.geometry import box

from gdptools.data.agg_gen_data import AggData
from gdptools.data.odap_cat_data import CatClimRItem
from gdptools.data.weight_gen_data import WeightData
from gdptools.helpers import build_subset
from gdptools.helpers import build_subset_tiff
from gdptools.utils import _check_for_intersection
from gdptools.utils import _check_for_intersection_nc
from gdptools.utils import _get_cells_poly
from gdptools.utils import _get_data_via_catalog
from gdptools.utils import _get_rxr_dataset
from gdptools.utils import _get_shp_bounds_w_buffer
from gdptools.utils import _get_shp_file
from gdptools.utils import _get_top_to_bottom
from gdptools.utils import _get_xr_dataset
from gdptools.utils import _process_period
from gdptools.utils import _read_shp_file

logger = logging.getLogger(__name__)


class UserData(ABC):
    """Prepare data for different sources for weight generation."""

    @abstractmethod
    def __init__(self) -> None:
        """Init class."""
        pass

    @abstractmethod
    def get_source_subset(self, key: str) -> xr.DataArray:
        """Abstract method for getting subset of source data."""
        pass

    @abstractmethod
    def prep_wght_data(self) -> WeightData:
        """Abstract interface for generating weight data."""
        pass

    @abstractmethod
    def prep_interp_data(self, key: str, poly_id: int) -> AggData:
        """Abstract method for preparing data for interpolation."""
        pass

    @abstractmethod
    def prep_agg_data(self, key: str) -> AggData:
        """Abstract method for preparing data for aggregation."""
        pass

    @abstractmethod
    def get_vars(self) -> list[str]:
        """Return a list of variables."""
        pass

    @abstractmethod
    def get_feature_id(self) -> str:
        """Abstract method for returning the id_feature parameter."""
        pass

    @abstractmethod
    def get_class_type(self) -> str:
        """Abstract method for returning the type of the data class."""
        pass


class ClimRCatData(UserData):
    """Instance of UserData using Climate-R catalog data."""

    def __init__(
        self: "ClimRCatData",
        *,
        cat_dict: dict[str, dict[str, Any]],
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        id_feature: str,
        period: List[Optional[Union[str, pd.Timestamp, datetime.datetime]]],
    ) -> None:  # sourcery skip: simplify-len-comparison
        """Initialize ClimRCatData class.

        This class uses wraps the ClimateR-catalogs developed by Mike Johnson
        and available here https://github.com/mikejohnson51/climateR-catalogs.

        This can be queried in pandas to return the dictionary associated with a
        specific source and variable in the ClimateR-catalog. The cat_dict argument
        is composed of a key defined by the variable name and a dictionary of the
        corresponding ClimateR-catalog dictionary from the variable.


        Args:
            cat_dict (dict[str, dict[str, Any]]): Parameter metadata from
            climateR-catalog.
            f_feature (Union[str, Path, gpd.GeoDataFrame]): GeoDataFrame
                or any path-like object that can be read by geopandas.read_file().
            id_feature (str): Header in GeoDataFrame to use as index for weights.
            period (List[Optional[Union[str, pd.Timestamp, datetime.datetime]]]): List containing date strings defining start and end
                time slice for aggregation.

        Raises:
            KeyError: Raises error if id_feature not in f_feature columns.

        Example:
            ::

                # Example of using climateR-catalog to prep cat_dict parameter
                >>> cat_url = "https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet"
                >>> cat = pd.read_parquet(cat_url)
                >>> _id = "terraclim"
                >>> cat_vars = ["aet", "pet", "PDSI"]
                >>> cat_params = [
                ... cat.query("id == @_id & variable == @_var")
                ... .to_dict(orient="records")[0]
                ... for _var in cat_vars
                ... ]
                >>> cat_dict = dict(zip(cat_vars, cat_params))
                >>> cat_dict.get("aet")
                {'id': 'terraclim',
                 'asset': 'agg_terraclimate_aet_1958_CurrentYear_GLOBE',
                 'URL': 'http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_terraclimate_aet_1958_CurrentYear_GLOBE.nc',  # noqa: B950
                 'type': 'opendap',
                 'varname': 'aet',
                 'variable': 'aet',
                 'description':
                 'water_evaporation_amount',
                 'units': 'mm',
                 'model': nan,
                 'ensemble': nan,
                 'scenario': 'total',
                 'T_name': 'time',
                 'duration':'1958-01-01/2021-12-01',
                 'interval': '1 months',
                 'nT': 768.0,
                 'X_name': 'lon',
                 'Y_name': 'lat',
                 'X1': -179.9792,
                 'Xn': 179.9792,
                 'Y1': 89.9792,
                 'Yn': -89.9792,
                 'resX': 0.0417,
                 'resY': 0.0417,
                 'ncols': 8640.0,
                 'nrows': 4320.0,
                 'crs': '+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs',  # noqa: B950
                 'toptobottom': 0.0,
                 'tiled': '
                }
        """
        logger.info("Initializing ClimRCatData")
        logger.info("  - loading data")
        self.cat_dict = cat_dict
        self.f_feature = f_feature
        self.id_feature = id_feature
        self.period = _process_period(period)
        self._check_input_dict()
        self._gdf = _read_shp_file(self.f_feature)
        if self.id_feature not in self._gdf.columns:
            # print(
            #     f"id_feature {self.id_feature} not in f_feature columns: "
            #     f" {self._gdf.columns}"
            # )
            raise KeyError((f"id_feature {self.id_feature} not in f_feature columns: " f" {self._gdf.columns}"))
        self.proj_feature = self._gdf.crs
        self._check_id_feature()
        self._keys = self.get_vars()
        cat_cr = self._create_climrcats(key=self._keys[0])

        logger.info("  - checking latitude bounds")
        is_intersect, is_degrees, is_0_360 = _check_for_intersection(
            cat_cr=cat_cr, gdf=self._gdf
        )  # Project the gdf to the crs of the gridded data
        self._gdf, self._gdf_bounds = _get_shp_file(shp_file=self._gdf, cat_cr=cat_cr, is_degrees=is_degrees)
        self._rotate_ds = bool((not is_intersect) & is_degrees & (is_0_360))

    def get_source_subset(self, key: str) -> xr.DataArray:
        """get_source_subset Get subset of source data by key.

        _extended_summary_

        Args:
            key (str): _description_

        Returns:
            xr.DataArray: _description_
        """
        cat_cr = self._create_climrcats(key=key)
        return _get_data_via_catalog(
            cat_cr=cat_cr,
            bounds=self._gdf_bounds,
            begin_date=self.period[0],
            end_date=self.period[1],
            rotate_lon=self._rotate_ds,
        )

    def prep_interp_data(self, key: str, poly_id: Union[str, int]) -> AggData:
        """Prep AggData from ClimRCatData.

        Args:
            key (str): Name of the xarray grided data variable
            poly_id (Union[str, int]): ID number of the geodataframe geometry to clip the
                gridded data to

        Returns:
            AggData: An instance of the AggData class
        """
        cat_cr = self._create_climrcats(key=key)

        # Select a feature and make sure it remains a geodataframe
        feature = self._gdf[self._gdf[self.id_feature] == poly_id]

        # Clip grid by x, y and time
        ds_ss = _get_data_via_catalog(
            cat_cr=cat_cr,
            bounds=self._gdf_bounds,
            begin_date=self.period[0],
            end_date=self.period[1],
            rotate_lon=self._rotate_ds,
        )

        return AggData(
            variable=key,
            cat_cr=cat_cr,
            da=ds_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_agg_data(self, key: str) -> AggData:
        """Prepare ClimRCatData data for aggregation methods.

        Args:
            key (str): _description_

        Returns:
            AggData: _description_
        """
        cat_cr = self._create_climrcats(key=key)

        feature = self._gdf

        ds_ss = _get_data_via_catalog(
            cat_cr=cat_cr,
            bounds=self._gdf_bounds,
            begin_date=self.period[0],
            end_date=self.period[1],
            rotate_lon=self._rotate_ds,
        )

        return AggData(
            variable=key,
            cat_cr=cat_cr,
            da=ds_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_wght_data(self) -> WeightData:
        """Prepare and return WeightData for weight generation."""
        # For weight generation we just need metadata for one variable
        cat_cr = self._create_climrcats(key=self._keys[0])
        ds_ss = _get_data_via_catalog(
            cat_cr=cat_cr,
            bounds=self._gdf_bounds,
            begin_date=self.period[0],
            end_date=self.period[1],
            rotate_lon=self._rotate_ds,
        )
        tsrt = time.perf_counter()
        gdf_grid = _get_cells_poly(
            xr_a=ds_ss,
            x=cat_cr.X_name,
            y=cat_cr.Y_name,
            crs_in=cat_cr.crs,
        )
        tend = time.perf_counter()
        print(f"grid cells generated in {tend-tsrt:0.4f} seconds")

        return WeightData(feature=self._gdf, id_feature=self.id_feature, grid_cells=gdf_grid)

    def get_feature_id(self) -> str:
        """Return id_feature."""
        return self.id_feature

    def get_vars(self) -> list[str]:
        """Return list of param_dict keys, proxy for varnames."""
        return list(self.cat_dict.keys())

    def _check_input_dict(self: "ClimRCatData") -> None:
        """Check input cat_dict."""
        if len(self.cat_dict) < 1:
            raise ValueError("cat_dict should have at least 1 key,value pair")

    def _check_id_feature(self: "ClimRCatData") -> None:
        """Check id_feature in gdf."""
        if self.id_feature not in self._gdf.columns[:]:
            raise ValueError(f"shp_poly_idx: {self.id_feature} not in gdf" f" columns: {self._gdf.columns}")

    def get_class_type(self) -> str:
        """Abstract method for returning the type of the data class."""
        return "ClimRCatData"

    def _create_climrcats(self: "ClimRCatData", key: str) -> CatClimRItem:
        """Returns an instance on the CatClimRItem data class"""
        return CatClimRItem(**self.cat_dict[key])


class UserCatData(UserData):
    """Instance of UserData using for datasets not in ClimRCatData or NHGFStacData."""

    def __init__(
        self,
        *,
        ds: Union[str, xr.Dataset],
        proj_ds: Any,
        x_coord: str,
        y_coord: str,
        t_coord: str,
        var: Union[str, List[str]],
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        proj_feature: Any,
        id_feature: str,
        period: List[Optional[Union[str, pd.Timestamp, datetime.datetime]]],
    ) -> None:
        """__init__ Contains data preparation methods based on UserData.

        Args:
            ds (Union[str, Path, xr.Dataset]): Xarray Dataset or str, URL or Path object
                that can be read by xarray.
            proj_ds (Any): Any object that can be passed to
                pyproj.crs.CRS.from_user_input for ds
            x_coord (str): String of x coordinate name in ds
            y_coord (str): String of y coordinate name in ds
            t_coord (str): string of time coordinate name in ds
            var (Union[str, List[str]]): List of variables to be used in aggregation.
                They must be present in ds.
            f_feature (Union[str, Path, gpd.GeoDataFrame]): GeoDataFrame or str, URL or
                Path object that can be read by geopandas.
            proj_feature (Any): Any object that can be passed to
                pyproj.crs.CRS.from_user_input for f_feature
            id_feature (str): String of id column name in f_feature.
            period (List[Optional[Union[str, pd.Timestamp, datetime.datetime]]]): List of two strings
                of the form 'YYYY-MM-DD' that define the start and end of the period to be used in aggregation.
                The format may be 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'. depending on the format of
                the time coordinate in ds.

        Raises:
            KeyError: Raises error if id_feature not in f_feature columns.
        """
        logger.info("Initializing UserCatData")
        logger.info("  - loading data")
        self.ds = _get_xr_dataset(ds=ds)
        self.id_feature = id_feature
        self.f_feature = _read_shp_file(shp_file=f_feature)
        if self.id_feature not in self.f_feature.columns:
            print(f"id_feature {self.id_feature} not in f_feature columns: " f" {self.f_feature.columns}")
            raise KeyError()
        self.proj_ds = proj_ds
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.t_coord = t_coord
        # self.period = pd.to_datetime(period)
        self.period = _process_period(period)
        if not isinstance(var, List):
            self.var = [var]
        else:
            self.var = var
        self.proj_feature = proj_feature

        self._gdf_bounds = _get_shp_bounds_w_buffer(
            gdf=self.f_feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )
        logger.info("  - checking latitude bounds")
        is_intersect, is_degrees, is_0_360 = _check_for_intersection_nc(
            ds=self.ds,
            x_name=self.x_coord,
            y_name=self.y_coord,
            proj=self.proj_ds,
            gdf=self.f_feature,
        )

        if bool((not is_intersect) & is_degrees & (is_0_360)):  # rotate
            logger.info("  - rotating into -180 - 180")
            self.ds.coords[self.x_coord] = (self.ds.coords[self.x_coord] + 180) % 360 - 180
            self.ds = self.ds.sortby(self.ds[self.x_coord])

        # calculate toptobottom (order of latitude coords)
        self._ttb = _get_top_to_bottom(self.ds, self.y_coord)
        logger.info("  - getting gridded data subset")
        self._agg_subset_dict = build_subset(
            bounds=self._gdf_bounds,
            xname=self.x_coord,
            yname=self.y_coord,
            tname=self.t_coord,
            toptobottom=self._ttb,
            date_min=self.period[0],
            date_max=self.period[1],
        )

    @classmethod
    def __repr__(cls) -> str:
        """Print class name."""
        return f"Class is {cls.__name__}"

    def get_source_subset(self, key: str) -> xr.DataArray:
        """get_source_subset Get source subset by key.

        _extended_summary_

        Args:
            key (str): Name of the xarray gridded data variable.

        Returns:
            xr.DataArray: A subsetted xarray DataArray of the original source gridded data.
        """
        return self.ds[key].sel(**self._agg_subset_dict)

    def get_feature_id(self) -> str:
        """Return id_feature."""
        return self.id_feature

    def get_vars(self) -> list[str]:
        """Return list of vars in data."""
        return self.var

    def get_class_type(self) -> str:
        """Abstract method for returning the type of the data class."""
        return "UserCatData"

    def prep_interp_data(self, key: str, poly_id: Union[str, int]) -> AggData:
        """Prep AggData from UserCatData.

        Args:
            key (str): Name of the xarray grided data variable
            poly_id (Union[str, int]): ID number of the geodataframe geometry to clip the
                gridded data to

        Returns:
            AggData: An instance of the AggData class
        """
        # Open grid and clip to geodataframe and time window
        data_ss: xr.DataArray = self.ds[key].sel(**self._agg_subset_dict)  # type: ignore

        # Select a feature and make sure it remains a geodataframe
        feature = self.f_feature[self.f_feature[self.id_feature] == poly_id]

        # Reproject the feature to grid crs and get a buffered bounding box
        bounds = _get_shp_bounds_w_buffer(
            gdf=feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )

        # Clip grid to time window and line geometry bbox buffer
        ss_dict = build_subset(
            bounds=bounds,
            xname=self.x_coord,
            yname=self.y_coord,
            tname=self.t_coord,
            toptobottom=self._ttb,
            date_min=str(self.period[0]),
            date_max=str(self.period[1]),
        )

        ds_ss = data_ss.sel(**ss_dict)
        cat_cr = self._create_climrcats(key=key, da=ds_ss)

        return AggData(
            variable=key,
            cat_cr=cat_cr,
            da=ds_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_agg_data(self, key: str) -> AggData:
        """Prep AggData from UserData."""
        logger.info("Agg Data preparation - beginning")
        data_ss: xr.DataArray = self.ds[key].sel(**self._agg_subset_dict)  # type: ignore
        cat_cr = self._create_climrcats(key=key, da=data_ss)

        feature = self.f_feature
        logger.info("  - returning AggData")
        return AggData(
            variable=key,
            cat_cr=cat_cr,
            da=data_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def _create_climrcats(self: "UserCatData", key: str, da: xr.DataArray) -> CatClimRItem:
        """Returns an instance on the CatClimRItem data class"""
        return CatClimRItem(
            # id=self.id,
            URL="",
            varname=key,
            long_name=str(self._get_ds_var_attrs(da, "long_name")),
            T_name=self.t_coord,
            units=str(self._get_ds_var_attrs(da, "units")),
            X_name=self.x_coord,
            Y_name=self.y_coord,
            proj=self.proj_ds,
            resX=max(np.diff(da[self.x_coord].values)),
            resY=max(np.diff(da[self.y_coord].values)),
            toptobottom=str(_get_top_to_bottom(da, self.y_coord)),
        )

    def _get_ds_var_attrs(self, da: xr.DataArray, attr: str) -> Any:
        """Return var attributes.

        Args:
            da (xr.DataArray): _description_
            attr (str): _description_

        Returns:
            Any: _description_
        """
        try:
            return da.attrs.get(attr)
        except KeyError:
            return "None"

    def prep_wght_data(self) -> WeightData:
        """Prepare and return WeightData for weight generation."""
        logger.info("Weight Data preparation - beginning")
        try:
            data_ss_wght = self.ds.sel(**self._agg_subset_dict)  # type: ignore
        except KeyError as e:
            if self.t_coord in str(e):
                example_time = self.ds[self.t_coord].values[0]
                new_message = (
                    f"The source data time coordinate is formatted as {example_time}, you specified time as"
                    f"{self.period[0]}. For non-standard time formats, Use a string to specify a time period that"
                    "matches the time format in the source data"
                )
                raise KeyError(new_message) from e

        logger.info("  - calculating grid-cell polygons")
        start = time.perf_counter()
        grid_poly = _get_cells_poly(
            xr_a=data_ss_wght,
            x=self.x_coord,
            y=self.y_coord,
            crs_in=self.proj_ds,
        )
        end = time.perf_counter()
        print(f"Generating grid-cell polygons finished in {round(end-start, 2)} second(s)")
        logger.info(f"Generating grid-cell polygons finished in {round(end-start, 2)} second(s)")
        return WeightData(feature=self.f_feature, id_feature=self.id_feature, grid_cells=grid_poly)


class NHGFStacData(UserData):
    """Instance of UserData for the purpose of accessing gridded datasets from the NHGF STAC."""

    def __init__(
        self,
        *,
        collection,
        var: Union[str, List[str]],
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        id_feature: str,
        period: List[Optional[Union[str, pd.Timestamp, datetime.datetime]]],
    ) -> None:
        # flake8: noqa
        """Initialize NHGFStacData class.

        This class is meant to read in gridded datasets from the National Hydrologic Geospatail Fabric (NHGF)
        Spatio-Temporal Asset Catalog (STAC) available here:

        https://code.usgs.gov/wma/nhgf/stac/-/raw/main/catalog/catalog.json

        The STAC is accessed and queried with the pystac Python package.

        Args:
            collection (pystac.collection.Collection): SpatioTemporal Asset Catalog (STAC)
                collection object.
            var (Union[str, List[str]]): List of variables to be used in aggregation.
                They must be present in ds.
            f_feature (Union[str, Path, gpd.GeoDataFrame]): GeoDataFrame or str, URL or
                Path object that can be read by geopandas.
            id_feature (str): String of id column name in f_feature.
            period (List[str]): List of two strings of the form 'YYYY-MM-DD' that define
                the start and end of the period to be used in aggregation.  The format
                may be 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'. depending on the format of
                the time coordinate in ds.

        Raises:
            KeyError: Raises error if id_feature not in f_feature columns.
        """
        logger.info("Initializing NHGFStacData")
        logger.info("  - loading data")
        self.id = collection.id
        self.asset = collection.assets["zarr-s3-osn"]
        self.ds = xr.open_dataset(self.asset)
        self.id_feature = id_feature
        self.f_feature = f_feature
        self._gdf = _read_shp_file(self.f_feature)
        if self.id_feature not in self._gdf.columns:
            logger.error(f"id_feature {self.id_feature} not in f_feature columns: " f" {self._gdf.columns}")
            raise KeyError(f"id_feature {self.id_feature} not in f_feature columns: " f" {self._gdf.columns}")
        self.period = period
        self.var = var if isinstance(var, List) else [var]
        # Ensure gridded data has proper dimensions
        # check_gridded_data_for_dimensions(self.ds, self.var)
        self.proj_feature = self._gdf.crs
        self.proj_ds = self.ds.crs.attrs["crs_wkt"]
        if type(CRS.from_string(self.proj_ds)) is not CRS:
            logger.error("Projection of the gridded dataset could not be identified")

        self.x_coord = "x"
        self.y_coord = "y"
        self.t_coord = "time"

        self._gdf_bounds = _get_shp_bounds_w_buffer(
            gdf=self._gdf,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )
        logger.info("  - checking latitude bounds")
        is_intersect, is_degrees, is_0_360 = _check_for_intersection_nc(
            ds=self.ds,
            x_name=self.x_coord,
            y_name=self.y_coord,
            proj=self.proj_ds,
            gdf=self._gdf,
        )

        if bool((not is_intersect) & is_degrees & (is_0_360)):  # rotate
            logger.info("  - rotating into -180 - 180")
            self.ds.coords[self.x_coord] = (self.ds.coords[self.x_coord] + 180) % 360 - 180
            self.ds = self.ds.sortby(self.ds[self.x_coord])

        # calculate toptobottom (order of latitude coords)
        self._ttb = _get_top_to_bottom(self.ds, self.y_coord)
        logger.info("  - getting gridded data subset")
        self._weight_subset_dict = build_subset(
            bounds=self._gdf_bounds,
            xname=self.x_coord,
            yname=self.y_coord,
            tname=self.t_coord,
            toptobottom=self._ttb,
            date_min=self.period[0],
        )
        self._agg_subset_dict = build_subset(
            bounds=self._gdf_bounds,
            xname=self.x_coord,
            yname=self.y_coord,
            tname=self.t_coord,
            toptobottom=self._ttb,
            date_min=self.period[0],
            date_max=self.period[1],
        )

    @classmethod
    def __repr__(cls) -> str:
        """Print class name."""
        return f"Class is {cls.__name__}"

    def get_source_subset(self, key: str) -> xr.DataArray:
        """Get source subset by key.

        Subset the Xarray Dataset by variable, time and space.

        Args:
            key (str): Name of the variable of interest.

        Returns:
            xr.DataArray: Subsetted dataarray.
        """
        return self.ds[key].sel(**self._agg_subset_dict)

    def get_feature_id(self) -> str:
        """Return id_feature."""
        return self.id_feature

    def get_vars(self) -> list[str]:
        """Return list of vars in data."""
        return self.var

    def get_class_type(self) -> str:
        """Abstract method for returning the type of the data class."""
        return "NHGFStacData"

    def prep_interp_data(self, key: str, poly_id: Union[str, int]) -> AggData:
        """Prep AggData from NHGFStacData.

        Args:
            key (str): Name of the xarray grided data variable
            poly_id (Union[str, int]): ID number of the geodataframe geometry to clip the
                gridded data to

        Returns:
            AggData: An instance of the AggData class
        """
        # Open grid and clip to geodataframe and time window
        data_ss = self.get_source_subset(key)
        cat_cr = self._create_climrcats(key=key, da=data_ss)

        # Select a feature and make sure it remains a geodataframe
        feature = self._gdf[self._gdf[self.id_feature] == poly_id]

        return AggData(
            variable=key,
            cat_cr=cat_cr,
            da=data_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_agg_data(self, key: str) -> AggData:
        """Prep AggData from UserData."""
        logger.info("Agg Data preparation - beginning")
        data_ss: xr.DataArray = self.get_source_subset(key)
        cat_cr = self._create_climrcats(key=key, da=data_ss)
        feature = self._gdf
        # If the time dimension has only one step:
        try:
            data_ss.coords.get(self.t_coord).all()
            period = self.period
        except Exception:
            period = ["None", "None"]

        logger.info("  - returning AggData")
        return AggData(
            variable=key,
            cat_cr=cat_cr,
            da=data_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=period,
        )

    def _create_climrcats(self: "NHGFStacData", key: str, da: xr.DataArray) -> CatClimRItem:
        """Returns an instance on the CatClimRItem data class"""
        return CatClimRItem(
            id=self.id,
            URL=self.asset.href,
            varname=key,
            long_name=str(self._get_ds_var_attrs(da, "description")),
            T_name=self.t_coord,
            units=str(self._get_ds_var_attrs(da, "units")),
            X_name=self.x_coord,
            Y_name=self.y_coord,
            proj=self.proj_ds,
            resX=max(np.diff(da[self.x_coord].values)),
            resY=max(np.diff(da[self.y_coord].values)),
            toptobottom=str(_get_top_to_bottom(da, self.y_coord)),
        )

    def _get_ds_var_attrs(self, da: xr.DataArray, attr: str) -> Any:
        """Return var attributes.

        Args:
            da (xr.DataArray): Target DataArray to pull attributes from
            attr (str): Name of the attribute to return

        Returns:
            Any: Value of the attribute.
        """
        try:
            return da.attrs.get(attr)
        except KeyError:
            return "None"

    def prep_wght_data(self) -> WeightData:
        """Prepare and return WeightData for weight generation."""
        logger.info("Weight Data preparation - beginning")
        data_ss_wght = self.ds.sel(**self._weight_subset_dict)  # type: ignore
        logger.info("  - calculating grid-cell polygons")
        start = time.perf_counter()
        grid_poly = _get_cells_poly(
            xr_a=data_ss_wght,
            x=self.x_coord,
            y=self.y_coord,
            crs_in=self.proj_ds,
        )
        end = time.perf_counter()
        print(f"Generating grid-cell polygons finished in {round(end-start, 2)} second(s)")
        logger.info(f"Generating grid-cell polygons finished in {round(end-start, 2)} second(s)")
        return WeightData(feature=self._gdf, id_feature=self.id_feature, grid_cells=grid_poly)


class UserTiffData(UserData):
    """Instance of UserData for zonal stats processing of geotiffs."""

    def __init__(
        self,
        var: str,
        ds: Union[str, xr.DataArray, xr.Dataset],
        proj_ds: Any,
        x_coord: str,
        y_coord: str,
        bname: str,
        band: int,
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        id_feature: str,
        # proj_feature: Any,
    ) -> None:
        """Initialize UserTiffData.

        UserTiffData is a structure that aids calculating zonal stats.

        Args:
            var (str): Name of variable - **Not currently used**
            ds (Union[str, xr.Dataset]): Target XArray dataset or path to dataset.
            proj_ds (Any): Any acceptable input to pyproj.crs.CRS.from_user_input() method for the source data.
            x_coord (str): Name of the x-coordinate.
            y_coord (str): Name of the y-coordinate.
            bname (str): Name of the band generally band.
            band (int): Band to use - generally 1.
            f_feature (Union[str, Path, gpd.GeoDataFrame]): Target GeoDataFrame or path to GeoDataFrame.
            id_feature (str): ID of the feature to identify the results with.
            proj_feature (Any): Any acceptable input to pyproj.crs.CRS.from_user_input() method for the target data.
        """
        self.varname = var
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.bname = bname
        self.band = band
        self.ds = _get_rxr_dataset(ds)
        self.proj_ds = proj_ds
        self.f_feature = _read_shp_file(shp_file=f_feature)

        self.id_feature = id_feature
        self.f_feature = self.f_feature.sort_values(self.id_feature).dissolve(by=self.id_feature, as_index=False)
        self.f_feature.reset_index()
        self.proj_feature = self.f_feature.crs.to_epsg()

        self._check_xname()
        self._check_yname()
        self._check_band()
        self._check_crs()
        self._toptobottom = _get_top_to_bottom(data=self.ds, y_coord=self.y_coord)

        @property
        def proj_ds(self):
            """Getter for proj_ds.

            Returns:
                Any: The proj_ds attribute, which is any acceptable input to pyproj.crs.CRS.from_user_input()
                    method for the source data.
            """
            return self._proj_ds

        @property
        def proj_feature(self):
            """Getter for proj_feature.

            Returns:
                Any: The proj_feature attribute, which is any acceptable input to pyproj.crs.CRS.from_user_input()
                    method for the target data.
            """
            return self._proj_feature

    def get_source_subset(self, key: str) -> xr.DataArray:
        """get_source_subset Get subset of source data.

        _extended_summary_

        Args:
            key (str): Key that identifies the source data - generally band.

        Returns:
            xr.DataArray: _description_
        """
        bb_feature = _get_shp_bounds_w_buffer(
            gdf=self.f_feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )

        subset_dict = build_subset_tiff(
            bounds=bb_feature,
            xname=self.x_coord,
            yname=self.y_coord,
            toptobottom=self._toptobottom,
            bname=self.bname,
            band=self.band,
        )

        return self.ds.sel(**subset_dict)  # type: ignore

    def get_vars(self) -> list[str]:
        """Return list of varnames."""
        return [self.varname]

    def get_feature_id(self) -> str:
        """Get Feature id."""
        return self.id_feature

    def prep_wght_data(self) -> WeightData:
        """Prepare data for weight generation."""
        pass

    def get_class_type(self) -> str:
        """Abstract method for returning the type of the data class."""
        return "UserTiffData"

    def prep_interp_data(self, key: str, poly_id: int) -> AggData:
        """Prep AggData from UserTiffData.

        Args:
            key (str): Name of the xarray grided data variable
            poly_id (int): ID number of the geodataframe geometry to clip the
                gridded data to

        Returns:
            AggData: An instance of the AggData class
        """
        # Select a feature and make sure it remains a geodataframe
        feature = self.f_feature[self.f_feature[self.id_feature] == poly_id]

        bb_feature = _get_shp_bounds_w_buffer(
            gdf=feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )

        subset_dict = build_subset_tiff(
            bounds=bb_feature,
            xname=self.x_coord,
            yname=self.y_coord,
            toptobottom=self._toptobottom,
            bname=self.bname,
            band=self.band,
        )

        data_ss: xr.DataArray = self.ds.sel(**subset_dict)  # type: ignore
        cat_cr = self._create_climrcats(key=key, da=data_ss)

        return AggData(
            variable=key,
            cat_cr=cat_cr,
            da=data_ss,
            feature=feature,
            id_feature=self.id_feature,
            period=["None", "None"],
        )

    def prep_agg_data(self, key: str) -> AggData:
        """Prepare data for aggregation or zonal stats."""
        bb_feature = _get_shp_bounds_w_buffer(
            gdf=self.f_feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )

        subset_dict = build_subset_tiff(
            bounds=bb_feature,
            xname=self.x_coord,
            yname=self.y_coord,
            toptobottom=self._toptobottom,
            bname=self.bname,
            band=self.band,
        )

        data_ss: xr.DataArray = self.ds.sel(**subset_dict)  # type: ignore
        if data_ss.size == 0:
            raise ValueError(
                "Sub-setting the raster resulted in no values",
                f"check the specified proj_ds value: {self.proj_ds}",
                f" and proj_feature value: {self.proj_feature}",
            )

        cat_cr = self._create_climrcats(key=key, da=data_ss)

        return AggData(
            variable=key,
            cat_cr=cat_cr,
            da=data_ss,
            feature=self.f_feature.copy(),
            id_feature=self.id_feature,
            period=["None", "None"],
        )

    def _check_xname(self: "UserTiffData") -> None:
        """Validate xname."""
        if self.x_coord not in self.ds.coords:
            raise ValueError(f"xname:{self.x_coord} not in {self.ds.coords}")

    def _check_yname(self: "UserTiffData") -> None:
        """Validate yname."""
        if self.y_coord not in self.ds.coords:
            raise ValueError(f"yname:{self.y_coord} not in {self.ds.coords}")

    def _check_band(self: "UserTiffData") -> None:
        """Validate band name."""
        if self.bname not in self.ds.coords:
            raise ValueError(f"band:{self.bname} not in {self.ds.coords} or {self.ds.data_vars}")

    def _check_crs(self: "UserTiffData") -> None:
        """Validate crs."""
        crs = CRS.from_user_input(self.proj_ds)
        if not isinstance(crs, CRS):
            raise ValueError(f"ds_proj:{self.proj_ds} not in valid")
        crs2 = CRS.from_user_input(self.proj_feature)
        if not isinstance(crs2, CRS):
            raise ValueError(f"ds_proj:{self.proj_feature} not in valid")

    def _create_climrcats(self: "UserTiffData", key: str, da: xr.DataArray) -> CatClimRItem:
        """Returns an instance on the CatClimRItem data class"""
        return CatClimRItem(
            # id=self.id,
            URL="",
            varname=key,
            long_name=str(self._get_ds_var_attrs(da, "description")),
            units=str(self._get_ds_var_attrs(da, "units")),
            X_name=self.x_coord,
            Y_name=self.y_coord,
            proj=self.proj_ds,
            resX=max(np.diff(da[self.x_coord].values)),
            resY=max(np.diff(da[self.y_coord].values)),
            toptobottom=str(_get_top_to_bottom(da, self.y_coord)),
        )

    def _get_ds_var_attrs(self: "UserTiffData", da: xr.DataArray, attr: str) -> str:
        """Return var attributes.

        Args:
            da (xr.DataArray): _description_
            attr (str): _description_

        Returns:
            str: _description_
        """
        try:
            return str(da.attrs.get(attr))
        except KeyError:
            return "None"
