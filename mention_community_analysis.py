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

# Mention Network community analysis

def analyze_clustering(G, liberals, conservatives, dir):
	if not dir:
		# cc = nx.connected_components(G)
		subgraphs = list(nx.connected_component_subgraphs(G))
		#print("Average Clustering Coefficient Undirected Full Graph: ", nx.average_clustering(G))
		# print("Average Clustering Coefficient Undirected Max Subgraph: ", nx.average_clustering(max(subgraphs, key=len)))
	else:
		# cc = nx.strongly_connected_components(G)
		subgraphs = list(nx.strongly_connected_component_subgraphs(G))
		with open("mention_subgraphs_sept28.pickle", 'wb') as handle:
			pickle.dump(subgraphs, handle, protocol = 2)
		G = None
		#print("Average Clustering Coefficient Directed Full Graph: ", nx.average_clustering(G))
	print [len(c) for c in sorted(subgraphs, key = len, reverse = True)][:10]
	largest_component = max(subgraphs, key = len)
	subgraphs = None
	# subgraphs.sort(key = len, reverse = True)
	# second_largest_component = subgraphs[1]
	# print(len(second_largest_component))
	nx.write_weighted_edgelist(largest_component, "mention_directed_mx_subgraph_sept28")
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

def community_detection(Graph, liberals, conservatives):
 	partitions = community.best_partition(Graph)
 	# mod = community.modularity(partitions, Graph)
 	with open("mention_community_louvain_sept28.pickle", 'wb') as handle:
 		pickle.dump(partitions, handle, protocol = 2)
 	# partitions = pickle.load(open("mention_community_louvain_sept27.pickle", "rb"))
  	mod = community.modularity(partitions, Graph)
 	print mod
 	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
 	with open("mention_community0_sept28.pickle", "wb") as handle:
 		pickle.dump(communities[0], handle, protocol = 2)
 	with open("mention_community1_sept28.pickle", "wb") as handle:
 		pickle.dump(communities[1], handle, protocol = 2)
 	with open("mention_community2_sept28.pickle", "wb") as handle:
 		pickle.dump(communities[2], handle, protocol = 2)

 	save_data_on_community(communities, 0, liberals, conservatives)
  	save_data_on_community(communities, 1, liberals, conservatives)
 	save_data_on_community(communities, 2, liberals, conservatives)

 	for comm in communities:
 		print len(communities[comm])
 		members = communities[comm]
 		num_liberals = 0
 		num_conservatives = 0
 		for member in members:
 			if member in liberals:
 				num_liberals += 1
 			if member in conservatives:
 				num_conservatives += 1
 		print (comm, num_liberals, num_conservatives)

def save_data_on_community(communities, comm, liberals, conservatives):
	members = {}
	for member in communities[comm]:
		if member in liberals:
			members[member] = "liberal"
		elif member in conservatives:
			members[member] = "conservative"
		else:
			members[member] = "not seeded"
	filename = "mention_community" + str(comm) + "_withlabels_sept28.pickle"
	with open(filename, "wb") as handle:
		pickle.dump(members, handle, protocol = 2)


def get_liberal_and_cons_communities():
	partitions = pickle.load(open("mention_community_louvain_oct6.pickle", "rb"))
	# mod = community.modularity(partitions, Graph)
 # 	print mod
 	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
 	liberal_comm = communities[0] + communities[1]
 	cons_comm = communities[2] + communities[4]

 	with open("mention_liberal_communities_oct6.pickle", "wb") as handle:
 		pickle.dump(liberal_comm, handle, protocol = 2)
 	with open("mention_conservative_communities_oct6.pickle", "wb") as handle:
 		pickle.dump(cons_comm, handle, protocol = 2)


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
	partitions = pickle.load(open("mention_community_louvain_sept28.pickle", "rb"))
	# mod = community.modularity(partitions, Graph)
 # 	print mod
 	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)

	community0 = pickle.load(open("mention_community0_sept28.pickle", 'rb'))
	community3 = communities[3]
	community4 = communities[4]

	graphic(G, liberals, conservatives, community0, community3, community4)

	# analyze_clustering(Gundir, liberals, conservatives, False)
	# analyze_clustering(G, liberals, conservatives, True)

