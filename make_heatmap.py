from scipy.interpolate import griddata
from sys import argv, exit
import numpy as np
import matplotlib.pyplot as plt

if len(argv) < 2:
	print("Usage:",argv[0],"file\nProduces a heatmap from the targeted csv file.")
	exit()

data = {}
# open datafile, read each line into dictionary of {point:[list of values]}
with open(argv[1], "r") as datafile:
	for line in datafile.readlines():
		line = [float(n) for n in line.split(",")]
		point = (line[0],line[1])
		if point not in data:
			data[point] = [line[2]]
		else:
			data[point].append(line[2])
# take the arithmetic mean, where a point has multiple
# values thanks to repeating the experiment
for point in data.keys():
	data[point] = sum(data[point])/len(data[point])

# generate the list of points we want to interpolate into
uncertainty = (min(n[0] for n in data.keys()), max(n[0] for n in data.keys()))
extremists = (min(n[1] for n in data.keys()), max(n[1] for n in data.keys()))
grid_x, grid_y = np.mgrid[uncertainty[0]:uncertainty[1]:1000j, extremists[1]:extremists[0]:1000j]

points = [[n for n in p] for p in data.keys()]

# interpolate heatmap data
heatmap = griddata(points, list(data.values()), (grid_x, grid_y) , method="cubic")

# render
plt.xlabel("Uncertainty")
plt.ylabel("Extremists")
plt.imshow(heatmap.T, extent=(*uncertainty,*extremists), aspect="auto", interpolation="bicubic", cmap="hot_r", vmin=0, vmax=1)
plt.colorbar()
plt.show()