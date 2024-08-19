##List of files
|file name |use |
|:-----|----:|
|01Get_Census_data.ipynb  |This is the basis for getting census block group data |        
|02cluster_quick_heatmap.ipynb |This notebook plots the boarding map across different time of day, and also plot the weekly boardings in slides|
|03cluster_heuristic_model.ipynb|This was the draft to test the heuristic model. Not used for final purpose but useful for extracting data from the database using sqlalchemy |
04classification.ipynb                
|**04final_heuristic_classification.sql**  |This is the the final code that produced the card_categories_final1 in ORCA database.Also in the DSSG2024_transit_equity/src/transit_equity/temporal_classification folder.|
|05user_pattern_comparison.ipynb |This is the code that produced some charts in slides, including box plots, violin plots, density plots |
|**06home_address_for_validation.sql**|This is the sql code that creates the final validation set for home block group location. Also in the DSSG2024_transit_equity/src/transit_equity/temporal_classification folder.|

The remaining files can be found in the private repository DSSG2024_transit_equity_private/note_siman.

##Objective:
The overarching goal of temporal classification (file starts with 03 to 06) is to help identify the home block group location for future service improvement, such as expanding the LIFT program to the right census block group.
The temporal classification itself is coming from a heauristic method rather than machine learning method.
The rationale for identifying the home block group is documented here.

| Group Classification	|Group Name	in graphics|Home Block Group Prediction Rationale|
|-----------------------|:----------|------------------------------------:|
|G1 One-time Use (used only once during the observed period, could be merged with the next group)	|BRG1 One-time User	|No specific rule for determining the home location|
|G2 Very Occasional Rider (monthly boarding average ≤ 1 trip per month)	|BRG2 Occasional Rider	|Assume the most frequent stop as the home location, though this may not be highly accurate|
|G3 Occasional Rider (boarding average between 1 and 2 trips per month; may not capture those who took several trips a day but only on 2 days)	|BRG2 Occasional Rider|	The first boarding on each day is likely the home location, although this is uncertain compared to simply using the most frequent location as the home.|
|G4A/B Frequent/Moderate Daytime Commuter (average morning and afternoon/evening days > threshold)	|BRG4 9-5 Commuters / Regular Peak Commuter|	The home location is likely in the earliest morning trips.|
|G5A/B Frequent/Moderate Afternoon Commuter (average afternoon and evening/late night days > threshold)	|BRG5 Noon-Afternoon Commuters	|The home location is within the earliest afternoon trips.|
|G6A/B Frequent/Moderate Noon Commuter (average noon and evening/late night days > threshold)	|BRG5 Noon-Afternoon Commuters	|The home location is in the earliest noon trips.|
|G7A/B Frequent/Moderate Early Commuter (average pre-dawn/morning and noon days > threshold)	|BRG6 Early Morning (Dawn) Commuters	|The home location is likely at the pre-dawn/morning stop; the earliest boarding in the morning is probably near home.|
|G8A/B Frequent/Moderate Long Afternoon Commuter (average afternoon and pre-dawn days > threshold; this category may overlap with Category 7)	|BRG7 Pre-Dawn and Afternoon Commuter (likely night shift workers)|	Uncertainty exists whether the pre-dawn or afternoon trip is the home location. Additional rules to check: <ul><li>Night shift workers: Afternoon location is likely the home location, especially if top locations are near warehouses, hospitals, airports, or manufacturing sites.</li><li>If weekly commute days ≤ 4, the commuter is likely a night shift worker.</li><li>If the top two locations have close frequencies, the location with lower rent is likely the home location.</li><li>For very early commuters, the pre-dawn location is likely the home location.</li></ul>|
|G9A/B Frequent/Moderate Noontime Activity (average noon and afternoon days > threshold)	|BRG10 Short-Time Roundtrip	| The noon locations are likely the home locations.|
|G10 A/B Frequent/Moderate Single Trip (one trip per day, any time period)	|BRG8 One-Way Commuter	|The most frequent or second most frequent location might be home. If the frequencies are close, the location with lower rent is likely the home location.|
|G11 Weekend Activity (average weekend days with two trips on the same day > 1)	|BRG9 Weekend Use	|The first trip on the weekend likely contains the home location.|
|G12 Same Time Window Trips (people who made two trips a day, with both trips within the same major time of day on multiple days)|	BRG10 Short-Time Roundtrip	|The first boarding in a day with the most frequency is likely the home location.|
|G13 Others (anyone who cannot be grouped into previous categories)	|BRG11 Others	|<ul><li>If distinct days per month ≥ 1 but do not fall into any previous categories:</li><li>If morning trips account for more than 1/3 of trips, the first morning boarding is likely the home location.</li><li>If noon trips account for more than 1/3 of trips, the first noon boarding is likely the home location.</li><li>If neither condition is met, use the typical earliest trip time for boarding as the home location.</li></ul>|

* Note:
- The threshold is shown in the A/B terms for frequent/moderate usage. For frequent usage, it requires > 6 days per month after COVID on average; for moderate usage, it requires 1-6 days per month after COVID on average. 

- The names in the first column is used in dssg.card_categories_final1. Group 1 will in dssg table be abbreviated as 'G1' in this documentation table. The names in column 2 are used for plotting purpose in gihub private repository under note_siman/05user_pattern_comparison.ipynb*