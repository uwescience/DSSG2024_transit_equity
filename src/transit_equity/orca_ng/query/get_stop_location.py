import datetime

from sqlalchemy import Table, Select, func, select, not_, or_, and_, case
from sqlalchemy.ext.automap import AutomapBase

from . import get_schema_key
from ..constants.schemas import DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA
from ..constants.schema_tables import DSSG_SCHEMA_TABLES, ORCA_SCHEMA_TABLES, TRAC_SCHEMA_TABLES, GTFS_SCHEMA_TABLES

def get_stop_locations_from_transactions_and_latest_gtfs(start_date: datetime, end_date: datetime, 
    automap_base_dict: dict, transactions_t: Table | None = None) -> Select:
    '''
    This function returns a query that can be used to get transactions with their stop locations.
    The transactions table is joined with the gtfs stop locations data.
    For each stop, we get the latest GTFS feed for each transit agency and assign the stop location from that feed.

    Parameters
    ----------
    start_date : datetime
        Earliest possible start date for the transactions. It is imperative to add start_date for performance reasons.
    end_date : datetime
        Earliest possible end date for the transactions. It is imperative to add end_date for performance reasons.
    automap_base_dict : dict
        A dictionary containing the automap base objects for the schemas of interest
        The keys are the schema names and the values are the automap base objects
        Naming convention for key: f'Base_{schema_name_in_lowercase}'
            Use transit_equity.orca_ng.query.get_schema_key if unsure
    transactions_t : sqlalchemy.Table, optional
        Table object for the transactions table. If not provided, the default orca.transactions table is used
    
    Returns
    -------
    select : sqlalchemy.sql.selectable.Select
        A select query that can be used to get transactions with their stop locations
    
    Examples
    --------
    Example 1:
    >>> from sqlalchemy import create_engine
    >>> engine = create_engine('postgresql://user:password@localhost:5432/dbname'))
    >>> Base = get_automap_base_with_views(engine=engine, schema='orca')
    >>> transactions_t = Base_orca.metadata.tables['transactions']
    >>> query = get_stop_locations_from_transactions_and_latest_gtfs(
    ...     start_date=datetime.datetime(2023, 4, 1),
    ...     end_date=datetime.datetime(2023, 4, 30),
    ...     automap_base_dict={'Base_orca': Base_orca},
    ...     transactions_t=transactions_t
    ... )
    >>> print(type(query))
    '''
    # Keys for schemas of interest
    schemas_required = [DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA]
    schema_keys = [get_schema_key(schema_name) for schema_name in schemas_required]
    Base_dssg: AutomapBase = automap_base_dict[get_schema_key(DSSG_SCHEMA)]
    Base_trac: AutomapBase = automap_base_dict[get_schema_key(TRAC_SCHEMA)]
    Base_orca: AutomapBase = automap_base_dict[get_schema_key(ORCA_SCHEMA)]
    Base_gtfs: AutomapBase = automap_base_dict[get_schema_key(GTFS_SCHEMA)]

    if transactions_t is None:
        transactions_t = Base_orca.metadata.tables[ORCA_SCHEMA_TABLES.TRANSACTIONS_TABLE]
    
    agencies = Base_trac.metadata.tables[TRAC_SCHEMA_TABLES.AGENCIES_TABLE.value]
    modes = Base_orca.metadata.tables[ORCA_SCHEMA_TABLES.MODES_TABLE.value]
    feed_info = Base_gtfs.metadata.tables[GTFS_SCHEMA_TABLES.FEED_INFO_TABLE.value]
    stops = Base_gtfs.metadata.tables[GTFS_SCHEMA_TABLES.STOPS_TABLE.value]
    agencies_gtfs = Base_gtfs.metadata.tables[GTFS_SCHEMA_TABLES.AGENCY_TABLE.value]

    # Get the feeds only for the given date range
    stmt_gtfs_feed = \
        select(feed_info)\
        .where(not_(or_(feed_info.c.feed_start_date >= start_date, 
                        feed_info.c.feed_end_date <= end_date)))

    stmt_gtfs_feed_alias = stmt_gtfs_feed.subquery('feed')

    # Rank the feeds for the given date range
    stmt_gtfs_feed_ranked = \
    select(stmt_gtfs_feed_alias, func.row_number().over(
        partition_by=stmt_gtfs_feed_alias.c.feed_publisher_name,
        order_by=stmt_gtfs_feed_alias.c.feed_id.desc()).label('feed_rank'))

    stmt_gtfs_feed_ranked_alias = stmt_gtfs_feed_ranked.subquery('feed_ranked')

    # Finally, get latest feed within the date range, for each transit agency, to get the feed_latest CTE
    stmt_gtfs_feed_latest = \
        select(stmt_gtfs_feed_ranked_alias)\
        .where(stmt_gtfs_feed_ranked_alias.c.feed_rank == 1)

    stmt_gtfs_feed_latest_alias = stmt_gtfs_feed_latest.cte('feed_latest')

    # Use the feed_latest CTE to get all the stop details based on the latest feed, to get the stop_latest CTE
    stmt_stop_latest = \
        select(stops, agencies_gtfs.c.agency_id, agencies_gtfs.c.agency_name)\
        .join(stmt_gtfs_feed_latest_alias, stops.c.feed_id == stmt_gtfs_feed_latest_alias.c.feed_id)\
        .join(agencies_gtfs, stmt_gtfs_feed_latest_alias.c.feed_id == agencies_gtfs.c.feed_id)

    # Get all the transactions that have either the device location or the stop code, to get the transactions_with_agency CTE
    stmt_transactions_with_agency = \
        select(transactions_t, agencies.c.agency_id, agencies.c.orca_agency_id, agencies.c.gtfs_agency_id, agencies.c.agency_name)\
        .join(agencies, transactions_t.c.source_agency_id == agencies.c.orca_agency_id)\
        .where(not_(and_(transactions_t.c.stop_id.is_(None), transactions_t.c.device_location.is_(None))))

    stmt_stop_latest_alias = stmt_stop_latest.cte('stop_latest')
    stmt_transactions_with_agency_alias = stmt_transactions_with_agency.cte('transactions_with_agency')

    # Combine the transactions_with_agency CTE data with stop_latest CTE data to get the locations of each transaction
    stmt_transactions_with_location = \
    select(stmt_transactions_with_agency_alias,
        case((stmt_stop_latest_alias.c.stop_location.is_not(None), stmt_stop_latest_alias.c.stop_location),
            else_=stmt_transactions_with_agency_alias.c.device_location).label('transaction_location'),
        stmt_stop_latest_alias)\
        .join(stmt_stop_latest_alias,
            and_(stmt_transactions_with_agency_alias.c.stop_code == stmt_stop_latest_alias.c.stop_id,
                stmt_transactions_with_agency_alias.c.gtfs_agency_id == stmt_stop_latest_alias.c.agency_id),
                isouter=True)

    stmt_transactions_with_location_alias = stmt_transactions_with_location.subquery('transactions_with_location')

    # Remove all the null entries (these would mostly come from any ORCA stop code that does not match with a GTFS stop id.)
    stmt_transactions_with_location_not_null = \
        select(stmt_transactions_with_location_alias)\
        .where(stmt_transactions_with_location_alias.c.transaction_location.is_not(None))

    return stmt_transactions_with_location_not_null
