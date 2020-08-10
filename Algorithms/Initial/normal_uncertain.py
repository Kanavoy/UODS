from random import uniform, randint, normalvariate

def set_initial(graph, opts):
	mi = opts.initial.min
	ma = opts.initial.max
	n = range(0,opts.graph.n)
	opinion = [uniform(mi, ma) for node in n]
	sigma = (opts.initial.uncertainty - opts.initial.extreme_uncertainty)/3
	uncertainty = [normalvariate(opts.initial.uncertainty, sigma) for node in n]
	extremists = int((len(n)*opts.initial.extreme)//1)
	for i in range(0, extremists):
		chosen = randint(0,opts.graph.n-1)
		if i<(extremists*opts.initial.extreme_bias):
			opinion[chosen] = 1
		else:
			opinion[chosen] = -1
		uncertainty[chosen] = opts.initial.extreme_uncertainty
	return {"opinion":opinion, "uncertainty":uncertainty}