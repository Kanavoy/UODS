from time import time, ctime
from random import seed, randint
start_time = time()
def timestamp(msg=""):
	current = time()
	diff = current - start_time
	print(" : ".join([str(diff), str(ctime(current)), msg]))
timestamp("Importing modules")

from sys import argv, exit
from networkx import number_of_nodes, draw_networkx_edges, draw_networkx_nodes
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from importlib import util
from numpy import linspace
from configparser import ConfigParser
from argparse import ArgumentParser

timestamp("Setting up")

class Group:
	def __init__(self, name):
		self._name = name
	def __str__(self):
		out = "["+self._name+"]\n"
		for k in vars(self):
			if k=="_name":
				continue
			out += k+" = "+str(getattr(self,k))+"\n"
		return out

class Options:
	def __init__(self, names):
		for name in names:
			if "_" not in name:
				continue
			group, label = name.split("_", 1)
			try:
				setattr(getattr(self,group), label, names[name])
			except AttributeError:
				setattr(self, group, Group(group))
				setattr(getattr(self,group), label, names[name])
	def __str__(self):
		return "\n".join(str(getattr(self,k)) for k in vars(self))

def parse_args(args):
	parser = ArgumentParser(description="Model the unified framework.")
	parser.add_argument("-c","--config")
	cfgcheck = ArgumentParser(add_help=False)
	cfgcheck.add_argument("-c","--config")
	cfgfile, unknown = cfgcheck.parse_known_args()
	config = ConfigParser()
	config.read("defaults.cfg")
	if cfgfile.config:
		config.read(cfgfile.config)
	for sec in config:
		for opt in config[sec]:
			params = {
				"default": config[sec][opt],
				"nargs": "?",
			}
			try:
				num = float(params["default"])
				params["type"] = float
				num = int(params["default"])
				params["type"] = int
			except ValueError:
				pass
			if params["default"].endswith(".f"):
				params["type"] = float
			parser.add_argument("-"+sec+"-"+opt, **params)
	argobj = parser.parse_args(args)
	argobj = Options(vars(argobj))
	if argobj.graph.n<2:
		raise ValueError("There must be at least 2 agents")
	return argobj

algs = {}
def load_alg(type, name):
	identifier = type+"-"+name
	# we want to reload algorithms each time this is called,
	# in case they set any globals
	#if identifier not in algs:
	spec = util.spec_from_file_location("", "Algorithms/"+type+"/"+name+".py")
	module = util.module_from_spec(spec)
	spec.loader.exec_module(module)
	algs[identifier] = module
	return algs[identifier]

def generate_graph(opts):
	if opts.graph.seed:
		seed(opts.graph.seed)
	module = load_alg("Edge", opts.graph.alg)
	return module.make_graph(opts)

def set_initial(graph, opts):
	module = load_alg("Initial", opts.initial.alg)
	return module.set_initial(graph, opts)

def generate_layout(graph, opts):
	module = load_alg("Layout", opts.layout.alg)
	return module.make_layout(graph, opts)

def main(args):
	timestamp("Begin")
	opts = parse_args(args)
	do_draw = opts.layout.draw
	
	pregen = time()
	timestamp("Generate Graph")
	graph = generate_graph(opts)
	
	timestamp("Set Initial Values")
	graph.values = set_initial(graph, opts)
	
	cmap = plt.cm.bwr
	new_cmap = colors.LinearSegmentedColormap.from_list(
		'trunc({name},{a:.2f},{b:.2f})'.format(name=cmap.name, a=0.0, b=1),
		cmap(linspace(0.0, 1, cmap.N)))
	
	timestamp("Generate Layout")
	pos = generate_layout(graph, opts)
	opts.layout.pos = pos
	
	if do_draw:		
		timestamp("Draw")
		plt.figure(figsize=(8,8))
		plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
		draw_networkx_edges(graph,pos,alpha=0.4)
		draw_networkx_nodes(graph,pos,node_size=80,
			node_color=graph.values["opinion"],
			cmap=new_cmap
		)
		plt.margins(x=0,y=0)
		#plt.xlim(-0.05,1.05)
		#plt.ylim(-0.05,1.05)
		plt.axis('off')
		plt.gca().autoscale_view(True,True,True)
		plt.show(block=False)
		plt.waitforbuttonpress()
		input("Press any key to begin:")
	
	timestamp("Build updater")
	select_module = load_alg("Group", opts.group.alg)	
	update_module = load_alg("Update", opts.update.alg)
	analysis_module = load_alg("Analysis", opts.analysis.alg)
	intervention_module = load_alg("Intervention", opts.intervention.alg)
	
	timestamp("Perform interventions")
	seed()
	interv_iter = opts.intervention.numb
	while interv_iter > 0:
		interv_iter -= 1
		intervention_module.intervene(graph, opts)
	
	timestamp("Update Loop")
	loop = opts.update.iterations
	if opts.update.iterations_each:
		loop = opts.update.iterations_each * opts.graph.n
	if opts.update.seed:
		seed(opts.update.seed)
	else:
		seed()
	timestamp("Beginning "+str(loop)+" iterations")
	while loop>0:
		loop -= 1
		if not (loop%50000):
			timestamp(str(loop)+" iterations remaining")
		if do_draw and not loop%opts.layout.redraw:
			draw_networkx_nodes(graph,pos,node_size=80,
				node_color=graph.values["opinion"],
				edgecolor=[[0,0,0]],
				cmap=new_cmap
			)
			plt.pause(opts.layout.delay)
		try:
			chosen = select_module.select_agents(graph,opts)
		except IndexError:
			continue
		update_module.perform_update(graph,opts,chosen)
		analysis_module.analyse(graph,opts,chosen)
	if do_draw:
		plt.draw()
	
	timestamp("Post-Analysis")
	analysis_module.final_analysis(graph,opts)
	if do_draw:
		plt.show(block=True)

if __name__=="__main__":
	# for repetition in range(20):
		# for extremists in range(0,20):
			# for uncertainty in range(0,20):
				# args = argv[1:] + [
					# "-initial-uncertainty", str(uncertainty*0.1),
					# "-initial-extreme", str(extremists*0.01)
				# ]
				# print(args)
				# main(args)
	#for p in [(0.5, 0.1), (1.0, 0.1), (1.5, 0.1), (0.5, 0.2), (1.0, 0.2), (1.5, 0.2)]:
	#    for k in range(0,101):
	#        args = argv[1:] + [
	#            "-initial-uncertainty", str(p[0]),
	#            "-initial-extreme", str(p[1]),
	#            "-intervention-numb", str(k),
	#        ]
	args = argv[1:]
	print(args)
	main(args)
