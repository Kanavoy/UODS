import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors #tyop intentional
from networkx import draw_networkx as nxdraw
from numpy import linspace
from imageio import imread, mimwrite
from os import remove

cdown = 0
imgs = 0
ims = []
fig = plt.figure(figsize=(8,8))
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.ioff()
cmap = plt.cm.bwr
new_cmap = colors.LinearSegmentedColormap.from_list(
	'trunc({name},{a:.2f},{b:.2f})'.format(name=cmap.name, a=0.0, b=1),
	cmap(linspace(0.0, 1, cmap.N)))

def analyse(graph,opts,chosen):
	global cdown, imgs
	
	cdown = (cdown+1)%opts.analysis.draw_interval
	if cdown == 0:
		plt.clf()
		nxdraw(graph, opts.layout.pos,
			node_color=graph.values["opinion"],
			cmap=new_cmap
		)
		fname = "temp_"+str(imgs)+".png"
		imgs += 1
		plt.savefig(fname, bbox_inches="tight")
		ims.append(fname)
	return

def final_analysis(graph,opts):
	images = [imread(f) for f in ims]
	fname = "out."+opts.analysis.file_format
	mimwrite(fname, images, fps=opts.analysis.frames_per_second)
	[remove(f) for f in ims]
	return