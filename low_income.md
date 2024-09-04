---
layout: page
title: Serving Low Income Riders
parent: Analyses
---

## Overview

In this line of analyses, we were interested in how we can specifically serve low income populations better. We wanted to identify areas where reduced fare cards are not being used adequately. These could serve as potential opportunities to improve the distribution and usage of the reduced fare cards. 

The most prominent card type analysed was the LIFT card, whose trace data is available in the ORCA database. 


## ORCA LIFT Card

The ORCA LIFT card, which provides discounted rides to low-income riders across the Puget Sound area, is the most famous of the reduced fare cards provided by ORCA. In the nearly 10 years since its inception, the LIFT program has become the largest of its kind in the nation, providing our team the unique opportunity to robustly understand the transit patterns of low-income riders in particular. This card is available for all Individuals who have an income below 200% of the Federal Poverty Level. 

In spite of the major success of the LIFT program, there is still room for improvement. Currently, about **18%** of the population in Puget Sound, qualifies for LIFT cards, yet only **4%** of the ORCA cards are actually LIFT. On average, there is only about 1 LIFT card for every 18 individuals who are eligible for it. These high-level statistics indicate that there may be low-income areas where LIFT cards are not adequately utilized. 
There could be a number of reasons for this disparity in different low-income regions:
- The LIFT cards may not have been adequately distributed
- Transit service may not be adequate in general, which means that low-income individuals may not even be using any ORCA card. 
- The low-income individuals may not have a regular need for public transport, hence they may not want to go through the hassle of applying for a card. 


## Problem Statement

The high-level idea is to compare low-income ridership with low-income populations, in different areas. The lowest geography level of granularity, that we intend to use to make these comparisons, is the census block group. 


## Data Sources

- ORCA dataset

The ORCA dataset stores the type of passenger for each ORCA transaction. This could be any one of: Adult (standard fare), Youth, Senior, Low-Income, and other Reduced Fare types. 

For this analysis, we are interested in the subset of transactions for Low-Income passengers. However, the entire dataset was also utilized throughout the analysis for comparison. 

- GTFS dataset

GTFS is the common data format used by all the transit agencies involved in ORCA, for public transportation schedules and associated geographic information. 

Different aspects of the transit system, such as the bus stop locations, can change over time. The GTFS data provided by the agencies can thus, be useful to obtain additional information about the transactions, such as the location of the bus stop at the time it was used.

- US Census Data

The US Census Data can be useful to obtain estimates for low income populations in census block groups. This is useful due to the eligibility criteria (discussed in the 'Low Income Population' subsection.)


## Methods

### Tools

The entire line of analyses was carried out on Python and PostgreSQL. While some of the queries were written directly in PostgreSQL, others were written in a flexible setup in Python, using SQLAlchemy, in order to be able to work with multiple data sources. 

Additional details can be found in the [Github repository](https://github.com/uwescience/DSSG2024_transit_equity). 


## Metrics

### Low-Income Ridership

We could measure ridership of a census block group, using several different but complementary metrics, using the LIFT subset of our ORCA database. For each block group, we can measure the following:

- Number of total Transactions using LIFT cards to measure the overall usage of the LIFT services in a block group.

- Number of initial Boardings using LIFT cards to measure the usage of the LIFT services by people who start their trips in a given block group.

- Number of Unique users who have used the LIFT cards in a block group at least once, to serve as a measure of the number of users who may need to use the transit services in the block group at least once. 

- Number of Unique frequent users, who have used the LIFT cards in a block group, a certain number of times, to serve as measure of users who need to regularly utilize the transit services in the block group. 

For brevity, the analysis described in this page will mostly revolve around the 3rd metric (Number of Unique users), however, other metrics will be mentioned as and when required. 


### Low-Income Population

The LIFT card is available for all Individuals who have an income below 200% of the Federal Poverty Level. The US census data provides us estimates of these low income populations for each block group. 


## Results




## Limitations**
