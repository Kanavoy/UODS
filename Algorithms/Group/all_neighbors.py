from random import choice

def select_agents(graph, opts):
	node = choice(list(graph.nodes()))
	return ([node], list(graph.neighbors(node)))