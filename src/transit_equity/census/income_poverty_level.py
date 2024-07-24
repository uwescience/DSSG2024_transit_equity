"""
TODO: Add module description

TODO: Make the module more cohesive by integrating the common code between the two main functions 
    into separate helper functions
"""

import pandas as pd
from enum import Enum

LOW_INCOME_RANGE = (0, 2.0)

class IncomePovertyLevelRatioDetails:
    """
    A class to store the details of the poverty level columns in the census data.
    Each column in the census data refers to the number of people in a specific range of income to poverty level ratios.

    Attributes:
    ----------
    field: str
        The field name in the census data
    label: str
        The human readable label for the field
    min_ratio: int
        The minimum income to poverty level ratio in the range. Inclusive.
    max_ratio: int
        The maximum income to poverty level ratio in the range. Exclusive.
    
    Thus the range is [min_ratio, max_ratio)
    """
    def __init__(self, field: str, label: str, min_ratio: int = 0, max_ratio: int = 0):
        # As it turns out, we do not need to use the @property decorator for the class attributes
        # since we are not using any setter methods
        self.field = field
        self.label = label
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

class INCOME_POVERTY_LEVEL_RATIO_COLUMNS(Enum):
    """
    This Enum class contains the details of the income to poverty level columns in the census data
        that will be relevant for the low income analysis

    Table: C17002 - RATIO OF INCOME TO POVERTY LEVEL IN THE PAST 12 MONTHS

    The min_ratio and max_ratio have been assigned as -1 for the total field, 
        since they are not used in the calculation of average income to poverty level ratio
    
    The max_ratio for the last column has been arbitrarily assigned as 1e6 
        since it is the highest income to poverty level ratio range.
        It is not recommended to use the last income to poverty level ratio range for any calculations.
    
    # TODO: Check an actual appropriate range for the last column
    """
    C17002_001E: IncomePovertyLevelRatioDetails = IncomePovertyLevelRatioDetails(field='C17002_001E',
        label='total', min_ratio=-1, max_ratio=-1)
    C17002_002E: IncomePovertyLevelRatioDetails = IncomePovertyLevelRatioDetails(field='C17002_002E',
        label='less_than_0.5', min_ratio=0, max_ratio=0.5)
    C17002_003E: IncomePovertyLevelRatioDetails = IncomePovertyLevelRatioDetails(field='C17002_003E',
        label='0.5_to_0.99', min_ratio=0.5, max_ratio=1.0)
    C17002_004E: IncomePovertyLevelRatioDetails = IncomePovertyLevelRatioDetails(field='C17002_004E',
        label='1_to_1.24', min_ratio=1.0, max_ratio=1.25)
    C17002_005E: IncomePovertyLevelRatioDetails = IncomePovertyLevelRatioDetails(field='C17002_005E',
        label='1.25_to_1.49', min_ratio=1.25, max_ratio=1.50)
    C17002_006E: IncomePovertyLevelRatioDetails = IncomePovertyLevelRatioDetails(field='C17002_006E',
        label='1.5_to_1.84', min_ratio=1.50, max_ratio=1.85)
    C17002_007E: IncomePovertyLevelRatioDetails = IncomePovertyLevelRatioDetails(field='C17002_007E',
        label='1.85_to_1.99', min_ratio=1.85, max_ratio=2.0)
    C17002_008E: IncomePovertyLevelRatioDetails = IncomePovertyLevelRatioDetails(field='C17002_008E',
        label='2_to_above', min_ratio=2.0, max_ratio=1e6)

