from enum import Enum

# B19001 - HOUSEHOLD INCOME IN THE PAST 12 MONTHS
class INCOME_DISTRIBUTION_COLUMNS(Enum):
    B19001_001E: str = 'total'
    B19001_002E: str = 'less_than_10000'
    B19001_003E: str = '10000_to_14999'
    B19001_004E: str = '15000_to_19999'
    B19001_005E: str = '20000_to_24999'
    B19001_006E: str = '25000_to_29999'
    B19001_007E: str = '30000_to_34999'
    B19001_008E: str = '35000_to_39999'
    B19001_009E: str = '40000_to_44999'
    B19001_010E: str = '45000_to_49999'
    B19001_011E: str = '50000_to_59999'
    B19001_012E: str = '60000_to_74999'
    B19001_013E: str = '75000_to_99999'
    B19001_014E: str = '100000_to_124999'
    B19001_015E: str = '125000_to_149999'
    B19001_016E: str = '150000_to_199999'
    B19001_017E: str = '200000_or_more'

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
