# filepaths, except with dots instead of slashes and no file extension
from Algorithms.Update.relative_agreement import perform_update as wrapped_update
from Algorithms.Intervention.degree import intervene as wrapped_intervene

# make sure you set opts.intervention.numb to 0, otherwise
# it'll execute the interventions at the start as well

count = 0

def perform_update(graph, opts, agents):
	global count
	count += 1
	if count == 1000:
		wrapped_intervene(graph, opts)
	wrapped_update(graph, opts, agents)
