import pandas as pd
import pickle
import networkx as nx
import re
import csv
import matplotlib.pyplot as plt
import copy
import collections
import numpy as np
import community

def edge_contraction(G, liberals, conservatives):

	print("Before contraction")
	print nx.number_of_nodes(G)
	print nx.number_of_edges(G)

	for node in G.nodes:
		neighbors_to_remove = []
		for neighbor in G.neighbors(node):
			if G[node][neighbor]['weight'] <= 2:
				neighbors_to_remove.append(neighbor)
		for nbr in neighbors_to_remove:
			G.remove_edge(node, nbr)
	nodes_to_remove = []
	for node in G.nodes:
		if (len(list(G.neighbors(node))) == 0):
		# if (len(list(G.neighbors(node))) == 0) and (len(list(G.predecessors(node))) == 0):
			nodes_to_remove.append(node)
	for nd in nodes_to_remove:
		G.remove_node(nd)

	print("After contraction")
	print nx.number_of_nodes(G)
	print nx.number_of_edges(G)

	# print(nx.average_clustering(G))

	graphic(G, liberals, conservatives)

	# analyze_clustering(Gundir, liberals, conservatives, False)
	# analyze_clustering(G, liberals, conservatives, True)

def degree_dist(G, liberals, conservatives):
	degree_sequence = sorted([d for n, d in G.degree()], reverse = True)
	degree_count = collections.Counter(degree_sequence)
	deg, cnt = zip(*degree_count.items())

	plt.loglog(deg, cnt, 'yo')
	plt.title("Degree Count on Log Scale")
	plt.xlabel("Degree")
	plt.ylabel("Number of Nodes")
	plt.savefig('degree_count.png')

def clique_analysis(Gundir):

	#print ("Cliques in Directed Graph: ", list(nx.enumerate_all_cliques(G)))
	cliques = list(nx.find_cliques(Gundir))
	cliques_sorted = [sorted(cliques, key = len, reverse = True)]
	for cliques in cliques_sorted:
		cliques_limited = [cli for cli in cliques if len(cli) > 17]
		print len(cliques_limited)
		for clique in cliques_limited:
			if len(clique) > 17:
				print clique
				liberal_users = set()
				conservative_users = set()
				for user in clique:
					user = str(user)
					if user in liberals:
						liberal_users.add(user)
					if user in conservatives:
						conservative_users.add(user)
				print("Size of Clique: ", len(clique))
				print("Num of liberals: ", len(liberal_users))
				print("Num of conservatives: ", len(conservative_users))

def analyze_clustering(G, liberals, conservatives, dir):
	if not dir:
		# cc = nx.connected_components(G)
		subgraphs = list(nx.connected_component_subgraphs(G))
		#print("Average Clustering Coefficient Undirected Full Graph: ", nx.average_clustering(G))
		# print("Average Clustering Coefficient Undirected Max Subgraph: ", nx.average_clustering(max(subgraphs, key=len)))
	else:
		# cc = nx.strongly_connected_components(G)
		subgraphs = list(nx.strongly_connected_component_subgraphs(G))
		with open("subgraphs_1750.pickle", 'wb') as handle:
			pickle.dump(subgraphs, handle, protocol = 2)
		G = None
		#print("Average Clustering Coefficient Directed Full Graph: ", nx.average_clustering(G))
	print [len(c) for c in sorted(subgraphs, key = len, reverse = True)][:10]
	largest_component = max(subgraphs, key = len)
	subgraphs = None
	# subgraphs.sort(key = len, reverse = True)
	# second_largest_component = subgraphs[1]
	# print(len(second_largest_component))
	nx.write_weighted_edgelist(largest_component, "directed_mx_subgraph_1750")
	# print("Average Clustering Coefficient Max Subgraph: ", nx.average_clustering(largest_component))
	liberal_users = set()
	conservative_users = set()
	for user in largest_component:
		# print user
		if user in liberals:
			liberal_users.add(user)
		if user in conservatives:
			conservative_users.add(user)
	# print "\n"
	# for user in second_largest_component:
	# 	print user
	print("Size of largest connected component: ", len(largest_component))
	print("Num of liberals: ", len(liberal_users))
	print("Num of conservatives: ", len(conservative_users))
	

def graphic(G, liberals, conservatives):
	# Keep track of political leaning
	left = []
	right = []
	others = []

	for user in G.nodes():
		if user in liberals:
			left.append(user)
		elif user in conservatives:
			right.append(user)
		else:
			others.append(user)


	pos = nx.spring_layout(G)
	print("post pos")

	nx.draw_networkx_nodes(G, pos, nodelist=right, node_color='r', node_size = 50)
	print("drew conservative")
	nx.draw_networkx_nodes(G, pos, nodelist=left, node_color='b', node_size = 50)
	print("drew liberal")
	nx.draw_networkx_nodes(G, pos, nodelist=others, node_color='k', node_size=2, alpha=0.1)
	print("drew others")
	nx.draw_networkx_edges(G, pos, edge_color='g', width=0.1, alpha=0.1)

	# nx.draw(G, nodelist=right, node_color='r', node_size = 50)
	# print("drew conservative")
	# nx.draw(G, nodelist=left, node_color='b', node_size = 50)
	# print("drew liberal")
	# nx.draw(G, nodelist=others, node_color='k', node_size=2, alpha=0.1)
	# print("drew others")
	# nx.draw(G, edge_color='g', width=0.1, alpha=0.1)

	print("should be displaying")

	plt.show()

