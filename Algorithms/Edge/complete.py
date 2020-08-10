def make_graph(opts):
	from networkx import complete_graph
	return complete_graph(opts.graph.n)