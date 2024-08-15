/* This script is used to classify card holders into different temporal categories 
based on their boarding patterns.
 */

------create the table for the final result of categorization
CREATE TABLE IF NOT exists dssg.card_categories_final1 (
    card_id integer PRIMARY KEY ---REFERENCES orca.cards(card_id)
    ,category text NOT null
    ,distinct_counts integer
);

----------new functions
----------cut off the time of day-- 5-10:59 morning; 11-14:59 noon; 15-19:59 afternoon; 
---------20-23:59 evening; 0-2:59 midnight; 3-4:49 pre-dawn
CREATE OR REPLACE FUNCTION get_time_of_day(device_dtm TIMESTAMP) RETURNS TEXT AS $$
BEGIN
    RETURN CASE
        WHEN EXTRACT(hour FROM device_dtm) BETWEEN 5 AND 9 THEN 'morning'
        WHEN EXTRACT(hour FROM device_dtm) BETWEEN 10 AND 14 THEN 'noon'
        WHEN EXTRACT(hour FROM device_dtm) BETWEEN 15 AND 19 THEN 'afternoon'
        WHEN EXTRACT(hour FROM device_dtm) BETWEEN 20 AND 23 THEN 'evening'
        WHEN EXTRACT(hour FROM device_dtm) BETWEEN 0 AND 2 THEN 'middle_of_night'
        ELSE 'pre_dawn'
    END;
END;
$$ LANGUAGE plpgsql;

 ----This function takes in the time stamp and gives out the time of the day 
 ----input: time stamp  
 ----output: weekday, text
-----create function that takes in the dates and get the month difference
CREATE FUNCTION month_diff(day1 timestamp,day2 timestamp) RETURNS real AS $$
BEGIN
    RETURN round(extract(day from day1::timestamp - day2::timestamp)/30.4,1); --- use 30.4 = 365/12
END;
$$ LANGUAGE plpgsql;

select month_diff('2023-05-31','2023-03-12');



-----------this create number of partitions and then subdivide the base queries into a few parts.
--A: > 6 days per month, B: > 1 day per month


-- Create a temporary table for later processing -- will make query much faster
CREATE TEMP TABLE base_query AS
SELECT vb.card_id, vb.device_dtm_pacific, vb.business_date as date, 
       EXTRACT(DOW FROM vb.business_date) AS weekday,
       get_time_of_day(vb.device_dtm_pacific) AS time_of_day
FROM orca.v_boardings vb
WHERE vb.business_date BETWEEN '2023-03-01' AND '2023-05-31' -------change the date if want
  AND vb.txn_type_id <> 84
;
 

--1) (once) one use during observed period (could merge this with next group ).
-- no specific rule for home location
INSERT INTO dssg.card_categories_final1 (card_id, category, distinct_counts)
SELECT DISTINCT card_id, 'Group 1', COUNT(*)
	FROM base_query 
	GROUP BY card_id
	HAVING COUNT(*) = 1
	ON CONFLICT (card_id) DO NOTHING;


--2)(once_monthly) boarding average <= 1 trip per month. 
--assume the most frequent stop as home (not likely really accurate)
INSERT INTO dssg.card_categories_final1 (card_id, category, distinct_counts)
SELECT DISTINCT card_id, 'Group 2', COUNT(*)
	FROM base_query
	GROUP BY card_id
	HAVING COUNT(*)/month_diff('2023-05-31','2023-03-01') <=1
	ON CONFLICT (card_id) DO NOTHING;



--3) --(occasional_rider) boarding average > 1 trip per month, but not on same day (and less than threshold for category 10 A/B)-- used 2 as threhold
-- the first location is probably home location (not very sure)
INSERT INTO dssg.card_categories_final1 (card_id, category, distinct_counts)
SELECT DISTINCT card_id, 'Group 3' AS category, COUNT(date)
	FROM base_query
	GROUP BY card_id
	HAVING COUNT(*)/month_diff('2023-05-31','2023-03-01') between 1 and 2 
	AND COUNT(date) >= 2
	ON CONFLICT (card_id) DO NOTHING;


