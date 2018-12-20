import ndjson
import jsonlines
import pandas as pd
import pickle
import networkx as nx
import re
import csv
import matplotlib.pyplot as plt

retweet_user_regex = r'RT (@[A-Za-z0-9_]+)'


def create_rt_network():
	liberals = set()

	with open('liberal.csv') as f:
		lines = f.readlines()
	for line in lines:
		line = line[:-2].lower()
		liberals.add(line)

	with open('Democrat Pol Figures.csv') as f:
		lines = f.readlines()
	for line in lines:
		line = line[:-2].lower()
		liberals.add(line)

	conservatives = set()

	with open('conservative.csv') as f:
		lines = f.readlines()
	for line in lines:
		line = line[:-2].lower()
		conservatives.add(line)

	with open('Republican Pol Figures.csv') as f:
		lines = f.readlines()
	for line in lines:
		line = line[:-2].lower()
		conservatives.add(line)

	print("num liberal:", len(liberals))
	print("num conservative:", len(conservatives))

	with(open("liberals.pickle", "wb")) as handle:
		pickle.dump(liberals, handle, protocol = 2)

	with(open("conservatives.pickle", "wb")) as handle:
		pickle.dump(conservatives, handle, protocol = 2)


	G = nx.DiGraph()
	# Gundir = nx.Graph()

	# G = nx.read_weighted_edgelist("directed_rt_graph_1000", create_using = nx.DiGraph())
	Gundir = None
	# Gundir = nx.read_weighted_edgelist("undirected_rt_graph_1000")
	# Retweet data dictionary contains who a particular user retweets and how many times. The key is the user that is doing the retweeting
	retweeter_data = {}
	retweeted_data = {}
	retweets_not_caught = []
	users = set()
	user_dict = {}
	for i in range(392,775):
		print i
		filename = "oct6_data_subset_" + str(i) + ".pickle"
		user_dict_i = pickle.load(open(filename, "rb"))
		G, Gundir, users, retweets_not_caught = build_rt_network(G, Gundir, user_dict_i, retweeted_data, retweeter_data, users, retweets_not_caught, liberals, conservatives)
		#user_dict.update(user_dict_i)

	"""user_dict = pickle.load(open("kavanaugh_data_subset_5.pickle", "rb"))
	user_dict2 = pickle.load(open("kavanaugh_data_subset_10.pickle", "rb"))
	#user_dict = merge_dicts(user_dict1, user_dict2)
	user_dict.update(user_dict2)
	user_dict3 = pickle.load(open("kavanaugh_data_subset_80.pickle", "rb"))
	#user_dict = merge_dicts(user_dict, user_dict3)
	user_dict.update(user_dict3)"""


	print nx.number_of_nodes(G)
	print nx.number_of_edges(G)
	nx.write_weighted_edgelist(G, "directed_rt_graph_oct6")

	# print nx.number_of_nodes(Gundir)
	# print nx.number_of_edges(Gundir)
	# nx.write_weighted_edgelist(Gundir, "undirected_rt_graph_1750")

	txtfile = open("retweets_not_caught_oct6.txt", "w")
	for item in retweets_not_caught:
		txtfile.write(item.encode('ascii', 'ignore'))
	txtfile.close()


	#analyze_clustering(Gundir, liberals, conservatives, False)
	#analyze_clustering(G, liberals, conservatives, True)

	"""# Keep track of political leaning
	left = []
	right = []
	others = []

	for user in users:
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
	nx.draw_networkx_nodes(G, pos, nodelist=others, node_color='k', node_size=10, alpha=0.1)
	print("drew others")
	nx.draw_networkx_edges(G, pos, edge_color='g', width=0.1, alpha=0.1)

	print("should be displaying")

	plt.show()"""
