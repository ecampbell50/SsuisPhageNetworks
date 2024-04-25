import pandas as pd
import igraph as ig
import argparse

#### This script is to take the elbow edgetable, get a list of every community, pyt them into their own file lists,

########## Argparse ##########
parser = argparse.ArgumentParser(description="Arguments for this script...")
# Define the inputs
parser.add_argument("-i", "--input", required=True, help="Path to input edgetable after finding the elbow variation")

args = parser.parse_args()

input_file = args.input
##############################

# Load in the elbow edgetable
data = pd.read_csv(input_file)

# Make the igraph graph of the edgetable
g = ig.Graph.TupleList(data.itertuples(index=False), directed=False, weights=True)
# Find the number of communities in the graph
communities = g.community_multilevel(weights=g.es["weight"], return_levels=False)

# Get the node names
node_names = g.vs["name"]


# Print the communities with both community names and community numbers
for community_num, community in enumerate(communities):
    community_names = [node_names[i] for i in community]
    print(f"Community {community_num + 1}: {community_names}")

# Use this to change igraph output to something usable
# cat AllCommunties_and_IDs.txt | sed 's/Community /Community_/g' | sed 's/\: \[/,/g' | sed 's/ //g' | sed 's/\]//g' | sed "s/'//g" > AllCommunities.csv

# Use this to replace 'Community_<anything>,' from the start of a line
# for i in Community_*.csv; do sed -i 's/[^,]*,//' $i; done

# use this to get each community list in a file of its Community name
# for i in `cat AllCommunitiesandIDs_18Dec23.csv`; do echo ${i#*,} > ${i%%,*}.csv; done
# then use sed -i 's/,/\n/g' to replace all commas with a new line

# Use this with every community ID list to get a list of all genomes and the ocmmunity it belongs to
# for i in *; do for j in `cat $i`; do echo "$j,${i%.csv}"; done; done
# NB: ADD "Genome,Community" TO THE TOP OF THIS TO MAKE IT COMPATIBLE FOR 10.

# Use this to get the Genome->Prophage Edges
# for i in `cat ProphageCommunityIDs.csv | cut -d',' -f1`; do echo "${i//_*}.fna,$i,GP"; done
