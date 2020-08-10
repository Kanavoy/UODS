from networkx import pagerank, all_neighbors, Graph, connected_components
from random import choice

def intervene(graph,opts):
	temp = Graph(graph)
	cc = list(max(connected_components(graph), key=len))
	ncc = [n for n in list(graph.nodes()) if n not in cc]
	temp.remove_nodes_from(ncc)
	c = pagerank(temp)
	o = graph.values["opinion"]
	eh = opts.initial.max * 0.9
	el = opts.initial.min * 0.9
	# limit removals to only non-extremist agents
	t = {n:c[n] for n in c if el < o[n] < eh}
	# get most central non-extreme agent
	te = max(t.keys(),key=lambda k: t[k])
	# get the most central extreme neighbor of that agent
	tn = None
	ex_neighbours = [n for n in list(all_neighbors(temp,te)) if not el < o[n] < eh]
	if len(ex_neighbours):
		if opts.intervention.mode == "central":
			tn = max(ex_neighbours,key=lambda k: c[k])			
		elif opts.intervention.mode == "random":
			tn = choice(ex_neighbours)
	if tn:
		graph.remove_edge(te,tn)
	return