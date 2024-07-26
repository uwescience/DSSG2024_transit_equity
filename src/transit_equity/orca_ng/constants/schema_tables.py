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
    TRANSACTIONS_MAT_VIEW: str = f'{DSSG_SCHEMA}.m_transactions_apr2023'

    #new
    V_BOARDINGS_APR2023: str = f'{ DSSG_SCHEMA}.v_boardings_apr2023'
    M_TXN_IDS_APR2023: str = f'{DSSG_SCHEMA}.m_txn_ids_apr2023'
    M_TRANSACTIONS_APR2023: str = f'{DSSG_SCHEMA}.m_transactions_apr2023'


class ORCA_SCHEMA_TABLES(Enum):
    """
    Access using ORCA_SCHEMA_TABLES.<table_name>.value
    """
    TRANSACTIONS_TABLE: str = f'{ORCA_SCHEMA}.transactions',
    TRANSACTION_TYPES_TABLE: str = f'{ORCA_SCHEMA}.transaction_types',
    MODES_TABLE: str = f'{ORCA_SCHEMA}.modes'

    ##new
    DATA_UPLOADS: str = f'{ ORCA_SCHEMA}.data_uploads'
    TRANSACTIONS: str = f'{ ORCA_SCHEMA}.transactions'
    TRANSACTION_TYPES: str = f'{ ORCA_SCHEMA}.transaction_types'
    LINKED_TRANSACTIONS: str = f'{ ORCA_SCHEMA}.linked_transactions'
    MODES: str = f'{ ORCA_SCHEMA}.modes'
    H_TRANSACTIONS: str = f'{ ORCA_SCHEMA}.h_transactions'
    CARDS: str = f'{ ORCA_SCHEMA}.cards'
    PASSENGER_TYPES: str = f'{ ORCA_SCHEMA}.passenger_types'
    ORGANIZATIONS: str = f'{ ORCA_SCHEMA}.organizations'
    DIRECTIONS: str = f'{ ORCA_SCHEMA}.directions'
    PARTICIPANT_GROUPS: str = f'{ ORCA_SCHEMA}.participant_groups'
    STOPS: str = f'{ ORCA_SCHEMA}.stops'
    PRODUCTS: str = f'{ ORCA_SCHEMA}.products'
    TRANSACTIONS_300M: str = f'{ ORCA_SCHEMA}.transactions_300m'
    TRANSACTIONS_400M: str = f'{ ORCA_SCHEMA}.transactions_400m'
    TRANSACTIONS_100M: str = f'{ ORCA_SCHEMA}.transactions_100m'
    TRANSACTIONS_200M: str = f'{ ORCA_SCHEMA}.transactions_200m'
    LINKED_TRANSACTIONS_100M: str = f'{ ORCA_SCHEMA}.linked_transactions_100m'
    LINKED_TRANSACTIONS_200M: str = f'{ ORCA_SCHEMA}.linked_transactions_200m'
    LINKED_TRANSACTIONS_300M: str = f'{ ORCA_SCHEMA}.linked_transactions_300m'
    LINKED_TRANSACTIONS_400M: str = f'{ ORCA_SCHEMA}.linked_transactions_400m'
    V_TRANSACTIONS: str = f'{ ORCA_SCHEMA}.v_transactions'
    V_ALIGHTINGS: str = f'{ ORCA_SCHEMA}.v_alightings'
    V_BOARDINGS: str = f'{ ORCA_SCHEMA}.v_boardings'
    V_LINKED_TRANSACTIONS: str = f'{ ORCA_SCHEMA}.v_linked_transactions'
    V_FINANCIAL_XFER_INFO: str = f'{ ORCA_SCHEMA}.v_financial_xfer_info'
    V_ORCA_TRANSFER: str = f'{ ORCA_SCHEMA}.v_orca_transfer'
    M_CARD_LATEST_TXN_DTM: str = f'{ ORCA_SCHEMA}.m_card_latest_txn_dtm'
    M_TRANSACTION_DATES: str = f'{ ORCA_SCHEMA}.m_transaction_dates'


