from os import listdir
from sys import argv
from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as st
import seaborn as sns
sns.set()

if len(argv) < 2:
	print("Usage",argv[0]," directory <nocost> <nonormalise>")

nocost = "nocost" in argv
nonormalise = "nonormalise" in argv

binsizes = {"degree":1, "paths":0.05, "edge":1}
axis_info = {
	"x":{"name":"uncertainty", "values":[0.60,1.00,1.30,1.60]},
	"y":{"name":"extremists", "values":[0.10,0.15,0.20,0.25]}
}
total_agents = None
total_edges = None

points = []
for fname in listdir(argv[1]):
	if fname.endswith(".csv"):
		points.append("_".join(fname.split("_")[-2:]))
print(list(set(points)))

fig, axes = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(6.4*4, 4.8*4))

totalct = len(set(points))
for ct, point in enumerate(set(points)):
	for alg in ["degree","paths","edge"]:#"degree", "paths", "edge"]: #edge for old tests
		anyfiles = False
		xall = []
		yall = []
		zall = []
		for fname in sorted(listdir(argv[1])):
			showalgs = ["edge rating", "risk rating"]
			if nocost:
				showalgs.extend(["degree", "random"])
			else:
				showalgs.extend(["edge rating (cost agnostic)", "risk rating (cost agnostic)"])
			if not fname.endswith(point) or (not any(x in fname for x in showalgs)) or "heatmap" in fname or ("random" in fname and not "random" in showalgs):
				continue
			
			fname_parts = fname[fname[0]=="_":].split("_")
			total_agents = 200
			total_edges = 400#int(fname_parts[3])*int(fname_parts[4]) #TODO: make this work it out for itself from the filename
			label = fname_parts[0]
			if label == "risk rating":
				label = "vulnerability"
			elif label == "edge rating":
				label = "influence "
			elif label == "risk rating (cost agnostic)":
				label = "vulnerability (cost agnostic)"
			elif label == "edge rating (cost agnostic)":
				label = "influence  (cost agnostic)"
			if fname_parts[1] != alg:
				continue
			if nocost and label.endswith("(cost agnostic)"):
				label = label[:-15]
				
			anyfiles = True
			x = []
			y = []
			z = []
			costs = []
			zeroval = []
			for line in open(argv[1]+"/"+fname, "r"):
				try:
					line = [float(n) for n in line.split(",")]
				except ValueError:
					print("Error in file: ", fname, line)
					continue
				if len(line) == 4: # moves the data along for older reporting alg
					line.append(line[2])
					line.append(line[3])
				if len(line) == 6: # for older alg that didn't track cost
					line.append(0)
				if len(line) != 7:
					continue
				if line[0] == 0:
					zeroval.append(1-line[4])
				else:
					try:
						if nocost:
							x.append(line[0]/total_edges*100)
							if nonormalise:
								y.append(line[4]*total_agents)
							else:
								y.append(1-line[4])
						else:
							binscalar = 1/binsizes[alg]
							x.append(round(line[6]*binscalar)/binscalar)
							y.append(1-line[4])
						z.append(label)
						costs.append(line[6])
					except IndexError:
						print(line, fname)
			
			if len(zeroval) and not nonormalise:
				zeroval = np.mean(zeroval)
				y = list((val-zeroval)/(1-zeroval) for val in y)
			#y = list(((val-zeroval)/(1-zeroval))/costs[i] for i,val in enumerate(y))
			xall.extend(x)
			yall.extend(y)
			zall.extend(z)          
			print(fname)

		if anyfiles:
			loc = point[0:-4].split("_")[:2] # filenames are in (y,x) format FNAR
			loc = [float(loc[1]), float(loc[0])]
			location = [
				axis_info["x"]["values"].index(loc[0]),
				3-axis_info["y"]["values"].index(loc[1]),
			]
			myax = axes[location[1]][location[0]]
			sns.lineplot(x=xall, y=yall, hue=zall, ax=myax)
			foutname = ["{:.2f}".format(float(x)).replace(".","") for x in point[0:-4].split("_")]
			#only show low cost, chosen to be about half of the maximum found
			if "paths" in foutname:
				myax.xlim(0,total_edges/800)
			elif "degree" in foutname:
				myax.set_xlim(0,25*0.5)
			if nocost:
				myax.set_xlim(0,25)
			myax.set_ylim(-0.1,1.0)
			if nonormalise:
				myax.set_ylim(0,200)
			print("Completed", str(ct+1)+"/"+str(totalct)+"\n")

textform = {"ha":"center", "va":"center", "fontsize":48}
smform = {"ha":"center", "va":"center", "fontsize":24}
fig.text(0.5, 0.04, "Uncertainty", **textform)
fig.text(0.21, 0.08, "0.60", **smform)
fig.text(0.41, 0.08, "1.00", **smform)
fig.text(0.61, 0.08, "1.30", **smform)
fig.text(0.81, 0.08, "1.60", **smform)
fig.text(0.06, 0.5, "Extremists", **textform, rotation="vertical")
fig.text(0.09, 0.20, "10%", **smform, rotation="vertical")
fig.text(0.09, 0.40, "15%", **smform, rotation="vertical")
fig.text(0.09, 0.60, "20%", **smform, rotation="vertical")
fig.text(0.09, 0.80, "25%", **smform, rotation="vertical")
plt.savefig(argv[1]+"/grid.png",bbox_inches="tight")
