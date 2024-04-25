###################################################################################
#       FindCommunities.py                                                        #
#       This script takes a weighted edgetable from sourmash (from                #
#       CreateEdgetable.py) and finds the communities based on Louvain method.    #
#       Output is a list of each community and it's members.                      #
###################################################################################

import pandas as pd
import argparse
import datetime
import igraph as ig

########## Argparse ##########
parser = argparse.ArgumentParser(description="Arguments for this script...")
# Define the inputs
parser.add_argument("-i", "--input", required=True, help="Path to input edgetable from CreateEdgetable.py")

args = parser.parse_args()

input_edgetable = args.input
##############################

# Load in input edgetable
edgetable = pd.read_csv(input_edgetable)

# Make the igraph graph of the edgetable
g = ig.Graph.TupleList(edgetable.itertuples(index=False), directed=False, weights=True)

# Find the number of communities in the graph
communities = g.community_multilevel(weights=g.es["weight"], return_levels=False)
num_communities = len(communities)

# Identify the communities
#print(num_communities)

# Print the edgetabel table with the number of communities
print(f"{input_edgetable},{num_communities}")