def build_rt_network(G, Gundir, user_dict, retweeted_data, retweeter_data, users, retweets_not_caught, liberals, conservatives):
	for k, v in user_dict.items():
		username = str(k).lower()
		if v:
			for i in range(len(v)):
				tweet_text = v[i][0]
				if tweet_text[0:2] == "RT":
					users.add(username)
					if re.findall(retweet_user_regex, tweet_text):
						retweeted_user = str(re.findall(retweet_user_regex, tweet_text)[0]).lower()
						users.add(retweeted_user)
					else:
						retweets_not_caught.append(tweet_text + "\n")

					#username = str(username)

					# DIRECTED GRAPH
					# Add edge weight for this retweet
					if username not in G:
						G.add_node(username)
					if retweeted_user not in G:
						G.add_node(retweeted_user)
					if G.has_edge(username, retweeted_user):
						G[username][retweeted_user]['weight'] += 1
					else:
						G.add_edge(username, retweeted_user, weight = 1)

					# # UNDIRECTED GRAPH
					# # Add edge weight for this retweet
					# if username not in Gundir:
					# 	Gundir.add_node(username)
					# if retweeted_user not in Gundir:
					# 	Gundir.add_node(retweeted_user)
					# if Gundir.has_edge(username, retweeted_user):
					# 	Gundir[username][retweeted_user]['weight'] += 1
					# else:
					# 	Gundir.add_edge(username, retweeted_user, weight = 1)

					"""# Keep track of who is being retweeted by a given user
					if username in retweeter_data:
						retweeter_info = retweeter_data[username]
						if retweeted_user in retweeter_info:
							retweeter_info[retweeted_user] += 1
						else:
							retweeter_info[retweeted_user] = 1
					else:
						retweeter_data[username] = {}
						retweeter_data[username][retweeted_user] = 1

					# Keep track of who is retweeting a given user
					if retweeted_user in retweeted_data:
						retweeted_info = retweeted_data[retweeted_user]
						if username in retweeted_info:
							retweeted_info[username] += 1
						else:
							retweeted_info[username] = 1
					else:
						retweeted_data[retweeted_user] = {}
						retweeted_data[retweeted_user][username] = 1"""

	return G, Gundir, users, retweets_not_caught

# def analyze_clustering(G, liberals, conservatives, dir):
# 	if not dir:
# 		cc = nx.connected_components(G)
# 		subgraphs = list(nx.connected_component_subgraphs(G))
# 		print("Average Clustering Coefficient Undirected: ", nx.average_clustering(max(subgraphs, key=len)))
# 	else:
# 		cc = nx.strongly_connected_components(G)
# 		subgraphs = list(nx.strongly_connected_component_subgraphs(G))
# 		print("Average Clustering Coefficient Directed: ", nx.average_clustering(max(subgraphs, key=len)))
# 	largest_component = sorted(cc, key = len, reverse = True)[0]
# 	liberal_users = set()
# 	conservative_users = set()
# 	for user in largest_component:
# 		if user in liberals:
# 			liberal_users.add(user)
# 		if user in conservatives:
# 			conservative_users.add(user)
# 	print("Size of largest connected component: ", len(largest_component))
# 	print("Num of liberals: ", len(liberal_users))
# 	print("Num of conservatives: ", len(conservative_users))
# 	#sorted_cc_lengths = [len(c) for c in sorted(nx.connected_components(G), key = len, reverse = True)]
# 	#print sorted_cc_lengths
# 	#print "here"

# def merge_dicts(dict1, dict2):
# 	new_dict = {}
# 	for k in dict1:
# 		if (k in dict2) and (dict1[k]):
# 			new_dict[k] = dict1[k].append(dict2[k])
# 		else:
# 			new_dict[k] = dict1[k]
# 	for k in dict2:
# 		if k not in new_dict:
# 			new_dict[k] = dict2[k]
# 	return new_dict


if __name__ == "__main__":
	#user_dict = pickle.load(open("kavanaugh_data_subset_5.pickle", "rb"))
	#print user_dict
	#for k, v in user_dict.items():
	#	print k
	#	print v[0][0]
	#	print "\n"
	create_rt_network()
