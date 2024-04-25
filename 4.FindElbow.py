#################################################################################
#       FindElbow.py                                                            #
#       This script finds the number of communities in each edgetable from      #
#       EdgetableVariations.py and plots the graph, and also gets the           #
#       cumulative area under the curve for this graph, to find the elbow       #
#       of the curve to determine which edgetable to use (this must be done)    #
#       in R though...                                                          #
#                                                                               #
#                                                                               #
#       TO USE:                                                                 #
#       This provide the pathway to the directory containing
#################################################################################

import pandas as pd
import igraph as ig
import datetime
import glob


# Get a list of all CSV files in the current directory (Edgetables from EdgetableVariations.py, make sure they're named in order)
csv_files = glob.glob("*.csv")

# Initialise dataframe for saving/using number of coms by iteration
ComsByIter = pd.DataFrame(columns=['Iteration', 'NumberCommunities'])

# Loop through the CSV files
for file in csv_files:
	# Read the CSV file into a DataFrame
	df = pd.read_csv(file)
	# Make the graph out of the edgetable
	g = ig.Graph.TupleList(df.itertuples(index=False), directed=False, edge_attrs=["Value"])
	# Find the number of communities
	communities = g.community_multilevel(weights=g.es["Value"], return_levels=False)
	num_coms = len(communities)

	# Get the filename without the '.csv' extension
	# NOTE: this is important as the filenames given by EdgetableVariations.py are numbers with .csv on the end, this allows for the AUC calc to work
	iteration = file.split('.csv')[0]
	# Append to dataframe
	ComsByIter = ComsByIter._append({"Iteration": iteration, "NumberCommunities": num_coms}, ignore_index=True)

# Reorder the dataframe numerically by iteration
ComsByIter = ComsByIter.sort_values(by="Iteration")
ComsByIter = ComsByIter.reset_index(drop=True)

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
NumCommunitiesOutput = f"NumComsByIteration_{formatted_datetime}.csv"
ComsByIter.to_csv(NumCommunitiesOutput, index=False)

print(f"{NumCommunitiesOutput} created...")

# Find the AUC of previous dataframe
# Initialise the variables to store the cumulative area and the previous point
cumulative_area = 0

prev_x = None
prev_y = None

# Initialise the AUC table
AUC = pd.DataFrame(columns=['Iteration', 'CumulativeAUC'])

# Iterate through the data to caluculate the areas
for index, row in ComsByIter.iterrows():
	x, y = row['Iteration'], row['NumberCommunities']
	if prev_x is not None:
		prev_y = float(prev_y)
		prev_x = float(prev_x)
		y = float(y)
		x = float(x)
		area = 0.5 * (y + prev_y) * (x - prev_x)
		cumulative_area += area
	prev_x = x
	prev_y = y
	AUC = AUC._append({'Iteration': x, 'CumulativeAUC': cumulative_area}, ignore_index=True)

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
AUCCommunitiesOutput = f"ComsAUCByIteration_{formatted_datetime}.csv"
AUC.to_csv(AUCCommunitiesOutput, index=False)

print(f"{AUCCommunitiesOutput} created...")

print(f"To find the elbow of the curve, load {AUCCommunitiesOutput} into R and run the following: ")
print('install.packages("pathviewr")')
print('library(pathviewr)')
print(f"AUC <- read.csv({NumCommunitiesOutput})")
print('find_curve_elbow(AUC, export_type="row_num", plot_curve=TRUE)')

print("This will give you the iteration to use for the edgetable")
