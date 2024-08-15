%load_ext autoreload
%autoreload 2
%reload_ext autoreload

import os
import sys
import datetime
from pprint import pprint
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
from census import Census
import us
from shapely import wkb
import binascii
import contextily as ctx
from geodatasets import get_path


from sqlalchemy import create_engine, inspect
from sqlalchemy import func, case, desc, or_, and_, not_
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Row
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.orm import aliased
from sqlalchemy.ext.automap import automap_base, AutomapBase
from sqlalchemy import extract
from sqlalchemy import text
from sqlalchemy import cast, Date
from sqlalchemy import inspect
from sqlalchemy import between
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func, extract, case, literal
from sqlalchemy.sql import select, union_all

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from geodatasets import get_path



from transit_equity.utils.db_helpers import get_engine_from_env, get_automap_base_with_views
from transit_equity.orca_ng.constants.schemas import DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA
from transit_equity.orca_ng.constants.schema_tables import DSSG_SCHEMA_TABLES, ORCA_SCHEMA_TABLES, TRAC_SCHEMA_TABLES, GTFS_SCHEMA_TABLES
from transit_equity.orca_ng.query.get_stop_location import get_stop_locations_from_transactions_and_latest_gtfs

##import the helper functions
import check_query_helper as cqh

from sqlalchemy import and_, func, extract, case, literal
from sqlalchemy.sql import select,text 
session.close()
# Define the base query

def create_base_query(session, boardings_v, linked_transactions, cards,
                      last_hash = '%0', start_date = '2023-03-01', 
                      end_date = '2023-05-31', morning_start = 5, morning_end = 10,
                      afternoon_start = 15, afternoon_end = 19, evening_start = 20, evening_end = 23,
                      night_start = 0, night_end = 3):   
    '''
    This function creates the base query for the classification of users based on the following criteria:
  
    Parameters
    ----------
    session : sqlalchemy.orm.session.Session
        The session object to use for the query
    boardings_v : sqlalchemy.Table
        The boardings view table
    linked_transactions : sqlalchemy.Table
        The linked transactions table
    cards : sqlalchemy.Table
        The cards table

    Returns
    -------
    sqlalchemy.sql.selectable.Select
        The base query for the classification
    '''
    base_query = select(
            boardings_v.c.card_id,
            # boardings_v.c.device_dtm_pacific,
            func.date(boardings_v.c.device_dtm_pacific).label('date'),
            extract('DOW',boardings_v.c.device_dtm_pacific).label('weekday'),
            cast(boardings_v.c.device_dtm_pacific,Date),  
            (boardings_v.c.device_lat/1000000).label('device_lat1') ,
        (boardings_v.c.device_lng/1000000).label('device_lng1'),
        boardings_v.c.passenger_type_id, 
        boardings_v.c.route_number,
        cards.c.csn_serial_hash,
            case(
                    (extract('hour', boardings_v.c.device_dtm_pacific).between(morning_start, morning_end), 'morning'),
                    (extract('hour', boardings_v.c.device_dtm_pacific).between(morning_end+0.1, afternoon_start-0.1), 'noon'),
                    (extract('hour', boardings_v.c.device_dtm_pacific).between(afternoon_start, afternoon_end), 'afternoon'),
                    (extract('hour', boardings_v.c.device_dtm_pacific).between(evening_start, evening_end), 'evening'),
                    (extract('hour', boardings_v.c.device_dtm_pacific).between(night_start, night_end), 'middle_of_night'),
                    else_= 'pre_dawn'
            ).label('time_of_day'))\
            .where(linked_transactions.c.is_orca_transfer == False, 
                cast(cards.c.csn_serial_hash, String).like('%0'),
                boardings_v.c.business_date.between(start_date, end_date)
                )\
            .join(linked_transactions, linked_transactions.c.txn_id == boardings_v.c.txn_id)\
            .join(cards, cards.c.card_id == boardings_v.c.card_id)\
    .subquery('base_query')
    return base_query




    

# ###test on getting the classification results
# session.close()
# base = get_results(session, select(base_query).limit(10))
# classfied = get_results(session, select(combined_groups))

