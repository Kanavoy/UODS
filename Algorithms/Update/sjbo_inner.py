from random import choice

def perform_update(graph, opts, agents):
	partner = choice(agents[1])
	x_j = graph.values["opinion"][partner]
	for node in agents[0]:
		x_i = graph.values["opinion"][node]
		e_i = graph.values["assim_thres"][node]
		t_i = graph.values["repul_thres"][node]
		a_i = graph.values["assim_coeff"][node]
		r_i = graph.values["repul_coeff"][node]

		diff = abs(x_i - x_j)
		if diff <= e_i:
			graph.values["opinion"][node] += a_i * (x_j-x_i)
		elif t_i <= diff:
			graph.values["opinion"][node] -= r_i * (x_j-x_i) * (1-abs(x_i))/2
