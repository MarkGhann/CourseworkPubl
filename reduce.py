def trueSearch(G):
	true_tracks = {}
	for task in G.Tree.keys():
		close_tasks = G.get_close_better(task)
		true_anomal_sets = {}
		for imanomal in G.get_anomal(task):
			paths = G.get_under_pseudopaths(imanomal)
			true_sets = {}
			for close in close_tasks:
				true_paths = {}
				i = 0
				for path in paths.value():
					if G.task_in_path(close, path):
						true_paths[i] = path
						i += 1
				true_sets[close] = true_paths
			true_anomal_sets[imanomal] = true_sets
		true_tracks[task] = true_anomal_sets
	return true_tracks

def reduceSets(G): # It is impossible to reduce any set without interval handling
	true_tracks = trueSearch(G)
	return G
	
	
	
	
def reduceIntervals(G,task):
	result_graph = copyGraph(G)
	true_tracks = trueSearch(result_graph)
	if not result_graph.Tasks[task].Inf:
		
	elif []
		pass
	else
		pass
	return result_graph
