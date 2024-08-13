"""
This file contains all the table, view and materialized view names in the database, with a list for each schema.
In this file, the schema name is attached to the names, which is necessary if we want to use the automap_base_with_views
The names are hard-coded because the database schema is static.
"""

from enum import Enum

from .schemas import DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA

class DSSG_SCHEMA_TABLES(Enum):
    """
    Access using DSSG_SCHEMA_TABLES.<table_name>.value
    """

    BOARDINGS_VIEW: str = f'{DSSG_SCHEMA}.v_boardings_apr2023'
    LINKED_TRANSACTIONS_VIEW: str = f'{DSSG_SCHEMA}.v_linked_transactions_apr2023'
    TRANSACTIONS_MAT_VIEW: str = f'{DSSG_SCHEMA}.m_transactions_apr2023'

    #new
    CT_BUS_STOPS: str = f'{DSSG_SCHEMA}.ct_bus_stops'
    KCM_STOPS: str = f'{DSSG_SCHEMA}.kcm_stops'
    KCM_EQ_JOB_EQUITY_ROUTES: str = f'{DSSG_SCHEMA}.kcm_eq_job_equity_routes'
    KCM_EQ_EQUITY_PRIORITY_AREAS: str = f'{DSSG_SCHEMA}.kcm_eq_equity_priority_areas'
    KCM_EQ_JOB_EQUITY_PRIORITY_AREAS: str = f'{DSSG_SCHEMA}.kcm_eq_job_equity_priority_areas'
    V_BOARDINGS_APR2023: str = f'{DSSG_SCHEMA}.v_boardings_apr2023'
    V_LINKED_TRANSACTIONS_APR2023: str = f'{DSSG_SCHEMA}.v_linked_transactions_apr2023'
    V_TRANSACTIONS_APR2023: str = f'{DSSG_SCHEMA}.v_transactions_apr2023'
    M_TXN_IDS_APR2023: str = f'{DSSG_SCHEMA}.m_txn_ids_apr2023'
    M_TRANSACTIONS_APR2023: str = f'{DSSG_SCHEMA}.m_transactions_apr2023'
    ST_SUBAREAS: str = f'{DSSG_SCHEMA}.st_subareas'


class ORCA_SCHEMA_TABLES(Enum):
    """
    Access using ORCA_SCHEMA_TABLES.<table_name>.value
    """
 
    TRANSACTIONS_TABLE: str = f'{ORCA_SCHEMA}.transactions',
    TRANSACTION_TYPES_TABLE: str = f'{ORCA_SCHEMA}.transaction_types',
    MODES_TABLE: str = f'{ORCA_SCHEMA}.modes'

    #new
    STOPS: str = f'{ORCA_SCHEMA}.stops'
    FARE_PRODUCTS: str = f'{ORCA_SCHEMA}.fare_products'
    LINKED_TRANSACTIONS: str = f'{ORCA_SCHEMA}.linked_transactions'
    CARD_TRANSIT_ACCOUNTS: str = f'{ORCA_SCHEMA}.card_transit_accounts'
    INSERT_DATETIMES: str = f'{ORCA_SCHEMA}.insert_datetimes'
    FILES: str = f'{ORCA_SCHEMA}.files'
    ORGANIZATION_NAMES: str = f'{ORCA_SCHEMA}.organization_names'
    PARTICIPANT_GROUPS: str = f'{ORCA_SCHEMA}.participant_groups'
    LINKED_TRANSACTIONS_0250M: str = f'{ORCA_SCHEMA}.linked_transactions_0250m'
    TRANSACTION_TYPES: str = f'{ORCA_SCHEMA}.transaction_types'
    TRANSACTIONS: str = f'{ORCA_SCHEMA}.transactions'
    TRANSACTIONS_0250M: str = f'{ORCA_SCHEMA}.transactions_0250m'
    LINKED_TRANSACTIONS_0500M: str = f'{ORCA_SCHEMA}.linked_transactions_0500m'
    PASSENGER_TYPES: str = f'{ORCA_SCHEMA}.passenger_types'
    DIRECTIONS: str = f'{ORCA_SCHEMA}.directions'
    TRANSACTIONS_0500M: str = f'{ORCA_SCHEMA}.transactions_0500m'
    ORGANIZATIONS: str = f'{ORCA_SCHEMA}.organizations'
    TRANSACTIONS_0750M: str = f'{ORCA_SCHEMA}.transactions_0750m'
    TRANSACTIONS_1000M: str = f'{ORCA_SCHEMA}.transactions_1000m'
    LINKED_TRANSACTIONS_0750M: str = f'{ORCA_SCHEMA}.linked_transactions_0750m'
    LINKED_TRANSACTIONS_1000M: str = f'{ORCA_SCHEMA}.linked_transactions_1000m'
    CARD_CENSUS_BLOCK_GROUPS: str = f'{ORCA_SCHEMA}.card_census_block_groups'
    CARDS: str = f'{ORCA_SCHEMA}.cards'
    V_TRANSACTIONS: str = f'{ORCA_SCHEMA}.v_transactions'
    V_BOARDINGS: str = f'{ORCA_SCHEMA}.v_boardings'
    V_ALIGHTINGS: str = f'{ORCA_SCHEMA}.v_alightings'
    M_TXN_TIMERANGES: str = f'{ORCA_SCHEMA}.m_txn_timeranges'
    M_CARD_LATEST_TXN_DTM: str = f'{ORCA_SCHEMA}.m_card_latest_txn_dtm'
    M_LATEST_FILE_UPLOAD: str = f'{ORCA_SCHEMA}.m_latest_file_upload'