def classify_user(session, base_query):
    '''
    This function classifies the users based on the following criteria:
    1) Group all CSNs that make 1 and only 1 trip
    2) Group all CSNs that make less than three trips, AND those trips are not on the same day
    3) Group all CSNs that make only two trips in a month but both trips are on the same day
    4) Group all CSNs that during the three-month period have more than 20 days on which they make both
    a WEEKDAY morning trip (5 AM – 9 AM) AND an afternoon trip (3:00 PM – 7:30 PM) on the same day
    5) Group all CSNs that during the three-month period have fewer than 20 days
    but more than two days on which they make both a WEEKDAY morning trip (5 AM – 9 AM)
    AND an afternoon trip (3:00 PM – 7:30 PM) on the same day
    6) Group all CSNs that during the three-month period have more than 20 days on which they make both
    an afternoon trip (3:00 PM – 7:30 PM) AND an evening trip (9:00 PM – 11:59 PM on the same day or up
    until 3:00 AM on the next day.
    7) Group all CSNs that during the three-month period have fewer than 20 days but more than two days
    on which they make both an afternoon trip (3:00 PM – 7:30 PM) AND an
    evening trip (9:00 PM – 11:59 PM on the same day or up until 3:00 AM on the next day.
    8) Group all CSNs that during the WEEKENDs make at least two trips on the same day.
    9) Group all remaining CSNs into a single group

    Parameters
    ----------
    session : sqlalchemy.orm.session.Session
        The session object to use for the query
    base_query : sqlalchemy.sql.selectable.Select
        The base query to use for the classification

    Returns
    -------
    sqlalchemy.engine.result.ResultProxy
        The result of the classification query
    '''
    # #1) Group all CSNs that make 1 and only 1 trip
    
    group1_subquery = (
        select(base_query.c.card_id, #base_query.c.date, 
            literal("Group 1").label("category"))
        .group_by(base_query.c.card_id, base_query.c.date)
        .having(func.count(base_query.c.date.distinct()) == 1)
    ).alias('group1')

    group1_ids = (
        select(group1_subquery.c.card_id)
        .distinct()
        # .alias('group1_ids')
    )

    #2) Group all CSNs that make less than three trips, AND those trips are not on the same day
    group2_subquery = (
        select(base_query.c.card_id, #base_query.c.date, 
            literal("Group 2").label("category"))
        .where(base_query.c.card_id.notin_(group1_ids))
        .group_by(base_query.c.card_id, base_query.c.date)
        .having(func.count(base_query.c.date.distinct()) == 2)
    ).alias('group2')

    group2_ids = (
        select(group2_subquery.c.card_id)
        .distinct()
        # .alias('group2_ids')
    )


    #3) Group all CSNs that make only two trips in a month but both trips are on the same day
    group3_subquery = (
        select(base_query.c.card_id, #base_query.c.date, 
            literal("Group 3").label("category"))
        .where(base_query.c.card_id.notin_(group1_ids),
            base_query.c.card_id.notin_(group2_ids))
        .group_by(base_query.c.card_id, base_query.c.date)
        .having(func.count(base_query.c.date.distinct()) == 1, func.count(base_query.c.date) == 2)
    ).alias('group3')

    group3_ids = (
        select(group3_subquery.c.card_id)
        .distinct()
        # .alias('group3_ids')
    )


    #4) Group all CSNs that during the three-month period have more than 20 days on which they make both
    # a WEEKDAY morning trip (5 AM – 9 AM) AND an afternoon trip (3:00 PM – 7:30 PM) on the same day

    # Main query to count the number of days with both morning and afternoon trips
    days_with_both_trips = (
        select(
                base_query.c.card_id,
                base_query.c.date
        )
        .where(
            (base_query.c.time_of_day == 'morning') | (base_query.c.time_of_day == 'afternoon'),        
            extract('dow', base_query.c.date).between(1, 5)
        )
        .group_by(base_query.c.card_id, base_query.c.date)
        .having(func.count(base_query.c.time_of_day.distinct()) == 2)
    ).subquery('days_with_both_trips')

    group4_subquery = (
        select(
            days_with_both_trips.c.card_id,
            literal("Group 4").label("category")
        )
        .group_by(days_with_both_trips.c.card_id)
        .having(func.count(days_with_both_trips.c.date) >= 20)
    ).alias('group4')

    group4_ids = (
        select(group4_subquery.c.card_id)
        .distinct()
        # .alias('group4_ids')
    )


    #5) Group all CSNs that during the three-month period have fewer than 20 days
    # but more than two days on which they make both a WEEKDAY morning trip (5 AM – 9 AM)
    # AND an afternoon trip (3:00 PM – 7:30 PM) on the same day

    # Main query to count the number of days with both morning and afternoon trips
    days_with_both_trips = (
        select(
                base_query.c.card_id,
                base_query.c.date
        )
        .where(
            (base_query.c.time_of_day == 'morning') | (base_query.c.time_of_day == 'afternoon'),        
            extract('dow', base_query.c.date).between(1, 5)
        )
        .group_by(base_query.c.card_id, base_query.c.date)
        .having(func.count(base_query.c.time_of_day.distinct()) == 2)
    ).subquery('days_with_both_trips')


    group5_subquery = (
        select(
            days_with_both_trips.c.card_id,
            literal("Group 5").label("category")
        )
        .group_by(days_with_both_trips.c.card_id)
        .having(func.count(days_with_both_trips.c.date) < 20, func.count(days_with_both_trips.c.date) > 2)
    ).alias('group5')

    group5_ids = (
        select(group5_subquery.c.card_id)
        .distinct()
        # .alias('group5_ids')
    )



    #6) Group all CSNs that during the three-month period have more than 20 days on which they make both
    # an afternoon trip (3:00 PM – 7:30 PM) AND an evening trip (9:00 PM – 11:59 PM on the same day or up
    # until 3:00 AM on the next day.

    # Main query to count the number of days with both afternoon and evening trips
    days_with_both_trips = (
        select(
                base_query.c.card_id,
                base_query.c.date
        )
        .where(
            (base_query.c.time_of_day == 'afternoon') | (base_query.c.time_of_day == 'evening')
            | (base_query.c.time_of_day == 'middle_of_night')        
        )
        .group_by(base_query.c.card_id, base_query.c.date)
        .having(func.count(base_query.c.time_of_day.distinct()) == 2)
    ).subquery('days_with_both_trips')

    group6_subquery = (
        select(
            days_with_both_trips.c.card_id,
            literal("Group 6").label("category")
        )
        .group_by(days_with_both_trips.c.card_id)
        .having(func.count(days_with_both_trips.c.date) >= 20)
    ).alias('group6')

    group6_ids = (
        select(group6_subquery.c.card_id)
        .distinct()
        # .alias('group6_ids')
    )

    #7) Group all CSNs that during the three-month period have fewer than 20 days but more than two days
    # on which they make both an afternoon trip (3:00 PM – 7:30 PM) AND an
    # evening trip (9:00 PM – 11:59 PM on the same day or up until 3:00 AM on the next day.

    # Main query to count the number of days with both afternoon and evening trips
    days_with_both_trips = (
        select(
                base_query.c.card_id,
                base_query.c.date
        )
        .where(
            (base_query.c.time_of_day == 'afternoon') | (base_query.c.time_of_day == 'evening')
            | (base_query.c.time_of_day == 'middle_of_night')        
        )
        .group_by(base_query.c.card_id, base_query.c.date)
        .having(func.count(base_query.c.time_of_day.distinct()) == 2)
    ).subquery('days_with_both_trips')

    group7_subquery = (
        select(
            days_with_both_trips.c.card_id,
            literal("Group 7").label("category")
        )
        .group_by(days_with_both_trips.c.card_id)
        .having(func.count(days_with_both_trips.c.date) < 20, func.count(days_with_both_trips.c.date) > 2)
    ).alias('group7')

    group7_ids = (
        select(group7_subquery.c.card_id)
        .distinct()
        # .alias('group7_ids')
    )



    #8) Group all CSNs that during the WEEKENDs make at least two trips on the same day.
    group8_subquery = (
        select(
                base_query.c.card_id,
                literal("Group 7").label("category")
        )
        .where(
            extract('dow', base_query.c.date).in_([5, 6])
        )
        .group_by(base_query.c.card_id, base_query.c.date)
        .having(func.count(base_query.c.date) >= 2)
    ).alias('group8')

    group8_ids = (
        select(group8_subquery.c.card_id)
        .distinct()
        # .alias('group8_ids')
    )


    #9) Group all remaining CSNs into a single group
    group_other_subquery = (
        select(
                base_query.c.card_id,
                literal("Group 9").label("category")
        )
        .where(
            base_query.c.card_id.notin_(group1_ids),
            base_query.c.card_id.notin_(group2_ids),
            base_query.c.card_id.notin_(group3_ids),
            base_query.c.card_id.notin_(group4_ids),
            base_query.c.card_id.notin_(group5_ids),
            base_query.c.card_id.notin_(group6_ids),
            base_query.c.card_id.notin_(group7_ids),
            base_query.c.card_id.notin_(group8_ids)
        )
    ).alias('group_other')

    group_other_ids = \
    (
        select(group_other_subquery.c.card_id)
        .distinct()
        # .alias('group_other_ids')
    )
    # Combine all group subqueries
    combined_groups = union_all(
        select(group1_subquery),
        select(group2_subquery),
        select(group3_subquery),
        select(group4_subquery),
        select(group5_subquery),
        select(group6_subquery),
        select(group7_subquery),
        select(group8_subquery),
        select(group_other_subquery)
    ).alias('combined_groups')

    # Subquery to find all card_ids that have been categorized
    categorized_card_ids = (
        select(combined_groups.c.card_id)
        .distinct()
        .alias('categorized_card_ids')
    )

    from transit_equity.classification.check_query_helper import get_results
    ###test on getting the classification results
    # base = get_results(session, select(base_query))
    classfied = get_results(session, select(combined_groups))
    return classfied




## for 3 month data, took about 25 min to run the whole

