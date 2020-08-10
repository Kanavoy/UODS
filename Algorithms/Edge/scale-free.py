def make_graph(opts):
	from networkx import barabasi_albert_graph
	return barabasi_albert_graph(opts.graph.n, opts.graph.e)