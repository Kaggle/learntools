from learntools.core import *

class PetCostumes(EqualityCheckProblem):
    _var = 'query_to_optimize'
    _expected = 3
    _hint = ("Do the queries run on big or small datasets?  Do they need to be run many times, or just once?  Is the data "
             "spread over multiple tables, or contained in just one?")
    _solution = \
"""
`query_to_optimize = 3`

Why **3**: Because data is sent for each costume at each second, this is the query that is likely to involve the most data (by far). And it will be run on a recurring basis. So writing this well could pay off on a recurring basis.

Why not **1**: This is the second most valuable query to optimize. It will be run on a recurring basis, and it involves merges, which is commonly a place where you can make your queries more efficient

Why not **2**: This sounds like it will be run only one time. So, it probably doesn’t matter if it takes a few seconds extra or costs a few cents more to run that one time. Also, it doesn’t involve JOINs. While the data has text fields (the reviews), that is the data you need. So, you can’t leave these out of your select query to save computation.
"""

class Mitzie(ThoughtExperiment):
    _hint = ("Do you see any large merges in the query?")
    _solution = \
"""
Yes. Working with the LocationsAndOwners table is very inefficient, because it’s a big table. There are a few options here, and which works best depends on database specifics. One likely improvement is

```
WITH CurrentOwnersCostumes AS
(
SELECT CostumeID 
FROM CostumeOwners 
WHERE OwnerID = MitzieOwnerID
),
OwnersCostumesLocations AS
(
SELECT cc.CostumeID, Timestamp, Location 
FROM CurrentOwnersCostumes cc INNER JOIN CostumeLocations cl
    ON cc.CostumeID = cl.CostumeID
),
LastSeen AS
(
SELECT CostumeID, MAX(Timestamp)
FROM OwnersCostumesLocations
GROUP BY CostumeID
)
SELECT ocl.CostumeID, Location 
FROM OwnersCostumesLocations ocl INNER JOIN LastSeen ls 
    ON ocl.timestamp = ls.timestamp AND ocl.CostumeID = ls.costumeID
```

**Why is this better?**

Instead of doing large merges and running calculations (like finding the last timestamp) for every costume, we discard the rows for other owners as the first step. So each subsequent step (like calculating the last timestamp) is working with something like 99.999% fewer rows than what was needed in the original query.

Databases have something called “Query Planners” to optimize details of how a query executes even after you write it. Perhaps some query planner would figure out the ability to do this. But the original query as written would be very inefficient on large datasets.
"""


qvars = bind_exercises(globals(), [
    PetCostumes,
    Mitzie
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)
