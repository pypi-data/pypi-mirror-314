"""Placeholder __init__.py for data package."""

import logging

from .user_data import ClimRCatData
from .user_data import NHGFStacData
from .user_data import UserCatData
from .user_data import UserTiffData

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ["ClimRCatData", "UserCatData", "UserTiffData", "NHGFStacData"]
