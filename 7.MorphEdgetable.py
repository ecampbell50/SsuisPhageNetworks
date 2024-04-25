############################################################
#    7.MorphEdgetable.py                                  #
#    This script takes the edgetable with GG, PP and GP    #
#    connections, the table of each prophage/genome and    #
#    community ID, and it replaces all genome/prophage     #
#    IDs with the community its in.                        #
############################################################

print("NOTE: this script needs edited to include argparse")

import pandas as pd
import argparse

########## Argparse ##########
parser = argparse.ArgumentParser(description="Arguments for this script...")
# Define the inputs
parser.add_argument("-i", "--input", required=True, help="Path to the full edgetable of all genome-genome and prophage-prophage edges")
parser.add_argument("-p", "--prophage", required=True, help="Path to the list of each prophage and the communtiy it belongs to")
parser.add_argument("-g", "--genome", required=True, help="Path to the list of each genome and the community it belongs to")

args = parser.parse_args()

input_edgetable = args.input
input_prophage = args.prophage
input_genome = args.genome
########## Argparse ##########

# Load in all tables to be used
edgetable = pd.read_csv(input_edgetable)
GComs = pd.read_csv(input_genome)
PComs = pd.read_csv(input_prophage)

# Make dictionaries out of the genome/prophage community tables
gcoms_dict = GComs.set_index('Genome')['Community'].to_dict()
pcoms_dict = PComs.set_index('Genome')['Community'].to_dict()

# Map the dictionaries to the edgetable
for column in edgetable.columns:
        edgetable[column] = edgetable[column].replace(gcoms_dict)

for column in edgetable.columns:
        edgetable[column] = edgetable[column].replace(pcoms_dict)

# Remove rows where column1 and 2 are the same (self-community loops)
edgetable = edgetable[edgetable['Genome1'] != edgetable['Genome2']]

edgetable.to_csv("CommunityEdgetable.csv", index=False)