def find_other_ideologues(G, liberals, conservatives):
	liberal_connections = {}
	conservative_connections = {}
	for lib in liberals:
		if G.has_node(lib):
			# neighbors looks at out edges
			# predecessors looks a in edges

			# for nbr in G.neighbors(lib):
			for nbr in G.predecessors(lib):
				if nbr in liberal_connections:
					liberal_connections[nbr] += 1
				else:
					liberal_connections[nbr] = 1
	for cons in conservatives:
		if G.has_node(cons):
			# for nbr in G.neighbors(cons):
			for nbr in G.predecessors(cons):
				if nbr in conservative_connections:
					conservative_connections[nbr] += 1
				else:
					conservative_connections[nbr] = 1
	print sorted(liberal_connections.items(), key = lambda x: x[1])
	with open("liberal_connections_undir.pickle", 'wb') as handle:
		pickle.dump(liberal_connections, handle, protocol = 2)
	with open("conservative_connections_undir.pickle", 'wb') as handle:
		pickle.dump(conservative_connections, handle, protocol = 2)

def community_detection(Graph, liberals, conservatives):
 	# partition = community.best_partition(Graph)
 	# mod = community.modularity(partition, Graph)
 	# with open("community_louvain_1750.pickle", 'wb') as handle:
 	# 	pickle.dump(partition, handle, protocol = 2)
 	partitions = pickle.load(open("community_louvain_1750.pickle", "rb"))
 	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
 	with open("community0_1750.pickle", "wb") as handle:
 		pickle.dump(communities[0], handle, protocol = 2)
 	with open("community1_1750.pickle", "wb") as handle:
 		pickle.dump(communities[1], handle, protocol = 2)
 	with open("community2_1750.pickle", "wb") as handle:
 		pickle.dump(communities[2], handle, protocol = 2)

 	save_data_on_community(communities, 0, liberals, conservatives)
  	save_data_on_community(communities, 1, liberals, conservatives)
 	save_data_on_community(communities, 2, liberals, conservatives)

 	# for comm in communities:
 	# 	members = communities[comm]
 	# 	num_liberals = 0
 	# 	num_conservatives = 0
 	# 	for member in members:
 	# 		if member in liberals:
 	# 			num_liberals += 1
 	# 		if member in conservatives:
 	# 			num_conservatives += 1
 	# 	print (comm, num_liberals, num_conservatives)

def save_data_on_community(communities, comm, liberals, conservatives):
	members = {}
	for member in communities[comm]:
		if member in liberals:
			members[member] = "liberal"
		elif member in conservatives:
			members[member] = "conservative"
		else:
			members[member] = "not seeded"
	filename = "community" + str(comm) + "_withlabels_1750.pickle"
	with open(filename, "wb") as handle:
		pickle.dump(members, handle, protocol = 2)

def between_community_connections(Graph):
 	# partitions = pickle.load(open("community_louvain_1750.pickle", "rb"))
 	# mod = community.modularity(partitions, Graph)
 	# print mod
 	# communities = {}
 	# for part in partitions:
 	# 	if partitions[part] in communities:
 	# 		communities[partitions[part]].append(part)
 	# 	else:
 	# 		communities[partitions[part]] = []
 	# 		communities[partitions[part]].append(part)
 	# first_community = communities[0]
 	# second_community = communities[1]
 	community_0_connections = set()
 	community_1_connections = set()
 	first_community, second_community = get_first_two_communities()
 	for node in first_community:
 		for nd in second_community:
 			if Graph.has_edge(node, nd):
 				if Graph[node][nd]['weight'] >= 2:
 					community_0_connections.add(node)
 					community_1_connections.add(nd)
 	with open("community_0_connections_1750.pickle", "wb") as handle:
 		pickle.dump(community_0_connections, handle, protocol = 2)
 	with open("community_1_connections_1750.pickle", "wb") as handle:
 		pickle.dump(community_1_connections, handle, protocol = 2)
 	new_Graph = copy.deepcopy(Graph)
	for node in Graph.nodes():
		if (node in community_1_connections) and (node in community_0_connections):
			new_Graph.remove_node(node)
	partitions = community.best_partition(Graph)
	mod = community.modularity(partitions, Graph)
 	print mod
	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
 	with open("bridge_nodes_deleted_1750.pickle", "wb") as handle:
		pickle.dump(communities, handle, protocol = 2)
 	for comm in communities:
 		members = communities[comm]
 		num_liberals = 0
 		num_conservatives = 0
 		for member in members:
 			if member in liberals:
 				num_liberals += 1
 			if member in conservatives:
 				num_conservatives += 1
 		print (comm, num_liberals, num_conservatives)




