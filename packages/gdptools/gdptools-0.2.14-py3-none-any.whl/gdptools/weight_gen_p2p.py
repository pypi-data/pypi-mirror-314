"""Calculate weights."""

import logging
import os
from typing import Any
from typing import Literal
from typing import Optional
from typing import Union

import geopandas as gpd
import pandas as pd

from gdptools.weights.calc_weight_engines import DaskWghtGenEngine
from gdptools.weights.calc_weight_engines import ParallelWghtGenEngine
from gdptools.weights.calc_weight_engines import SerialWghtGenEngine

logger = logging.getLogger(__name__)

WEIGHT_GEN_METHODS = Literal["serial", "parallel", "dask"]
"""Defines the methods used for weight generation in the `WeightGen` class.

Methods:
    serial: Iterates through each polygon one at a time to calculate weights.
            This method is generally sufficient for small to moderate numbers of polygons.

    parallel: Divides the polygons into chunks and distributes them across available CPU cores.
              This method provides a substantial speedup when dealing with a large number of polygons.

    dask: Utilizes Dask for parallel computing to distribute tasks. Suitable for very large datasets
          and can also be used for distributed computing.

Raises:
    TypeError: Raised if the specified method is not one of the following: "serial", "parallel", "dask".

Returns:
    str: The method used for weight generation.

Examples:
    >>> method = "serial"  # For smaller datasets
    >>> method = "parallel"  # For larger datasets
    >>> method = "dask"  # For very large or distributed datasets
"""


