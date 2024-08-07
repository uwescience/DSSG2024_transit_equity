"""
This module contains the functions and classes to get and analyze income to poverty level ratio data from the US Census Bureau.

Constants
---------
LOW_INCOME_RANGE : Tuple[int, int]

Classes
-------
IncomePovertyLevelRatioDetails :
    A class to store the details of the poverty level columns in the census data

INCOME_POVERTY_LEVEL_RATIO_COLUMNS :
    An Enum class containing the details of the income to poverty level columns in the census data

Functions
---------
get_income_poverty_level_ratio_df:
    A function to get the income to poverty level ratio columns from the US Census Bureau API.
    Works at the block group level.

get_population_in_income_poverty_level_range_df :
    A function to get the population in the given income to poverty level ratio range.

get_low_income_population_df:
    A highly specific function to get the low income population from the census data.
    Works at the block group level.
"""

import pandas as pd
from enum import Enum
from census import Census
import us

from .population import POPULATION_COLUMNS
from .puget_sound import FIPS_PUGET_SOUND
from .utils import CENSUS_MAIN_COLUMNS, get_geo_id

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

def get_income_poverty_level_ratio_df(census: Census,
                                      fields: list = None, state_fips: str = us.states.WA.fips,
                                      county_fips: list = None, blockgroup: str|list = '*', year: int = 2022) -> pd.DataFrame:
    """
    A function to get the income to poverty level ratio columns from the US Census Bureau API
    The income to poverty level ratio columns are present in the C17002 table in the census data.
    The income to poverty level ratio columns contain the number of people in different income to poverty level ratio ranges.
    Additionally, the total population is also present in the census data.

    Currently only works at the block group level. 
    TODO: Check if this function can be made more flexible in terms of granularity of the census data. 

    Parameters:
    -----------
    census: Census
        The Census object that is connected to the API

    fields: list
        The list of fields to get from the census data.
        The default fields are the income to poverty level ratio columns and the total population column.
    
    state_fips: str
        The FIPS code of the state for which the census data is required.
    
    county_fips: list
        The list of FIPS codes of the counties for which the census data is required.
    
    blockgroup: str|list
        The block group for which the census data is required.
    
    year: int
        The year for which the census data is required.
    
    Returns:
    --------
    income_poverty_level_ratio_df: pd.DataFrame
        A pandas DataFrame containing the income to poverty level ratio columns
    """
    if fields is None:
        INCOME_POVERTY_LEVEL_RATIO_COLUMNS_KEYS = [column.value.field for column in INCOME_POVERTY_LEVEL_RATIO_COLUMNS]
        POPULATION_COLUMN_KEY = POPULATION_COLUMNS.TOTAL_POPULATION.value.field
        fields = ('NAME', *INCOME_POVERTY_LEVEL_RATIO_COLUMNS_KEYS, POPULATION_COLUMN_KEY)
    if county_fips is None:
        county_fips = FIPS_PUGET_SOUND
    
    census_income_poverty_ratio = census.acs5.state_county_blockgroup(fields = fields,
        #'C17002_001E', 'C17002_002E', 'C17002_003E', 'B01003_001E'),
        state_fips = us.states.WA.fips,
        county_fips = ','.join(county_fips), 
        blockgroup = "*",
        year = 2022)
    income_poverty_level_ratio_df = pd.DataFrame(census_income_poverty_ratio)
    return income_poverty_level_ratio_df

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
        One way to get this DataFrame is by using the `get_income_poverty_level_ratio_df` function.
        
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

def get_low_income_population_df(income_poverty_level_ratio_df: pd.DataFrame,
                              min_ratio: int = LOW_INCOME_RANGE[0], max_ratio: int = LOW_INCOME_RANGE[1],
                              low_income_population_column: str = 'low_income_population',
                              population_column: str = 'population') -> pd.DataFrame:
    """
    A highly specific function to get the low income population from the census data.

    Parameters:
    -----------
    income_poverty_level_ratio_df: pd.DataFrame
        A pandas DataFrame containing the income to poverty level ratio columns
        It contains different income to poverty level ratio ranges (e.g. less_than_0.5, 0.5_to_0.99, etc.)
            in a census area.
        One way to get this DataFrame is by using the `get_income_poverty_level_ratio_df` function.
    
    min_ratio: int
        The minimum income to poverty level ratio for the range
    
    max_ratio: int
        The maximum income to poverty level ratio for the range. Exclusive.
        Thus the range is [min_ratio, max_ratio)
    
    low_income_population_column: str
        The name of the column that will contain the low income population data
    
    population_column: str
        The name of the column that will contain the total population data
    
    Returns:
    --------
    low_income_population_df: pd.DataFrame
        A pandas DataFrame containing the low income population and the total population data
        The DataFrame will contain the same columns as the input DataFrame with the addition of the low income population column and the total population column.
        The DataFrame will also contain a new column 'GEOID' that contains the GEOID values
    """
    low_income_population_details = get_population_in_income_poverty_level_range_df(
        income_poverty_level_ratio_df, min_ratio, max_ratio)
    if low_income_population_details is None:
        return None
    
    income_poverty_level_ratio_df[low_income_population_column] = low_income_population_details['population']

    POPULATION_COLUMN_KEY = POPULATION_COLUMNS.TOTAL_POPULATION.value.field
    low_income_population_df = income_poverty_level_ratio_df[[
        *CENSUS_MAIN_COLUMNS, low_income_population_column, POPULATION_COLUMN_KEY]]
    low_income_population_df.rename(columns={POPULATION_COLUMN_KEY: population_column}, inplace=True)
    low_income_population_df.loc[:,'GEOID'] = get_geo_id(low_income_population_df)

    return low_income_population_df