--A: > 6 days per month, B: > 1 day per month
--4A&B (frequent/moderate_daytime_commuter) average morning and afternoon/evening days > threshold above
-- the home location is in the morning trips
with days_with_both_trips AS (
    SELECT card_id,  date
    FROM base_query
    WHERE weekday BETWEEN 1 AND 5 AND 
    (time_of_day = 'morning' OR 
    time_of_day = 'afternoon' OR 
    time_of_day = 'evening')
    GROUP BY card_id, date
    HAVING COUNT(DISTINCT time_of_day) >= 2
)
INSERT INTO dssg.card_categories_final1 (card_id, category, distinct_counts)
SELECT card_id,
	   CASE WHEN COUNT(DISTINCT date)/month_diff('2023-05-31','2023-03-01') > 6 THEN 'Group 4A'
	        WHEN COUNT(DISTINCT date)/month_diff('2023-05-31','2023-03-01') BETWEEN 1 AND 6 THEN 'Group 4B'
	        ELSE 'BAD!'
	   END AS category, COUNT(*)
	FROM days_with_both_trips
	GROUP BY card_id
	HAVING COUNT(DISTINCT date)/month_diff('2023-05-31','2023-03-01') >=1
	ON CONFLICT (card_id) DO NOTHING;



--A: > 6 days per month, B: > 1 day per month
--5A&B (frequent/moderate_afternoon_commuter) average afternoon and evening/late night days > threshold above
with days_with_both_trips AS (
    SELECT base_query.card_id AS card_id, base_query.date AS date 
        FROM base_query 
        WHERE (base_query.time_of_day = 'afternoon' 
        or base_query.time_of_day = 'evening' OR 
        base_query.time_of_day = 'middle_of_night') 
        GROUP BY base_query.card_id, base_query.date 
        HAVING count(DISTINCT base_query.time_of_day) >= 2)
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT days_with_both_trips.card_id, 
        CASE WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') > 6) THEN 'Group 5A' 
            WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') BETWEEN 1 AND 6) THEN 'Group 5B'
            ELSE 'BAD!6&7'         -- shouldn't get this
            END AS category, 
        count(distinct(days_with_both_trips.date))
        FROM  days_with_both_trips
        GROUP BY days_with_both_trips.card_id 
        HAVING  count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >=1
        ON CONFLICT (card_id) DO NOTHING;

--6A&B (frequent/moderate_noon_commuter) average noon and evening/late night days > threshold above
--afternoon trip (11:00 AM – 14:59 AM) AND an evening trip (9:00 PM – 11:59 PM on the same day or up until 3:00 AM on the next day.

with days_with_both_trips AS (
    SELECT base_query.card_id AS card_id, base_query.date AS date 
        FROM base_query 
        WHERE (base_query.time_of_day = 'noon' or
        base_query.time_of_day = 'evening' OR 
        base_query.time_of_day = 'middle_of_night') 
        GROUP BY base_query.card_id, base_query.date 
        HAVING count(DISTINCT base_query.time_of_day) >= 2)
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT days_with_both_trips.card_id, 
        CASE WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >6) THEN 'Goup 6A' 
            WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') BETWEEN 1 AND 6) THEN 'Group 6B'
            ELSE 'BAD!6&7'         -- shouldn't get this
            END AS category, 
        count(distinct(days_with_both_trips.date))
        FROM  days_with_both_trips
        GROUP BY days_with_both_trips.card_id 
        HAVING  count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >=1
        ON CONFLICT (card_id) DO NOTHING;
       
       
--7A&B (frequent/moderate_early_commuter) average pre-dawn/morning and noon days > threshold above      
--a morning (5-9:59 am) or pre-dawn (3-4:59 am) and a noon trip (11:00 AM – 14:59 AM)
with days_with_both_trips AS (
    SELECT base_query.card_id AS card_id, base_query.date AS date 
        FROM base_query 
        WHERE (base_query.time_of_day = 'pre_dawn' or 
        base_query.time_of_day = 'morning' OR 
        base_query.time_of_day = 'noon' 
        ) 
        GROUP BY base_query.card_id, base_query.date 
        HAVING count(DISTINCT base_query.time_of_day) >= 2)
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT days_with_both_trips.card_id, 
        CASE WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') > 6) THEN 'Group 7A' 
            WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') BETWEEN 1 AND 6) THEN 'Group 7B'
            ELSE 'BAD!6&7'         -- shouldn't get this
            END AS category, 
        count(distinct(days_with_both_trips.date))
        FROM  days_with_both_trips
        GROUP BY days_with_both_trips.card_id 
        HAVING  count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >=1
        ON CONFLICT (card_id) DO NOTHING;
       

