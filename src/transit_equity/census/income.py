import pandas as pd
from enum import Enum

class IncomeDetails:
    """
    A class to store the details of the income distribution columns in the census data

    Attributes:
    ----------
    field: str
        The field name in the census data
    label: str
        The human readable label for the field
    min_income: int
        The minimum income in the range
    max_income: int
        The maximum income in the range
    """
    def __init__(self, field: str, label: str, min_income: int = 0, max_income: int = 0):
        self._field = field
        self._label = label
        self._min_income = min_income
        self._max_income = max_income
    
    @property
    def field(self):
        return self._field
    
    @property
    def label(self):
        return self._label
    
    @property
    def min_income(self):
        return self._min_income
    
    @property
    def max_income(self):
        return self._max_income

class INCOME_DISTRIBUTION_COLUMNS(Enum):
    """
    This Enum class contains the details of the income distribution columns in the census data
        that will be relevant for the low income analysis

    Table: B19001 - HOUSEHOLD INCOME IN THE PAST 12 MONTHS
    https://api.census.gov/data/2019/acs/acs5/groups/B19001.html

    The min_income and max_income have been assigned as -1 for the total field, 
        since they are not used in the calculation of average household income
    
    The max_income for the last column has been assigned as math.inf since it is the highest income range.
        Please note this if you intend to use this class for any other purpose such as average income calculation.
    """
    B19001_001E: IncomeDetails = IncomeDetails(field='B19001_001E',
        label='total', min_income=-1, max_income=-1)
    B19001_002E: IncomeDetails = IncomeDetails(field='B19001_002E',
        label='less_than_10000', min_income=0, max_income=9999)
    B19001_003E: IncomeDetails = IncomeDetails(field='B19001_003E',
        label='10000_to_14999', min_income=10000, max_income=14999)
    B19001_004E: IncomeDetails = IncomeDetails(field='B19001_004E',
        label='15000_to_19999', min_income=15000, max_income=19999)
    B19001_005E: IncomeDetails = IncomeDetails(field='B19001_005E',
        label='20000_to_24999', min_income=20000, max_income=24999)
    B19001_006E: IncomeDetails = IncomeDetails(field='B19001_006E',
        label='25000_to_29999', min_income=25000, max_income=29999)
    B19001_007E: IncomeDetails = IncomeDetails(field='B19001_007E',
        label='30000_to_34999', min_income=30000, max_income=34999)
    B19001_008E: IncomeDetails = IncomeDetails(field='B19001_008E',
        label='35000_to_39999', min_income=35000, max_income=39999)
    B19001_009E: IncomeDetails = IncomeDetails(field='B19001_009E',
        label='40000_to_44999', min_income=40000, max_income=44999)
    B19001_010E: IncomeDetails = IncomeDetails(field='B19001_010E',
        label='45000_to_49999', min_income=45000, max_income=49999)
    B19001_011E: IncomeDetails = IncomeDetails(field='B19001_011E',
        label='50000_to_59999', min_income=50000, max_income=59999)
    B19001_012E: IncomeDetails = IncomeDetails(field='B19001_012E',
        label='60000_to_74999', min_income=60000, max_income=74999)
    B19001_013E: IncomeDetails = IncomeDetails(field='B19001_013E',
        label='75000_to_99999', min_income=75000, max_income=99999)
    B19001_014E: IncomeDetails = IncomeDetails(field='B19001_014E',
        label='100000_to_124999', min_income=100000, max_income=124999)
    B19001_015E: IncomeDetails = IncomeDetails(field='B19001_015E',
        label='125000_to_149999', min_income=125000, max_income=149999)
    B19001_016E: IncomeDetails = IncomeDetails(field='B19001_016E',
        label='150000_to_199999', min_income=150000, max_income=199999)
    B19001_017E: IncomeDetails = IncomeDetails(field='B19001_017E',
        label='200000_or_more', min_income=200000, max_income=1e9)


# TODO: This function can be extended to do a calculation on an entire pandas DataFrame
# The extended function will also have better performance.
# TODO: Create another function that returns the columns that fall within the income range
# Such a function is more extensible as we can do more nuanced analysis, with less assumptions about the data
def get_households_in_income_range(income_distribution_row: pd.Series, min_income: int, max_income: int) -> int:
    """
    A function to get the number of households in a given income range from a census row.
    Since the range is variable, we will have to check all the columns in the series that are present in the range.
    If a column is partially in the range, we will consider the whole column.

    Parameters:
    ----------
    census_row: pd.Series
        A pandas series containing the income distribution data
        It contains different income ranges (e.g. 10000 to 14999, 15000 to 19999, etc.), in a census area, 
            along with the number of households in each range.
        It is recommended to have all the columns in transit_equity.census.income.INCOME_DISTRIBUTION_COLUMNS
    
    min_income: int
        Left end of the income range
    
    max_income: int
        Right end of the income range
    
    Returns:
    -------
    float
        The number of households in the given income range

    Examples:
    --------
    Example 1:

    The following example shows the calculation of number of households in a given income range from a census row
    with 100 households in total, 20 households with income less than 10000, 30 households with income between 10000 and 14999,
    50 households with income between 15000 and 19999, and 0 households with income after.
    The income range is [0, 14999].
    Expected Answer: (20 + 30) = 50

    >>> import pandas as pd
    >>> from transit_equity.census.income import INCOME_DISTRIBUTION_COLUMNS
    >>> from transit_equity.census.income import get_households_in_income_range
    >>> income_distribution_dict = {
    ...     'B19001_001E': 100,
    ...     'B19001_002E': 20,
    ...     'B19001_003E': 30,
    ...     'B19001_004E': 50,
    ...     'B19001_005E': 0,
    ...     # Rest of the columns are 0
    }
    >>> income_distribution_row = pd.Series(income_distribution_dict)
    >>> get_households_in_income_range(income_distribution_row, 0, 14999)
    50
    """
    households = 0
    for column in INCOME_DISTRIBUTION_COLUMNS:
        if column.value.field not in income_distribution_row:
            continue
        # Check if the value of the field is within [min_income, max_income]
        if column.value.min_income >= min_income and column.value.max_income <= max_income:
            households += income_distribution_row[column.value.field]
        # Else check if the value of the field has no overlap with [min_income, max_income]
        elif column.value.min_income >= max_income or column.value.max_income <= min_income:
            pass
        # Else, there is some overlap with [min_income, max_income]
        else:
            # As mentioned in the docstrings, in such a case, we will consider the whole column.
            # This logic can be improved based on some heuristics
            households += income_distribution_row[column.value.field]
    return households
