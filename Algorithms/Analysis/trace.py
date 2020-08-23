from random import sample
import matplotlib.pyplot as plt

def analyse(graph,opts,chosen):
	try:
		opts.analysis.choices
		opts.analysis.output
	except AttributeError:
		opts.analysis.choices = sample(range(opts.graph.n),int(opts.graph.n*opts.analysis.p))
		opts.analysis.output = {}
	if not len(chosen[1]):
		return
	agent = chosen[1][0]
	if agent in opts.analysis.choices:
		try:
			opts.analysis.output[agent].append(graph.values["opinion"][agent])
		except KeyError:
			opts.analysis.output[agent] = [graph.values["opinion"][agent]]

def final_analysis(graph,opts):
	for k,v in opts.analysis.output.items():
		plt.plot(v)
	plt.xlabel("Interaction")
	plt.ylabel("Opinion")
	plt.show()