class TRAC_SCHEMA_TABLES(Enum):
    """
    Access using TRAC_SCHEMA_TABLES.<table_name>.value
    """

    AGENCIES_TABLE: str = f'{TRAC_SCHEMA}.agencies'

    ##new
    BAD_TRANSACTIONS: str = f'{ TRAC_SCHEMA}.bad_transactions'
    AGENCIES: str = f'{ TRAC_SCHEMA}.agencies'
    BAD_TRANSACTION_TYPES: str = f'{ TRAC_SCHEMA}.bad_transaction_types'
    BAD_TRANSACTIONS_200M: str = f'{ TRAC_SCHEMA}.bad_transactions_200m'
    DIRECTION_UPDATE_NOTE: str = f'{ TRAC_SCHEMA}.direction_update_note'
    ROUTE_NAME_LOOKUP: str = f'{ TRAC_SCHEMA}.route_name_lookup'
    STOP_UPDATE_NOTE: str = f'{ TRAC_SCHEMA}.stop_update_note'
    BAD_TRANSACTIONS_100M: str = f'{ TRAC_SCHEMA}.bad_transactions_100m'
    BAD_TRANSACTIONS_300M: str = f'{ TRAC_SCHEMA}.bad_transactions_300m'
    BAD_TRANSACTIONS_400M: str = f'{ TRAC_SCHEMA}.bad_transactions_400m'
    V_PREVIOUS_DUPLICATE_TXN: str = f'{ TRAC_SCHEMA}.v_previous_duplicate_txn'


