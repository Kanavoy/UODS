def intervene(graph, opts):
	# agent IDs need to be numbers, so just give the new one
	# the next available ID number
	agent_num = len(list(graph.nodes()))
	# add the node to the graph, and its opinion/uncertainty
	# to the appropriate value lists
	graph.add_node(agent_num)
	graph.values["opinion"].append(0)
	graph.values["uncertainty"].append(0.1)
	# if you're adding a value that wasn't set in the initial algorithm,
	# you have to pre-seed values for the nodes like so
	if "is_intervention_agent" not in graph.values:
		graph.values["is_intervention_agent"] = [False for n in graph.nodes]
	graph.values["is_intervention_agent"].append(True)
	print("Added agent", agent_num)
	# connect it to every node in the graph
	for node in graph.nodes():
		graph.add_edge(agent_num, node)
