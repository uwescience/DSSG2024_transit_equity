import pandas as pd
from enum import Enum

LOW_INCOME_RANGE = (0, 2.0)

class IncomePovertyLevelDetails:
    """
    A class to store the details of the poverty level columns in the census data

    Attributes:
    ----------
    field: str
        The field name in the census data
    label: str
        The human readable label for the field
    min_income_poverty_level: int
        The minimum income to poverty level ratio
    max_income_poverty_level: int
        The maximum income to poverty level ratio. Exclusive.
        Thus the range is [min_income_poverty_level, max_income_poverty_level)
    """
    def __init__(self, field: str, label: str, min_income_poverty_level: int = 0, max_income_poverty_level: int = 0):
        # As it turns out, we do not need to use the @property decorator for the class attributes
        # since we are not using any setter methods
        self.field = field
        self.label = label
        self.min_income_poverty_level = min_income_poverty_level
        self.max_income_poverty_level = max_income_poverty_level

class INCOME_POVERTY_LEVEL_COLUMNS(Enum):
    """
    This Enum class contains the details of the income to poverty level columns in the census data
        that will be relevant for the low income analysis

    Table: C17002 - RATIO OF INCOME TO POVERTY LEVEL IN THE PAST 12 MONTHS

    The min_income_poverty_level and max_income_poverty_level have been assigned as -1 for the total field, 
        since they are not used in the calculation of average income to poverty level ratio
    
    The max_income_poverty_level for the last column has been arbitrarily assigned as 1e6 
        since it is the highest income to poverty level ratio range.
        It is not recommended to use the last income to poverty level ratio range for any calculations.
    
    # TODO: Check an actual appropriate range for the last column
    """
    C17002_001E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_001E',
        label='total', min_income_poverty_level=-1, max_income_poverty_level=-1)
    C17002_002E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_002E',
        label='less_than_0.5', min_income_poverty_level=0, max_income_poverty_level=0.5)
    C17002_003E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_003E',
        label='0.5_to_0.99', min_income_poverty_level=0.5, max_income_poverty_level=1.0)
    C17002_004E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_004E',
        label='1_to_1.24', min_income_poverty_level=1.0, max_income_poverty_level=1.25)
    C17002_005E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_005E',
        label='1.25_to_1.49', min_income_poverty_level=1.25, max_income_poverty_level=1.50)
    C17002_006E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_006E',
        label='1.5_to_1.84', min_income_poverty_level=1.50, max_income_poverty_level=1.85)
    C17002_007E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_007E',
        label='1.85_to_1.99', min_income_poverty_level=1.85, max_income_poverty_level=2.0)
    C17002_008E: IncomePovertyLevelDetails = IncomePovertyLevelDetails(field='C17002_008E',
        label='2_to_above', min_income_poverty_level=2.0, max_income_poverty_level=1e6)

