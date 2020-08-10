from random import choice

def set_initial(graph, opts):
	ch = list(range(0,getattr(opts.initial, "options", 2)))
	mi = opts.initial.min
	ma = opts.initial.max
	ra = (ma-mi)/(len(ch)-1)
	n = range(0,opts.graph.n)
	opinion = [mi+(choice(ch)*ra) for node in n]
	return {"opinion":opinion}