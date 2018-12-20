import pickle
import networkx as nx


def save_data_on_community(communities, comm, liberals, conservatives):
	members = {}
	for member in communities[comm]:
		if member in liberals:
			members[member] = "liberal"
		elif member in conservatives:
			members[member] = "conservative"
		else:
			members[member] = "not seeded"
	filename = "community" + str(comm) + "_withlabels_bridgenodesdeleted_1750.pickle"
	with open(filename, "wb") as handle:
		pickle.dump(members, handle, protocol = 2)

def edge_contraction(G, liberals, conservatives, community0, community1):

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

	graphic(G, liberals, conservatives, community0, community1)

	# analyze_clustering(Gundir, liberals, conservatives, False)
	# analyze_clustering(G, liberals, conservatives, True)

def graphic(G, liberals, conservatives, community0, community1):
	# Keep track of political leaning
	left = set()
	right = set()
	others = set()

	right = right.add(set(community0))
	left = left.add(set(community1))

	for user in G.nodes():
		if (user in liberals) and (user not in right):
			left.append(user)
		elif (user in conservatives) and (user not in left):
			right.append(user)
		else:
			if (user not in left) and (user not in right):
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

def bridge_nodes(G, liberal_comm, cons_comm, liberals, conservatives):
	bridge_node = set()
	for node in liberal_comm:
 		for nd in cons_comm:
 			if G.has_edge(node, nd):
 				if G[node][nd]['weight'] >= 2:
 					bridge_node.add(node)

 	print("Liberal bridge nodes:")
 	for node in bridge_node:
 		if node in liberals:
 			print node


 	print("conservative bridge nodes:")
 	for node in bridge_node:
 		if node in conservatives:
 			print node


if __name__ == "__main__":
	liberals = pickle.load(open("liberals.pickle", "rb"))
	conservatives = pickle.load(open("conservatives.pickle", "rb"))

	# Sept 27
	partitions = pickle.load(open("community_louvain_sept27.pickle", "rb"))
 	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
	G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_sept27")
	cons_comm = pickle.load(open("community0_sept27.pickle"))
	liberal_comm = pickle.load(open("community1_sept27.pickle")) + communities[2] + communities[3]
	print "Sept 27"
	bridge_nodes(G_scc, liberal_comm, cons_comm, liberals, conservatives)

	# Sept 28
	G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_sept28")
	cons_comm = pickle.load(open("community1_sept28.pickle"))
	liberal_comm = pickle.load(open("community0_sept28.pickle")) + pickle.load(open("community2_sept28.pickle"))
	print "Sept 28"
	bridge_nodes(G_scc, liberal_comm, cons_comm, liberals, conservatives)

	# Oct 4
	partitions = pickle.load(open("community_louvain_oct4.pickle", "rb"))
 	communities = {}
 	for part in partitions:
 		if partitions[part] in communities:
 			communities[partitions[part]].append(part)
 		else:
 			communities[partitions[part]] = []
 			communities[partitions[part]].append(part)
 	cons_comm = communities[2] + communities[3]
 	liberal_comm = communities[0] + communities[1]
 	G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_oct4")
 	print "Oct 4"
 	bridge_nodes(G_scc, liberal_comm, cons_comm, liberals, conservatives)

	# Oct 6
	G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_oct6")
	cons_comm = pickle.load(open("community1_oct6.pickle"))
	liberal_comm = pickle.load(open("community2_oct6.pickle"))
	print "Oct 6"
	bridge_nodes(G_scc, liberal_comm, cons_comm, liberals, conservatives)




	# community0 = pickle.load(open("community0_1750.pickle"))
	# community1 = pickle.load(open("community1_1750.pickle"))
	# community2 = pickle.load(open("community2_1750.pickle"))

	# community0_withlabels = pickle.load(open("community0_withlabels_oct6.pickle"))
	# community1_withlabels = pickle.load(open("community1_withlabels_oct6.pickle"))
	# community2_withlabels = pickle.load(open("community2_withlabels_oct6.pickle"))
	# for username in community0_withlabels:
	# 	if community0_withlabels[username] == "conservative":
	# 		print username

	# G_scc = nx.read_weighted_edgelist("directed_mx_subgraph_1750")

	# edge_contraction(G_scc, liberals, conservatives, community0_1750, community1_1750)

	# liberals = pickle.load(open("liberals.pickle", "rb"))
	# conservatives = pickle.load(open("conservatives.pickle", "rb"))
	# community0_bridge_nodes = pickle.load(open("community_0_connections_1750.pickle"))
	# community1_bridge_nodes = pickle.load(open("community_1_connections_1750.pickle"))

	# for node in community1_bridge_nodes:
	# 	if node in liberals:
	# 		print node
	# print community0_bridge_nodes

	# communities = pickle.load(open("bridge_nodes_deleted_1750.pickle"))
	# Graph = nx.read_weighted_edgelist("directed_mx_subgraph_1750")

	# save_data_on_community(communities, 0, liberals, conservatives)
 #  	save_data_on_community(communities, 1, liberals, conservatives)
 # 	save_data_on_community(communities, 2, liberals, conservatives)

	# first_community = communities[0]
	# second_community = communities[1]
	# third_community = communities[2]

	# community_0_to_1_connections = set()
 # 	community_1_to_0_connections = set()

 # 	for node in first_community:
 # 		for nd in second_community:
 # 			if Graph.has_edge(node, nd):
 # 				if Graph[node][nd]['weight'] >= 2:
 # 					community_0_to_1_connections.add(node)
 # 					community_1_to_0_connections.add(nd)
 # 	with open("community_0_to_1_connections_1750.pickle", "wb") as handle:
 # 		pickle.dump(community_0_to_1_connections, handle, protocol = 2)
 # 	with open("community_1_to_0_connections_1750.pickle", "wb") as handle:
 # 		pickle.dump(community_1_to_0_connections, handle, protocol = 2)

 # 	for node in community_0_to_1_connections:
	# 	if node in conservatives:
	# 		print node

 	# community_1_to_2_connections = set()
 	# community_2_to_1_connections = set()

 	# for node in second_community:
 	# 	for nd in third_community:
 	# 		if Graph.has_edge(node, nd):
 	# 			if Graph[node][nd]['weight'] >= 2:
 	# 				community_1_to_2_connections.add(node)
 	# 				community_1_connections.add(nd)
 	# with open("community_1_to_2_connections_1750.pickle", "wb") as handle:
 	# 	pickle.dump(community_1_to_2_connections, handle, protocol = 2)
 	# with open("community_2_to_1_connections_1750.pickle", "wb") as handle:
 	# 	pickle.dump(community_2_to_1_connections, handle, protocol = 2)

 	# community_0_to_2_connections = set()
 	# community_2_to_0_connections = set()

  # 	for node in first_community:
 	# 	for nd in third_community:
 	# 		if Graph.has_edge(node, nd):
 	# 			if Graph[node][nd]['weight'] >= 2:
 	# 				community_0_to_2_connections.add(node)
 	# 				community_2_to_0_connections.add(nd)
 	# with open("community_0_to_2_connections_1750.pickle", "wb") as handle:
 	# 	pickle.dump(community_0_to_2_connections, handle, protocol = 2)
 	# with open("community_2_to_0_connections_1750.pickle", "wb") as handle:
 	# 	pickle.dump(community_2_to_0_connections, handle, protocol = 2)



