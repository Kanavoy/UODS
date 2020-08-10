from networkx import Graph, connected_components

def intervene(graph,opts):
	# make a temporary copy of the giant component
	temp = Graph(graph)
	cc = list(max(connected_components(graph), key=len))
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
		neighbors = list(temp[node])
		myop = graph.values["opinion"][node]
		extreme_neighbors = [n for n in neighbors if extremists[n]]
		# weight is 1/(distance to closest extremist neighbour) * (proportion of extreme neighbors)
		if len(extreme_neighbors):
			weight = max(abs(1/(myop-graph.values["opinion"][n])) for n in extreme_neighbors)
			weight *= len(extreme_neighbors)/len(neighbors)
			for ex_n in extreme_neighbors:
				target_edges[(node,ex_n)] = weight

	# get the edge with the highest weight and remove it
	targets = sorted(target_edges.items(), key=lambda e: e[1])
	if len(targets):
		edge = targets[-1][0]
		graph.remove_edge(*edge)
	return
