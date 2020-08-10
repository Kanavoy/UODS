from math import copysign

def perform_update(graph, opts, agents):
	step = copysign(opts.update.mu, graph.values["opinion"][agents[1][0]])
	for node in agents[0]:
		graph.values["opinion"][node] += step