def get_population_in_income_poverty_level_range_df(income_poverty_level_ratio_df: pd.DataFrame,
                                                    min_ratio: int = LOW_INCOME_RANGE[0],
                                                    max_ratio: int = LOW_INCOME_RANGE[1]):
    """
    A function to get the population in the given income to poverty level ratio range 
        for each row in a census DataFrame.
    Since the income to poverty level ratio is a continuous variable, 
        we will have to check all the columns in the DataFrame that are present in the range.
    If a column is partially in the range, we will consider the whole column.

    Parameters:
    -----------
    income_poverty_level_ratio_df: pd.DataFrame
        A pandas DataFrame containing the income to poverty level ratio columns
        It contains different income to poverty level ratio ranges (e.g. less_than_0.5, 0.5_to_0.99, etc.)
            in a census area.
        
    min_ratio: int
        The minimum income to poverty level ratio for the range
    
    max_ratio: int
        The maximum income to poverty level ratio for the range. Exclusive.
        Thus the range is [min_ratio, max_ratio)
    
    Returns:
    --------
    population: pd.Series
        The population in the given income to poverty level ratio range for each row in the DataFrame
    
    true_min_ratio: int
        The actual minimum income to poverty level ratio that was used in the calculation.
        This is useful when the input range is not within the bounds of the income to poverty level ratio ranges.

    true_max_ratio: int
        The actual maximum income to poverty level ratio that was used in the calculation.
        This is useful when the input range is not within the bounds of the income to poverty level ratio ranges.
    
    Examples:
    ---------
    Example 1:

    The following example shows the calculation of population in a given income to poverty level ratio range 
        from a census dataframe with 3 rows
    
    The income to poverty level ratio range is [0, 2.0).
    
    First Row: There are 100 people in total, 20 people with income to poverty level ratio less than 0.5,
    30 people with income to poverty level ratio between 0.5 and 0.99, 
    10 people with income to poverty level ratio between 1.0 and 1.24, 
    40 people with income to poverty level ratio between 2.0 and above, 
    and 0 people with income to poverty level ratio in between.
    
    First Row Expected Answer: (20 + 30 + 10) = 60
    
    >>> import pandas as pd
    >>> from transit_equity.census.level import INCOME_POVERTY_LEVEL_RATIO_COLUMNS
    >>> from transit_equity.census.level import get_population_in_income_poverty_level_range_df
    >>> level_dict = {
    ...     'C17002_001E': [100, 100, 200],
    ...     'C17002_002E': [20, 20, 20],
    ...     'C17002_003E': [30, 30, 30],
    ...     'C17002_004E': [10, 10, 60],
    ...     'C17002_005E': [0, 0, 0],
    ...     'C17002_006E': [0, 0, 0],
    ...     'C17002_007E': [0, 0, 0],
    ...     'C17002_008E': [40, 40, 90],
    }
    >>> income_poverty_level_ratio_df = pd.DataFrame(level_dict)
    >>> get_population_in_income_poverty_level_range_df(income_poverty_level_ratio_df, 0, 2.0)
    0    60
    1    60
    2    110
    dtype: int64
    """
    true_min_ratio = min_ratio
    true_max_ratio = max_ratio
    population = pd.Series([0] * len(income_poverty_level_ratio_df))
    
    for column in INCOME_POVERTY_LEVEL_RATIO_COLUMNS:
        if column.value.field not in income_poverty_level_ratio_df:
            continue
        # Check if the value of the field is within [min_ratio, max_ratio]
        if column.value.min_ratio >= min_ratio and column.value.max_ratio < max_ratio:
            population += income_poverty_level_ratio_df[column.value.field]
        # Else check if the value of the field has no overlap with [min_ratio, max_ratio]
        elif column.value.min_ratio >= max_ratio or column.value.max_ratio < min_ratio:
            pass
        # Else there is some overlap with [min_ratio, max_ratio)
        else:
            population += income_poverty_level_ratio_df[column.value.field]
            if column.value.min_ratio < min_ratio:
                true_min_ratio = column.value.min_ratio
            if column.value.max_ratio > max_ratio:
                true_max_ratio = column.value.max_ratio
    return {
        'population': population,
        'true_min_ratio': true_min_ratio,
        'true_max_ratio': true_max_ratio
    }