---
layout: page
title: Stop Improvements for Transfer Hotspots
parent: Analyses
---

## Overview

Bus stop shelters are incredibly vital to the public transportation experience as they allow commuters to wait for their ride in a safe and secure location. This analysis is focused on ensuring that the prioritization for the installation of bus shelters is equitable. The goal is to provide equal access to shelter at bus stops, particularly in underserved or vulnerable communities where such amenities can significantly impact residents' daily lives.

## ORCA and Transfer Hotspots

The new format of ORCA has made it possible to analyze transfers. Focusing on transfer hotspots when installing bus shelters is a strategic approach that enhances transit equity. By providing shelters at these high-usage areas, agencies like King County Metro can ensure that the needs of a diverse group of users are met, particularly those who might face longer wait times due to transfers. Currently, King County Metro’s prioritization framework does not consider transfers. We are working on including transfers into the scoring mechanism and improving the current shelter priority ranking.

## Mobility Framework Analysis

We are also working on analysis to validate King County Metro’s Mobility Framework. The Mobility Framework was created to ensure that public transit in the county serves the people who need it the most, such as low-income communities and people of color. The framework focuses on improving access to transportation for those who rely on it the most. By analyzing the ORCA data, we aim to answer questions about how low-income communities are being served by transit.

## Data Sources

- ORCA dataset
- GTFS dataset
- King County Metro’s current prioritization framework
- Mobility Framework - King County Metro
- Stop improvements dataset - King County Metro
- Equity and Social Justice metrics - King County

## Processes

### Recreating the KCM Priority Framework

King County Metro has 5 categories of scoring for their stop improvement prioritization, namely - Ridership, Activity Location, ESJ, Strategic Initiative and Community Request. We have successfully recreated this scoring in Python in a reproducible way, which allows easy modification in the future and facilitates the addition of new factors when they become available. It also makes it easier to adjust the weights of different categories according to King County Metro’s current interests.

### Incorporating Transfer Hotspots

With the ORCA dataset and the Stop improvements dataset, we analyzed the number of transfer transactions for each stop and assessed the existing amenities. Although the previous KCM framework did not consider transfers, we have suggested a new framework that does. Analyzing Transfer Hotspots — stops with a high number of daily transfer counts — can inform stop prioritization.

### Incorporating Low Income Usage

The ORCA dataset also contains information about whether the passenger is using a Reduced Fare Card - like the LIFT card. To make the bus stop prioritization framework more equitable, we suggest incorporating low income boardings and transfers into the scoring mechanism. 

### Identifying new bus shelter locations 

After recreating KCM's framework and adding 3 new metrics, we looked for stops that got a boost in ranking. While the direct inclusion of these metrics only had a modest impact on the current priority list, likely due to the fact that overall boarding size is already part of the scoring framework, there is additional restructuring and more analysis possible. 

### Transfer Hotspot Tables and GIS Maps

We created Transfer Hotspot Tables and Geospatial maps for agencies to have a closer look at these bus stops. By identifying bus stops that are transfer hotspots, we can help agencies better serve low income card holders, and also increase operational efficiency in general. Understanding how the current population is affected by transfers might make them aware of patterns that they could address in service changes with new stops and increased route frequency.