def get_population_in_income_poverty_level_range(income_poverty_level_row: pd.Series, 
                                         min_income_poverty_level: int = LOW_INCOME_RANGE[0],
                                         max_income_poverty_level: int = LOW_INCOME_RANGE[1]):
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
        
    min_income_poverty_level: int
        The minimum income to poverty level ratio for the range
    
    max_income_poverty_level: int
        The maximum income to poverty level ratio for the range. Exclusive.
        Thus the range is [min_income_poverty_level, max_income_poverty_level)
    
    Returns:
    --------
    population
        The population in the given income to poverty level ratio range
    
    true_min_income_poverty_level: int
        The actual minimum income to poverty level ratio that was used in the calculation.
        This is useful when the input range is not within the bounds of the income to poverty level ratio ranges.
    
    true_max_income_poverty_level: int
        The actual maximum income to poverty level ratio that was used in the calculation.
        This is useful when the input range is not within the bounds of the income to poverty level ratio ranges.
    
    Examples:
    ---------
    Example 1:

    The following example shows the calculation of population in a given income to poverty level ratio range from a census row
    with 100 people in total, 20 people with income to poverty level ratio less than 0.5,
    30 people with income to poverty level ratio between 0.5 and 0.99, 
    10 people with income to poverty level ratio between 1.0 and 1.24, 
    40 people with income to poverty level ratio between 2.0 and above, 
    and 0 people with income to poverty level ratio in between.

    The income to poverty level ratio range is [0, 2.0).
    
    Expected Answer: (20 + 30 + 10) = 60

    >>> import pandas as pd
    >>> from transit_equity.census.income_poverty_level import INCOME_POVERTY_LEVEL_COLUMNS
    >>> from transit_equity.census.income_poverty_level import get_population_in_income_poverty_level_range
    >>> income_poverty_level_dict = {
    ...     'C17002_001E': 100,
    ...     'C17002_002E': 20,
    ...     'C17002_003E': 30,
    ...     'C17002_004E': 10,
    ...     'C17002_005E': 0,
    ...     'C17002_006E': 0,
    ...     'C17002_007E': 0,
    ...     'C17002_008E': 40,
    }
    >>> income_poverty_level_row = pd.Series(income_poverty_level_dict)
    >>> get_population_in_income_poverty_level_range(income_poverty_level_row, 0, 2.0)
    60
    """
    population = 0
    true_min_income_poverty_level = min_income_poverty_level
    true_max_income_poverty_level = max_income_poverty_level
    for column in INCOME_POVERTY_LEVEL_COLUMNS:
        if column.value.field not in income_poverty_level_row:
            continue
        # Check if the value of the field is within [min_income_poverty_level, max_income_poverty_level]
        if column.value.min_income_poverty_level >= min_income_poverty_level and column.value.max_income_poverty_level < max_income_poverty_level:
            population += income_poverty_level_row[column.value.field]
        # Else check if the value of the field has no overlap with [min_income_poverty_level, max_income_poverty_level]
        elif column.value.min_income_poverty_level >= max_income_poverty_level or column.value.max_income_poverty_level < min_income_poverty_level:
            pass
        # Else there is some overlap with [min_income_poverty_level, max_income_poverty_level)
        else:
            population += income_poverty_level_row[column.value.field]
            if column.value.min_income_poverty_level < min_income_poverty_level:
                true_min_income_poverty_level = column.value.min_income_poverty_level
            if column.value.max_income_poverty_level > max_income_poverty_level:
                true_max_income_poverty_level = column.value.max_income_poverty_level
    return {
        'population': population,
        'true_min_income_poverty_level': true_min_income_poverty_level,
        'true_max_income_poverty_level': true_max_income_poverty_level
    }

def get_population_in_income_poverty_level_range_df(income_poverty_level_row_df: pd.DataFrame,
                                                    min_income_poverty_level: int = LOW_INCOME_RANGE[0],
                                                    max_income_poverty_level: int = LOW_INCOME_RANGE[1]):
    """
    A function to get the population in the given income to poverty level ratio range 
        for each row in a census DataFrame.
    Since the income to poverty level ratio is a continuous variable, 
        we will have to check all the columns in the DataFrame that are present in the range.
    If a column is partially in the range, we will consider the whole column.

    Parameters:
    -----------
    income_poverty_level_row_df: pd.DataFrame
        A pandas DataFrame containing the income to poverty level ratio columns
        It contains different income to poverty level ratio ranges (e.g. less_than_0.5, 0.5_to_0.99, etc.)
            in a census area.
        
    min_income_poverty_level: int
        The minimum income to poverty level ratio for the range
    
    max_income_poverty_level: int
        The maximum income to poverty level ratio for the range. Exclusive.
        Thus the range is [min_income_poverty_level, max_income_poverty_level)
    
    Returns:
    --------
    population: pd.Series
        The population in the given income to poverty level ratio range for each row in the DataFrame
    
    true_min_income_poverty_level: int
        The actual minimum income to poverty level ratio that was used in the calculation.
        This is useful when the input range is not within the bounds of the income to poverty level ratio ranges.

    true_max_income_poverty_level: int
        The actual maximum income to poverty level ratio that was used in the calculation.
        This is useful when the input range is not within the bounds of the income to poverty level ratio ranges.
    
    Examples:
    ---------
    Example 1:

    The following example shows the calculation of population in a given income to poverty level ratio range from a census row
    with 100 people in total, 20 people with income to poverty level ratio less than 0.5,
    30 people with income to poverty level ratio between 0.5 and 0.99, 
    10 people with income to poverty level ratio between 1.0 and 1.24, 
    40 people with income to poverty level ratio between 2.0 and above, 
    and 0 people with income to poverty level ratio in between.

    The income to poverty level ratio range is [0, 2.0).
    
    Expected Answer: (20 + 30 + 10) = 60
    
    >>> import pandas as pd
    >>> from transit_equity.census.income_poverty_level import INCOME_POVERTY_LEVEL_COLUMNS
    >>> from transit_equity.census.income_poverty_level import get_population_in_income_poverty_level_range_df
    >>> income_poverty_level_dict = {
    ...     'C17002_001E': [100, 100, 100],
    ...     'C17002_002E': [20, 20, 20],
    ...     'C17002_003E': [30, 30, 30],
    ...     'C17002_004E': [10, 10, 10],
    ...     'C17002_005E': [0, 0, 0],
    ...     'C17002_006E': [0, 0, 0],
    ...     'C17002_007E': [0, 0, 0],
    ...     'C17002_008E': [40, 40, 40],
    }
    >>> income_poverty_level_row_df = pd.DataFrame(income_poverty_level_dict)
    >>> get_population_in_income_poverty_level_range_df(income_poverty_level_row_df, 0, 2.0)
    0    60
    1    60
    2    60
    dtype: int64
    """
    true_min_income_poverty_level = min_income_poverty_level
    true_max_income_poverty_level = max_income_poverty_level
    population = pd.Series([0] * len(income_poverty_level_row_df))
    
    for column in INCOME_POVERTY_LEVEL_COLUMNS:
        if column.value.field not in income_poverty_level_row_df:
            continue
        # Check if the value of the field is within [min_income_poverty_level, max_income_poverty_level]
        if column.value.min_income_poverty_level >= min_income_poverty_level and column.value.max_income_poverty_level < max_income_poverty_level:
            population += income_poverty_level_row_df[column.value.field]
        # Else check if the value of the field has no overlap with [min_income_poverty_level, max_income_poverty_level]
        elif column.value.min_income_poverty_level >= max_income_poverty_level or column.value.max_income_poverty_level < min_income_poverty_level:
            pass
        # Else there is some overlap with [min_income_poverty_level, max_income_poverty_level)
        else:
            population += income_poverty_level_row_df[column.value.field]
            if column.value.min_income_poverty_level < min_income_poverty_level:
                true_min_income_poverty_level = column.value.min_income_poverty_level
            if column.value.max_income_poverty_level > max_income_poverty_level:
                true_max_income_poverty_level = column.value.max_income_poverty_level
    return {
        'population': population,
        'true_min_income_poverty_level': true_min_income_poverty_level,
        'true_max_income_poverty_level': true_max_income_poverty_level
    }