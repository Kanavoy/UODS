from random import choice

def perform_update(graph, opts, agents):
	partner = choice(agents[1])
	x_i = graph.values["opinion"][partner]
	u_i = graph.values["uncertainty"][partner]
	for node in agents[0]:
		x_j = graph.values["opinion"][node]
		u_j = graph.values["uncertainty"][node]
		h_ij = min((x_i+u_i,x_j+u_j)) - max((x_i-u_i,x_j-u_j))
		if h_ij <= u_i:
			continue
		rel_a = (h_ij/u_i)-1
		mu = opts.update.mu
		graph.values["opinion"][node] = x_j + mu * rel_a * (x_i-x_j)
		graph.values["uncertainty"][node] = u_j + mu * rel_a * (u_i-u_j)