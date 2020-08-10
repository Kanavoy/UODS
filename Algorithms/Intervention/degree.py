from networkx import all_neighbors
from networkx.exception import NetworkXError as nxerror
from random import random

def intervene(graph,opts):
	try:
		graph.successors
	except AttributeError:
		graph.successors = graph.neighbors

	o = graph.values["opinion"]
	eh = opts.initial.max * 0.9
	el = opts.initial.min * 0.9
	# limit removals to only extremist agents
	t = {n:len(list(graph.successors(n))) for n in graph if not el < o[n] < eh}
	# get most central extreme agent
	te = max(t.keys(),key=lambda k: t[k])
	# get the most central neighbor of that agent
	if not len(list(graph.successors(te))):
		return
	tn = max(list(graph.successors(te)),key=lambda k: len(list(graph[k])))
	
	# compute costs
	try:
		opts.intervention.costs
	except AttributeError:
		opts.intervention.costs = []
	edge_costs = {}
	for k in [(te,tn)]:
		my_adj = list(all_neighbors(graph,k[0]))
		other_adj = list(all_neighbors(graph,k[1]))
		if opts.intervention.mode in ["degree","degree-ignore"]:
			edge_costs[k] = (len(my_adj)+len(other_adj))/(2*max([len(list(all_neighbors(graph,n))) for n in graph]))
		elif opts.intervention.mode == "random":
			edge_costs[k] = random()
		elif opts.intervention.mode in ["paths","paths-ignore"]:
			edge_costs[k] = (sum([n in other_adj for n in my_adj])/len(my_adj)+sum([n in my_adj for n in other_adj])/len(other_adj))/2
		else:
			edge_costs[k] = 1
	
	try:
		graph.remove_edge(te,tn)
	except nxerror:
		try:
			graph.remove_edge(tn,te)
		except nxerror:
			pass
	opts.intervention.costs.append(edge_costs[(te,tn)] or 1)
	return
