---
layout: page
title: Low Income Card Analyses
parent: Analyses
---

**Data**

What data sets are you using?
What did you do to prepare the data?

<code style="color: red">-- TODO</code>

**Tools (aka “component specification”)**

What software packages, modules, etc. did you use? 
What are the dependencies between these and how did you render them interoperable?

<code style="color: red">-- TODO</code>

**Problem Context**

The high-level idea is to compare low-income ridership with low-income populations, on an equity basis. The level of granularity we intend to use to make these comparisons is the census block group. 

One left side, we could measure ridership of a census block group, either by boardings, unique users, or trips. We can measure this using the LIFT card (low-income card) details that we have in the ORCA database. 

- Boardings can be used to measure the actual usage (in a way, realizations of the potential) of the services offered by transit services. 

- Unique users are those who have used their LIFT cards at least once 

- When we say trips, we mean estimating the number of routes (multiplied by their frequency) that go through a census block group. Thus, trips can be used to measure the expected potential of the services offered by transit services. 

One the right side, we could measure low-income population in a census block group. Not just that, we could also measure other equity-based factors such as transit (or other) activity by low-income populations in a census block group, or jobs available for low-income populations in the census-block group.

**Processes**

What does your workflow or pipeline look like? 
What steps did you follow? 

**Analyses**

***Preliminary Analysis***

1. Check if it is necessary to consider low income proportions. 

We concluded that it may not be necessary, since block groups have comparable populations, thus low_income_proportion values would have comparable denominators.

I thought of investigating just a little more on that. Here is the distribution on that, along with some other stats. 

Statistics:

count    1545.000000

mean     1459.139806

std       433.057374

min         0.000000

25%      1160.000000

50%      1424.000000

75%      1693.000000

max      4373.000000

Name: population, dtype: float64

Standard deviation = 433, thus the extreme (>2 std) left and right would differ by > 1800, but these would be rare cases, owing to the close to normal distribution.

**Limitations**

What are the shortcomings of your approach?
How can your work be improved?

<code style="color: red">-- TODO</code>
