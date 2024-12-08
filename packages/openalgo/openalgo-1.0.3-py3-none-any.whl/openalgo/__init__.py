# -*- coding: utf-8 -*-
"""
OpenAlgo Python Library
"""

from .orders import OrderAPI
from .data import DataAPI

class api(OrderAPI, DataAPI):
    """
    Unified API class that combines order management and market data functionality.
    Inherits from both OrderAPI and DataAPI.
    """
    pass

__version__ = "1.0.3"
