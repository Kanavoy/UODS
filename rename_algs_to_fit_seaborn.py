from os import listdir, rename
from os.path import splitext
from sys import argv, exit

if len(argv) < 2:
	print("Usage:",argv[0],"directory")
	exit()

for fname in listdir(argv[1]):
	fn, fe = splitext(fname)
	newfn = fn.replace("uniform_no_extreme_hubs", "uniform no extreme hubs")
	newfn = newfn.replace("degree-ignore", "(cost agnostic)_degree")
	newfn = newfn.replace("paths-ignore", "(cost agnostic)_paths")
	newfn = newfn.replace("uniform_extreme_hubs", "uniform extreme hubs")
	newfn = newfn.replace("edge_rating", "edge rating")
	newfn = newfn.replace("risk_rating", "risk rating")
	newfn = newfn.replace("_(cost agnostic)", " (cost agnostic)")
	rename(argv[1]+"/"+fname, argv[1]+"/"+newfn+fe)