class GTFS_SCHEMA_TABLES(Enum):
    """
    Access using GTFS_SCHEMA_TABLES.<table_name>.value
    """

    FEED_INFO_TABLE: str = f'{GTFS_SCHEMA}.tl_feed_info'
    FEEDS_TABLE: str = f'{GTFS_SCHEMA}.transitland_feeds'
    STOPS_TABLE: str = f'{GTFS_SCHEMA}.tl_stops'
    AGENCY_TABLE: str = f'{GTFS_SCHEMA}.tl_agency'

    #new
    E_CONTINUOUS_DROP_OFF: str = f'{GTFS_SCHEMA}.e_continuous_drop_off'
    E_CONTINUOUS_PICKUP: str = f'{GTFS_SCHEMA}.e_continuous_pickup'
    E_DROP_OFF_TYPES: str = f'{GTFS_SCHEMA}.e_drop_off_types'
    E_BIKES_ALLOWED: str = f'{GTFS_SCHEMA}.e_bikes_allowed'
    E_DIRECTION_IDS: str = f'{GTFS_SCHEMA}.e_direction_ids'
    E_FARE_TRANSFER_TYPES: str = f'{GTFS_SCHEMA}.e_fare_transfer_types'
    E_IS_BIDIRECTIONAL: str = f'{GTFS_SCHEMA}.e_is_bidirectional'
    E_SERVICE_AVAILABILITY: str = f'{GTFS_SCHEMA}.e_service_availability'
    E_DURATION_LIMIT_TYPES: str = f'{GTFS_SCHEMA}.e_duration_limit_types'
    E_EXACT_TIMES: str = f'{GTFS_SCHEMA}.e_exact_times'
    E_PATHWAY_MODES: str = f'{GTFS_SCHEMA}.e_pathway_modes'
    E_EXCEPTION_TYPES: str = f'{GTFS_SCHEMA}.e_exception_types'
    E_TIMEPOINTS: str = f'{GTFS_SCHEMA}.e_timepoints'
    E_ROUTE_TYPES: str = f'{GTFS_SCHEMA}.e_route_types'
    E_FARE_MEDIA_TYPES: str = f'{GTFS_SCHEMA}.e_fare_media_types'
    E_PICKUP_TYPES: str = f'{GTFS_SCHEMA}.e_pickup_types'
    E_PAYMENT_METHODS: str = f'{GTFS_SCHEMA}.e_payment_methods'
    E_IS_ROLE: str = f'{GTFS_SCHEMA}.e_is_role'
    E_LOCATION_TYPES: str = f'{GTFS_SCHEMA}.e_location_types'
    E_WHEELCHAIR_ACCESSIBILITY: str = f'{GTFS_SCHEMA}.e_wheelchair_accessibility'
    TL_FARE_MEDIA: str = f'{GTFS_SCHEMA}.tl_fare_media'
    E_TRANSFER_TYPES: str = f'{GTFS_SCHEMA}.e_transfer_types'
    TL_AGENCY: str = f'{GTFS_SCHEMA}.tl_agency'
    TL_AREAS: str = f'{GTFS_SCHEMA}.tl_areas'
    TL_CALENDAR: str = f'{GTFS_SCHEMA}.tl_calendar'
    TL_CALENDAR_DATES: str = f'{GTFS_SCHEMA}.tl_calendar_dates'
    TL_BAD_FEEDS: str = f'{GTFS_SCHEMA}.tl_bad_feeds'
    TL_FARE_ATTRIBUTES: str = f'{GTFS_SCHEMA}.tl_fare_attributes'
    TL_EXTRA_FILES: str = f'{GTFS_SCHEMA}.tl_extra_files'
    E_TRANSFERS: str = f'{GTFS_SCHEMA}.e_transfers'
    TL_FARE_LEG_RULES: str = f'{GTFS_SCHEMA}.tl_fare_leg_rules'
    TL_ATTRIBUTIONS: str = f'{GTFS_SCHEMA}.tl_attributions'
    E_WHEELCHAIR_BOARDINGS: str = f'{GTFS_SCHEMA}.e_wheelchair_boardings'
    TL_FARE_PRODUCTS: str = f'{GTFS_SCHEMA}.tl_fare_products'
    TL_FARE_RULES: str = f'{GTFS_SCHEMA}.tl_fare_rules'
    TL_FREQUENCIES: str = f'{GTFS_SCHEMA}.tl_frequencies'
    TL_FEED_INFO: str = f'{GTFS_SCHEMA}.tl_feed_info'
    TL_PATHWAYS: str = f'{GTFS_SCHEMA}.tl_pathways'
    TL_LEVELS: str = f'{GTFS_SCHEMA}.tl_levels'
    TL_NETWORKS: str = f'{GTFS_SCHEMA}.tl_networks'
    TL_ROUTES: str = f'{GTFS_SCHEMA}.tl_routes'
    TL_SHAPES: str = f'{GTFS_SCHEMA}.tl_shapes'
    TL_ROUTE_NETWORKS: str = f'{GTFS_SCHEMA}.tl_route_networks'
    TL_STOP_TIMES: str = f'{GTFS_SCHEMA}.tl_stop_times'
    TL_STOP_AREAS: str = f'{GTFS_SCHEMA}.tl_stop_areas'
    TL_STOPS: str = f'{GTFS_SCHEMA}.tl_stops'
    TL_FARE_TRANSFER_RULES: str = f'{GTFS_SCHEMA}.tl_fare_transfer_rules'
    TL_TIMEFRAMES: str = f'{GTFS_SCHEMA}.tl_timeframes'
    TL_TRIPS: str = f'{GTFS_SCHEMA}.tl_trips'
    TL_TRANSLATIONS: str = f'{GTFS_SCHEMA}.tl_translations'
    TRANSITLAND_AGENCIES: str = f'{GTFS_SCHEMA}.transitland_agencies'
    TL_TRANSFERS: str = f'{GTFS_SCHEMA}.tl_transfers'
    TRANSITLAND_FEEDS: str = f'{GTFS_SCHEMA}.transitland_feeds'
    V_TRANSITLAND_FEED_INFO: str = f'{GTFS_SCHEMA}.v_transitland_feed_info'
