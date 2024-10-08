"""
This file contains the TransactionsWithLocations class that can be used to get transactions with their stop locations.
Classes
-------
TransactionsWithLocations
    A class to get locations of transactions using customizable logic
"""
import datetime

from sqlalchemy import Engine
from sqlalchemy import Table, Select
from sqlalchemy import func, select, not_, or_, and_, case

from ..constants.schemas import DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA
from ..constants.schema_tables import DSSG_SCHEMA_TABLES, ORCA_SCHEMA_TABLES, TRAC_SCHEMA_TABLES, GTFS_SCHEMA_TABLES
from ...utils.db_helpers import get_automap_base_with_views

class TransactionsWithLocations:
    """
    A class to get locations of transactions using customizable logic.
    Attributes
    ----------
    start_date : datetime
        Earliest possible start date for the transactions. It is imperative to add start_date for performance reasons.
    end_date : datetime
        Earliest possible end date for the transactions. It is imperative to add end_date for performance reasons.
    engine : sqlalchemy.Engine
        Engine that is already connected to a database
    transactions_t : sqlalchemy.Table, optional
        Table object for the transactions table. If not provided, the default orca.transactions table is used
    Methods
    -------
    get_automap_bases :
        Get the automap bases for the schemas of interest
    
    get_latest_gtfs_feed :
        Get the latest GTFS feed for each transit agency
    
    get_stop_with_agency_from_feed :
        Get the stop details based on the given feeds.
        The CRS for the stop location is changed to 4326 to be compatible with the transaction location.
    
    get_transactions_with_agency :
        Get transactions with their agency details.
    
    get_transactions_with_stop_or_device_locations :
        Get transactions with their stop or device locations.
    
    get_transactions_with_stop_or_device_locations_from_latest_gtfs :
        Get transactions with their stop or device locations using the latest GTFS feed.
        Uses logic from get_latest_gtfs_feed, get_stop_with_agency_from_feed and 
        get_transactions_with_stop_or_device_locations.
    """
    STOP_LOCATION_TRANSFORMED_KEY = 'stop_location_transformed'
    TRANSACTION_LOCATION_KEY = 'transaction_location'
    STOP_CRS = 32610

    def __init__(self, start_date: datetime, end_date: datetime, engine: Engine, transactions_t: Table | None = None):
        self.start_date = start_date
        self.end_date = end_date
        self.engine = engine
        self.get_automap_bases()
        if transactions_t is None:
            transactions_t = self.Base_orca.metadata.tables[ORCA_SCHEMA_TABLES.TRANSACTIONS.value]
        self.transactions_t = transactions_t

    def get_automap_bases(self):
        """
        Get the automap bases for the schemas of interest
        """
        self.Base_dssg = get_automap_base_with_views(engine=self.engine, schema=DSSG_SCHEMA)
        self.Base_trac = get_automap_base_with_views(engine=self.engine, schema=TRAC_SCHEMA)
        self.Base_orca = get_automap_base_with_views(engine=self.engine, schema=ORCA_SCHEMA)
        self.Base_gtfs = get_automap_base_with_views(engine=self.engine, schema=GTFS_SCHEMA)

    def get_latest_gtfs_feed(self) -> Select:
        """
        This function returns a query that can be used to get the latest GTFS feed for each transit agency.
        Returns
        -------
        select : sqlalchemy.sql.selectable.Select
            A select query that can be used to get the latest GTFS feed for each transit agency
        """
        # feed_info = self.Base_gtfs.metadata.tables[GTFS_SCHEMA_TABLES.TL_FEED_INFO.value]
        feeds = self.Base_gtfs.metadata.tables[GTFS_SCHEMA_TABLES.TRANSITLAND_FEEDS.value]

        # Get the feeds only for the given date range
        stmt_gtfs_feed = \
            select(feeds)\
            .where(not_(or_(feeds.c.earliest_calendar_date >= self.end_date, 
                            feeds.c.latest_calendar_date <= self.start_date)))

        stmt_gtfs_feed_alias = stmt_gtfs_feed.subquery('feed')

        # Rank the feeds for the given date range
        stmt_gtfs_feed_ranked = \
        select(stmt_gtfs_feed_alias, func.row_number().over(
            partition_by=stmt_gtfs_feed_alias.c.agency_id,
            order_by=stmt_gtfs_feed_alias.c.feed_id.desc()).label('feed_rank'))

        stmt_gtfs_feed_ranked_alias = stmt_gtfs_feed_ranked.subquery('feed_ranked')

        # Finally, get latest feed within the date range, for each transit agency, to get the feed_latest CTE
        stmt_gtfs_feed_latest = \
            select(stmt_gtfs_feed_ranked_alias)\
            .where(stmt_gtfs_feed_ranked_alias.c.feed_rank == 1)

        return stmt_gtfs_feed_latest

    def get_stop_with_agency_from_feed(self, stmt_gtfs_feed: Select) -> Select:
        """
        This function returns a query that can be used to get the stop details based on the given feeds.
        Thus, contains gtfs agency details as well (including gtfs agency id).
        The CRS for the stop location is changed to 4326 to be compatible with the transaction location.
        Parameters
        ----------
        stmt_gtfs_feed : sqlalchemy.sql.selectable.Select
            A select query that can be used to get relevant GTFS feeds based on customizable logic
        Returns
        -------
        select : sqlalchemy.sql.selectable.Select
            A select query that can be used to get the stop details based on the given feeds.
            The CRS for the stop location is changed to 4326 to be compatible with the transaction location.
        """
        stops = self.Base_gtfs.metadata.tables[GTFS_SCHEMA_TABLES.TL_STOPS.value]
        agencies_gtfs = self.Base_gtfs.metadata.tables[GTFS_SCHEMA_TABLES.TL_AGENCY.value]

        stmt_gtfs_feed_alias = stmt_gtfs_feed.cte('feed_custom')

        stmt_stop_with_agency = \
            select(stops, func.ST_TRANSFORM(stops.c.stop_location, self.STOP_CRS).label(self.STOP_LOCATION_TRANSFORMED_KEY), 
                   agencies_gtfs.c.agency_id, agencies_gtfs.c.agency_name)\
            .join(stmt_gtfs_feed_alias, stops.c.feed_id == stmt_gtfs_feed_alias.c.feed_id)\
            .join(agencies_gtfs, stmt_gtfs_feed_alias.c.feed_id == agencies_gtfs.c.feed_id)

        return stmt_stop_with_agency

    def get_transactions_with_agency(self) -> Select:
        """
        This function returns a query that can be used to get transactions 
        Returns
        -------
        select : sqlalchemy.sql.selectable.Select
            A select query that can be used to get transactions with their agency details
        """
        agencies = self.Base_trac.metadata.tables[TRAC_SCHEMA_TABLES.AGENCIES.value]
        stmt_transactions_with_agency = \
            select(self.transactions_t, agencies.c.agency_id, agencies.c.orca_agency_id, agencies.c.gtfs_agency_id, agencies.c.agency_name)\
            .join(agencies, self.transactions_t.c.source_agency_id == agencies.c.orca_agency_id)
        return stmt_transactions_with_agency

    def get_transactions_with_stop_or_device_locations(self, stmt_stop_with_agency: Select) -> Select:
        """
        This function returns a query that can be used to get transactions with their stop or device locations.
        The stop location is used as the transaction location if present in stmt_stop_with_agency, 
            else the device location is used.
        Parameters
        ----------
        stmt_stop_with_agency : sqlalchemy.sql.selectable.Select
            A select query that can be used to get stop location details based on customizable logic
            Based on current implementation, this should be (or compatible with) the output of get_stop_with_agency_from_feed
        """
        stmt_transactions_with_agency = self.get_transactions_with_agency()
        stmt_transactions_with_agency_alias = stmt_transactions_with_agency.cte('transactions_with_agency')
        # stmt_transactions_with_agency_and_location = \
        #     select(stmt_transactions_with_agency_alias)\
        #     .where(not_(and_(self.transactions_t.c.stop_id.is_(None), self.transactions_t.c.device_location.is_(None))))
        stmt_stop_with_agency_alias = stmt_stop_with_agency.cte('stop_custom')

        # TODO: Add functionality to rename common columns in the second cte
        # Currently, the following statement has a glaring issue.
        # The ctes stmt_transactions_with_agency_alias and stmt_stop_with_agency_alias
        # Have columns with the same name. SqlAlchemy handles this by appending _1 to the column names of the second cte.
        # This is not very human readable and can cause confusion.
        stmt_transactions_with_location = \
            select(stmt_transactions_with_agency_alias,
                case((getattr(stmt_stop_with_agency_alias.c, self.STOP_LOCATION_TRANSFORMED_KEY).is_not(None), 
                      getattr(stmt_stop_with_agency_alias.c, self.STOP_LOCATION_TRANSFORMED_KEY)),
                    else_=stmt_transactions_with_agency_alias.c.device_location).label(self.TRANSACTION_LOCATION_KEY),
                stmt_stop_with_agency_alias)\
            .join(stmt_stop_with_agency_alias,
                and_(stmt_transactions_with_agency_alias.c.stop_code == stmt_stop_with_agency_alias.c.stop_id,
                    stmt_transactions_with_agency_alias.c.gtfs_agency_id == stmt_stop_with_agency_alias.c.agency_id),
                    isouter=True)

        return stmt_transactions_with_location

    def get_transactions_with_stop_or_device_locations_from_latest_gtfs(self) -> Select:
        """
        This function returns a query that can be used to get transactions with their stop or device locations.
        The stop location is used as the transaction location if present in the latest GTFS feed, 
            else the device location is used.
        Returns
        -------
        select : sqlalchemy.sql.selectable.Select
            A select query that can be used to get transactions with their stop or device locations
            The CRS for the transaction location is 4326
        
        Example
        -------
        Example 1:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('postgresql://user:password@localhost:5432/dbname'))
        >>> transactions_t = Base_orca.metadata.tables['transactions']
        >>> transactions_with_locations = TransactionsWithLocations(
        ...     start_date=datetime.datetime(2023, 4, 1),
        ...     end_date=datetime.datetime(2023, 4, 30),
        ...     engine=engine,
        ...     transactions_t=transactions_t
        ... )
        >>> query = transactions_with_locations.get_transactions_with_stop_or_device_locations_from_latest_gtfs()
        >>> print(type(query))
        """
        stmt_gtfs_feed_latest = self.get_latest_gtfs_feed()
        stmt_stop_with_agency = self.get_stop_with_agency_from_feed(stmt_gtfs_feed_latest)
        return self.get_transactions_with_stop_or_device_locations(stmt_stop_with_agency)