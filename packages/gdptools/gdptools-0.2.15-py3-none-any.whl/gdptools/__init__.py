"""Top-level package for pygeoapi plugin: Gdptools."""

import logging

from .agg_gen import AggGen
from .agg_gen import InterpGen
from .data.user_data import ClimRCatData
from .data.user_data import NHGFStacData
from .data.user_data import UserCatData
from .data.user_data import UserTiffData
from .weight_gen import WeightGen
from .weight_gen_p2p import WeightGenP2P
from .zonal_gen import WeightedZonalGen
from .zonal_gen import ZonalGen

__author__ = "Richard McDonald"
__email__ = "rmcd@usgs.gov"
__version__ = "0.2.15"

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "WeightGen",
    "WeightGenP2P",
    "AggGen",
    "ZonalGen",
    "WeightedZonalGen",
    "ClimRCatData",
    "UserCatData",
    "InterpGen",
    "UserTiffData",
    "NHGFStacData",
]