--8A&B (frequent/moderate_long_afternoon_commuter) average afternoon and per-dawn days > threshold above 
--(will this differ much from category 7?)
with days_with_both_trips AS (
    SELECT base_query.card_id AS card_id, base_query.date AS date
        FROM base_query 
        WHERE ( base_query.time_of_day = 'afternoon' OR 
        base_query.time_of_day = 'pre_dawn'
        ) 
        GROUP BY base_query.card_id, base_query.date  
        HAVING count(DISTINCT base_query.time_of_day) = 2 )
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT days_with_both_trips.card_id, 
        CASE WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01')>6) THEN 'Group 8A'
            WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01')  BETWEEN 1 AND 6) THEN 'Group 8B'
            ELSE 'BAD!'         -- shouldn't get this
            END AS category, 
        count(distinct(days_with_both_trips.date))
        FROM  days_with_both_trips
        GROUP BY days_with_both_trips.card_id 
        HAVING  count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >=1
        ON CONFLICT (card_id) DO NOTHING;  
       
       
 
--9A&B (frequent/moderate_noontime_activity) average noon and afternoon days 
---> threshold above

with days_with_both_trips AS (
    SELECT base_query.card_id AS card_id, base_query.date AS date
        FROM base_query 
        WHERE ( base_query.time_of_day = 'afternoon' OR 
        base_query.time_of_day = 'noon'
        ) 
        GROUP BY base_query.card_id, base_query.date  
        HAVING count(DISTINCT base_query.time_of_day) = 2 )
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT days_with_both_trips.card_id, 
        CASE WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >= 6) THEN 'Group 9A'
            WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') BETWEEN 1 AND 6) THEN 'Group 9B'
            ELSE 'BAD!'         -- shouldn't get this
            END AS category, 
        count(distinct(days_with_both_trips.date))
        FROM  days_with_both_trips
        GROUP BY days_with_both_trips.card_id 
        HAVING  count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >=1
        ON CONFLICT (card_id) DO NOTHING;
       
   
--10A&B (frequent/moderate_single_trip) one trip per day (any time period)
WITH days_with_one_trip AS (
    SELECT base_query.card_id AS card_id, base_query.date AS date, count(*)
        FROM base_query 
        GROUP BY base_query.card_id, base_query.date 
        HAVING count(base_query.time_of_day) = 1)        
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT days_with_one_trip.card_id, 
        CASE WHEN (count(distinct(days_with_one_trip.date))/month_diff('2023-05-31','2023-03-01') > 6) THEN 'Group 10A' 
            WHEN (count(distinct(days_with_one_trip.date))/month_diff('2023-05-31','2023-03-01') BETWEEN 1 AND 6) THEN 'Group 10B'
            ELSE 'BAD!'         -- shouldn't get this
            END AS category, 
        count(distinct(days_with_one_trip.date))
        FROM  days_with_one_trip
        GROUP BY days_with_one_trip.card_id 
        HAVING  count(distinct(days_with_one_trip.date)) /month_diff('2023-05-31','2023-03-01')>= 1
        ON CONFLICT (card_id) DO NOTHING;

       

       
--11 (weekend_activity) average weekend days with two trips in same day > 1  
WITH weekend_trips as  (
	SELECT base_query.card_id, base_query.date, COUNT(*) AS trips_per_day
        FROM  base_query
        WHERE (
          EXTRACT(dow FROM base_query.date) in (0,6)) 
        GROUP BY base_query.card_id, base_query.date 
        HAVING count(*) >= 2 )
 ,card_weekend_trips AS (
    SELECT weekend_trips.card_id, COUNT(*) AS distinct_trip_dates
	    FROM  weekend_trips
	    GROUP BY weekend_trips.card_id
	    HAVING  count(distinct(weekend_trips.date)) /month_diff('2023-05-31','2023-03-01')>= 1     
)
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT card_id,'Group 11 (old G8)' AS category, distinct_trip_dates
	FROM card_weekend_trips
	ON CONFLICT (card_id) DO NOTHING;

 ----G12 people who made two trips a day but both trips are within same major time of day, multiple days