class WeightGenP2P:
    """Class for calculating weights between two sets of polygons represented as GeoDataFrames.

    This class is designed to calculate weights between a target set of polygons and a source set of polygons.
    The weights are calculated based on the fractional area contribution of each source polygon to each target polygon.
    The calculated weights can be saved to a CSV file for future use.

    Attributes:
        target_poly (gpd.GeoDataFrame): GeoDataFrame containing target polygons.
        source_poly (gpd.GeoDataFrame): GeoDataFrame containing source polygons.
        method (str): Method used for weight calculation.
        weight_gen_crs (Any): Coordinate Reference System (CRS) for weight generation.
        output_file (str, optional): Path to the output CSV file.
        jobs (int, optional): Number of processors to use for parallel computation.
        calc_intersections (bool, optional): Whether to calculate intersections.
        verbose (bool, optional): Whether to print additional information during execution.
    """

    def __init__(
        self,
        *,
        target_poly: gpd.GeoDataFrame,
        target_poly_idx: str,
        source_poly: gpd.GeoDataFrame,
        source_poly_idx: str,
        method: WEIGHT_GEN_METHODS,
        weight_gen_crs: Any,
        output_file: Optional[Union[str, None]] = None,
        jobs: Optional[int] = -1,
        intersections: Optional[int] = False,
        verbose: Optional[bool] = False,
    ) -> None:
        """Initialize the WeightGenP2P class.

        Args:
            target_poly (gpd.GeoDataFrame): GeoDataFrame containing target polygons.
                Must include a column with the name specified in `target_poly_idx` and a geometry column.
            target_poly_idx (str): Column name for the target polygon IDs.
            source_poly (gpd.GeoDataFrame): GeoDataFrame containing source polygons.
                Must include a column with the name specified in `source_poly_idx` and a geometry column.
            source_poly_idx (str): Column name for the source polygon IDs.
            method (WEIGHT_GEN_METHODS): Method for weight calculation. Must be one of the values defined in
                `WEIGHT_GEN_METHODS`.
            weight_gen_crs (Any): CRS to be used for weight generation. Accepts any format compatible with
                `pyproj.CRS.from_user_input`.
            output_file (Optional[Union[str, None]], optional): Path to save the output CSV file. If None, no file
                will be saved. Defaults to None.
            jobs (Optional[int], optional): Number of processors to use for parallel computation. Defaults to -1,
                which uses half of the available processors.
            intersections (Optional[bool], optional): Whether to calculate intersections between polygons. Defaults to
                False.
            verbose (Optional[bool], optional): If True, additional runtime information will be printed. Defaults to
                False.

        Raises:
            TypeError: If the `method` argument is not one of the allowed values in `WEIGHT_GEN_METHODS`.

        Examples:
            >>> weight_gen = WeightGenP2P(target_poly=target_gdf, target_poly_idx='target_id',
                                          source_poly=source_gdf, source_poly_idx='source_id',
                                          method='serial', weight_gen_crs='EPSG:4326')
        """
        self.target_poly = target_poly.reset_index()
        self.target_poly_idx = target_poly_idx
        self.target_poly = self.target_poly.sort_values(self.target_poly_idx).dissolve(
            by=self.target_poly_idx, as_index=False
        )
        self.source_poly = source_poly.reset_index()
        self.source_poly_idx = source_poly_idx
        self.method = method
        if output_file is None:
            self.output_file = ""
        else:
            self.output_file = output_file
        self.weight_gen_crs = weight_gen_crs
        self.jobs = jobs
        self.calc_intersections = intersections
        self.verbose = verbose
        self._intersections: gpd.GeoDataFrame
        self.__calc_method: Union[SerialWghtGenEngine, ParallelWghtGenEngine, DaskWghtGenEngine]
        if self.method == "serial":
            self.__calc_method = SerialWghtGenEngine()
            print("Using serial engine")
        elif self.method == "parallel":
            self.__calc_method = ParallelWghtGenEngine()
            print("Using parallel engine")
        elif self.method == "dask":
            self.__calc_method = DaskWghtGenEngine()
        else:
            raise TypeError(f"method: {self.method} not in [serial, parallel]")

        if jobs == -1:
            self.jobs = int(os.cpu_count() / 2)  # type: ignore
            if self.method in ["parallel", "dask"]:
                logger.info(" Getting jobs from os.cpu_count()")
        else:
            self.jobs = jobs
        if self.method in ["parallel", "dask"]:
            logger.info(f"  Parallel or Dask multiprocessing  using {self.jobs} jobs")
        self.verbose = verbose

    def calculate_weights(self) -> pd.DataFrame:
        """Calculate and return the weights DataFrame.

        This method calculates the weights between the target and source polygons based on the method specified during
        initialization. If intersections are to be calculated, they will be stored in the `_intersections` attribute.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated weights between the target and source polygons.
                The DataFrame includes the following columns:
                - target_id: The identifier for each target polygon feature.
                - source_id: The identifier for each source polygon feature.
                - weight: The calculated weight representing the fractional area contribution of the source polygon to
                    the target polygon. If the source polygons are spatially continuous with no overlaps, summing the
                    weights for a given target polygon should result in a value of 1.

        Examples:
            >>> weight_gen = WeightGenP2P(...)
            >>> weights_df = weight_gen.calculate_weights()
        """
        if self.calc_intersections:
            weights, self._intersections = self.__calc_method.calc_weights(
                target_poly=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                source_poly=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type="poly",
                wght_gen_crs=self.weight_gen_crs,
                filename=self.output_file,
                intersections=self.calc_intersections,
                jobs=self.jobs,
                verbose=self.verbose,
            )
        else:
            weights = self.__calc_method.calc_weights(
                target_poly=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                source_poly=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type="poly",
                wght_gen_crs=self.weight_gen_crs,
                filename=self.output_file,
                intersections=self.calc_intersections,
                jobs=self.jobs,
                verbose=self.verbose,
            )

        return weights

    @property
    def intersections(self) -> gpd.GeoDataFrame:
        """Retrieve the calculated intersections as a GeoDataFrame.

        This property returns the intersections calculated during the weight calculation process. If intersections
            have not been calculated, a message will be printed.

        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing the calculated intersections.

        Examples:
            >>> weight_gen = WeightGenP2P(...)
            >>> intersections_gdf = weight_gen.intersections
        """
        if self._intersections is None:
            print("intersections not calculated, " "Run calculate_weights(intersectiosn=True)")
        return self._intersections
