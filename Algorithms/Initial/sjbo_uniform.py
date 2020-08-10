from random import uniform, randint

def set_initial(graph, opts):
	mi = opts.initial.min
	ma = opts.initial.max
	n = range(0,opts.graph.n)
	opinion = [uniform(mi, ma) for node in n]
	assim_thres = [opts.initial.assim_thres for node in n]
	repul_thres = [opts.initial.repul_thres for node in n]
	assim_coeff = [opts.initial.assim_coeff for node in n]
	repul_coeff = [opts.initial.repul_coeff for node in n]
	decay_thres = [opts.initial.decay_thres for node in n]
	decay_coeff = [opts.initial.decay_coeff for node in n]
	hesitation = [opts.initial.hesitation for node in n]
	extremists = int((len(n)*opts.initial.extreme)//1)
	for i in range(0, extremists):
		chosen = randint(0,opts.graph.n-1)
		if i<(extremists*opts.initial.extreme_bias):
			opinion[chosen] = 1
		else:
			opinion[chosen] = -1
	return {
		"opinion":opinion,
		"assim_thres":assim_thres,
		"repul_thres":repul_thres,
		"assim_coeff":assim_coeff,
		"repul_coeff":repul_coeff,
		"decay_thres":decay_thres,
		"decay_coeff":decay_coeff,
		"hesitation":hesitation
	}