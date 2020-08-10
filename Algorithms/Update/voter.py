from collections import Counter

def perform_update(graph, opts, agents):
	counts = Counter(graph.values["opinion"][n] for n in agents[1])
	new_op = counts.most_common(1)[0][0]
	for node in agents[0]:
		graph.values["opinion"][node] = new_op