"""Calculate zonal methods."""

import time
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Literal
from typing import Optional
from typing import Union

import pandas as pd

from gdptools.agg.zonal_engines import ZonalEngineDask
from gdptools.agg.zonal_engines import ZonalEngineParallel
from gdptools.agg.zonal_engines import ZonalEngineSerial
from gdptools.data.user_data import UserData

ZONAL_ENGINES = Literal["serial", "parallel", "dask"]
"""
Literal type alias for the zonal engines.

Options:
- "serial": Perform zonal calculations in a serial manner.
- "parallel": Perform zonal calculations in parallel.
- "dask": Perform zonal calculations using Dask for distributed computing.
"""

ZONAL_WRITERS = Literal["csv"]
"""
Literal type alias for the zonal writers.

Options:
- "csv": Write zonal statistics to a CSV file.
"""


class ZonalGen:
    """Class for aggregating zonal statistics."""

    def __init__(
        self,
        user_data: UserData,
        zonal_engine: ZONAL_ENGINES,
        zonal_writer: ZONAL_WRITERS,
        out_path: Optional[Union[str, None]] = None,
        file_prefix: Optional[Union[str, None]] = None,
        append_date: Optional[bool] = False,
        precision: Optional[int] = None,
        jobs: int = 1,
    ) -> None:
        """Initialize ZonalGen class.

        Args:
            user_data (UserData): An instance of UserTiffData containing the user-specific data.
            zonal_engine (ZONAL_ENGINES): The engine used for calculating zonal statistics.
                                          Options include "serial", "parallel", or "dask".
            zonal_writer (ZONAL_WRITERS): The format for writing the output zonal statistics. Currently supports "csv".
            out_path (str): The directory path where the output files will be saved.
            file_prefix (str): A prefix for the output file name.
            append_date (bool): Whether to append the current date and time to the file name. Defaults to False.
            precision (int): The number of decimal places to include in the output statistics (not currently implemented).
            jobs (int): The number of parallel jobs to use in calculations (applicable for parallel or dask engines). Defaults to 1.

        Raises:
            FileNotFoundError: Raised if the provided output path does not exist.
            TypeError: Raised if an invalid zonal engine is specified.
        """
        self._user_data = user_data
        self._zonal_engine = zonal_engine
        self._zonal_writer = zonal_writer
        self._jobs = jobs
        self._out_path = Path(out_path)
        if not self._out_path.exists():
            raise FileNotFoundError(f"Path: {self._out_path} does not exist")
        self._file_prefix = file_prefix
        self._append_date = append_date
        if self._append_date:
            self._fdate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            self._fname = f"{self._fdate}_{self._file_prefix}"
        else:
            self._fname = f"{self._file_prefix}"
        self.precision = precision
        self.agg: Union[ZonalEngineSerial, ZonalEngineParallel, ZonalEngineDask]
        if self._zonal_engine == "serial":
            self.agg = ZonalEngineSerial()
        elif self._zonal_engine == "parallel":
            self.agg = ZonalEngineParallel()
        elif self._zonal_engine == "dask":
            self.agg = ZonalEngineDask()
        else:
            raise TypeError(f"agg_engine: {self._zonal_engine} not in {ZONAL_ENGINES}")

    def calculate_zonal(self, categorical: bool = False) -> pd.DataFrame:
        """Calculate zonal statistics.

        This method performs the zonal statistics calculation using the specified engine
        and writes the results to a file if specified.

        Args:
            categorical (bool): If True, calculate categorical zonal statistics (e.g., mode).
                                If False, calculate continuous zonal statistics (e.g., mean, sum).
                                Defaults to False.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated zonal statistics.
        """
        tstrt = time.perf_counter()
        stats = self.agg.calc_zonal_from_aggdata(user_data=self._user_data, categorical=categorical, jobs=self._jobs)
        if self.precision is not None:
            stats = stats.round(self.precision)
        if self._zonal_writer == "csv":
            fullpath = self._out_path / f"{self._fname}.csv"
            stats.to_csv(fullpath, sep=",")
        tend = time.perf_counter()
        print(f"Total time for serial zonal stats calculation {tend - tstrt:0.4f} seconds")
        return stats
        # elif self._zonal_writer == "feather":
        #     fullpath = self._out_path / f"{self._fname}"
        #     stats.to_feather(path=fullpath, )


