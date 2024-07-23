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
        The maximum income to poverty level ratio. Exclusive.
        Thus the range is [min_income_level, max_income_level)
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
        It is not recommended to use the last income to poverty level ratio range for any calculations.
    
    # TODO: Check an actual appropriate range for the last column
    """
    C17002_001E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_001E',
        label='total', min_income_level=-1, max_income_level=-1)
    C17002_002E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_002E',
        label='less_than_0.5', min_income_level=0, max_income_level=0.5)
    C17002_003E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_003E',
        label='0.5_to_0.99', min_income_level=0.5, max_income_level=1.0)
    C17002_004E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_004E',
        label='1_to_1.24', min_income_level=1.0, max_income_level=1.25)
    C17002_005E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_005E',
        label='1.25_to_1.49', min_income_level=1.25, max_income_level=1.50)
    C17002_006E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_006E',
        label='1.5_to_1.84', min_income_level=1.50, max_income_level=1.85)
    C17002_007E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_007E',
        label='1.85_to_1.99', min_income_level=1.85, max_income_level=2.0)
    C17002_008E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_008E',
        label='2_to_2.99', min_income_level=2.0, max_income_level=1e6)
    
def get_population_in_income_level_range(income_poverty_level_row: pd.Series, 
                                         min_income_level: int, max_income_level: int):
    """
    A function to get the population in the given income to poverty level ratio range from a census row.
    Since the income to poverty level ratio is a continuous variable, 
        we will have to check all the columns in the series that are present in the range.
    If a column is partially in the range, we will consider the whole column.

    Parameters:
    -----------
    income_poverty_level_row: pd.Series
        A pandas series containing the income to poverty level ratio columns
        It contains different income to poverty level ratio ranges (e.g. less_than_0.5, 0.5_to_0.99, etc.)
            in a census area.
        
    min_income_level: int
        The minimum income to poverty level ratio for the range
    
    max_income_level: int
        The maximum income to poverty level ratio for the range. Exclusive.
        Thus the range is [min_income_level, max_income_level)
    
    Returns:
    --------
    int
        The population in the given income to poverty level ratio range
    """
    population = 0
    for column in INCOME_POVERTY_LEVEL_COLUMNS:
        if column.value.field not in income_poverty_level_row:
            continue
        # Check if the value of the field is within [min_income_level, max_income_level]
        if column.value.min_income_level >= min_income_level and column.value.max_income_level < max_income_level:
            population += income_poverty_level_row[column.value.field]
        # Else check if the value of the field has no overlap with [min_income_level, max_income_level]
        elif column.value.min_income_level >= max_income_level or column.value.max_income_level < min_income_level:
            pass
        # Else there is some overlap with [min_income_level, max_income_level)
        else:
            population += income_poverty_level_row[column.value.field]
    return population