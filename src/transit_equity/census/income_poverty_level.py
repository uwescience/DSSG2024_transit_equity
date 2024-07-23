import pandas as pd
from enum import Enum

class IncomePovertyLevelDetails:
    """
    A class to store the details of the poverty level columns in the census data

    Attributes:
    ----------
    field: str
        The field name in the census data
    label: str
        The human readable label for the field
    min_income_level: int
        The minimum income to poverty level ratio
    max_income_level: int
        The maximum income to poverty level ratio
    """
    def __init__(self, field: str, label: str, min_income_level: int = 0, max_income_level: int = 0):
        # As it turns out, we do not need to use the @property decorator for the class attributes
        # since we are not using any setter methods
        self.field = field
        self.label = label
        self.min_income_level = min_income_level
        self.max_income_level = max_income_level

class INCOME_POVERTY_LEVEL_COLUMNS(Enum):
    """
    This Enum class contains the details of the income to poverty level columns in the census data
        that will be relevant for the low income analysis

    Table: C17002 - RATIO OF INCOME TO POVERTY LEVEL IN THE PAST 12 MONTHS

    The min_income_level and max_income_level have been assigned as -1 for the total field, 
        since they are not used in the calculation of average income to poverty level ratio
    
    The max_income_level for the last column has been arbitrarily assigned as 1e6 
        since it is the highest income to poverty level ratio range.
    # TODO: Check an actual appropriate range for the last column
    """
    C17002_001E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_001E',
        label='total', min_income_level=-1, max_income_level=-1)
    