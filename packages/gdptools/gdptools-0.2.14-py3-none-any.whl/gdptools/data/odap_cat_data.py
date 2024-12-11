"""OpenDAP Catalog Data classes."""

from __future__ import annotations

from typing import Optional, Dict, Any

# from typing import Tuple

import numpy as np
from pydantic import BaseModel
from pydantic import validator, root_validator


class CatClimRItem(BaseModel):
    """Mike Johnson's CatClimRItem class.

    Source data from which this is derived comes from:
        'https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet'
    """

    id: Optional[str] = None
    asset: Optional[str] = None
    URL: str
    varname: str
    long_name: Optional[str] = None  # type: ignore
    variable: Optional[str] = None
    description: Optional[str] = None
    units: Optional[str] = None
    model: Optional[str] = None
    ensemble: Optional[str] = None
    scenario: Optional[str] = None
    T_name: Optional[str] = None
    duration: Optional[str] = None
    interval: Optional[str] = None
    nT: Optional[int] = 0  # noqa
    X_name: str  # noqa
    Y_name: str  # noqa
    X1: Optional[float] = None
    Xn: Optional[float] = None
    Y1: Optional[float] = None
    Yn: Optional[float] = None
    resX: float  # noqa
    resY: float  # noqa
    ncols: Optional[int] = None
    nrows: Optional[int] = None
    proj: Optional[str] = None
    toptobottom: str
    tiled: Optional[str] = None
    crs: Optional[str] = None

    @root_validator(pre=False)
    @classmethod
    def set_default_long_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Sets long_name to asset value if long_name is None or empty."""
        if not values.get("long_name"):
            values["long_name"] = values.get("description", "None")
        return values

    # @validator("crs", pre=True, always=True)
    # @classmethod
    # def _default_crs(cls, val: str, values: Dict[str, Any]) -> str:
    #     """Sets to a default CRS if none is provided."""
    #     if val is None or not val:
    #         # Only set crs from proj if crs is not provided
    #         return values.get("proj", "EPSG:4326")
    #     return val
    # @root_validator(pre=False)
    # @classmethod
    # def _set_crs(cls, values: Dict[str, Any]) -> str:
    #     """Sets to a default PROJ if none is provided."""
    #     if not values.get("crs"):
    #         # Only set proj from crs if proj is not provided
    #         values["crs"] = values.get("proj", "EPSG:4326")
    #     return values

    @root_validator(pre=False)
    @classmethod
    def _set_proj(cls, values: Dict[str, Any]) -> str:
        """Sets to a default PROJ if none is provided."""
        if not values.get("proj"):
            # Only set proj from crs if proj is not provided
            values["proj"] = values.get("crs", "EPSG:4326")
        return values

    @validator("nT", pre=True, always=False)
    @classmethod
    def set_nt(cls, v: int) -> int:  # noqa:
        """Convert to int."""
        return 0 if np.isnan(v) else v

    @validator("toptobottom", always=False)
    @classmethod
    def _toptobottom_as_bool(cls, val: str) -> bool:
        """Convert to python boolean type."""
        return val.upper() == "TRUE"  # type: ignore

    @validator("tiled", always=False)
    @classmethod
    def _tiled(cls, val: str) -> str:
        """Must be one of just a few options.  Returns NA if left blank."""
        if val.upper() not in ["", "NA", "T", "XY"]:
            raise ValueError("tiled must be one of ['', 'NA', 'T', 'XY']")
        return val.upper() if val else "NA"

    class Config:
        """interior class to direct pydantic's behavior."""

        anystr_strip_whitespace = False
        allow_mutations = False
