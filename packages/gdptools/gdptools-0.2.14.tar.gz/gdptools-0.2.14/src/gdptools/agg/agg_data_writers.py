"""Method for saving aggregation data."""

import warnings
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import geopandas as gpd
import netCDF4
import numpy as np
import numpy.typing as npt
import pandas as pd
import pyproj
import xarray as xr
from shapely.geometry import Point

from gdptools.data.agg_gen_data import AggData


class AggDataWriter(ABC):
    """Abstract writer Template method."""

    def save_file(
        self: "AggDataWriter",
        agg_data: Dict[str, AggData],
        feature: gpd.GeoDataFrame,
        vals: List[npt.NDArray[Union[np.int_, np.double]]],
        p_out: str,
        file_prefix: str,
        append_date: Optional[bool] = False,
        precision: Optional[int] = None,
    ) -> None:
        """Abstract Template method for writing aggregation data.

        Args:
            agg_data (List[AggData]): AggData generated during aggregation.
            feature (gpd.GeoDataFrame): The target dataframe.
            vals (List[npt.NDArray[Union[int, np.double]]]): The aggregated values.
            p_out (str): Output path.
            file_prefix (str): User defined prefix for output file.
            append_date (Optional[bool], optional): Append current date to output file name. Defaults to False.
            precision (Optional[int], optional): Specify the precision of output values.

        Raises:
            FileNotFoundError: _description_
        """
        self.agg_data = agg_data
        self.feature = feature
        self.vals = vals
        self.append_date = append_date
        self.precision = precision
        self.fdate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.outpath = Path(p_out)
        if not self.outpath.exists():
            raise FileNotFoundError(f"Path: {p_out} does not exist")
        if self.append_date:
            self.fname = f"{self.fdate}_{file_prefix}"
        else:
            self.fname = f"{file_prefix}"

        self.create_out_file()

    @abstractmethod
    def create_out_file(self) -> None:
        """Abstract method for writing aggregation data."""
        pass


class CSVWriter(AggDataWriter):
    """Class for writing csv files."""

    def create_out_file(self) -> None:
        """Method for writing csv files."""
        # for idx in range(len(self.agg_data)):
        for idx, (_key, value) in enumerate(self.agg_data.items()):
            gdf = self.feature
            gdf_idx = self.agg_data[_key].id_feature
            param_values = value.cat_cr
            t_coord = param_values.T_name
            units = param_values.units
            varname = param_values.varname
            time = value.da.coords[t_coord].values
            # units = self.agg_data[idx].param_dict

            df_key = pd.DataFrame(data=self.vals[idx], columns=gdf[gdf_idx].T.values)

            df_key.insert(0, "units", [units] * df_key.shape[0])
            df_key.insert(0, "varname", [varname] * df_key.shape[0])
            df_key.insert(0, "time", time)

            if idx == 0:
                df = df_key
            else:
                df = pd.concat([df, df_key])
        df.reset_index(inplace=True)
        if self.precision is not None:
            df = df.round(self.precision)
        path_to_file = self.outpath / f"{self.fname}.csv"
        print(f"Saving csv file to {path_to_file}")
        df.to_csv(path_to_file, index=False)


class JSONWriter(AggDataWriter):
    """Class for writing json output."""

    def create_out_file(self) -> None:
        """Method for writing json files."""
        # for idx in range(len(self.agg_data)):
        for idx, (_key, value) in enumerate(self.agg_data.items()):
            gdf = self.feature
            gdf_idx = self.agg_data[_key].id_feature
            param_values = value.cat_cr
            t_coord = param_values.T_name
            units = param_values.units
            varname = param_values.varname
            time = value.da.coords[t_coord].values
            # units = self.agg_data[idx].param_dict

            df_key = pd.DataFrame(data=self.vals[idx], columns=gdf[gdf_idx].T.values)

            df_key.insert(0, "units", [units] * df_key.shape[0])
            df_key.insert(0, "varname", [varname] * df_key.shape[0])
            df_key.insert(0, "time", time)

            if idx == 0:
                df = df_key
            else:
                df = pd.concat([df, df_key])
        df.reset_index(inplace=True)
        path_to_file = self.outpath / f"{self.fname}.json"
        print(f"Saving csv file to {path_to_file}")
        df.to_json(path_to_file, orient="records", date_format="iso")


