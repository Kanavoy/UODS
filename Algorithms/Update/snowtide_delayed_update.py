from random import choice

count = 0

def perform_update(graph, opts, agents):
	global count
	count+=1
	partner = choice(agents[1])
	x_i = graph.values["opinion"][partner]
	u_i = graph.values["uncertainty"][partner]
	int_agent = graph.values["is_intervention_agent"][partner]
	# we can't choose new agents in this stage, that's a communication rule,
	# and is handled by -group-alg. All we can do is abort the communication
	# and wait for the next iteration
	if int_agent is True and count < opts.initial.delay_int:
		print("choosing new agent because", partner, "is one of ours")
		return
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