with days_with_both_trips AS (
    SELECT base_query.card_id AS card_id, base_query.date AS date
        FROM base_query 
        GROUP BY base_query.card_id, base_query.date  
        HAVING count(DISTINCT base_query.time_of_day) = 1 and  count(base_query.time_of_day)>=2)
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT days_with_both_trips.card_id, 
        CASE WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >= 6) THEN 'Group 12A'
            WHEN (count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') BETWEEN 1 AND 6) THEN 'Group 12B'
            ELSE 'BAD!'         -- shouldn't get this
            END AS category, 
        count(distinct(days_with_both_trips.date))
        FROM  days_with_both_trips
        GROUP BY days_with_both_trips.card_id 
        HAVING  count(distinct(days_with_both_trips.date))/month_diff('2023-05-31','2023-03-01') >=1
        ON CONFLICT (card_id) DO NOTHING;

DELETE FROM dssg.card_categories_final1
WHERE category ='Others'; ---''
    
------------others still not being processed will be count as other
WITH other_trips as (
	SELECT base_query.card_id,count(*)
        FROM  base_query
        GROUP BY base_query.card_id, base_query.date 
)     
, card_trips AS (
    SELECT other_trips.card_id, COUNT(*) AS distinct_trip_dates
	    FROM  other_trips
	    GROUP BY  other_trips.card_id
)
INSERT INTO dssg.card_categories_final1 (card_id, category,distinct_counts )
    SELECT card_id,'Others' AS category, distinct_trip_dates
		FROM card_trips
		ON conflict (card_id) DO NOTHING;


---------------
------check how many different cards in each group
select  dc.category, count(*) from dssg.card_categories_final1 dc
group by  dc.category; ---46518

select  count(*) from dssg.card_categories_final1 dc  --536013

-----check how many different days on the other group
select count(*) from dssg.card_categories_renamed_categories dc
where dc.category = 'Others'
group by  dc.category,dc.distinct_counts;


-----check how many different days on the other group and group 8
select count(*), category from dssg.card_categories_renamed_categories dc
where dc.category IN ('Group 6A', 'Others')
group by  dc.category, dc.distinct_counts;


--------do some sanity check
select * from orca.v_boardings vb 
where business_date between '2023-03-01' and '2023-05-31' and card_id =  10;

------ check out certain id in other but looks suspicious
with base as (select 
vb.card_id AS card_id
            , vb.business_date AS date
            , EXTRACT(DOW FROM vb.device_dtm_pacific) AS weekday
            , CASE WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 5 AND 10) THEN 'morning'
                   WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 11 AND 14) THEN 'noon'
                   WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 15 AND 19) THEN 'afternoon'
                   WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 20 AND 23) THEN 'evening'
                   WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 0 AND 2) THEN 'middle_of_night'
                   ELSE 'pre_dawn'
                END AS time_of_day             
from orca.v_boardings vb 
where business_date between '2023-03-01' and '2023-05-31' and card_id = 8810452 and txn_type_id <> 84)
select base.date, base.time_of_day,weekday
from base;

------ check out certain id in other but looks suspicious-- more aggregated level
with base as (select 
vb.card_id AS card_id
            , vb.business_date AS date
            , vb.device_dtm_pacific as device_dtm_pacific
            , vb.device_lat*0.000001 as lat 
            ,vb.device_lng*0.000001 as long
            , EXTRACT(DOW FROM vb.device_dtm_pacific) AS weekday
			 , to_char( vb.device_dtm_pacific, 'day') AS weekday1
            , CASE WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 5 AND 10) THEN 'morning'
                   WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 11 AND 14) THEN 'noon'
                   WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 15 AND 19) THEN 'afternoon'
                   WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 20 AND 23) THEN 'evening'
                   WHEN (EXTRACT(hour FROM vb.device_dtm_pacific) BETWEEN 0 AND 2) THEN 'middle_of_night'
                   ELSE 'pre_dawn'
                END AS time_of_day             
from orca.v_boardings vb 
where business_date between '2023-03-01' and '2023-05-31' and card_id = 161948 and txn_type_id <> 84)
select base.card_id, base.date, base.time_of_day,base.weekday1, base.lat, base.long, device_dtm_pacific
from base;


      
       
-- Optionally drop the temporary table if not automatically dropped at the end of the session
DROP TABLE base_query;