def delete_disconnected_nodes(Graph, liberals, conservatives):
	first_community, second_community = get_first_two_communities()
	new_Graph = copy.deepcopy(Graph)
	for node in Graph.nodes():
		if (node not in first_community) and (node not in second_community):
			new_Graph.remove_node(node)
	# partitions = community.best_partition(Graph)
	# with open("community_louvain_1750_deleted_nodes.pickle", 'wb') as handle:
 # 		pickle.dump(partitions, handle, protocol = 2)
 	partitions = pickle.load(open("community_louvain_1750_deleted_nodes.pickle", 'rb'))
 	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
 	save_data_on_community(communities, 0, liberals, conservatives)
  	save_data_on_community(communities, 1, liberals, conservatives)
 	save_data_on_community(communities, 2, liberals, conservatives)
	mod = community.modularity(partitions, Graph)
 	print mod
	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
 	for comm in communities:
 		members = communities[comm]
 		num_liberals = 0
 		num_conservatives = 0
 		for member in members:
 			if member in liberals:
 				num_liberals += 1
 			if member in conservatives:
 				num_conservatives += 1
 		print (comm, num_liberals, num_conservatives)


def get_first_two_communities():
	partitions = pickle.load(open("community_louvain_1750.pickle", "rb"))
	# mod = community.modularity(partitions, Graph)
 # 	print mod
 	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
 	first_community = communities[0]
 	second_community = communities[1]
 	return first_community, second_community


def swing_senators(Graph):
 	senators = ["@realdonaldtrump", "@jeffflake", "@senatorcollins", "@senbobcorker", "@sen_joemanchin"]
 	for sen in senators:
 		sen = unicode(sen, "utf-8")
 		sen_graph = nx.DiGraph()
 		sen_graph.add_node(sen)
 		for pred in Graph.predecessors(sen):
 			sen_graph.add_edge(pred, sen)
 		for succ in Graph.successors(sen):
 			sen_graph.add_edge(sen, succ)
 		graph_name = sen + "graph"
 		nx.write_weighted_edgelist(sen_graph, graph_name)

if __name__ == "__main__":
	# G = nx.read_weighted_edgelist("directed_rt_graph_3M", create_using = nx.DiGraph())
	# Gundir = nx.read_weighted_edgelist("undirected_rt_graph_3M")

	# G = nx.read_weighted_edgelist("directed_rt_graph_1000", create_using = nx.DiGraph())
	# Gundir = nx.read_weighted_edgelist("undirected_rt_graph_1000")

	# G = nx.read_weighted_edgelist("directed_rt_graph_1750", create_using = nx.DiGraph())
	# Gundir = nx.read_weighted_edgelist("directed_rt_graph_1750")

	# G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_3M", create_using = nx.DiGraph())
	# G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_1000", create_using = nx.DiGraph())
	# G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_1000")
	G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_1750")
	# G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_1750", create_using = nx.DiGraph())

	# print nx.number_of_nodes(G_scc)
	liberals = pickle.load(open("liberals.pickle", "rb"))
	conservatives = pickle.load(open("conservatives.pickle", "rb"))

	# find_other_ideologues(G, liberals, conservatives)
	# find_other_ideologues(Gundir, liberals, conservatives)

	# sorted_by_degree = sorted(G.degree, key = lambda x: x[1], reverse = True)
	# for node, degree in sorted_by_degree[:30]:
	# 	print("Node: ", node)
	# 	print("Degree: ", degree)

	# degree_dist(G, liberals, conservatives)

	# hub, auth = nx.hits(G_scc)
	# hubs_sorted = sorted(hub.items(), key = lambda x: x[1], reverse = True)
	# auths_sorted = sorted(auth.items(), key = lambda x: x[1], reverse = True)
	# print "The top 3 authorities in the network by HITS scores are: "
	# for item in auths_sorted[:5]:
	# 	print("Authority ID: ", item[0])
	# 	print("HITS score: ", item[1])
	# print "\nThe top 3 hubs in the network by HITS scores are: "
	# for item in hubs_sorted[:5]:
	# 	print("Hub ID: ", item[0])
	# 	print("HITS score: ", item[1])

	# edge_contraction(G, liberals, conservatives)
	# edge_contraction(Gundir, liberals, conservatives)
	# edge_contraction(G_scc, liberals, conservatives)
	
	# clique_analysis(Gundir)

	# community_detection(G_scc, liberals, conservatives)
	between_community_connections(G_scc) #use undirected SCC
	# delete_disconnected_nodes(G_scc, liberals, conservatives)

	# S_liberal_users, S_conservative_users, S_hat_liberal_users, S_hat_conservative_users = normalized_cut_minimization(G_scc, liberals, conservatives)

	# graphic(G_scc, liberals, conservatives)
	
	# analyze_clustering(G, liberals, conservatives, True)
	# analyze_clustering(Gundir, liberals, conservatives, False)

	# swing_senators(G)