class TRAC_SCHEMA_TABLES(Enum):
    """
    Access using TRAC_SCHEMA_TABLES.<table_name>.value
    """
   
    AGENCIES_TABLE: str = f'{TRAC_SCHEMA}.agencies'

    #new
    ST_BUS_OPERATORS: str = f'{TRAC_SCHEMA}.st_bus_operators'
    ROUTE_NAME_LOOKUP: str = f'{TRAC_SCHEMA}.route_name_lookup'
    PARAMETERS: str = f'{TRAC_SCHEMA}.parameters'
    TRANSITLAND_AGENCIES: str = f'{TRAC_SCHEMA}.transitland_agencies'
    MODES: str = f'{TRAC_SCHEMA}.modes'
    AGENCIES: str = f'{TRAC_SCHEMA}.agencies'
    BAD_TRANSACTIONS_0250M: str = f'{TRAC_SCHEMA}.bad_transactions_0250m'
    BAD_TRANSACTIONS_0750M: str = f'{TRAC_SCHEMA}.bad_transactions_0750m'
    BAD_TRANSACTIONS_0500M: str = f'{TRAC_SCHEMA}.bad_transactions_0500m'
    BAD_TRANSACTIONS_1000M: str = f'{TRAC_SCHEMA}.bad_transactions_1000m'
    BAD_TRANSACTIONS: str = f'{TRAC_SCHEMA}.bad_transactions'
    E_GEOCODE_RESULT_TYPES: str = f'{TRAC_SCHEMA}.e_geocode_result_types'
    E_BAD_TRANSACTION_TYPES: str = f'{TRAC_SCHEMA}.e_bad_transaction_types'
    V_PREVIOUS_DUPLICATE_TXN: str = f'{TRAC_SCHEMA}.v_previous_duplicate_txn'


