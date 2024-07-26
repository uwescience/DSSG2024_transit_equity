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
    TRANSACTIONS_MAT_VIEW: str = 'm_transactions_apr2023'

    ##new
    V_BOARDINGS_APR2023: str ='v_boardings_apr2023'
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
    DATA_UPLOADS: str ='data_uploads'
    TRANSACTIONS: str ='transactions'
    TRANSACTION_TYPES: str ='transaction_types'
    LINKED_TRANSACTIONS: str ='linked_transactions'
    MODES: str ='modes'
    H_TRANSACTIONS: str ='h_transactions'
    CARDS: str ='cards'
    PASSENGER_TYPES: str ='passenger_types'
    ORGANIZATIONS: str ='organizations'
    DIRECTIONS: str ='directions'
    PARTICIPANT_GROUPS: str ='participant_groups'
    STOPS: str ='stops'
    PRODUCTS: str ='products'
    TRANSACTIONS_300M: str ='transactions_300m'
    TRANSACTIONS_400M: str ='transactions_400m'
    TRANSACTIONS_100M: str ='transactions_100m'
    TRANSACTIONS_200M: str ='transactions_200m'
    LINKED_TRANSACTIONS_100M: str ='linked_transactions_100m'
    LINKED_TRANSACTIONS_200M: str ='linked_transactions_200m'
    LINKED_TRANSACTIONS_300M: str ='linked_transactions_300m'
    LINKED_TRANSACTIONS_400M: str ='linked_transactions_400m'
    V_TRANSACTIONS: str ='v_transactions'
    V_ALIGHTINGS: str ='v_alightings'
    V_BOARDINGS: str ='v_boardings'
    V_LINKED_TRANSACTIONS: str ='v_linked_transactions'
    V_FINANCIAL_XFER_INFO: str ='v_financial_xfer_info'
    V_ORCA_TRANSFER: str ='v_orca_transfer'
    M_CARD_LATEST_TXN_DTM: str ='m_card_latest_txn_dtm'
    M_TRANSACTION_DATES: str ='m_transaction_dates'


class TRAC_TABLES(Enum):
    """
    Access using TRAC_TABLES.<table_name>.value
    """

    AGENCIES_TABLE: str = 'agencies'
    #new
    BAD_TRANSACTIONS: str ='bad_transactions'
    AGENCIES: str ='agencies'
    BAD_TRANSACTION_TYPES: str ='bad_transaction_types'
    BAD_TRANSACTIONS_200M: str ='bad_transactions_200m'
    DIRECTION_UPDATE_NOTE: str ='direction_update_note'
    ROUTE_NAME_LOOKUP: str ='route_name_lookup'
    STOP_UPDATE_NOTE: str ='stop_update_note'
    BAD_TRANSACTIONS_100M: str ='bad_transactions_100m'
    BAD_TRANSACTIONS_300M: str ='bad_transactions_300m'
    BAD_TRANSACTIONS_400M: str ='bad_transactions_400m'
    V_PREVIOUS_DUPLICATE_TXN: str ='v_previous_duplicate_txn'



class GTFS_TABLES(Enum):
    """
    Access using GTFS_TABLES.<table_name>.value
    """

    FEED_INFO_TABLE: str = 'tl_feed_info'
    FEEDS_TABLE: str = 'transitland_feeds'
    STOPS_TABLE: str = 'tl_stops'
    AGENCY_TABLE: str = 'tl_agency'

    # new
    E_CONTINUOUS_DROP_OFF: str ='e_continuous_drop_off'
    E_CONTINUOUS_PICKUP: str ='e_continuous_pickup'
    E_DROP_OFF_TYPES: str ='e_drop_off_types'
    E_BIKES_ALLOWED: str ='e_bikes_allowed'
    E_DIRECTION_IDS: str ='e_direction_ids'
    E_FARE_TRANSFER_TYPES: str ='e_fare_transfer_types'
    E_IS_BIDIRECTIONAL: str ='e_is_bidirectional'
    E_SERVICE_AVAILABILITY: str ='e_service_availability'
    E_DURATION_LIMIT_TYPES: str ='e_duration_limit_types'
    E_EXACT_TIMES: str ='e_exact_times'
    E_PATHWAY_MODES: str ='e_pathway_modes'
    E_EXCEPTION_TYPES: str ='e_exception_types'
    E_TIMEPOINTS: str ='e_timepoints'
    E_ROUTE_TYPES: str ='e_route_types'
    E_FARE_MEDIA_TYPES: str ='e_fare_media_types'
    E_PICKUP_TYPES: str ='e_pickup_types'
    E_PAYMENT_METHODS: str ='e_payment_methods'
    E_IS_ROLE: str ='e_is_role'
    E_LOCATION_TYPES: str ='e_location_types'
    E_WHEELCHAIR_ACCESSIBILITY: str ='e_wheelchair_accessibility'
    TL_FARE_MEDIA: str ='tl_fare_media'
    E_TRANSFER_TYPES: str ='e_transfer_types'
    TL_AGENCY: str ='tl_agency'
    TL_AREAS: str ='tl_areas'
    TL_CALENDAR: str ='tl_calendar'
    TL_CALENDAR_DATES: str ='tl_calendar_dates'
    TL_BAD_FEEDS: str ='tl_bad_feeds'
    TL_FARE_ATTRIBUTES: str ='tl_fare_attributes'
    TL_EXTRA_FILES: str ='tl_extra_files'
    E_TRANSFERS: str ='e_transfers'
    TL_FARE_LEG_RULES: str ='tl_fare_leg_rules'
    TL_ATTRIBUTIONS: str ='tl_attributions'
    E_WHEELCHAIR_BOARDINGS: str ='e_wheelchair_boardings'
    TL_FARE_PRODUCTS: str ='tl_fare_products'
    TL_FARE_RULES: str ='tl_fare_rules'
    TL_FREQUENCIES: str ='tl_frequencies'
    TL_FEED_INFO: str ='tl_feed_info'
    TL_PATHWAYS: str ='tl_pathways'
    TL_LEVELS: str ='tl_levels'
    TL_NETWORKS: str ='tl_networks'
    TL_ROUTES: str ='tl_routes'
    TL_SHAPES: str ='tl_shapes'
    TL_ROUTE_NETWORKS: str ='tl_route_networks'
    TL_STOP_TIMES: str ='tl_stop_times'
    TL_STOP_AREAS: str ='tl_stop_areas'
    TL_STOPS: str ='tl_stops'
    TL_FARE_TRANSFER_RULES: str ='tl_fare_transfer_rules'
    TL_TIMEFRAMES: str ='tl_timeframes'
    TL_TRIPS: str ='tl_trips'
    TL_TRANSLATIONS: str ='tl_translations'
    TRANSITLAND_AGENCIES: str ='transitland_agencies'
    TL_TRANSFERS: str ='tl_transfers'
    TRANSITLAND_FEEDS: str ='transitland_feeds'
    V_TRANSITLAND_FEED_INFO: str ='v_transitland_feed_info'

