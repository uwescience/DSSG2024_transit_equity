-- TRANSFER HOTSPOTS FOR KING COUNTY METRO
-- This SQL code gets the stop code, routes transferred to and from, and the agency ids for joining with GFTS, and the number of transfers.
SELECT
    t2.stop_code AS boarding_stop_of_transfer,
    t1.route_number AS route_transferred_from,
    t2.route_number AS route_transferred_to,
    t1.service_agency_id,
    t2.service_agency_id,
    t2.source_agency_id,
    COUNT(*) AS transfer_count
FROM
    orca.v_boardings t1
JOIN
    orca.linked_transactions lt
ON
    t1.txn_id = lt.txn_id
JOIN
    orca.v_boardings t2
ON
    lt.next_txn_id = t2.txn_id
WHERE
    lt.is_orca_transfer = 'true'
    AND t2.service_agency_id = '4'
GROUP BY
    t2.stop_code, t1.route_number, t2.route_number, t1.service_agency_id,
    t2.service_agency_id,
    t2.source_agency_id
HAVING
    t1.route_number != t2.route_number
ORDER BY
    transfer_count DESC;

-- GETTING TRANSFER COUNTS FOR STOPS

-- Step 1: Filter transfers to include only weekdays (Monday to Friday)
WITH weekday_transfers AS (
    SELECT
        v_boardings.stop_code,
        v_boardings.business_date,
        COUNT(*) AS daily_transfer_count
    FROM
        orca.linked_transactions
    JOIN
        orca.v_boardings
        ON v_boardings.txn_id = orca.linked_transactions.next_txn_id
    WHERE
        orca.linked_transactions.is_orca_transfer AND
        EXTRACT(DOW FROM v_boardings.business_date) BETWEEN 1 AND 5  -- 1 is Monday, 5 is Friday
        -- AND orca.v_boardings.passenger_type_id = 'I' -- IF LOOKING AT LOW INCOME CARDS ONLY

    GROUP BY
        v_boardings.stop_code, v_boardings.business_date
),

-- Step 2: Calculate total transfers and number of weekdays per stop
total_weekday_transfers_per_stop AS (
    SELECT
        stop_code,
        SUM(daily_transfer_count) AS total_weekday_transfers,
        COUNT(DISTINCT business_date) AS total_weekdays
    FROM
        weekday_transfers
    GROUP BY
        stop_code
),

-- Step 3: Calculate the average transfers per weekday, adjusted by dividing by 0.65 (Factoring in Cash Usage)
average_weekday_transfers AS (
    SELECT
        stop_code,
        (total_weekday_transfers / total_weekdays) / 0.65 AS avg_transfers_per_weekday
    FROM
        total_weekday_transfers_per_stop
)

-- Step 4: Filter stops with an average of [threshold] per adjusted weekday
SELECT stop_code, avg_transfers_per_weekday
FROM average_weekday_transfers
-- WHERE avg_transfers_per_weekday >= 2; -- SETTING THRESHOLDS
