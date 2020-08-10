from networkx import Graph, connected_components, DiGraph, all_neighbors
from networkx.exception import NetworkXError as nxerror
from random import random

def intervene(graph,opts):
	# make a temporary copy of the giant component
	temp = DiGraph(graph)
	cc = []
	try:
		cc = list(max(connected_components(graph), key=len))
	except:
		cc = list(graph)
	ncc = [n for n in list(graph.nodes()) if n not in cc]
	
	temp.remove_nodes_from(ncc)

	# get a dictionary of "is a node extremist"
	eh = opts.initial.max * 0.9
	el = opts.initial.min * 0.9
	extremists = {n: not el < graph.values["opinion"][n] < eh for n in temp.nodes()}

	# assign weights to edges
	target_edges = {}
	for node in temp.nodes():
		# we don't trim edges from the extremist agents, but rather from their targets
		if extremists[node]:
			continue
		neighbors = temp.predecessors(node)
		myop = graph.values["opinion"][node]
		extreme_neighbors = [n for n in neighbors if extremists[n]]
		# weight is 1/(distance to closest extremist neighbour)
		if len(extreme_neighbors):
			weight = max(abs(1/(myop-graph.values["opinion"][n] or 0.001)) for n in extreme_neighbors)
			for ex_n in extreme_neighbors:
				target_edges[(node,ex_n)] = weight
	
	# compute costs
	try:
		opts.intervention.costs
	except AttributeError:
		opts.intervention.costs = []
	edge_costs = {}
	for k in target_edges:
		my_adj = list(all_neighbors(temp,k[0]))
		other_adj = list(all_neighbors(temp,k[1]))
		if opts.intervention.mode in ["degree","degree-ignore"]:
			edge_costs[k] = (len(my_adj)+len(other_adj))/(2*max([len(list(all_neighbors(temp,n))) for n in temp]))
		elif opts.intervention.mode == "random":
			edge_costs[k] = random()
		elif opts.intervention.mode in ["paths","paths-ignore"]:
			edge_costs[k] = (sum([n in other_adj for n in my_adj])/len(my_adj)+sum([n in my_adj for n in other_adj])/len(other_adj))/2
			if edge_costs[k] == 0:
				edge_costs[k] = 0.01 # avoids /0 error when we divide by costs
		else:
			edge_costs[k] = 1

	# get the edge with the highest weight and remove it
	targets = []
	if opts.intervention.mode.endswith("-ignore"):
		targets = sorted(target_edges.items(), key=lambda e: e[1])
	else:
		targets = sorted(target_edges.items(), key=lambda e: e[1]/max(edge_costs[e[0]],0.01))
	if len(targets):
		edge = targets[-1][0]
		opts.intervention.costs.append(edge_costs[edge])
		try:
			graph.remove_edge(*edge)
		except nxerror:
			try:
				graph.remove_edge(edge[1],edge[0])
				print("removed edge ("+str(edge[1])+", "+str(edge[0])+")")
			except nxerror:
				pass
	return
