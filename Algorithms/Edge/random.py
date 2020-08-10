def make_graph(opts):
	from networkx import fast_gnp_random_graph
	return fast_gnp_random_graph(opts.graph.n, opts.graph.p)