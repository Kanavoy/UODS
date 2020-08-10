from random import sample, randint
import matplotlib.pyplot as plt

def analyse(graph,opts,chosen):
	try:
		opts.analysis.output
	except AttributeError:
		s = sample(range(opts.graph.n),int(opts.graph.n*opts.analysis.p))
		opts.analysis.output = {a:[] for a in s}
	for agent in opts.analysis.output.keys():
		opts.analysis.output[agent].append(graph.values["opinion"][agent])

def final_analysis(graph,opts):
	for k,v in opts.analysis.output.items():
		plt.plot(v)
	#plt.title("Extremists: "+str(len([n for n in list(graph.nodes()) if graph.values["opinion"][n] > opts.initial.max * 0.9 or graph.values["opinion"][n] < opts.initial.min * 0.9])))
	plt.xlabel("Interaction Number")
	plt.ylabel("Opinion")
	fname = "_".join([str(p) for p in [
		opts.intervention.alg, opts.intervention.mode, opts.intervention.numb,
		opts.graph.n, opts.graph.e,
		opts.initial.uncertainty, opts.initial.extreme,
		randint(10000,99999)
	]])+".png"
	plt.savefig(fname)
	plt.gcf().clear()