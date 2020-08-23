from os import listdir
from sys import argv, exit

if len(argv) < 2:
	print("Usage:",argv[0],"directory\nCombines .csv files in the targeted directory. Intended to be used with the heatmap analysis algorithm")
	exit()
for file in listdir(argv[1]):
	if file.endswith(".csv"):
		with open(file[:-9]+".csv", "a") as outfile:
			with open(file, "r") as infile:
				outfile.write(infile.read())
