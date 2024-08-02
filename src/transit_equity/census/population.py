"""
This module contains functions for working with population data from the US Census Bureau.
"""

import pandas as pd
from enum import Enum

class PopulationDetails:
    """
    A class to store the details of the population columns in the census data.

    Attributes:
    ----------
    field: str
        The field name in the census data
    label: str
        The human readable label for the field
    """
    def __init__(self, field: str, label: str):
        self._field = field
        self._label = label
    
    @property
    def field(self):
        return self._field
    
    @property
    def label(self):
        return self._label
    
class POPULATION_COLUMNS(Enum):
    """
    This Enum class contains the details of the population columns in the census data
        that will be relevant for the low income analysis
    
    Table: B01003 - TOTAL POPULATION
    https://api.census.gov/data/2022/acs/acs5/groups/B01003.html
    """
    TOTAL_POPULATION = PopulationDetails('B01003_001E', 'Total Population')
