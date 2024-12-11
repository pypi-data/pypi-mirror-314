# sourcery skip: inline-immediately-returned-variable
"""Abstract Base Class for Template behavior pattern for calculating weights."""
import logging
import os
import time
from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import Any
from typing import List
from typing import Literal
from typing import Tuple
from typing import Union

import dask.bag as db
import dask_geopandas as dgpd
import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
from joblib import delayed
from joblib import Parallel
from joblib import parallel_backend
from shapely import area
from shapely import intersection

from gdptools.utils import _check_feature_crs
from gdptools.utils import _check_grid_cell_crs
from gdptools.utils import _check_source_poly_idx
from gdptools.utils import _check_target_poly_idx
from gdptools.utils import _get_crs
from gdptools.utils import _make_valid
from gdptools.utils import _reproject_for_weight_calc

logger = logging.getLogger(__name__)

SOURCE_TYPES = Literal["grid", "poly"]


class CalcWeightEngine(ABC):
    """Abstract Base Class for Weight Calculation Engines.

    This class serves as a template for various weight calculation methods. It defines a common workflow for weight
    calculation, encapsulated in the `calc_weights()` method. The actual weight calculation logic is defined in the
    abstract method `get_weight_components()`.

    The class is designed to handle both grid-to-polygon and polygon-to-polygon weight calculations. It produces a table
    that describes the area intersections between each source and target polygon, which can be used for area-weighted
    interpolation.

    Note:
        This class is generally not used directly but through subclasses controlled by either the `WeightGen` class for
        grid-to-polygon calculations or the `WeightGenP2P` class for polygon-to-polygon calculations.

    Attributes:
        target_poly (gpd.GeoDataFrame): The GeoDataFrame containing the target polygons.
        target_poly_idx (str): The column name in `target_poly` serving as a unique identifier for each target polygon.
        source_poly (gpd.GeoDataFrame): The GeoDataFrame containing the source polygons.
        source_poly_idx (List[str]): The list of column names in `source_poly` serving as unique identifiers for each
            source polygon.
        source_type (str): The type of the source polygons, which may indicate their use or attributes.
        wght_gen_crs (Any): The coordinate reference system used for weight generation.
        filename (str): Optional filename to which the weight DataFrame will be saved.
        intersections (bool): Flag indicating whether to calculate intersections between target and source polygons.
        jobs (int): Number of parallel jobs to run for weight calculation.
        verbose (bool): Flag for verbose output during execution.
        plist (List[object]): List of target polygon IDs (populated during weight calculation).
        ilist (List[int]): List of i-indices for grid cells (populated during weight calculation, applicable when
            source_type is "grid").
        jlist (List[int]): List of j-indices for grid cells (populated during weight calculation, applicable when
            source_type is "grid").
        wghtlist (List[float]): List of calculated weights (populated during weight calculation).
        splist (List[object]): List of source polygon IDs (populated during weight calculation, applicable when
            source_type is "poly").
        wght_df (pd.DataFrame): DataFrame storing the final calculated weights.
        _intersections (gpd.GeoDataFrame, optional): GeoDataFrame storing calculated intersections (if applicable).
    """

    def calc_weights(
        self,
        target_poly: gpd.GeoDataFrame,
        target_poly_idx: str,
        source_poly: gpd.GeoDataFrame,
        source_poly_idx: List[str],
        source_type: SOURCE_TYPES,
        wght_gen_crs: Any,
        filename: str = "",
        intersections: bool = False,
        jobs: int = -1,
        verbose: bool = False,
    ) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Calculate weights between target and source polygons.

        This is the template method that orchestrates the weight calculation process. It prepares the data, invokes the
        weight calculation logic, and optionally saves the results to a file.

        Args:
            target_poly (gpd.GeoDataFrame): The GeoDataFrame that holds the target polygons.
                These are the polygons for which the weights will be calculated.
            target_poly_idx (str): The name of the column in `target_poly` that contains unique
                identifiers for each target polygon. This is used to tag the resulting weights file.
            source_poly (gpd.GeoDataFrame): The GeoDataFrame that holds the source polygons.
                These polygons are used to calculate the weights for each target polygon.
            source_poly_idx (List[str]): A list of column names in `source_poly` that contain
                unique identifiers for each source polygon. These identifiers are used in the
                resulting weights file.
            source_type (SOURCE_TYPES): An enumeration indicating the type of the source polygons.
                This provides context on how the source polygons are used or what attributes they have.
            wght_gen_crs (Any): The coordinate reference system (CRS) to use for weight generation.
                This should be any format that is compatible with pyproj.CRS.from_user_input.
            filename (str): The path where the resulting weights DataFrame will be saved as a CSV file.
                If not provided, the DataFrame will not be saved. Defaults to an empty string.
            intersections (bool): A flag indicating whether to calculate and store the intersections
                between the target and source polygons. If set to True, intersections will be calculated.
                Defaults to False.
            jobs (int): The number of parallel jobs to run for weight calculation.
                If set to -1, the algorithm will use half of the available CPU cores. Defaults to -1.
            verbose (bool): A flag for verbose logging. If set to True, additional details
                will be printed during the execution of the algorithm. Defaults to False.

        Returns:
            Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]: A DataFrame containing the calculated weights
            between target and source polygons. If intersections are calculated, a GeoDataFrame containing those
            intersections is also returned.
        """
        # Buffer polygons with self-intersections
        tstrt = time.perf_counter()
        print("     - validating target polygons")
        target_poly = _make_valid(target_poly)
        print("     - validating source polygons")
        source_poly = _make_valid(source_poly)
        tend = time.perf_counter()
        print(f"Validate polygons finished in {tend - tstrt:0.4f} seconds")

        self.target_poly = target_poly.reset_index()
        self.target_poly_idx = target_poly_idx

        self.source_poly = source_poly.reset_index()
        self.source_poly_idx = source_poly_idx

        self.source_type = source_type
        self.wght_gen_crs = wght_gen_crs
        self.filename = filename
        self.intersections = intersections

        if jobs == -1:
            self.jobs = int(os.cpu_count() / 2)  # type: ignore
            logger.info(" ParallelWghtGenEngine getting jobs from os.cpu_count()")
        else:
            self.jobs = jobs
        logger.info(f"  ParallelWghtGenEngine using {self.jobs} jobs")
        self.verbose = verbose
        _check_target_poly_idx(self.target_poly, self.target_poly_idx)
        _check_source_poly_idx(self.source_poly, self.source_poly_idx)
        _check_feature_crs(poly=self.target_poly)
        _check_grid_cell_crs(grid_cells=self.source_poly)
        self.grid_out_crs = _get_crs(self.wght_gen_crs)
        self.target_poly, self.source_poly = _reproject_for_weight_calc(
            target_poly=self.target_poly,
            source_poly=self.source_poly,
            wght_gen_crs=self.grid_out_crs,
        )
        if self.intersections:
            print(f"Intersections = {self.intersections}")
            if self.source_type == "grid":
                (
                    self.plist,
                    self.ilist,
                    self.jlist,
                    self.wghtlist,
                    self.calc_intersect,
                ) = self.get_weight_components_and_intesections()
            elif self.source_type == "poly":
                (
                    self.plist,
                    self.splist,
                    self.wghtlist,
                    self.calc_intersect,
                ) = self.get_weight_components_and_intesections()
        elif self.source_type == "grid":
            (
                self.plist,
                self.ilist,
                self.jlist,
                self.wghtlist,
            ) = self.get_weight_components()
        elif self.source_type == "poly":
            (
                self.plist,
                self.splist,
                self.wghtlist,
            ) = self.get_weight_components()
        self.wght_df = self.create_wght_df()
        if self.filename:
            self.wght_df.to_csv(self.filename, index=False)
        if self.intersections:
            return self.wght_df, self.calc_intersect
        else:
            return self.wght_df
        # return (  # type: ignore
        #     self.wght_df, self.calc_intersect
        #     if self.intersections
        #     else self.wght_df
        # )

    @abstractmethod
    def get_weight_components(
        self,
    ) -> Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object], List[float]]]:
        """Abstract method for weight component calculation.

        This method must be implemented by subclasses to provide the actual weight calculation logic.

        Returns:
            Union[Tuple[...], Tuple[...]]: Depending on the source type, returns a tuple containing lists of target IDs,
            source IDs, and calculated weights.
        """
        pass

    @abstractmethod
    def get_weight_components_and_intesections(
        self,
    ) -> Union[
        Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame],
        Tuple[List[object], List[object], List[float], gpd.GeoDataFrame],
    ]:
        """Abstract method for weight and intersection calculation.

        This method must be implemented by subclasses to provide the actual weight and intersection calculation logic.

        Returns:
            Union[Tuple[...], Tuple[...]]: Depending on the source type, returns a tuple containing lists of target IDs,
            source IDs, calculated weights, and a GeoDataFrame of intersections.
        """
        pass

    def create_wght_df(self) -> pd.DataFrame:
        """Create and return a DataFrame from calculated weight components.

        This method constructs a DataFrame from the calculated weight components, which can be used for further
        analysis or saved to disk.

        Returns:
            pd.DataFrame: A DataFrame containing target IDs, source IDs, and their calculated weights.
        """
        if self.source_type == "grid":
            wght_df = pd.DataFrame(
                {
                    self.target_poly_idx: self.plist,
                    "i": self.ilist,
                    "j": self.jlist,
                    "wght": self.wghtlist,
                }
            )
            wght_df = wght_df.astype({"i": int, "j": int, "wght": float, self.target_poly_idx: str})
        elif self.source_type == "poly":
            wght_df = pd.DataFrame(
                {
                    self.target_poly_idx: self.plist,
                    self.source_poly_idx[0]: self.splist,
                    "wght": self.wghtlist,
                }
            )
            wght_df = wght_df.astype({"wght": float, self.target_poly_idx: str, self.source_poly_idx[0]: str})
        return wght_df


class SerialWghtGenEngine(CalcWeightEngine):
    """Generate grid-to-polygon weight using area tables binning method.

    This class is an implementation of the CalcWeightEngine Abstract Base Class (ABC).
    It is based on and adapted from methods provided in the Tobler package, specifically
    the `area_tables_binning()` method.

    Attributes:
        CalcWeightEngine (ABC): Abstract Base Class employing the Template behavior
            pattern. The abstract method `get_weight_components` provides a method to plug-
            in new weight generation methods.

    """

    def get_weight_components(
        self,
    ) -> Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object], List[float]]]:
        """Generate weight components based on source type.

        This method overrides the template method from the CalcWeightEngine class.
        It generates weight components based on the `source_type` attribute.

        Returns:
            Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object],
                List[float]]]:
                - If `source_type` is "grid", returns a tuple containing:
                    1. List of target polygon IDs.
                    2. List of i-indices of grid cells.
                    3. List of j-indices of grid cells.
                    4. List of weight values for each i,j index of grid cells.
                - If `source_type` is "poly", returns a tuple containing:
                    1. List of target polygon IDs.
                    2. List of source polygon IDs.
                    3. List of weight values for source polygons.

        """
        tsrt = time.perf_counter()
        if self.source_type == "grid":
            (
                plist,
                ilist,
                jlist,
                wghtslist,
            ) = self.area_tables_binning(
                source_df=self.source_poly,
                target_df=self.target_poly,
                source_type=self.source_type,
            )
        elif self.source_type == "poly":
            (
                plist,
                splist,
                wghtslist,
            ) = self.area_tables_binning(
                source_df=self.source_poly,
                target_df=self.target_poly,
                source_type=self.source_type,
            )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend - tsrt:0.4f} seconds")
        if self.source_type == "grid":
            return plist, ilist, jlist, wghtslist
        elif self.source_type == "poly":
            return plist, splist, wghtslist

    def get_weight_components_and_intesections(
        self,
    ) -> Union[
        Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame],
        Tuple[List[object], List[object], List[float], gpd.GeoDataFrame],
    ]:
        """Generate weight components and intersection geometries based on source type.

        This method overrides the template method from the CalcWeightEngine class.
        It generates weight components and intersection geometries based on the `source_type` attribute.

        Returns:
            Union[Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame], Tuple[List[object],
                List[object], List[float], gpd.GeoDataFrame]]:
                - If `source_type` is "grid", returns a tuple containing:
                    1. List of target polygon IDs.
                    2. List of i-indices of grid cells.
                    3. List of j-indices of grid cells.
                    4. List of weight values for each i,j index of grid cells.
                    5. GeoDataFrame of intersection geometries.
                - If `source_type` is "poly", returns a tuple containing:
                    1. List of target polygon IDs.
                    2. List of source polygon IDs.
                    3. List of weight values for source polygons.
                    4. GeoDataFrame of intersection geometries.

        """
        tsrt = time.perf_counter()
        if self.source_type == "grid":
            (
                plist,
                ilist,
                jlist,
                wghtslist,
                gdf,
            ) = self.area_tables_binning_and_intersections(
                source_df=self.source_poly,
                target_df=self.target_poly,
                source_type=self.source_type,
            )
        elif self.source_type == "poly":
            (
                plist,
                splist,
                wghtslist,
                gdf,
            ) = self.area_tables_binning_and_intersections(
                source_df=self.source_poly,
                target_df=self.target_poly,
                source_type=self.source_type,
            )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend - tsrt:0.4f} seconds")
        if self.source_type == "grid":
            return plist, ilist, jlist, wghtslist, gdf
        elif self.source_type == "poly":
            return plist, splist, wghtslist, gdf

    def area_tables_binning(
        self: "SerialWghtGenEngine",
        source_df: gpd.GeoDataFrame,
        target_df: gpd.GeoDataFrame,
        source_type: SOURCE_TYPES,
    ) -> Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object], List[float]]]:
        """Generate area allocation and source-target correspondence tables.

        This method constructs area allocation and source-target correspondence tables
        using a parallel spatial indexing approach. It is based on and adapted from the Tobler package.

        Args:
            source_df (gpd.GeoDataFrame): GeoDataFrame containing the source polygons.
            target_df (gpd.GeoDataFrame): GeoDataFrame containing the target polygons.
            source_type (SOURCE_TYPES): Type of the source geometry, either "grid" or "poly".

        Returns:
            Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object],
                List[float]]]:
                - If `source_type` is "grid", returns a tuple containing:
                    1. List of target polygon IDs.
                    2. List of i-indices of grid cells.
                    3. List of j-indices of grid cells.
                    4. List of weight values for each i,j index of grid cells.
                - If `source_type` is "poly", returns a tuple containing:
                    1. List of target polygon IDs.
                    2. List of source polygon IDs.
                    3. List of weight values for source polygons.

        """
        tstrt = time.perf_counter()
        ids_tgt, ids_src = source_df.sindex.query(target_df.geometry, predicate="intersects")

        areas = (
            source_df.geometry.values[ids_src].intersection(target_df.geometry.values[ids_tgt]).area
            / target_df.geometry.values[ids_tgt].area
        )
        tend = time.perf_counter()
        print(f"Intersections finished in {tend - tstrt:0.4f} seconds")

        if source_type == "grid":
            return (
                target_df[self.target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
                source_df.i_index.iloc[ids_src].values.astype(int).tolist(),
                source_df.j_index.iloc[ids_src].values.astype(int).tolist(),
                areas.astype(float).tolist(),
            )
        else:
            return (
                target_df[self.target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
                source_df[self.source_poly_idx[0]].iloc[ids_src].values.astype(object).tolist(),
                areas.astype(float).tolist(),
            )

    def area_tables_binning_and_intersections(
        self: "SerialWghtGenEngine",
        source_df: gpd.GeoDataFrame,
        target_df: gpd.GeoDataFrame,
        source_type: SOURCE_TYPES,
    ) -> Union[
        Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame],
        Tuple[List[object], List[object], List[float], gpd.GeoDataFrame],
    ]:
        """Generate area allocation, source-target correspondence tables, and intersection geometries.

        This method constructs area allocation and source-target correspondence tables
        as well as intersection geometries using a parallel spatial indexing approach.
        It is based on and adapted from the Tobler package.

        Args:
            source_df (gpd.GeoDataFrame): GeoDataFrame containing the source polygons.
            target_df (gpd.GeoDataFrame): GeoDataFrame containing the target polygons.
            source_type (SOURCE_TYPES): Type of the source geometry, either "grid" or "poly".

        Returns:
            Union[Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame], Tuple[List[object],
                List[object], List[float], gpd.GeoDataFrame]]:
                - If `source_type` is "grid", returns a tuple containing:
                    1. List of target polygon IDs.
                    2. List of i-indices of grid cells.
                    3. List of j-indices of grid cells.
                    4. List of weight values for each i,j index of grid cells.
                    5. GeoDataFrame of intersection geometries.
                - If `source_type` is "poly", returns a tuple containing:
                    1. List of target polygon IDs.
                    2. List of source polygon IDs.
                    3. List of weight values for source polygons.
                    4. GeoDataFrame of intersection geometries.

        """
        tstrt = time.perf_counter()
        ids_tgt, ids_src = source_df.sindex.query(target_df.geometry, predicate="intersects")
        f_intersect = source_df.geometry.values[ids_src].intersection(target_df.geometry.values[ids_tgt])
        weights = f_intersect.area / target_df.geometry.values[ids_tgt].area
        gdf_inter = target_df.iloc[ids_tgt]
        # gdf_inter.set_geometry(f_intersect, inplace=True)
        gdf_inter = gdf_inter.iloc[:].set_geometry(f_intersect)
        gdf_inter["weights"] = weights.astype(float)
        tend = time.perf_counter()
        print(f"Intersections finished in {tend - tstrt:0.4f} seconds")

        if source_type == "grid":
            return (
                target_df[self.target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
                source_df.i_index.iloc[ids_src].values.astype(int).tolist(),
                source_df.j_index.iloc[ids_src].values.astype(int).tolist(),
                weights.astype(float).tolist(),
                gdf_inter,
            )
        elif source_type == "poly":
            return (
                target_df[self.target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
                source_df[self.source_poly_idx[0]].iloc[ids_src].values.astype(object).tolist(),
                weights.astype(float).tolist(),
                gdf_inter,
            )


class ParallelWghtGenEngine(CalcWeightEngine):
    """Generates spatial weighting matrices using parallel processing.

    This class is an extension of the CalcWeightEngine Abstract Base Class (ABC) and
    utilizes parallel processing to generate grid-to-polygon or polygon-to-polygon
    weighting matrices. The implementation is adapted from methods in the Tobler package.

    Args:
        CalcWeightEngine (ABC): An abstract base class that defines the template method
            for generating weight components. Subclasses should implement the
            `get_weight_components` method to provide custom weight generation logic.
    """

    def get_weight_components(
        self,
    ) -> Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object], List[float]]]:
        """Generates weight components based on the source and target geometries.

        Returns:
            Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object],
                List[float]]]:
                - If `self.source_type` is "grid", the returned tuple contains:
                    1. List of target polygon IDs.
                    2. i-indices of grid cells.
                    3. j-indices of grid cells.
                    4. Weight values corresponding to each grid cell.

                - If `self.source_type` is "poly", the returned tuple contains:
                    1. List of target polygon IDs.
                    2. List of source polygon IDs.
                    3. Weight values corresponding to each source polygon.
        """
        tsrt = time.perf_counter()
        if self.source_type == "grid":
            plist, ilist, jlist, wghtslist = _area_tables_binning_parallel(
                source_df=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type=self.source_type,
                target_df=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                n_jobs=self.jobs,
            )
        elif self.source_type == "poly":
            plist, splist, wghtslist = _area_tables_binning_parallel(
                source_df=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type=self.source_type,
                target_df=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                n_jobs=self.jobs,
            )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend - tsrt:0.4f} seconds")
        if self.source_type == "grid":
            return plist, ilist, jlist, wghtslist
        elif self.source_type == "poly":
            return plist, splist, wghtslist

    def get_weight_components_and_intesections(
        self,
    ) -> Union[
        Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame],
        Tuple[List[object], list[object], List[float], gpd.GeoDataFrame],
    ]:
        """Generates weight components and their corresponding intersection geometries.

        Returns:
            Union[Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame], Tuple[List[object],
                List[object], List[float], gpd.GeoDataFrame]]:
                - If `self.source_type` is "grid", the returned tuple contains:
                    1. List of target polygon IDs.
                    2. i-indices of grid cells.
                    3. j-indices of grid cells.
                    4. Weight values corresponding to each grid cell.
                    5. GeoDataFrame containing the intersection geometries.

                - If `self.source_type` is "poly", the returned tuple contains:
                    1. List of target polygon IDs.
                    2. List of source polygon IDs.
                    3. Weight values corresponding to each source polygon.
                    4. GeoDataFrame containing the intersection geometries.
        """
        tsrt = time.perf_counter()
        if self.source_type == "grid":
            (
                plist,
                ilist,
                jlist,
                wghtslist,
                gdf,
            ) = _area_tables_binning_parallel_and_intersections(
                source_df=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type=self.source_type,
                target_df=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                n_jobs=self.jobs,
            )
        elif self.source_type == "poly":
            (
                plist,
                splist,
                wghtslist,
                gdf,
            ) = _area_tables_binning_parallel_and_intersections(
                source_df=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type=self.source_type,
                target_df=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                n_jobs=self.jobs,
            )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend - tsrt:0.4f} seconds")

        if self.source_type == "grid":
            return plist, ilist, jlist, wghtslist, gdf
        elif self.source_type == "poly":
            return plist, splist, wghtslist, gdf


def _area_tables_binning_parallel_and_intersections(
    source_df: gpd.GeoDataFrame,
    source_poly_idx: str,
    source_type: SOURCE_TYPES,
    target_df: gpd.GeoDataFrame,
    target_poly_idx: str,
    n_jobs: int = -1,
) -> Union[
    Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame],
    Tuple[List[object], List[object], List[float], gpd.GeoDataFrame],
]:
    """Computes spatial intersections and area tables in parallel.

    This function performs spatial intersections and calculates area tables using parallel
    processing. It is adapted from methods in the Tobler package.

    Args:
        source_df (gpd.GeoDataFrame): GeoDataFrame containing the source polygons.
        source_poly_idx (str): Column name for unique IDs of source polygons.
        source_type (SOURCE_TYPES): Type of the source geometry, either "grid" or "poly".
        target_df (gpd.GeoDataFrame): GeoDataFrame containing the target polygons.
        target_poly_idx (str): Column name for unique IDs of target polygons.
        n_jobs (int): Number of parallel jobs. Defaults to -1, which uses all available CPUs.

    Returns:
        Union[Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame], Tuple[List[object],
            List[object], List[float], gpd.GeoDataFrame]]:
            - If `source_type` is "grid", the tuple contains:
                1. List of target polygon IDs.
                2. i-indices of grid cells.
                3. j-indices of grid cells.
                4. Weight values for each grid cell.
                5. GeoDataFrame of intersection geometries.

            - If `source_type` is "poly", the tuple contains:
                1. List of target polygon IDs.
                2. List of source polygon IDs.
                3. Weight values for each source polygon.
                4. GeoDataFrame of intersection geometries.
    """
    if n_jobs == -1:
        n_jobs = int(os.cpu_count() / 2)  # type: ignore
        logger.info(" ParallelWghtGenEngine getting jobs from os.cpu_count()")
    logger.info(f"  ParallelWghtGenEngine using {n_jobs} jobs")

    # Chunk the largest, ship the smallest in full
    to_chunk, df_full = _get_chunks_for_parallel(source_df, target_df)

    # Spatial index query: Reindex on positional IDs
    to_workers = _chunk_dfs(
        gpd.GeoSeries(to_chunk.geometry.values, crs=to_chunk.crs),
        gpd.GeoSeries(df_full.geometry.values, crs=df_full.crs),
        n_jobs,
    )

    worker_out = _get_ids_for_parallel(n_jobs, to_workers)
    ids_src, ids_tgt = np.concatenate(worker_out).T

    # Intersection + area calculation
    chunks_to_intersection = _chunk_polys(
        np.vstack([ids_src, ids_tgt]).T, source_df.geometry, target_df.geometry, n_jobs
    )
    worker_out = _get_areas_and_intersections_for_parallel(n_jobs, chunks_to_intersection)
    areas = np.concatenate([item[0] for item in worker_out])
    inter_geom = np.concatenate([item[1] for item in worker_out])

    print("Processing intersections for output.")
    inter_sect = target_df.iloc[ids_tgt, :].set_geometry(inter_geom)
    weights = areas.astype(float) / target_df.geometry[ids_tgt].area
    inter_sect["weights"] = weights

    if source_type == "grid":
        return (
            target_df[target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            source_df.i_index.iloc[ids_src].values.astype(int).tolist(),
            source_df.j_index.iloc[ids_src].values.astype(int).tolist(),
            weights.tolist(),
            inter_sect,
        )
    elif source_type == "poly":
        return (
            target_df[target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            source_df[source_poly_idx[0]].iloc[ids_src].values.astype(object).tolist(),
            weights.tolist(),
            inter_sect,
        )


def _get_areas_and_intersections_for_parallel(
    n_jobs: int,
    chunks_to_intersection: Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any],
) -> Any:
    """Get poly-to-poly intersections."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(
            delayed(_intersect_area_on_chunk)(*chunk_pair) for chunk_pair in chunks_to_intersection
        )
    return worker_out


