"""Primary functions for poly-to-poly area-weighted mapping."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import numpy as np
import numpy.typing as npt


logger = logging.getLogger(__name__)

pd_offset_conv: Dict[str, str] = {
    "years": "Y",
    "months": "M",
    "days": "D",
    "hours": "H",
}


def build_subset(
    bounds: npt.NDArray[np.double],
    xname: str,
    yname: str,
    tname: str,
    toptobottom: bool,
    date_min: Optional[str] = None,
    date_max: Optional[str] = None,
) -> Dict[str, object]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        bounds (np.ndarray): _description_
        xname (str): _description_
        yname (str): _description_
        tname (str): _description_
        toptobottom (bool): _description_
        date_min (str): _description_
        date_max (Optional[str], optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """
    print("bounds: ", type(bounds), bounds)
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    if not toptobottom:
        if date_max is None and date_min is None:
            return {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
            }
        elif date_max is None:
            return {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: date_min,
            }
        else:
            return {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: slice(date_min, date_max),
            }

    elif date_max is None and date_min is None:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
        }

    elif date_max is None:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            tname: date_min,
        }

    else:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            tname: slice(date_min, date_max),
        }


def build_subset_tiff(
    bounds: npt.NDArray[np.double],
    xname: str,
    yname: str,
    toptobottom: bool,
    bname: str,
    band: int,
) -> Mapping[Any, Any]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        bounds (npt.NDArray[np.double]): _description_
        xname (str): _description_
        yname (str): _description_
        toptobottom (bool): _description_
        bname (str): _description_
        band (int): _description_

    Returns:
        Dict[str, object]: _description_
    """
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]

    return (
        {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            bname: band,
        }
        if toptobottom
        else {
            xname: slice(minx, maxx),
            yname: slice(maxy, miny),
            bname: band,
        }
    )


def build_subset_tiff_da(
    bounds: npt.NDArray[np.double],
    xname: str,
    yname: str,
    toptobottom: Union[int, bool],
) -> Mapping[Any, Any]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        bounds (npt.NDArray[np.double]): _description_
        xname (str): _description_
        yname (str): _description_
        toptobottom (bool): _description_

    Returns:
        Dict[str, object]: _description_
    """
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]

    return (
        {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
        }
        if toptobottom
        else {
            xname: slice(minx, maxx),
            yname: slice(maxy, miny),
        }
    )


def check_gridded_data_for_dimensions(ds, vars) -> None:
    """Abstract method for checking the dimensions of the input gridded data.

    Checks each DataArray in the Xarray Dataset to confirm that the gridded data
    has only three dimensions: x, y, and time.

    Args:
        ds (xr.Dataset): Gridded data to check for x,y,time dimensions
        vars (list): List of the names of the DataArrays within the Dataset

    Raises:
        KeyError: Cannot process these DataArrays because their dimensions do not match the requirements of GDPtools
    """
    bad_vars = []

    for var in vars:
        da = ds[var]
        if len(da.shape) == 3:
            if list(da.indexes)[0] == "time":
                continue
        else:
            bad_vars.append(var)

    if bad_vars:
        raise KeyError(
            f"Cannot process these DataArrays because their dimensions do not match the requirements of GDPtools: \
            {bad_vars}"
        )
