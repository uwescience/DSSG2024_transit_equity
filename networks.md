---
layout: page
title: Trip Networks Across Card Types
parent: Analyses
---

The goal of this analysis is to understand the differences between trip origin and destination networks between riders who use the different ORCA card reduced fare programs. Understanding the patterns of trip behavior has potential to be used to inform targeted service and stop improvements that could benefit the different demographics that ride transit using the different card types. Specifically, we are interested in the following questions:  

### 1) How do the trip networks vary between card types?  
Understanding and visualizing trip networks can reveal large-scale patterns of ridership across the different ORCA card types. Identifying similarities and differences between the networks could provide insight into the importance of different stops and connections in the travel patterns of users of each card type. Networks can vary in a multitude of ways, however for this analysis we are focusing on several metrics particularly relevant to transit:  

 A) Degree centrality (based on the number of trip arrivals and departures that each stop has), which will reflect which stops are most frequently used by users of each card type. A higher value indicates that a stop is frequented more by riders that use the same card type. This metric is computed at the stop level, for both origins and destinations independently as well as the total sum for both.  

 B) Eigenvector centrality (based on the connections of all of the stops that are connected to a particular stop), which indicates the relationship a stop has to other stops in the network and can be used to identify stops that connect to popular stops. A higher value indicates that a particular stop is connected to more well-connected stops, representing a hub. This metric is computed at the stop level, for both origins and destinations independently as well as the total sum for both. 

C) Network density (the proportion of actual origin-destination trips in the network to the total number of possible trips), which will show if different card user types use more direct versus more circuitous routes. A fully connected network would mean that every origin stop has at least one instance of a trip that ends at every destination stop. A higher value indicates that a higher proportion of trips in the network are direct. This metric is computed at the whole network level.  

D) Modularity (the strength of division of the network into clusters that see more frequent trips between stops within the module than stops outside of the cluster), which will identify whether there are distinct clusters of stops used by different rider groups. A higher value indicates that there are more distinct clusters in the network. This metric is computed at the whole network level.  

### 2) Are stops that are central in transit ridership networks shared across all card demographics?  
This question will allow us to understand whether there are universally-important stops across card demographics that could be improved to benefit all riders. Conversely, it could reveal stops that are particularly important to certain demographics that would be considered less important when considering all riders, which would provide insight to inform targeted improvements to support those demographics.  

### 3) Is the structure of these networks reflected by the geographic layout of the transportation network?  
This question will generate insight to whether the trip networks are geographically structured (i.e. the most frequented stops tend to be in the center of the network geographically). If this is not the case (i.e. the most frequented stops tend to be in the periphery of the network geographically), it will provide evidence for non-geographic drivers of transit patterns that can be further explored in future analyses.  


**Data**

For this analysis, we used a subset of ORCA origin-destination trip data from April 2023 in the ORCA next generation database. At the time of analysis, the full updated trip table was not available. This analysis is ready to complete for each month at a later date as the data becomes available.  
 
Additionally, we incorporated census block data and USGS National Hydrography Dataset data to create regional spatial hexgrid shapefiles to aggregate stops that are close to each other.  

Data was filtered by card type into the following groups: adult, youth, lift card (low-income riders), senior, and disability. Each group was analyzed as a separate network for comparison.  

The following data cleaning steps were taken to prepare the trip table for network analysis:  
    1)  Duplicated rows were dropped because some trips were duplicated erroneously in the database.  
    2)  The absolute time difference between boarding and destination was calculated. We used the absolute time difference because some trips erroneously had a destination time that was prior to the origin time.  
    3)  Trips with duration longer than 3 hours were dropped. This is because some trips had unreasonably long trip times due an issue with the algorithm that determines start and stop location for each trip.  
    4)  Trip frequency for each unique origin-destination trip was calculated.  
    5)  Duplicate trips were dropped after trip frequency was calculated.  

Each of the issues mentioned above in the cleaning steps were reported to the project leads, who maintain the database. These issues will be taken into account and corrected as the project leads prepare to release the most recent iteration of the trips table in the database.  

 

**Tools**

To clean and filter the network data, we used the packages sqlalchemy, pandas, numpy, geopandas, and shapely. To calculate network metrics, we used networkx. For network visualization, we used folium. We also developed an open-source package available in our github repository with custom functions for each analysis, including the cleaning functions to prepare the data for network analysis.



**Processes**

We imported the origin-destination trips table for April 2023 from the ORCA postgres database and loaded each table as a pandas geodataframe. Data was filtered following the steps outlined in the above Data section. We ran each network analysis separately for each of the card types: adult, youth, senior, disability, and low-income. We then assigned each stop to the centroid of a 1/4 mile hexagonal grid overlaid on the spatial extent of the stop points to aggregate the data and improve visibility in the plots. Then, we calculated trip frequency and filtered out any duplicates as well as origin-destination trip combinations with fewer instances than 20 that month to focus only on the most frequent trips. Next, we used networkx to create networks for each card type with nodes representing origin and destination location and edges representing trip area. We used the networkx object to calculate network metrics. Then, we used folium to create interactive maps for each card type, with and without inclusion of the downtown Seattle area to reduce overplotting of the high density-high frequency downtown stops. 

**Analyses**

Originally, we planned to pursue a multilayer network approach to directly compare the networks of different users, but this quickly became overcomplicated due to the size of the dataset. 

Instead, analyzing each user type network discretely provided more easily interpretable results and visualizations without overtaxing our computers.

**Limitations**

This approach has only been tested with one month of trip data, and even then we ran up against memory and computing limitations to complete the analysis. Additionally, we identified several issues with the data including negative trip times, impossibly long trip times, and trips that had the same start and stop location. These will be addressed in new iterations of the database, but for now were just filtered out. 
How can your work be improved?  
Running analysis on a more powerful computer would speed up the computation time and enable the use of larger subsets of the data. Additionally, examining how the networks change over time would yield additional valuable insight. 

**Results**

Adult trip network  

<iframe src="assets/img/adult_no_downtown_network.html" height="500" width="500"></iframe>
