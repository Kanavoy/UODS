def make_graph(opts):
	from networkx import grid_2d_graph, convert_node_labels_to_integers
	m = opts.graph.n**0.5//1
	n = 0
	while m:
		t = opts.graph.n % m
		if not t:
			n = opts.graph.n / m
			break
		m -= 1
	return convert_node_labels_to_integers(grid_2d_graph(int(m),int(n)))