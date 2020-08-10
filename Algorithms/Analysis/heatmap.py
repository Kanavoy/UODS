import networkx as nx
from pprint import pprint
from random import randint

def analyse(graph,opts,chosen):
	pass

def final_analysis(graph,opts):
	data = {}
	
	all_agents = list(graph.nodes())
	conn_agents = []
	try:
		conn_agents = list(max(nx.connected_components(graph), key=len))
	except nx.exception.NetworkXNotImplemented:
		conn_agents = list(graph.nodes())
	
	data["agents"] = nx.number_of_nodes(graph)
	data["conn_agents"] = len(conn_agents)
	data["disconnected"] = (data["agents"] - len(conn_agents))/data["agents"]
	
	#all
	data["pos_extremists"] = len([n for n in all_agents if graph.values["opinion"][n] > opts.initial.max * 0.9])
	data["neg_extremists"] = len([n for n in all_agents if graph.values["opinion"][n] < opts.initial.min * 0.9])
	data["extremist_proportion"] = (data["pos_extremists"]+data["neg_extremists"])/data["agents"]
	data["y_metric"] = (data["pos_extremists"]/data["agents"])**2+(data["neg_extremists"]/data["agents"])**2
	
	fname = opts.analysis.x.split(".")[-1]+"_"+opts.analysis.y.split(".")[-1]+str(randint(10000,99999))+".csv"

	with open("heatmap_"+str(opts.update.mu)+"_"+fname,"a") as f:		
		x = opts
		xloc = opts.analysis.x.split(".")[1:]
		for part in xloc:
			x = getattr(x, part)
		y = opts
		yloc = opts.analysis.y.split(".")[1:]
		for part in yloc:
			y = getattr(y, part)
		
		f.write(str(x)+",")
		f.write(str(y)+",")
		f.write(str(data["y_metric"])+"\n")
