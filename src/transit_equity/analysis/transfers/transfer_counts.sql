-- GETTING TRANSFER COUNTS FOR STOPS
-- This SQL code gets a count of average boardings and transfers for each stop per weekday, adjusted by 0.65 for cash transactions.
-- We can also look at Low Income Boardings and Transfers and set different thresholds.

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

-- GETTING BOARDING COUNTS FOR STOPS

-- Step 1: Filter boardings to include only weekdays (Monday to Friday)
WITH weekday_boardings AS (
    SELECT
        stop_code,
        business_date,
        COUNT(*) AS daily_boarding_count
    FROM
        orca.v_boardings
    WHERE
        EXTRACT(DOW FROM business_date) BETWEEN 1 AND 5-- 1 is Monday, 5 is Friday
        --AND passenger_type_id = 'I'  -- IF LOOKING AT LOW INCOME CARDS ONLY
    GROUP BY
        stop_code, business_date
),

-- Step 2: Calculate total boardings and number of weekdays per stop
total_weekday_boardings_per_stop AS (
    SELECT
        stop_code,
        SUM(daily_boarding_count) AS total_weekday_boardings,
        COUNT(DISTINCT business_date) AS total_weekdays
    FROM
        weekday_boardings
    GROUP BY
        stop_code
),

-- Step 3: Calculate the average boardings per weekday, adjusted by dividing by 0.65
avg_boardings_per_weekday_low_income AS (
    SELECT
        stop_code,
        (total_weekday_boardings / total_weekdays) / 0.65 AS avg_boardings_per_weekday_low_income
    FROM
        total_weekday_boardings_per_stop
)

-- Step 4: Filter stops with an average of 50 or more boardings per adjusted weekday
SELECT stop_code, avg_boardings_per_weekday_low_income
FROM avg_boardings_per_weekday_low_income
--WHERE avg_boardings_per_weekday_low_income >= 5; -- SETTING THRESHOLDS