from random import choice, randrange

def perform_update(graph, opts, agents):
	speaker = choice(agents[0])
	x_i = graph.values["opinion"][speaker]
	u_i = graph.values["uncertainty"][speaker]
	for listener in agents[1]:
		x_j = graph.values["opinion"][listener]
		u_j = graph.values["uncertainty"][listener]
		h_ij = min((x_i+u_i,x_j+u_j)) - max((x_i-u_i,x_j-u_j))
		if h_ij <= u_i:
			try:
				graph.remove_edge(listener, speaker)
			except nxerror:
				try:
					graph.remove_edge(speaker, listener)
				except nxerror:
					pass
			continue
			new_friend = randrange(0,opts.graph.n)
			current_friends = list(graph.neighbors(listener)) 
			while new_friend == listener or new_friend in current_friends:
				new_friend = randrange(0,opts.graph.n)
			graph.add_edge(listener, new_friend)
		rel_a = (h_ij/u_i)-1
		mu = opts.update.mu
		graph.values["opinion"][listener] = x_j + mu * rel_a * (x_i-x_j)
		graph.values["uncertainty"][listener] = u_j + mu * rel_a * (u_i-u_j)