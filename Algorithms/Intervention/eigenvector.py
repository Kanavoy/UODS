from networkx import eigenvector_centrality, all_neighbors

def intervene(graph,opts):
	c = eigenvector_centrality(graph,max_iter=1000,tol=1e-3)
	o = graph.values["opinion"]
	eh = opts.initial.max * 0.9
	el = opts.initial.min * 0.9
	# limit removals to only extremist agents
	t = {n:c[n] for n in c if not el < o[n] < eh}
	# get most central extreme agent
	te = max(t.keys(),key=lambda k: t[k])
	# get the most central neighbor of that agent
	tn = max(all_neighbors(graph,te),key=lambda k: c[k])
	if opts.intervention.mode == "agent":
		graph.remove_node(te)
	elif opts.intervention.mode == "edge":
		graph.remove_edge(te,tn)
	return