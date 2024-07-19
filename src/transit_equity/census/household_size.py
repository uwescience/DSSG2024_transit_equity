import pandas as pd
from enum import Enum

# This class will be useful for calculating statistics on households
class HouseholdSizeDetails:
    '''
    A class to store the details of a household size

    Attributes:
    ----------
    field: str
        The field name in the census data
    label: str
        The human readable label for the field
    count: int
        The number of people in the household
    '''
    def __init__(self, field: str, label: str, count: int = 0):
        self._field = field
        self._label = label
        self._count = count
    
    @property
    def field(self):
        return self._field
    
    @property
    def label(self):
        return self._label
    
    @property
    def count(self):
        return self._count

# B11016 - HOUSEHOLD TYPE BY HOUSEHOLD SIZE
# The counts have been assigned as 0 for total, family_households and non-family households
# since they are not used in the calculation of average household size
class HOUSEHOLD_SIZE_COLUMNS(Enum):
    B11016_001E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_001E', 
        label='total')
    B11016_002E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_002E',
        label='family_households')
    B11016_003E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_003E',
        label='family_2_person_household', count=2)
    B11016_004E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_004E',
        label='family_3_person_household', count=3)
    B11016_005E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_005E',
        label='family_4_person_household', count=4)
    B11016_006E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_006E',
        label='family_5_person_household', count=5)
    B11016_007E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_007E',
        label='family_6_person_household', count=6)
    B11016_008E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_008E',
        label='family_7_or_more_person_household', count=7)
    B11016_009E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_009E',
        label='nonfamily_households')
    B11016_010E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_010E',
        label='nonfamily_1_person_household', count=1)
    B11016_011E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_011E',
        label='nonfamily_2_person_household', count=2)
    B11016_012E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_012E',
        label='nonfamily_3_person_household', count=3)
    B11016_013E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_013E',
        label='nonfamily_4_person_household', count=4)
    B11016_014E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_014E',
        label='nonfamily_5_person_household', count=5)
    B11016_015E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_015E',
        label='nonfamily_6_person_household', count=6)
    B11016_016E: HouseholdSizeDetails = HouseholdSizeDetails(field='B11016_016E',
        label='nonfamily_7_or_more_person_household', count=7)

# The main motive of this dictionary is to map the column names to human readable names
HOUSEHOLD_SIZE_COLUMNS_DICT = {
    'B11016_001E': 'total',
    'B11016_002E': 'family_households',
    'B11016_003E': 'family_2_person_household',
    'B11016_004E': 'family_3_person_household',
    'B11016_005E': 'family_4_person_household',
    'B11016_006E': 'family_5_person_household',
    'B11016_007E': 'family_6_person_household',
    'B11016_008E': 'family_7_or_more_person_household',
    'B11016_009E': 'nonfamily_households',
    'B11016_010E': 'nonfamily_1_person_household',
    'B11016_011E': 'nonfamily_2_person_household',
    'B11016_012E': 'nonfamily_3_person_household',
    'B11016_013E': 'nonfamily_4_person_household',
    'B11016_014E': 'nonfamily_5_person_household',
    'B11016_015E': 'nonfamily_6_person_household',
    'B11016_016E': 'nonfamily_7_or_more_person_household',
}

# TODO: This function can be extended to do a calculation on an entire pandas DataFrame
# The extended function will also have better performance.
def get_average_household_size_from_census_row(census_row: pd.Series) -> float:
    '''
    A function to get the average household size for a census row.
    The census row contains the number of households of different sizes (e.g. 2-person, 3-person, etc.).

    Parameters:
    ----------
    census_row: pd.Series
        A pandas series containing the census data
        Should contain all the columns in transit_equity.census.household_size.HOUSEHOLD_SIZE_COLUMNS
    
    Returns:
    -------
    float

    Examples:
    --------
    
    Example 1:

    The following example shows the calculation of average household size from a census row
    with 100 family households (0 non-family households), 
    50 2-person households, 30 3-person households, 20 4-person households.
    Expected Answer: (50*2 + 30*3 + 20*4 / 100) = 2.7

    >>> import pandas as pd
    >>> from transit_equity.census.household_size import HOUSEHOLD_SIZE_COLUMNS
    >>> from transit_equity.census.household_size import get_average_household_size_from_census_row
    >>> census_row_dict = {
    ...     'B11016_001E': 100,
    ...     'B11016_002E': 100,
    ...     'B11016_003E': 50,
    ...     'B11016_004E': 30,
    ...     'B11016_005E': 20}
    >>> census_row = pd.Series(census_row_dict)
    >>> get_average_household_size_from_census_row(census_row)
    2.7
    '''
    if HOUSEHOLD_SIZE_COLUMNS.B11016_001E.value.field not in census_row:
        return 0
    total_households = census_row[HOUSEHOLD_SIZE_COLUMNS.B11016_001E.value.field]
    if total_households == 0:
        return 0
    total_people = 0
    for column in HOUSEHOLD_SIZE_COLUMNS:
        if column.value.field not in census_row:
            continue
        total_people += census_row[column.value.field] * column.value.count
    return total_people / total_households