################################################################################
#      FindCentroids.py                                                        #
#      This script takes a weighted edge table (Source, Target, Weight)        #
#      and finds a representative centroid for each community based on          #
#      either node degree or edge weight                                       #
################################################################################

import pandas as pd
import igraph as ig
import argparse
import datetime

########## Argparse ##########
parser = argparse.ArgumentParser(description="Input edgetable...")
# Define the input file argument
parser.add_argument("-i", "--input", required=True, help="Path to the input file")
args = parser.parse_args()
input_file = args.input
##############################

# Read the CSV edgetable (replace 'your_edgetable.csv' with your actual file path)
edgetable = pd.read_csv(input_file)

# Create an igraph graph with edge weights
g = ig.Graph.TupleList(edgetable.itertuples(index=False), directed=False, edge_attrs=["Value"])

# Identify communities using the Louvain method (you can choose a different algorithm if needed)
communities = g.community_multilevel(weights=g.es["Value"], return_levels=False)

# Initialise dataframe to create a csv of each community and it's representative
Community_IDs = pd.DataFrame(columns=['CommunityID', 'Representative'])

# Iterate through communities and print information
for community_id, community in enumerate(communities, start=0):
	community_size = len(community)

	# Node Degree Representative
	degree_representative = max(community, key=lambda node_id: g.degree(node_id))
	degree_representative_name = g.vs[degree_representative]["name"]
	NODE_node_degree_of_representative = g.degree(degree_representative)
	NODE_sum_of_edge_weights_of_representative = sum(g.es.select(_within=community).select(_source=degree_representative)["Value"])


	# Edge Weight Representative
	weight_representative = max(community, key=lambda node_id: sum(g.es.select(_within=community).select(_source=node_id)["Value"]))
	weight_representative_name = g.vs[weight_representative]["name"]
	WEIGHT_node_degree_of_representative = g.degree(weight_representative)
	WEIGHT_sum_of_edge_weights_of_representative = sum(g.es.select(_within=community).select(_source=weight_representative)["Value"])

	Community_IDs.loc[len(Community_IDs)] = [community_id, weight_representative_name]	# Change the weight to node, for the other method

	# Print community information for interpretation
	#print(f"Community: {community_id}")
	#print(f"Size: {community_size} nodes")
	#print(f"Node Degree Representative: {degree_representative_name}, Node Degree: {NODE_node_degree_of_representative}, Node Weights: {NODE_sum_of_edge_weights_of_representative}")
	#print(f"Edge Weight Representative: {weight_representative_name}, Node Degree: {WEIGHT_node_degree_of_representative}, Node Weights: {WEIGHT_sum_of_edge_weights_of_representative}")
	#print()
  
	# Use this instead to print in a downstream-applicable format
	# Edge weight representative
	print(f"{community_id},{weight_representative_name}")
	# Node degree representative
	#print(f"{community_id},{degree_representative_name}")

# Save the community IDs and representatives dataframe as a csv for downstream use
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
output_file = f"Communities_and_Centroids_{formatted_datetime}.csv"
Community_IDs.to_csv(output_file, index=False)
