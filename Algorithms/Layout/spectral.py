def make_layout(graph, opts, layout=None):	
	from networkx import spectral_layout
	return spectral_layout(graph)