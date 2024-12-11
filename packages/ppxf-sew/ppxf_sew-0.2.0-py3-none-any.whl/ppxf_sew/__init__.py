# __init__.py
"""
Identifier:     ewfit/__init__.py
Name:           __init__.py
Description:    __init__ of ewsps
Author:         Jiafeng Lu
Created:        2024-06-01
Modified-History:
    2024-06-01, Jiafeng Lu, created
"""
import os
from .ew_fit import ewfit,temp_l_make,galaxy_l_make
from .ew_util import all_temp_make


__version__ = "0.2.0"

__all__ = ["ewfit",
           "temp_l_make",
           "all_temp_make",
           "galaxy_l_make"
           ]
