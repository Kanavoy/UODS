from random import choice

steps = 0

def perform_update(graph, opts, agents):
	global steps
	for poster in agents[0]:
		x_i = graph.values["opinion"][poster]
		if steps < opts.intervention.block_extreme_until:
			if x_i < opts.initial.min * 0.9 or x_i > opts.initial.max * 0.9:
				continue
		u_i = graph.values["uncertainty"][poster]
		for reader in agents[1]:
			x_j = graph.values["opinion"][reader]
			u_j = graph.values["uncertainty"][reader]
			h_ij = min((x_i+u_i,x_j+u_j)) - max((x_i-u_i,x_j-u_j))
			if h_ij <= u_i:
				continue
			rel_a = (h_ij/u_i)-1
			mu = opts.update.mu
			graph.values["opinion"][reader] = x_j + mu * rel_a * (x_i-x_j)
			if abs(x_j-x_i) < opts.update.nearby_opinion_range:
				graph.values["uncertainty"][reader] = u_j * 0.9
			elif abs(x_j-x_i) < opts.update.far_opinion_range:
				graph.values["uncertainty"][reader] = u_j * 1.1
				
	steps += 1
