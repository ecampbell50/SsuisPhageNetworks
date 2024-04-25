#################################################################################
#       EdgetableVariations.py                                                  #
#       This script takes an edgetable generated from CreateEdgetable.py        #
#       and makes variations by removing edges below a certain threshold        #
#################################################################################

import pandas as pd
import argparse

########## Argparse ##########
parser = argparse.ArgumentParser(description="Arguments for this script...")
# Define the inputs
parser.add_argument("-i", "--input", required=True, help="Path to input edgetable from CreateEdgetable.py")

args = parser.parse_args()

input_file = args.input
##############################

# Read in the original edgetable
edgetable = pd.read_csv(input_file)

# Make a for loop that iterates through 0-100 in steps of 5
for i in range(0,100,1):
    edgetable_variant = edgetable[edgetable['Value'] > (i / 100)]
    output_file = f"{i:02d}.csv"
    edgetable_variant.to_csv(output_file, index=False)
    print(f"Created {output_file}...")
