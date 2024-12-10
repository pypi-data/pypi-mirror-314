
# -*- coding: utf-8 -*-
"""
OpenAlgo Python Library
"""

from .orders import OrderAPI
from .data import DataAPI
from .account import AccountAPI

class api(OrderAPI, DataAPI, AccountAPI):
    """
    Unified API class that combines order management, market data, and account functionality.
    Inherits from OrderAPI, DataAPI, and AccountAPI.
    """
    pass

__version__ = "1.0.4"
