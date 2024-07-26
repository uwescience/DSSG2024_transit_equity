"""
This file contains all the table, view and materialized view names in the database, with a list for each schema.
The names are hard-coded because the database schema is static.
"""

from enum import Enum

class DSSG_TABLES(Enum):
    """
    Access using DSSG_TABLES.<table_name>.value
    """

    BOARDINGS_VIEW: str = 'v_boardings_apr2023'
    LINKED_TRANSACTIONS_VIEW: str = 'v_linked_transactions_apr2023'
    TRANSACTIONS_MAT_VIEW: str = 'm_transactions_apr2023'

    #new
    CT_BUS_STOPS: str ='ct_bus_stops'
    KCM_STOPS: str ='kcm_stops'
    KCM_EQ_JOB_EQUITY_ROUTES: str ='kcm_eq_job_equity_routes'
    KCM_EQ_EQUITY_PRIORITY_AREAS: str ='kcm_eq_equity_priority_areas'
    KCM_EQ_JOB_EQUITY_PRIORITY_AREAS: str ='kcm_eq_job_equity_priority_areas'
    V_BOARDINGS_APR2023: str ='v_boardings_apr2023'
    V_LINKED_TRANSACTIONS_APR2023: str ='v_linked_transactions_apr2023'
    V_TRANSACTIONS_APR2023: str ='v_transactions_apr2023'
    M_TXN_IDS_APR2023: str ='m_txn_ids_apr2023'
    M_TRANSACTIONS_APR2023: str ='m_transactions_apr2023'


class ORCA_TABLES(Enum):
    """
    Access using ORCA_TABLES.<table_name>.value
    """

    TRANSACTIONS_TABLE: str = 'transactions',
    TRANSACTION_TYPES_TABLE: str = 'transaction_types',
    MODES_TABLE: str = 'modes'

    #new
    STOPS: str ='stops'
    FARE_PRODUCTS: str ='fare_products'
    LINKED_TRANSACTIONS: str ='linked_transactions'
    CARD_TRANSIT_ACCOUNTS: str ='card_transit_accounts'
    INSERT_DATETIMES: str ='insert_datetimes'
    FILES: str ='files'
    ORGANIZATION_NAMES: str ='organization_names'
    PARTICIPANT_GROUPS: str ='participant_groups'
    LINKED_TRANSACTIONS_0250M: str ='linked_transactions_0250m'
    TRANSACTION_TYPES: str ='transaction_types'
    TRANSACTIONS: str ='transactions'
    TRANSACTIONS_0250M: str ='transactions_0250m'
    LINKED_TRANSACTIONS_0500M: str ='linked_transactions_0500m'
    PASSENGER_TYPES: str ='passenger_types'
    DIRECTIONS: str ='directions'
    TRANSACTIONS_0500M: str ='transactions_0500m'
    ORGANIZATIONS: str ='organizations'
    TRANSACTIONS_0750M: str ='transactions_0750m'
    TRANSACTIONS_1000M: str ='transactions_1000m'
    LINKED_TRANSACTIONS_0750M: str ='linked_transactions_0750m'
    LINKED_TRANSACTIONS_1000M: str ='linked_transactions_1000m'
    CARD_CENSUS_BLOCK_GROUPS: str ='card_census_block_groups'
    CARDS: str ='cards'
    V_TRANSACTIONS: str ='v_transactions'
    V_BOARDINGS: str ='v_boardings'
    V_ALIGHTINGS: str ='v_alightings'
    M_TXN_TIMERANGES: str ='m_txn_timeranges'
    M_CARD_LATEST_TXN_DTM: str ='m_card_latest_txn_dtm'
    M_LATEST_FILE_UPLOAD: str ='m_latest_file_upload'


class TRAC_TABLES(Enum):
    """
    Access using TRAC_TABLES.<table_name>.value
    """
    AGENCIES_TABLE: str = 'agencies'

    ##new
    ST_BUS_OPERATORS: str ='st_bus_operators'
    ROUTE_NAME_LOOKUP: str ='route_name_lookup'
    PARAMETERS: str ='parameters'
    TRANSITLAND_AGENCIES: str ='transitland_agencies'
    MODES: str ='modes'
    AGENCIES: str ='agencies'
    BAD_TRANSACTIONS_0250M: str ='bad_transactions_0250m'
    BAD_TRANSACTIONS_0750M: str ='bad_transactions_0750m'
    BAD_TRANSACTIONS_0500M: str ='bad_transactions_0500m'
    BAD_TRANSACTIONS_1000M: str ='bad_transactions_1000m'
    BAD_TRANSACTIONS: str ='bad_transactions'
    E_GEOCODE_RESULT_TYPES: str ='e_geocode_result_types'
    E_BAD_TRANSACTION_TYPES: str ='e_bad_transaction_types'
    V_PREVIOUS_DUPLICATE_TXN: str ='v_previous_duplicate_txn'



