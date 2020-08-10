from random import uniform, randint, choice
from networkx import degree_centrality as degree

def set_initial(graph, opts):
	mi = opts.initial.min
	ma = opts.initial.max
	n = range(0,opts.graph.n)
	opinion = [uniform(mi, ma) for node in n]
	uncertainty = [opts.initial.uncertainty for node in n]
	extremists = int((len(n)*opts.initial.extreme)//1)
	# hubs are loosely defined as the top 25% of agents by degree	
	hubs = sorted(degree(graph).items(), key=lambda i:i[1], reverse=True)[:len(graph)//4]
	hubs = [n[0] for n in hubs]
	for i in range(0, extremists-2):
		chosen = randint(0,opts.graph.n-1)
		if i<(extremists*opts.initial.extreme_bias):
			opinion[chosen] = 1
		else:
			opinion[chosen] = -1
		uncertainty[chosen] = opts.initial.extreme_uncertainty
	for i in range(2):
		chosen = choice(hubs)
		if uncertainty[chosen] == opts.initial.extreme_uncertainty:
			chosen = choice(hubs)
		opinion[chosen] = 1 if i else -1
		uncertainty[chosen] = opts.initial.extreme_uncertainty
	return {"opinion":opinion, "uncertainty":uncertainty}