class ParquetWriter(AggDataWriter):
    """Class for writing csv files."""

    def create_out_file(self) -> None:
        """Method for writing csv files."""
        # for idx in range(len(self.agg_data)):
        for idx, (_key, value) in enumerate(self.agg_data.items()):
            gdf = self.feature
            gdf_idx = self.agg_data[_key].id_feature
            param_values = value.cat_cr
            t_coord = param_values.T_name
            units = param_values.units
            varname = param_values.varname
            time = value.da.coords[t_coord].values
            # units = self.agg_data[idx].param_dict

            df_key = pd.DataFrame(data=self.vals[idx], columns=gdf[gdf_idx].T.values)

            df_key.insert(0, "units", [units] * df_key.shape[0])
            df_key.insert(0, "varname", [varname] * df_key.shape[0])
            df_key.insert(0, "time", time)

            if idx == 0:
                df = df_key
            else:
                df = pd.concat([df, df_key])
        df.reset_index(inplace=True)
        if self.precision is not None:
            df = df.round(self.precision)
        # df.columns = df.columns.map(str)
        path_to_file = self.outpath / f"{self.fname}.parquet.gzip"
        print(f"Saving csv file to {path_to_file}")
        df.to_parquet(path_to_file, compression="gzip")


class NetCDFWriter(AggDataWriter):
    """NetCDF writer class."""

    def create_out_file(self) -> None:
        """Create NetCDF file from aggregation data."""
        # Suppres UserWarning from centroid calc - Here lat/lon centroid are
        # a convenience method.
        warnings.filterwarnings(action="ignore", category=UserWarning)
        dataset = []
        # for idx in range(len(self.agg_data)):
        for idx, (_key, value) in enumerate(self.agg_data.items()):
            # convert geometry to 4326
            gdf = self.feature.to_crs(4326)
            gdf_idx = value.id_feature
            param_values = value.cat_cr
            t_coord = param_values.T_name
            v_units = param_values.units
            v_varname = param_values.varname
            v_long_name = param_values.long_name
            time = value.da.coords[t_coord].values
            locs = gdf[gdf_idx].values

            def getxy(pt: Point) -> Tuple[np.double, np.double]:
                """Return x y components of point."""
                return pt.x, pt.y

            centroid_series = gdf.geometry.centroid
            tlon, tlat = [list(t) for t in zip(*map(getxy, centroid_series))]  # noqa B905
            crs_meta = pyproj.CRS(gdf.crs).to_cf()
            if self.precision is not None:
                # Assuming self.vals[idx] is the array you want to round
                data_vals = np.round(self.vals[idx], self.precision)
            else:
                data_vals = self.vals[idx]
            dsn = xr.Dataset(
                data_vars={
                    v_varname: (
                        ["time", gdf_idx],
                        data_vals,
                        dict(
                            units=v_units,
                            long_name=v_long_name,
                            coordinates="time lat lon",
                            grid_mapping="crs",
                        ),
                    ),
                    # "crs": (["one"], np.ones((1), dtype=np.double), crs_meta),
                    "crs": ([], 1.0, crs_meta),
                },
                coords={
                    "time": time,
                    gdf_idx: ([gdf_idx], locs, {"feature_id": gdf_idx}),
                    "lat": (
                        [gdf_idx],
                        tlat,
                        {
                            "long_name": "Latitude of HRU centroid",
                            "units": "degrees_north",
                            "standard_name": "latitude",
                            "axis": "Y",
                        },
                    ),
                    "lon": (
                        [gdf_idx],
                        tlon,
                        {
                            "long_name": "Longitude of HRU centroid",
                            "units": "degrees_east",
                            "standard_name": "longitude",
                            "axis": "X",
                        },
                    ),
                },
            )
            if self.vals[idx].dtype.str == "<f8":
                dsn[v_varname].encoding.update({"_FillValue": netCDF4.default_fillvals["f8"]})
            elif self.vals[idx].dtype.str == "<i8":
                dsn[v_varname].encoding.update({"_FillValue": netCDF4.default_fillvals["i8"]})

            dataset.append(dsn)

        ds = xr.merge(dataset)
        ds.encoding["time"] = {"unlimited": True}
        ds.attrs = {
            "Conventions": "CF-1.8",
            "featureType": "timeSeries",
            "history": (
                f"{self.fdate} Original fileccreated  by gdptools package: "
                "https://code.usgs.gov/wma/nhgf/toolsteam/gdptools \n"
            ),
        }
        path_to_file = self.outpath / f"{self.fname}.nc"
        print(f"Saving netcdf file to {path_to_file}")
        ds.to_netcdf(path_to_file, format="NETCDF4", engine="netcdf4")
