from networkx import all_neighbors
from random import choice

def intervene(graph,opts):
	te = choice(list(graph.nodes()))
	if opts.intervention.mode == "agent":
		graph.remove_node(te)
	elif opts.intervention.mode == "edge":
		neighbors = graph.predecessors(te)
		if len(neighbors):
			tn = choice(neighbors)
			graph.remove_edge(te,tn)
	return