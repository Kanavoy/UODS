import networkx as nx
from pprint import pprint
from random import randint

def analyse(graph,opts,chosen):
	pass

def final_analysis(graph,opts):
	data = {}
	
	all_agents = list(graph.nodes())
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
	
	#connected only
	data["conn_pos_extremists"] = len([n for n in conn_agents if graph.values["opinion"][n] > opts.initial.max * 0.9])
	data["conn_neg_extremists"] = len([n for n in conn_agents if graph.values["opinion"][n] < opts.initial.min * 0.9])
	data["conn_extremist_proportion"] = (data["conn_pos_extremists"]+data["conn_neg_extremists"])/data["conn_agents"]
	data["conn_y_metric"] = (data["conn_pos_extremists"]/data["conn_agents"])**2+(data["conn_neg_extremists"]/data["conn_agents"])**2
	fname = "_".join([str(p) for p in [
		opts.intervention.alg, opts.intervention.mode, abs(opts.intervention.edges),
		opts.graph.n, opts.graph.e,
		opts.initial.extreme, opts.initial.uncertainty,
	]])
	fname += "_00"+str(randint(10,99))+".csv"
	if opts.analysis.name != "default":
		fname = opts.analysis.name + "_" + fname
	print(fname)
	with open(fname,"a") as f:
		#numb, disconnected, total extreme proportion, y metric, connected previous two, total cost
		f.write(str(opts.intervention.numb)+",")
		f.write(str(data["disconnected"])+",")
		f.write(str(data["extremist_proportion"])+",")
		f.write(str(data["y_metric"])+",")
		f.write(str(data["conn_extremist_proportion"])+",")
		f.write(str(data["conn_y_metric"])+",")
		try:
			f.write(str(sum(opts.intervention.costs)))
		except AttributeError as e:
			f.write(str(opts.intervention.numb))
		f.write("\n")
