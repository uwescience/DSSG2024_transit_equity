from enum import Enum

# B11016 - HOUSEHOLD TYPE BY HOUSEHOLD SIZE
class B11016_HOUSEHOLD_SIZE_COLUMNS(Enum):
    B11016_001E: str = 'total'
    B11016_002E: str = 'family_households'
    B11016_003E: str = 'family_2_person_household'
    B11016_004E: str = 'family_3_person_household'
    B11016_005E: str = 'family_4_person_household'
    B11016_006E: str = 'family_5_person_household'
    B11016_007E: str = 'family_6_person_household'
    B11016_008E: str = 'family_7_or_more_person_household'
    B11016_009E: str = 'nonfamily_households'
    B11016_010E: str = 'nonfamily_1_person_household'
    B11016_011E: str = 'nonfamily_2_person_household'
    B11016_012E: str = 'nonfamily_3_person_household'
    B11016_013E: str = 'nonfamily_4_person_household'
    B11016_014E: str = 'nonfamily_5_person_household'
    B11016_015E: str = 'nonfamily_6_person_household'
    B11016_016E: str = 'nonfamily_7_or_more_person_household'


B11016_HOUSEHOLD_SIZE_COLUMNS_DICT = {
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