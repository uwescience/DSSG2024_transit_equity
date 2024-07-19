import pandas as pd
from enum import Enum

class IncomeDetails:
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

# B19001 - HOUSEHOLD INCOME IN THE PAST 12 MONTHS
# The min_income and max_income have been assigned as 0 and -1 respectively for the total field, 
# # since they are not used in the calculation of average household income
class INCOME_DISTRIBUTION_COLUMNS(Enum):
    B19001_001E: IncomeDetails = IncomeDetails(field='B19001_001E', label='total', min_income=0, max_income=-1)
    B19001_002E: IncomeDetails = IncomeDetails(field='B19001_002E', label='less_than_10000', min_income=0, max_income=9999)
    B19001_003E: IncomeDetails = IncomeDetails(field='B19001_003E', label='10000_to_14999', min_income=10000, max_income=14999)
    B19001_004E: IncomeDetails = IncomeDetails(field='B19001_004E', label='15000_to_19999', min_income=15000, max_income=19999)
    B19001_005E: IncomeDetails = IncomeDetails(field='B19001_005E', label='20000_to_24999', min_income=20000, max_income=24999)
    B19001_006E: IncomeDetails = IncomeDetails(field='B19001_006E', label='25000_to_29999', min_income=25000, max_income=29999)
    B19001_007E: IncomeDetails = IncomeDetails(field='B19001_007E', label='30000_to_34999', min_income=30000, max_income=34999)
    B19001_008E: IncomeDetails = IncomeDetails(field='B19001_008E', label='35000_to_39999', min_income=35000, max_income=39999)
    B19001_009E: IncomeDetails = IncomeDetails(field='B19001_009E', label='40000_to_44999', min_income=40000, max_income=44999)
    B19001_010E: IncomeDetails = IncomeDetails(field='B19001_010E', label='45000_to_49999', min_income=45000, max_income=49999)
    B19001_011E: IncomeDetails = IncomeDetails(field='B19001_011E', label='50000_to_59999', min_income=50000, max_income=59999)
    B19001_012E: IncomeDetails = IncomeDetails(field='B19001_012E', label='60000_to_74999', min_income=60000, max_income=74999)
    B19001_013E: IncomeDetails = IncomeDetails(field='B19001_013E', label='75000_to_99999', min_income=75000, max_income=99999)
    B19001_014E: IncomeDetails = IncomeDetails(field='B19001_014E', label='100000_to_124999', min_income=100000, max_income=124999)
    B19001_015E: IncomeDetails = IncomeDetails(field='B19001_015E', label='125000_to_149999', min_income=125000, max_income=149999)
    B19001_016E: IncomeDetails = IncomeDetails(field='B19001_016E', label='150000_to_199999', min_income=150000, max_income=199999)
    B19001_017E: IncomeDetails = IncomeDetails(field='B19001_017E', label='200000_or_more', min_income=200000, max_income=200000)

# The main motive of this dictionary is to map the column names to human readable names
INCOME_DISTRIBUTION_COLUMNS_DICT = {
    'B19001_001E': 'total',
    'B19001_002E': 'less_than_10000',
    'B19001_003E': '10000_to_14999',
    'B19001_004E': '15000_to_19999',
    'B19001_005E': '20000_to_24999',
    'B19001_006E': '25000_to_29999',
    'B19001_007E': '30000_to_34999',
    'B19001_008E': '35000_to_39999',
    'B19001_009E': '40000_to_44999',
    'B19001_010E': '45000_to_49999',
    'B19001_011E': '50000_to_59999',
    'B19001_012E': '60000_to_74999',
    'B19001_013E': '75000_to_99999',
    'B19001_014E': '100000_to_124999',
    'B19001_015E': '125000_to_149999',
    'B19001_016E': '150000_to_199999',
    'B19001_017E': '200000_or_more',
}

def get_households_in_income_range(income_distribution_row: pd.Series, min_income: int, max_income: int) -> int:
    '''
    A function to get the number of households in a given income range from a census row.
    Since the range is variable, we will have to check all the columns in the series that are present in the range.
    If a column is partially in the range, we will consider the whole column.
    '''
    households = 0
    column: IncomeDetails
    for column in INCOME_DISTRIBUTION_COLUMNS:
        if column.name not in income_distribution_row:
            continue
        # Check if the value of the field is within [min_income, max_income]
