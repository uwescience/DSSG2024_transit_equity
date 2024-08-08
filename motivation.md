---
layout: page
title: Motivation
has_children: true
---

**Background**

Intentional movement from one location to another has characterized human history irrespective of time and spatial scales. The globally-connected society that we live in would be impossible without the dynamic transport of people and objects between places. Whether via air, water, land, or even space, transit represents the spatial networks that enable us to experience the world outside of our own backyards. 

In particular, public transit reflects the truth that, although we may have unique ultimate origins and destinations, there are shared patterns in our movements that allow us to go from point A to point B together. Public transit has existed for much of recorded human history: for example, Greek mythology features one of the earliest tales of public transit in the story of the ferryman Charon, who required payment in the form of coins from travelers that needed to cross the river Styx (cite?). 

The issue of payment for public transit has grown as transit networks have become more complicated. Where once single ferries or trains would connect regions adequately, now there are multiple routes serviced by multiple modes of transit operated by multiple different agencies within a singular region. As technology has enabled our society to become increasingly cashless, transit systems have followed. Understandably, for regions with multiple transit agencies, developing a unified system to allow seamless cashless payments between modes of transit and across agencies was necessary. Thus, the inception of the Puget Sound regional ORCA (One Regional Card for All) system was long awaited. 

What work has previously been done? (thinking of moving this to the questions section maybe at the end to highlight past work of DSSG?)
 
**Questions** 

Though ORCA fare cards have existed in some form since 2009, there have been limited opportunities to explore the data and synthesize meaning from the millions of trips recorded in the ORCA database. This is not from lack of interest by the participating agencies; rather, due to the size and complexity of the dataset, just managing the data is a full time job for multiple employees. Performing data analysis is a much desired and necessary next step to facilitate data-driven improvements to our region's transit systems. Our transit equity team, comprised of graduate students from the fields of urban planning, data and computer science, and community ecology, is using ORCA data to reveal insights into usage patterns of ORCA riders from disadvantaged communities that can identify areas for improvement and guide transportation in the Puget Sound region towards a more equitable future. 


We are interested broadly in identifying patterns in transit use between ORCA card user demographics that will enable us assess quality of service across all types of ORCA card users. More specifically, our analyses seek to answer several questions:  

1) Are stops that are central in transit ridership networks shared across all card demographics? How do the networks vary in structure between card demographics? Is the structure of these networks reflected by the geographic layout of the transportation network?

2) Can we improve our prediction for people's home locations so we can provide better services?

3) Do hotspots of transfer have adequate shelters? Do low-income riders suffer more from not having adequate shelters? 

4) Are low-income riders receiving an adequate level of service across all regions in Puget Sound? Where is the service inadequate for low-income riders?

5) How do ORCA users look like in terms of behavior? Do low-income riders behave differently?



**Stakeholders**


Because transit is a multifaceted social good, we considered stakeholders from multiple sectors. Our transit organization and policy stakeholders include Sound Transit, King County Metro, the Federal Transit Administration, the ORCA joint board, and other local transit agencies. Our transit advocacy stakeholder groups include the Transit Riders Union, Disability Rights Washington, El Centro de la Raza, the Amalgamated Transit Union, King County Social Services, and Commute Seattle. Additionally, businesses are stakeholders from the perspective of organizations who purchase bulk ORCA cards for employees through the business passport program and as locations serviced by transit. Finally, stakeholders internal to our internship program include the University of Washington eScience Institute, Data Science for Social Good Fellows and project leads present and future, and the Washington State Transportation Center (TRAC).

To incorporate stakeholder feedback into our project, we met with representatives from the Transit Riders Union, Disability Rights Washington, and King County Metro who are familiar with ORCA fare card data. We took into consideration their suggestions for project direction and concerns surrounding transit accessibility and improvement in the Puget Sound region. We ensured that the types of analysis we completed would be useful for their organizations and that there were not unintentional pitfalls that could negatively affect the demographics that their organizations advocate for. 

The primary use case for our project is internally by TRAC and ORCA employees to produce further insights and improvements surrounding the ORCA database. Additionally, future Data Science for Social Good fellows at University of Washington will be able to build upon our work for years to come. 

**Ethics**

One of the main ethical considerations we navigated as a team is the issue of our dataset not being fully representative of the demographics for the different types of ORCA cards available. For example, the LIFT cards for low-income riders and the reduced fare ride program for disabled riders requires knowledge of the programs and an application process, which represents two barriers to full use by the people who are eligible for them. Many low-income riders use cash payments to access transit, which is missing from the ORCA database. Additionally, because there are many definitions of disability and self-identification as disabled must preclude securing a reduced fare disability rider card, there are real concerns about using the subset of riders with disability cards to represent the whole disabled community. 

Additionally, the use of individual-level transit data presents a potential privacy concern. 


Following input from our meeting with our contact at Disability Rights Washington, we have decided to focus on the low-income rider data from LIFT cards rather than using the disabled rider card data. We recognize the intersection between the needs of the low-income and disabled communities in the Puget Sound region and feel that improvements that can benefit the low-income community will also benefit disabled riders. Using our limited data from the reduced fare disability riders program to make conclusions about the entire community of disabled transit riders runs the risk of misidentifying transit needs based on a non-representative subset of riders. To account for privacy concerns related to our data, we have taken care to not publicly share any disaggregated data that could potentially lead to identification of an individual. Along that line, we have also avoided sharing any data that could identify companies that provide business passport ORCA cards to employess to prevent that data from being accessed by competing companies. 
