from networkx import shell_layout

def make_layout(graph, opts, layout=None):
	sortlist = sorted(graph, key=lambda l: len(graph[l]), reverse=True)
	shells = []
	sh = 0
	cu = 0
	while cu < len(sortlist):
		shells.append(sortlist[cu: cu+3**sh])
		cu += 3**sh
		sh += 1
	return shell_layout(graph, shells)