class WeightedZonalGen:
    """Class for aggregating weighted zonal statistics.

    This class handles the calculation of zonal statistics with weights based on the provided CRS (Coordinate Reference
    System).
    """

    def __init__(
        self,
        user_data: UserData,
        weight_gen_crs: Any,
        zonal_engine: ZONAL_ENGINES,
        zonal_writer: ZONAL_WRITERS,
        out_path: Optional[Union[str, None]] = None,
        file_prefix: Optional[Union[str, None]] = None,
        append_date: Optional[bool] = False,
        precision: Optional[int] = None,
        jobs: Optional[int] = 1,
    ) -> None:
        """Initialize a WeightedZonalGen object.

        Args:
            user_data (UserData): An instance containing the user-specific data for zonal analysis.
            weight_gen_crs (Any): The Coordinate Reference System (CRS) used for generating weights.
            zonal_engine (ZONAL_ENGINES): The engine used for calculating zonal statistics.
                                          Options include "serial", "parallel", or "dask".
            zonal_writer (ZONAL_WRITERS): The format for writing the output zonal statistics. Currently supports "csv".
            out_path (str, optional): The directory path where the output files will be saved. Defaults to None.
            file_prefix (str, optional): A prefix for the output file name. Defaults to None.
            append_date (bool, optional): Whether to append the current date and time to the file name. Defaults to
                                          False.
            precision (int, optional): The number of decimal places to include in the output statistics. Defaults to
                                       None.
            jobs (int, optional): The number of parallel jobs to use in calculations (applicable for parallel or dask
                                  engines). Defaults to 1.

        Raises:
            FileNotFoundError: Raised if the provided output path does not exist.
            TypeError: Raised if an invalid zonal engine is specified.

        Examples:
            >>> zonal_gen = WeightedZonalGen(
                    user_data=user_data,
                    weight_gen_crs=weight_gen_crs,
                    zonal_engine="parallel",
                    zonal_writer="csv",
                    out_path="/path/to/output",
                    file_prefix="data",
                    append_date=True,
                    jobs=4
                )
        """
        self._user_data = user_data
        self._weight_gen_crs = weight_gen_crs
        self._zonal_engine = zonal_engine
        self._zonal_writer = zonal_writer
        self._jobs = jobs
        self._out_path = Path(out_path)
        if not self._out_path.exists():
            raise FileNotFoundError(f"Path: {self._out_path} does not exist")
        self._file_prefix = file_prefix
        self._append_date = append_date
        if self._append_date:
            self._fdate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            self._fname = f"{self._fdate}_{self._file_prefix}"
        else:
            self._fname = f"{self._file_prefix}"
        self.precision = precision
        self.agg: Union[ZonalEngineSerial, ZonalEngineParallel, ZonalEngineDask]
        if self._zonal_engine == "serial":
            self.agg = ZonalEngineSerial()
        elif self._zonal_engine == "parallel":
            self.agg = ZonalEngineParallel()
        elif self._zonal_engine == "dask":
            self.agg = ZonalEngineDask()
        else:
            raise TypeError(f"agg_engine: {self._zonal_engine} not in {ZONAL_ENGINES}")

    def calculate_weighted_zonal(self, categorical: Optional[bool] = False) -> pd.DataFrame:
        """Calculate weighted zonal statistics.

        This method performs the weighted zonal statistics calculation using the specified engine
        and writes the results to a file if specified.

        Args:
            categorical (bool, optional): If True, calculate categorical zonal statistics (e.g., mode).
                                          If False, calculate continuous zonal statistics (e.g., mean, sum).
                                          Defaults to False.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated weighted zonal statistics.

        Example:
            >>> stats = zonal_gen.calculate_weighted_zonal(categorical=True)
        """
        tstrt = time.perf_counter()
        stats = self.agg.calc_weights_zonal_from_aggdata(
            user_data=self._user_data, crs=self._weight_gen_crs, categorical=categorical, jobs=self._jobs
        )
        if self.precision is not None:
            stats = stats.round(self.precision)
        if self._zonal_writer == "csv":
            fullpath = self._out_path / f"{self._fname}.csv"
            stats.to_csv(fullpath, sep=",")
        tend = time.perf_counter()
        print(f"Total time for serial zonal stats calculation {tend - tstrt:0.4f} seconds")
        return stats
        # elif self._zonal_writer == "feather":
        #     fullpath = self._out_path / f"{self._fname}"
        #     stats.to_feather(path=fullpath, )
