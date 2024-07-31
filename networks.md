---
layout: page
title: Trip Networks Across Card Types
parent: Analyses
---

The goal of this analysis is to understand the differences between trip origin and destination networks among ORCA card types. Specifically, we are interested in the following questions:  

### 1) How do the networks vary in structure between card demographics?  
    This question will reveal large-scale patterns of ridership across different ORCA card types. We assume that different categories of riders will have different travel behaviors which will lead to varying network structure, but this has not been confirmed analytically. Networks can vary in a multitude of ways, however for this analysis we are focusing on several metrics particularly relevant to transit:  

        A) Degree centrality (the number of trips that each stop has), which will reflect which stops are most frequently used by each group. A higher value indicates that a stop is frequented more by riders of the target demographic. This metric is computed at the stop level.  

        B) Closeness centrality (the average length of the shortest path between a stop and all other stops in the network), which measures how quickly a stop can be reached from other stops. A higher value indicates that more stops are more accessible from other stops in that network. This metric is computed at the stop level.  

        C) Network density (the proportion of actual origin-destination trips in the network to the total number of possible trips), which will show if different rider demographics use more direct versus more circuitous routes. A higher value indicates that a higher proportion of trips in the network are direct. This metric is computed at the whole network level.  
        
        D) Modularity (the strength of division of the network into clusters that see more frequent trips between stops within the module than stops outside of the cluster), which will identify whether there are distinct clusters of stops used by different rider groups. A higher value indicates that there are more distinct clusters in the network. This metric is computed at the whole network level.  

### 2) Are stops that are central in transit ridership networks shared across all card demographics?  
    This question will allow us to understand whether there are universally-important stops across card demographics that could be improved to benefit all riders. Conversely, it could reveal stops that are particularly important to certain demographics that would be considered less important when considering all riders, which would provide insight to inform targeted improvements to support those demographics. 

### 3) Is the structure of these networks reflected by the geographic layout of the transportation network?  
    This question will generate insight to whether the trip networks are geographically structured (i.e. the most frequented stops tend to be in the center of the network geographically). If this is not the case (i.e. the most frequented stops tend to be in the periphery of the network geographically), it will provide evidence for non-geographic drivers of transit patterns that can be further explored in future analyses.



**Data**

What data sets are you using?
What did you do to prepare the data?

**Tools (aka “component specification”)**

What software packages, modules, etc. did you use? 
What are the dependencies between these and how did you render them interoperable?

**Processes**

What does your workflow or pipeline look like? 
What steps did you follow? 

**Analyses**

What approaches did you try that didn’t work?
What analyses did you end up sticking with?

**Limitations**

What are the shortcomings of your approach?
How can your work be improved?

