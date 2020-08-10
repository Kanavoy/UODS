import networkx as nx
from numpy.random import lognormal, choice, random

def make_graph(opts):
	graph = nx.DiGraph()
	n = opts.graph.n
	mean_out = opts.graph.mean or max(1,(n//50))
	std_out = opts.graph.std or (n/20)

	# Copy of Barabasi-Albert graph, except using DiGraph constructor
	G = nx.empty_graph(mean_out, create_using=nx.DiGraph)
	targets = list(range(mean_out))
	repeated_nodes = []
	source = mean_out
	while source < n:
		m = min(int(lognormal(mean_out, std_out)), len(G)-1)
		G.add_edges_from(zip(targets, [source] * m)) # swap order so nodes choose who influenced by
		repeated_nodes.extend(targets)
		repeated_nodes.extend([source] * m)
		targets = _random_subset(repeated_nodes, m)
		source += 1
	# For each node, create reciprocal link to follower depending on their follower count
	new_edges = []
	max_followers = max([len(G.succ[follower]) for follower in G])
	for node in G:
		for follower in G.succ[node]:
			if random() < ((len(G.succ[follower])+1)/(max_followers+1)): # +1 so even those with 0 followers have chance
				new_edges.append((follower, node))
	G.add_edges_from(new_edges)
	return G
	
def _random_subset(seq, m):
	targets = set()
	if len(seq) <= m:
		return set(seq)
	while len(targets) < m and len(targets) != len(seq)-1:
		x = choice(seq)
		targets.add(x)
	return targets