class GTFS_SCHEMA_TABLES(Enum):
    """
    Access using GTFS_SCHEMA_TABLES.<table_name>.value
    """
    FEED_INFO_TABLE: str = f'{GTFS_SCHEMA}.tl_feed_info'
    FEEDS_TABLE: str = f'{GTFS_SCHEMA}.transitland_feeds'
    STOPS_TABLE: str = f'{GTFS_SCHEMA}.tl_stops'
    AGENCY_TABLE: str = f'{GTFS_SCHEMA}.tl_agency'

    ##new
    TRANSITLAND_FEEDS: str = f'{GTFS_SCHEMA}.transitland_feeds'
    TL_TRANSLATIONS: str = f'{GTFS_SCHEMA}.tl_translations'
    TL_NETWORKS: str = f'{GTFS_SCHEMA}.tl_networks'
    TL_FARE_MEDIA: str = f'{GTFS_SCHEMA}.tl_fare_media'
    TL_FARE_RULES: str = f'{GTFS_SCHEMA}.tl_fare_rules'
    E_LOCATION_TYPES: str = f'{GTFS_SCHEMA}.e_location_types'
    TL_TIMEFRAMES: str = f'{GTFS_SCHEMA}.tl_timeframes'
    TL_FARE_PRODUCTS: str = f'{GTFS_SCHEMA}.tl_fare_products'
    E_EXCEPTION_TYPES: str = f'{GTFS_SCHEMA}.e_exception_types'
    E_PAYMENT_METHODS: str = f'{GTFS_SCHEMA}.e_payment_methods'
    E_TRANSFERS: str = f'{GTFS_SCHEMA}.e_transfers'
    E_WHEELCHAIR_BOARDINGS: str = f'{GTFS_SCHEMA}.e_wheelchair_boardings'
    E_DIRECTION_IDS: str = f'{GTFS_SCHEMA}.e_direction_ids'
    E_WHEELCHAIR_ACCESSIBILITY: str = f'{GTFS_SCHEMA}.e_wheelchair_accessibility'
    E_SERVICE_AVAILABILITY: str = f'{GTFS_SCHEMA}.e_service_availability'
    E_ROUTE_TYPES: str = f'{GTFS_SCHEMA}.e_route_types'
    TL_TRIPS: str = f'{GTFS_SCHEMA}.tl_trips'
    E_BIKES_ALLOWED: str = f'{GTFS_SCHEMA}.e_bikes_allowed'
    E_PICKUP_TYPES: str = f'{GTFS_SCHEMA}.e_pickup_types'
    E_EXACT_TIMES: str = f'{GTFS_SCHEMA}.e_exact_times'
    E_DURATION_LIMIT_TYPES: str = f'{GTFS_SCHEMA}.e_duration_limit_types'
    E_TIMEPOINTS: str = f'{GTFS_SCHEMA}.e_timepoints'
    E_TRANSFER_TYPES: str = f'{GTFS_SCHEMA}.e_transfer_types'
    E_FARE_MEDIA_TYPES: str = f'{GTFS_SCHEMA}.e_fare_media_types'
    E_IS_ROLE: str = f'{GTFS_SCHEMA}.e_is_role'
    TL_EXTRA_FILES: str = f'{GTFS_SCHEMA}.tl_extra_files'
    E_IS_BIDIRECTIONAL: str = f'{GTFS_SCHEMA}.e_is_bidirectional'
    TL_AGENCY: str = f'{GTFS_SCHEMA}.tl_agency'
    TL_FEED_INFO: str = f'{GTFS_SCHEMA}.tl_feed_info'
    E_CONTINUOUS_PICKUP: str = f'{GTFS_SCHEMA}.e_continuous_pickup'
    E_CONTINUOUS_DROP_OFF: str = f'{GTFS_SCHEMA}.e_continuous_drop_off'
    TL_CALENDAR: str = f'{GTFS_SCHEMA}.tl_calendar'
    TL_AREAS: str = f'{GTFS_SCHEMA}.tl_areas'
    TL_ROUTES: str = f'{GTFS_SCHEMA}.tl_routes'
    TL_CALENDAR_DATES: str = f'{GTFS_SCHEMA}.tl_calendar_dates'
    E_DROP_OFF_TYPES: str = f'{GTFS_SCHEMA}.e_drop_off_types'
    E_FARE_TRANSFER_TYPES: str = f'{GTFS_SCHEMA}.e_fare_transfer_types'
    TL_FARE_ATTRIBUTES: str = f'{GTFS_SCHEMA}.tl_fare_attributes'
    E_PATHWAY_MODES: str = f'{GTFS_SCHEMA}.e_pathway_modes'
    TL_FARE_LEG_RULES: str = f'{GTFS_SCHEMA}.tl_fare_leg_rules'
    TL_FARE_TRANSFER_RULES: str = f'{GTFS_SCHEMA}.tl_fare_transfer_rules'
    TL_STOP_AREAS: str = f'{GTFS_SCHEMA}.tl_stop_areas'
    TL_ROUTE_NETWORKS: str = f'{GTFS_SCHEMA}.tl_route_networks'
    TL_FREQUENCIES: str = f'{GTFS_SCHEMA}.tl_frequencies'
    TL_TRANSFERS: str = f'{GTFS_SCHEMA}.tl_transfers'
    TL_ATTRIBUTIONS: str = f'{GTFS_SCHEMA}.tl_attributions'
    TL_PATHWAYS: str = f'{GTFS_SCHEMA}.tl_pathways'
    TL_SHAPES: str = f'{GTFS_SCHEMA}.tl_shapes'
    TL_LEVELS: str = f'{GTFS_SCHEMA}.tl_levels'
    TL_STOP_TIMES: str = f'{GTFS_SCHEMA}.tl_stop_times'
    TL_STOPS: str = f'{GTFS_SCHEMA}.tl_stops'
    TL_BAD_FEEDS: str = f'{GTFS_SCHEMA}.tl_bad_feeds'
    V_TRANSITLAND_FEED_INFO: str = f'{GTFS_SCHEMA}.v_transitland_feed_info'


