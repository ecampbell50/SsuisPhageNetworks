# SsuisPhageNetworks
Personal scripts used to perform a network analysis on Streptococcus suis and it's prophages. Not in the most reproducible format, but up-to-date on what I used.

Scripts no doubt could be improved, please feel free to leave advice!

Tools used in this analysis:
- Prokka (v1.14.5)
- Sourmash (v4.8.5)
- Roary (v3.13.0)
- IQTree (v2.2.6)
- PADLOC (v2.0.0)
- geNomad (v1.8.0)
- Pharokka (v1.7.1)

1. CreateEdgetable.py: takes sourmash output csv and converts it to a non-looped edgetable for use in loading into cytoscape.
2. EdgetableVariations.py: takes edgetable from 1. and iteratively removes edges below a certain threshold to create a range of edgetables of a minimum weight.
3. FindCommunities.py: takes a weighted edgetable and uses the Louvain method to find communities
4. FindElbow.py: when used in the directory storing the edgetable variations, finds the cumulative area under the curve of iteratively removing edge weights. Also prints instructions on how to find the elbow using the R package pathviewr.
5. GetCommunityIDs.py: for the elbow-edgetable from 4. finds all communities and collates members into a list of each community. Also contains bash instructions for restructuring this into more usable downstream formats.
6. FindCentroids.py: takes a weighted edgetable and finds a representative node for each community based on either edge weight or node degree.
7. MorphEdgetable.py: takes a weighted edgetable and replaces the name of nodes with the community it is in, essentially creating a community-level edgetable.

List does not include ad-hoc commands used to restructure data or edit data. 

In order to create a bacterial community to prophage community edgetable, prophages were named in the following format:
(isolate ID it was isolated from)_prophage_(nucleotide coordinates in the isolate) 

This allowed me to create prophage-to-host connections, which were maintained upon renaming nodes within an edgetable to their community. Creating a BacterialCommunity-Prophage edgetable. Then prophages were renamed to their community as well.
