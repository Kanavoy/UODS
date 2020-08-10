from networkx import pagerank, all_neighbors, Graph, connected_components

def intervene(graph,opts):
	temp = Graph(graph)
	cc = list(max(connected_components(graph), key=len))
	ncc = [n for n in list(graph.nodes()) if n not in cc]
	temp.remove_nodes_from(ncc)
	c = pagerank(temp)
	o = graph.values["opinion"]
	eh = opts.initial.max * 0.9
	el = opts.initial.min * 0.9
	# limit removals to only extremist agents
	t = {n:c[n] for n in c if not el < o[n] < eh}
	# get most central extreme agent
	te = max(t.keys(),key=lambda k: t[k])
	# get the most central neighbor of that agent
	tn = max(all_neighbors(temp,te),key=lambda k: c[k])
	if opts.intervention.mode == "agent":
		graph.remove_node(te)
	elif opts.intervention.mode == "edge":
		graph.remove_edge(te,tn)
	return