def _get_areas_for_parallel(
    n_jobs: int,
    chunks_to_intersection: Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any],
) -> Any:
    """Get poly-to-poly intersections."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(
            delayed(_area_on_chunk)(*chunk_pair) for chunk_pair in chunks_to_intersection
        )
    return worker_out


def _get_ids_for_parallel(n_jobs: int, to_workers: Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]) -> Any:
    """Get poly-to-poly intersection ids."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(delayed(_index_n_query)(*chunk_pair) for chunk_pair in to_workers)
    return worker_out


def _get_chunks_for_parallel(df1: gpd.GeoDataFrame, df2: gpd.GeoDataFrame) -> Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Chunk dataframes."""
    to_chunk = df1
    df_full = df2
    return to_chunk, df_full


def _area_tables_binning_parallel(
    source_df: gpd.GeoDataFrame,
    source_poly_idx: str,
    source_type: SOURCE_TYPES,
    target_df: gpd.GeoDataFrame,
    target_poly_idx: str,
    n_jobs: int = -1,
) -> Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object], List[float]]]:
    """Calculates spatial intersections and area tables using parallel processing.

    This function performs spatial intersections and computes area tables in parallel.
    It is adapted from methods in the Tobler package. For licensing details, refer to Tobler's BSD 3-Clause License.

    Args:
        source_df (gpd.GeoDataFrame): GeoDataFrame containing the source polygons.
        source_poly_idx (str): Column name for unique IDs of source polygons.
        source_type (SOURCE_TYPES): Enum specifying the type of source geometry, either "grid" or "poly".
        target_df (gpd.GeoDataFrame): GeoDataFrame containing the target polygons.
        target_poly_idx (str): Column name for unique IDs of target polygons.
        n_jobs (int): Number of parallel jobs. Defaults to -1, which uses all available CPUs.

    Returns:
        Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object], List[float]]]:
            - If `source_type` is "grid", the tuple contains:
                1. List of target polygon IDs.
                2. i-indices of grid cells.
                3. j-indices of grid cells.
                4. Weight values for each grid cell.

            - If `source_type` is "poly", the tuple contains:
                1. List of target polygon IDs.
                2. List of source polygon IDs.
                3. Weight values for each source polygon.

    Notes:
        - The function uses half of the available CPUs if `n_jobs` is set to -1.
        - Polygons with self-intersections are automatically validated.
        - The function performs spatial indexing, chunking, and area calculations as part of its workflow.
    """
    if n_jobs == -1:
        n_jobs = int(os.cpu_count() / 2)  # type: ignore
        logger.info(" ParallelWghtGenEngine getting jobs from os.cpu_count()")
    logger.info(f"  ParallelWghtGenEngine using {n_jobs} jobs")

    # Chunk the largest, ship the smallest in full
    to_chunk, df_full = _get_chunks_for_parallel(source_df, target_df)

    # Spatial index query: Reindex on positional IDs
    to_workers = _chunk_dfs(
        gpd.GeoSeries(to_chunk.geometry.values, crs=to_chunk.crs),
        gpd.GeoSeries(df_full.geometry.values, crs=df_full.crs),
        n_jobs,
    )

    worker_out = _get_ids_for_parallel(n_jobs, to_workers)
    ids_src, ids_tgt = np.concatenate(worker_out).T

    # Intersection + area calculation
    chunks_to_intersection = _chunk_polys(
        np.vstack([ids_src, ids_tgt]).T, source_df.geometry, target_df.geometry, n_jobs
    )
    worker_out = _get_areas_for_parallel(n_jobs, chunks_to_intersection)
    areas = np.concatenate(worker_out)

    if source_type == "grid":
        return (
            target_df[target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            source_df.i_index.iloc[ids_src].values.astype(int).tolist(),
            source_df.j_index.iloc[ids_src].values.astype(int).tolist(),
            (areas.astype(float) / target_df.geometry[ids_tgt].area).tolist(),
        )
    elif source_type == "poly":
        return (
            target_df[target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            source_df[source_poly_idx[0]].iloc[ids_src].values.astype(object).tolist(),
            (areas.astype(float) / target_df.geometry[ids_tgt].area).tolist(),
        )


class DaskWghtGenEngine(CalcWeightEngine):
    """Class for generating grid-to-polygon weights using Dask for parallelization.

    This class is an extension of the CalcWeightEngine Abstract Base Class (ABC) and
    implements the Template Method pattern. It is inspired by methods available in the
    Tobler package, specifically the `area_tables_bining_parallel()` method.

    Args:
        CalcWeightEngine (ABC): The parent class that defines the template methods and
            provides a framework for weight generation algorithms.
    """

    def get_weight_components(
        self,
    ) -> Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object], List[float]]]:
        """Generate weight components based on source and target geometries.

        This method overrides the template method from the CalcWeightEngine class.

        Returns:
            Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object],
                List[float]]]:
            - For "grid" source_type, the tuple contains:
                1. Target polygon IDs.
                2. i-indices of grid cells.
                3. j-indices of grid cells.
                4. Weight values for each grid cell.

            - For "poly" source_type, the tuple contains:
                1. Target polygon IDs.
                2. Source polygon IDs.
                3. Weight values for each source polygon.
        """
        tsrt = time.perf_counter()
        if self.source_type == "grid":
            plist, ilist, jlist, wghtslist = _area_tables_binning_for_dask(
                source_df=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type=self.source_type,
                target_df=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                n_jobs=self.jobs,
            )
        elif self.source_type == "poly":
            plist, splist, wghtslist = _area_tables_binning_for_dask(
                source_df=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type=self.source_type,
                target_df=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                n_jobs=self.jobs,
            )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend - tsrt:0.4f} seconds")

        if self.source_type == "grid":
            return plist, ilist, jlist, wghtslist
        elif self.source_type == "poly":
            return plist, splist, wghtslist

    def get_weight_components_and_intesections(
        self,
    ) -> Union[
        Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame],
        Tuple[List[object], List[object], List[float], gpd.GeoDataFrame],
    ]:
        """Generate weight components along with their intersection geometries.

        This method extends the functionality of `get_weight_components` by also returning
        the GeoDataFrame of intersection geometries.

        Returns:
            Union[Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame], Tuple[List[object],
                List[object], List[float], gpd.GeoDataFrame]]:
            - For "grid" source_type, the tuple contains:
                1. Target polygon IDs.
                2. i-indices of grid cells.
                3. j-indices of grid cells.
                4. Weight values for each grid cell.
                5. GeoDataFrame of intersection geometries.

            - For "poly" source_type, the tuple contains:
                1. Target polygon IDs.
                2. Source polygon IDs.
                3. Weight values for each source polygon.
                4. GeoDataFrame of intersection geometries.
        """
        tsrt = time.perf_counter()
        if self.source_type == "grid":
            (
                plist,
                ilist,
                jlist,
                wghtslist,
                gdf,
            ) = _area_tables_binning_and_intersections_for_dask(
                source_df=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type=self.source_type,
                target_df=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                n_jobs=self.jobs,
            )
        elif self.source_type == "poly":
            (
                plist,
                splist,
                wghtslist,
                gdf,
            ) = _area_tables_binning_and_intersections_for_dask(
                source_df=self.source_poly,
                source_poly_idx=self.source_poly_idx,
                source_type=self.source_type,
                target_df=self.target_poly,
                target_poly_idx=self.target_poly_idx,
                n_jobs=self.jobs,
            )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend - tsrt:0.4f} seconds")

        if self.source_type == "grid":
            return plist, ilist, jlist, wghtslist, gdf
        elif self.source_type == "poly":
            return plist, splist, wghtslist, gdf


def _area_tables_binning_and_intersections_for_dask(
    source_df: gpd.GeoDataFrame,
    source_poly_idx: str,
    source_type: SOURCE_TYPES,
    target_df: gpd.GeoDataFrame,
    target_poly_idx: str,
    n_jobs: int = -1,
) -> Union[
    Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame],
    Tuple[List[object], List[object], List[float], gpd.GeoDataFrame],
]:
    """Calculate intersection tables and weights using Dask for parallelization.

    This function is adapted from the Tobler package and employs a parallel spatial
    indexing approach to calculate intersections and weights between source and target
    polygons.

    Args:
        source_df (gpd.GeoDataFrame): GeoDataFrame containing the source polygons and data.
        source_poly_idx (str): Column name for the unique ID of source polygons.
        source_type (SOURCE_TYPES): Type of source data, either "grid" or "poly".
        target_df (gpd.GeoDataFrame): GeoDataFrame containing the target polygons.
        target_poly_idx (str): Column name for the unique ID of target polygons.
        n_jobs (int): Number of processes for parallel execution.
                                If -1, raises a ValueError. Default is -1.

    Returns:
        Union[Tuple, Tuple]:
            - If source_type is "grid", returns a tuple containing:
                1. List of target polygon IDs.
                2. i-indices of grid cells.
                3. j-indices of grid cells.
                4. Weight values for each grid cell.
                5. GeoDataFrame of intersection geometries.

            - If source_type is "poly", returns a tuple containing:
                1. List of target polygon IDs.
                2. List of source polygon IDs.
                3. Weight values for each source polygon.
                4. GeoDataFrame of intersection geometries.

    Raises:
        ValueError: If n_jobs is set to -1. Dask requires the number of jobs to be explicitly set.

    Note:
        For licensing details, please refer to Tobler's BSD 3-Clause License.
    """
    if n_jobs == -1:
        raise ValueError(" ")

    # Chunk the largest, ship the smallest in full
    sdf, tdf = _get_chunks_for_dask(n_jobs, source_df, target_df)
    sdf.calculate_spatial_partitions()

    id_chunks = _ids_for_dask_generator(sdf=sdf, tdf=tdf)
    worker_out = _get_ids_for_dask(id_chunks)
    ids_src, ids_tgt = np.concatenate(worker_out).T

    # Intersection + area calculation
    chunks_to_intersection = _chunk_polys_dask(
        np.vstack([ids_src, ids_tgt]).T, source_df.geometry, target_df.geometry, n_jobs
    )

    worker_out = _get_areas_and_intersections_for_dask(n_jobs, chunks_to_intersection)
    areas = np.concatenate([item[0] for item in worker_out])
    inter_geom = np.concatenate([item[1] for item in worker_out])

    print("Processing intersections for output.")
    inter_sect = target_df.iloc[ids_tgt, :].set_geometry(inter_geom)
    weights = areas.astype(float) / target_df.geometry[ids_tgt].area
    inter_sect["weights"] = weights

    if source_type == "grid":
        return (
            target_df[target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            source_df.i_index.iloc[ids_src].values.astype(int).tolist(),
            source_df.j_index.iloc[ids_src].values.astype(int).tolist(),
            weights.tolist(),
            inter_sect,
        )
    elif source_type == "poly":
        return (
            target_df[target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            source_df[source_poly_idx[0]].iloc[ids_src].values.astype(object).tolist(),
            weights.tolist(),
            inter_sect,
        )


def _ids_for_dask_generator(
    sdf: dgpd.GeoDataFrame, tdf: dgpd.GeoDataFrame
) -> Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]:
    for part in tdf.partitions:
        target_chunk = part.compute()
        bnds = target_chunk.total_bounds
        source_chunk = sdf.cx[bnds[0] : bnds[1], bnds[2] : bnds[3]].compute()
        yield (
            gpd.GeoSeries(
                source_chunk.geometry.values,
                index=source_chunk.index,
                crs=source_chunk.crs,
            ),
            gpd.GeoSeries(
                target_chunk.geometry.values,
                index=target_chunk.index,
                crs=target_chunk.crs,
            ),
        )


def _get_areas_and_intersections_for_dask(
    jobs: int,
    chunks_to_intersection: Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any],
) -> Any:
    """Get poly-to-poly intersections."""
    b = db.from_sequence(chunks_to_intersection, npartitions=jobs)  # type: ignore
    b = b.map(_intersect_area_on_chunk_dask)
    return b.compute()


def _get_areas_for_dask(
    jobs: int,
    chunks_to_intersection: Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any],
) -> Any:
    """Get poly-to-poly intersections."""
    b = db.from_sequence(chunks_to_intersection, npartitions=jobs)  # type: ignore
    b = b.map(_area_on_chunk_dask)
    return b.compute()


def _get_ids_for_dask(to_workers: Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]) -> Any:
    """Get poly-to-poly intersection ids."""
    b = db.from_sequence(to_workers)  # type: ignore
    result = b.map(_index_n_query_dask)
    return result.compute()


def _area_tables_binning_for_dask(
    source_df: gpd.GeoDataFrame,
    source_poly_idx: str,
    source_type: SOURCE_TYPES,
    target_df: gpd.GeoDataFrame,
    target_poly_idx: str,
    n_jobs: int = -1,
) -> Union[Tuple[List[object], List[int], List[int], List[float]], Tuple[List[object], List[object], List[float]]]:
    """Calculate intersection tables and weights using Dask for parallelization.

    This function is adapted from the Tobler package and employs a parallel spatial
    indexing approach to calculate intersections and weights between source and target
    polygons.

    Args:
        source_df (gpd.GeoDataFrame): GeoDataFrame containing the source polygons and data.
        source_poly_idx (str): Column name for the unique ID of source polygons.
        source_type (SOURCE_TYPES): Type of source data, either "grid" or "poly".
        target_df (gpd.GeoDataFrame): GeoDataFrame containing the target polygons.
        target_poly_idx (str): Column name for the unique ID of target polygons.
        n_jobs (int): Number of processes for parallel execution.
                                If -1, raises a ValueError. Default is -1.

    Returns:
        Union[Tuple, Tuple]:
            - If source_type is "grid", returns a tuple containing:
                1. List of target polygon IDs.
                2. i-indices of grid cells.
                3. j-indices of grid cells.
                4. Weight values for each grid cell.

            - If source_type is "poly", returns a tuple containing:
                1. List of target polygon IDs.
                2. List of source polygon IDs.
                3. Weight values for each source polygon.

    Raises:
        ValueError: If n_jobs is set to -1. Dask requires the number of jobs to be explicitly set.

    Note:
        For licensing details, please refer to Tobler's BSD 3-Clause License.
    """
    if n_jobs == -1:
        raise ValueError(" Dask generator requires the Optional jobs parameter to be set")

    # Chunk the largest, ship the smallest in full
    sdf, tdf = _get_chunks_for_dask(n_jobs, source_df, target_df)
    sdf.calculate_spatial_partitions()

    id_chunks = _ids_for_dask_generator(sdf=sdf, tdf=tdf)
    worker_out = _get_ids_for_dask(id_chunks)
    ids_src, ids_tgt = np.concatenate(worker_out).T

    # Intersection + area calculation
    chunks_to_intersection = _chunk_polys_dask(
        np.vstack([ids_src, ids_tgt]).T, source_df.geometry, target_df.geometry, n_jobs
    )

    worker_out = _get_areas_for_dask(n_jobs, chunks_to_intersection)
    areas = np.concatenate(worker_out)
    if source_type == "grid":
        return (
            target_df[target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            source_df.i_index.iloc[ids_src].values.astype(int).tolist(),
            source_df.j_index.iloc[ids_src].values.astype(int).tolist(),
            (areas.astype(float) / target_df.geometry[ids_tgt].area).tolist(),
        )
    elif source_type == "poly":
        return (
            target_df[target_poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            source_df[source_poly_idx[0]].iloc[ids_src].values.astype(object).tolist(),
            (areas.astype(float) / target_df.geometry[ids_tgt].area).tolist(),
        )


def _get_chunks_for_dask(
    jobs: int, source_df: gpd.GeoDataFrame, target_df: gpd.GeoDataFrame
) -> Tuple[dgpd.GeoDataFrame, dgpd.GeoDataFrame]:
    """Partition GeoDataFrames into chunks for parallel processing with Dask.

    This function takes GeoDataFrames and the number of jobs, and returns
    Dask GeoDataFrames partitioned into 'npartitions' equal to the number of jobs.

    Args:
        jobs (int): The number of jobs (partitions) for parallel processing.
        source_df (gpd.GeoDataFrame): The source GeoDataFrame to be partitioned.
        target_df (gpd.GeoDataFrame): The target GeoDataFrame to be partitioned.

    Returns:
        Tuple[dgpd.GeoDataFrame, dgpd.GeoDataFrame]: A tuple containing the partitioned
        source and target Dask GeoDataFrames.
    """
    return (
        dgpd.from_geopandas(source_df, npartitions=jobs),
        dgpd.from_geopandas(target_df, npartitions=jobs),
    )


def _chunk_dfs(
    geoms_to_chunk: gpd.GeoSeries, geoms_full: gpd.GeoSeries, n_jobs: int
) -> Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]:
    """Partition GeoSeries into chunks for parallel processing.

    This function takes two GeoSeries and the number of jobs, and yields
    tuples of GeoSeries chunks for parallel processing. The 'geoms_to_chunk'
    GeoSeries is divided into 'n_jobs' number of chunks, while 'geoms_full'
    is passed as is in each tuple.

    Args:
        geoms_to_chunk (gpd.GeoSeries): The GeoSeries to be chunked.
        geoms_full (gpd.GeoSeries): The full GeoSeries to be included in each chunk.
        n_jobs (int): The number of jobs (chunks) for parallel processing.

    Yields:
        Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]: A generator that yields
        tuples containing a chunk of 'geoms_to_chunk' and the full 'geoms_full' GeoSeries.
    """
    chunk_size = geoms_to_chunk.shape[0] // n_jobs + 1
    for i in range(n_jobs):
        start = i * chunk_size
        yield geoms_to_chunk.iloc[start : start + chunk_size], geoms_full


def _index_n_query(geoms1: gpd.GeoSeries, geoms2: gpd.GeoSeries) -> npt.ArrayLike:
    """Retrieve intersecting geometry IDs using spatial indexing.

    This function takes two GeoSeries, builds an STRTree spatial index on the
    first GeoSeries, and then queries the second GeoSeries to find intersecting
    geometries. The function returns an array of tuples containing the global IDs
    of intersecting geometries from both GeoSeries.

    Args:
        geoms1 (gpd.GeoSeries): The first GeoSeries, used for building the STRTree spatial index.
        geoms2 (gpd.GeoSeries): The second GeoSeries, used for querying against the spatial index.

    Returns:
        npt.ArrayLike: A NumPy array containing tuples of global IDs for intersecting geometries.
                       Each tuple contains two elements:
                       - The global ID from 'geoms1'
                       - The global ID from 'geoms2'
    """
    # Pick largest for STRTree, query the smallest

    # Build tree + query
    qry_polyids, tree_polyids = geoms1.sindex.query(geoms2, predicate="intersects")
    # Remap IDs to global
    large_global_ids = geoms1.iloc[tree_polyids].index.values
    small_global_ids = geoms2.iloc[qry_polyids].index.values

    return np.array([large_global_ids, small_global_ids]).T


def _index_n_query_dask(bag: Tuple[gpd.GeoSeries, gpd.GeoSeries]) -> npt.ArrayLike:
    """Retrieve intersecting geometry IDs for parallel processing using Dask.

    This function takes a tuple of two GeoSeries, builds an STRTree spatial index on the
    first GeoSeries, and then queries the second GeoSeries to find intersecting
    geometries. The function returns an array of tuples containing the global IDs
    of intersecting geometries from both GeoSeries.

    Args:
        bag (Tuple[gpd.GeoSeries, gpd.GeoSeries]): A tuple containing two GeoSeries.
            - bag[0]: The first GeoSeries, used for building the STRTree spatial index.
            - bag[1]: The second GeoSeries, used for querying against the spatial index.

    Returns:
        npt.ArrayLike: A NumPy array containing tuples of global IDs for intersecting geometries.
                       Each tuple contains two elements:
                       - The global ID from 'bag[0]'
                       - The global ID from 'bag[1]'
    """
    # Build tree + query
    source_df = bag[0]
    target_df = bag[1]
    qry_polyids, tree_polyids = source_df.sindex.query(target_df, predicate="intersects")
    # Remap IDs to global
    large_global_ids = source_df.iloc[tree_polyids].index.values
    small_global_ids = target_df.iloc[qry_polyids].index.values

    return np.array([large_global_ids, small_global_ids]).T


def _chunk_polys(
    id_pairs: npt.NDArray[np.int_],
    geoms_left: gpd.GeoSeries,
    geoms_right: gpd.GeoSeries,
    n_jobs: int,
) -> Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any]:
    """Divide geometry pairs into chunks for parallel processing.

    This function takes an array of ID pairs and two GeoSeries, and divides them into
    smaller chunks for parallel processing. The function yields tuples containing
    chunks of geometries from both GeoSeries based on the provided ID pairs.

    Args:
        id_pairs (npt.NDArray[np.int_]): A NumPy array of shape (N, 2) containing pairs of IDs
                                         that correspond to intersecting geometries in
                                         'geoms_left' and 'geoms_right'.
        geoms_left (gpd.GeoSeries): The first GeoSeries containing geometries.
        geoms_right (gpd.GeoSeries): The second GeoSeries containing geometries.
        n_jobs (int): Number of chunks to create for parallel processing.

    Yields:
        Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any]: A generator that yields
                                                                  tuples of NumPy arrays.
                                                                  Each tuple contains:
                                                                  - A chunk of geometries from 'geoms_left'
                                                                  - A chunk of geometries from 'geoms_right'

    """
    chunk_size = id_pairs.shape[0] // n_jobs + 1
    for i in range(n_jobs):
        start = i * chunk_size
        chunk1 = np.asarray(geoms_left.values[id_pairs[start : start + chunk_size, 0]])
        chunk2 = np.asarray(geoms_right.values[id_pairs[start : start + chunk_size, 1]])
        yield chunk1, chunk2


def _chunk_polys_dask(
    id_pairs: npt.NDArray[np.int_],
    geoms_left: gpd.GeoSeries,
    geoms_right: gpd.GeoSeries,
    n_jobs: int,
) -> Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any]:
    """Chunk polys for parallel processing."""
    chunk_size = id_pairs.shape[0] // n_jobs + 1
    for i in range(n_jobs):
        start = i * chunk_size
        chunk1 = np.asarray(geoms_left.values[id_pairs[start : start + chunk_size, 0]])
        chunk2 = np.asarray(geoms_right.values[id_pairs[start : start + chunk_size, 1]])
        yield (chunk1, chunk2)


def _intersect_area_on_chunk(geoms1: npt.ArrayLike, geoms2: npt.ArrayLike) -> Tuple[gpd.GeoSeries, gpd.GeoSeries]:
    """Get intersection areas."""
    f_intersect = intersection(geoms1, geoms2)
    return area(f_intersect), f_intersect


def _area_on_chunk(geoms1: gpd.GeoSeries, geoms2: gpd.GeoSeries) -> gpd.GeoSeries:
    """Get intersection areas."""
    return area(intersection(geoms1, geoms2))


def _area_on_chunk_dask(dask_bag: Tuple[npt.ArrayLike, npt.ArrayLike]) -> gpd.GeoSeries:
    """Get intersection areas."""
    geoms1 = dask_bag[0]
    geoms2 = dask_bag[1]
    return area(intersection(geoms1, geoms2))


def _intersect_area_on_chunk_dask(dask_bag: Tuple[npt.ArrayLike, npt.ArrayLike]) -> gpd.GeoSeries:
    """Get intersection areas."""
    geoms1 = dask_bag[0]
    geoms2 = dask_bag[1]
    f_intersect = intersection(geoms1, geoms2)
    return area(f_intersect), f_intersect
