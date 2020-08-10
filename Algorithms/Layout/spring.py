def make_layout(graph, opts, layout=None):	
	from networkx import spring_layout
	return spring_layout(graph)