class GTFS_TABLES(Enum):
    """
    Access using GTFS_TABLES.<table_name>.value
    """

    FEED_INFO_TABLE: str = 'tl_feed_info'
    FEEDS_TABLE: str = 'transitland_feeds'
    STOPS_TABLE: str = 'tl_stops'
    AGENCY_TABLE: str = 'tl_agency'

    #new
    TRANSITLAND_FEEDS: str ='transitland_feeds'
    TL_TRANSLATIONS: str ='tl_translations'
    TL_NETWORKS: str ='tl_networks'
    TL_FARE_MEDIA: str ='tl_fare_media'
    TL_FARE_RULES: str ='tl_fare_rules'
    E_LOCATION_TYPES: str ='e_location_types'
    TL_TIMEFRAMES: str ='tl_timeframes'
    TL_FARE_PRODUCTS: str ='tl_fare_products'
    E_EXCEPTION_TYPES: str ='e_exception_types'
    E_PAYMENT_METHODS: str ='e_payment_methods'
    E_TRANSFERS: str ='e_transfers'
    E_WHEELCHAIR_BOARDINGS: str ='e_wheelchair_boardings'
    E_DIRECTION_IDS: str ='e_direction_ids'
    E_WHEELCHAIR_ACCESSIBILITY: str ='e_wheelchair_accessibility'
    E_SERVICE_AVAILABILITY: str ='e_service_availability'
    E_ROUTE_TYPES: str ='e_route_types'
    TL_TRIPS: str ='tl_trips'
    E_BIKES_ALLOWED: str ='e_bikes_allowed'
    E_PICKUP_TYPES: str ='e_pickup_types'
    E_EXACT_TIMES: str ='e_exact_times'
    E_DURATION_LIMIT_TYPES: str ='e_duration_limit_types'
    E_TIMEPOINTS: str ='e_timepoints'
    E_TRANSFER_TYPES: str ='e_transfer_types'
    E_FARE_MEDIA_TYPES: str ='e_fare_media_types'
    E_IS_ROLE: str ='e_is_role'
    TL_EXTRA_FILES: str ='tl_extra_files'
    E_IS_BIDIRECTIONAL: str ='e_is_bidirectional'
    TL_AGENCY: str ='tl_agency'
    TL_FEED_INFO: str ='tl_feed_info'
    E_CONTINUOUS_PICKUP: str ='e_continuous_pickup'
    E_CONTINUOUS_DROP_OFF: str ='e_continuous_drop_off'
    TL_CALENDAR: str ='tl_calendar'
    TL_AREAS: str ='tl_areas'
    TL_ROUTES: str ='tl_routes'
    TL_CALENDAR_DATES: str ='tl_calendar_dates'
    E_DROP_OFF_TYPES: str ='e_drop_off_types'
    E_FARE_TRANSFER_TYPES: str ='e_fare_transfer_types'
    TL_FARE_ATTRIBUTES: str ='tl_fare_attributes'
    E_PATHWAY_MODES: str ='e_pathway_modes'
    TL_FARE_LEG_RULES: str ='tl_fare_leg_rules'
    TL_FARE_TRANSFER_RULES: str ='tl_fare_transfer_rules'
    TL_STOP_AREAS: str ='tl_stop_areas'
    TL_ROUTE_NETWORKS: str ='tl_route_networks'
    TL_FREQUENCIES: str ='tl_frequencies'
    TL_TRANSFERS: str ='tl_transfers'
    TL_ATTRIBUTIONS: str ='tl_attributions'
    TL_PATHWAYS: str ='tl_pathways'
    TL_SHAPES: str ='tl_shapes'
    TL_LEVELS: str ='tl_levels'
    TL_STOP_TIMES: str ='tl_stop_times'
    TL_STOPS: str ='tl_stops'
    TL_BAD_FEEDS: str ='tl_bad_feeds'
    V_TRANSITLAND_FEED_INFO: str ='v_transitland_feed_info'
