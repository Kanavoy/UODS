def make_graph(opts):
	from networkx import newman_watts_strogatz_graph
	return newman_watts_strogatz_graph(opts.graph.n, opts.graph.e, opts.graph.p)