def graphic(G, liberals, conservatives, community0, community3, community4):
	# Keep track of political leaning
	left = set()
	right = set()
	others = set()

	for user in G.nodes():
		if user in liberals:
			left.add(user)
		elif user in conservatives:
			right.add(user)
		elif user in community0:
			left.add(user)
		elif (user in community3) or (user in community4):
			right.add(user)
		else:
			others.add(user)


	pos = nx.spring_layout(G)
	print("post pos")

	nx.draw_networkx_nodes(G, pos, nodelist=right, node_color='r', node_size = 50)
	print("drew conservative")
	nx.draw_networkx_nodes(G, pos, nodelist=left, node_color='b', node_size = 50)
	print("drew liberal")
	nx.draw_networkx_nodes(G, pos, nodelist=others, node_color='k', node_size=2, alpha=0.1)
	print("drew others")
	nx.draw_networkx_edges(G, pos, edge_color='k', width=0.7, alpha=0.7)

	# nx.draw(G, nodelist=right, node_color='r', node_size = 50)
	# print("drew conservative")
	# nx.draw(G, nodelist=left, node_color='b', node_size = 50)
	# print("drew liberal")
	# nx.draw(G, nodelist=others, node_color='k', node_size=2, alpha=0.1)
	# print("drew others")
	# nx.draw(G, edge_color='g', width=0.1, alpha=0.1)

	print("should be displaying")

	plt.show()

def swing_senators(Graph):
 	senators = ["@realdonaldtrump", "@jeffflake", "@senatorcollins", "@senbobcorker", "@sen_joemanchin", "@lisamurkowski"]
 	for sen in senators:
 		sen = unicode(sen, "utf-8")
 		sen_graph = nx.DiGraph()
 		if Graph.has_node(sen):
	 		sen_graph.add_node(sen)
	 		for pred in Graph.predecessors(sen):
	 			sen_graph.add_edge(pred, sen)
	 		for succ in Graph.successors(sen):
	 			sen_graph.add_edge(sen, succ)
	 		graph_name = sen + "_oct4_graph"
	 		nx.write_weighted_edgelist(sen_graph, graph_name)


if __name__ == "__main__":
	liberals = pickle.load(open("liberals.pickle", "rb"))
	conservatives = pickle.load(open("conservatives.pickle", "rb"))
	G = nx.read_weighted_edgelist("mention_edges_oct4", create_using = nx.DiGraph())
	# G = nx.read_weighted_edgelist("mention_edges_sept27", create_using = nx.DiGraph())
	# G = nx.read_weighted_edgelist("mention_edges_sept28", create_using = nx.DiGraph())
	# G = nx.read_weighted_edgelist("mention_edges_oct6", create_using = nx.DiGraph())
 # 	print G.number_of_nodes()
 # 	print G.number_of_edges()
	# G_scc = nx.read_weighted_edgelist("mention_directed_mx_subgraph_oct4")
	# G_scc = nx.read_weighted_edgelist("mention_directed_mx_subgraph_oct6")
	# G_scc = nx.read_weighted_edgelist("mention_directed_mx_subgraph_sept27")
	# G_scc = nx.read_weighted_edgelist("mention_directed_mx_subgraph_sept28")
	# G_scc = nx.read_weighted_edgelist("max_scc_mention_edges_sept28")
 	# print G_scc.number_of_nodes()
 	# print G_scc.number_of_edges()
	# for nodes in G_scc.nodes():
	# 	if nodes in liberals:
	# 		print nodes
	# 	elif nodes in conservatives:
	# 		print nodes
	# G = nx.read_weighted_edgelist("mention_edges_oct6", create_using = nx.DiGraph())
	# analyze_clustering(G, liberals, conservatives, True)
	# community_detection(G_scc, liberals, conservatives)
	# get_liberal_and_cons_communities()
	swing_senators(G)
	# edge_contraction(G_scc, liberals, conservatives)


	# liberal_comm = pickle.load(open("mention_liberal_communities_oct6.pickle"))
	# cons_comm = pickle.load(open("mention_conservative_communities_oct6.pickle"))
	# liberal_bridges = set()
	# cons_bridges = set()

	# for node in liberal_comm:
 # 		for nd in cons_comm:
 # 			if G_scc.has_edge(node, nd):
 # 				if G_scc[node][nd]['weight'] >= 2:
 # 					liberal_bridges.add(node)
 # 					cons_bridges.add(nd)
 # 	liberalcount = 0
 # 	conscount = 0
 # 	print "Liberal"
 # 	for nd in liberal_bridges:
 # 		if nd in liberals:
 # 			liberalcount += 1
 # 			print nd
 # 	print liberalcount
 # 	print "Conservatives"
 # 	for nd in cons_bridges:
 # 		if nd in conservatives:
 # 			conscount += 1
 # 			print nd
 # 	print conscount




