# A Python script for temporal analysis of multiplex networks

R and Python offer many packages for temporal network analysis: pathpy, tsna, ndtv. However, in my experience, at least some of these packages do not allow us to handle multiplex networks (i.e., networks with parallel edges). This script aims to fill this gap. It was originally designed for measuring the growth of correspondence networks over time. It implements the following three functions: 

individualDegree: for every year, it returns the number of both incoming and out-coming edges of ego;
individualCorrespondents: for every year, it returns a list of all couples formed by ego and one of its alters, and the total number of edges within each couple.
correspondencePerYear: for every year, it returns the total number of edges within a single couple formed by ego and a given alter.
Building on these functions, it is then possible to measure other variables, such as the total number of nodes and edges per year.

## Acknowledgements

I would like to thank my brother, Luca Rossini, for helping me fix some of the issues with the code.
