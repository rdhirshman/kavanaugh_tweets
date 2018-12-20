import ndjson
import jsonlines
import json_lines
import json
import pandas as pd
import pickle

def parseData():
	# dataframe = pd.DataFrame()

	# with jsonlines.open('Brett_Kavanaugh_Nomination_Tweets.ndjson') as reader:
	# 	i = 0
	# 	j = 1500
	# 	user_dict = {}
	# 	for obj in reader:
	# 		if i > 15000000:
	# 			d = obj
	# 			tweet_text = d['full_text']
	# 			user_handle = "@" + d['user']['screen_name']
	# 			tweet_date = d["created_at"]
	# 			# Each user associated with the text of the tweet, date and time of tweet, attrs of tweet and attrs of user
	# 			user_attrs = [tweet_text, tweet_date, d['entities'], d['user']]
	# 			if user_handle in user_dict:
	# 				user_dict[user_handle].append(user_attrs)
	# 			else:
	# 				user_dict[user_handle] = []
	# 				user_dict[user_handle].append(user_attrs)
	# 			if (i % 10000) == 0:
	# 				print j
	# 				filename = "kavanaugh_data_subset_" + str(j) + ".pickle"
	# 				with open(filename, "wb") as handle:
	# 					pickle.dump(user_dict, handle, protocol = 2)
	# 				user_dict = {}
	# 				j += 1
	# 		i += 1

	with jsonlines.open('Brett_Kavanaugh_Nomination_Tweets.ndjson') as reader:
		i = 0
		j = 0
		user_dict = {}
		sept27_dict = {}
		sept28_dict = {}
		oct4_dict = {}
		oct6_dict = {}

		# september 27, september 28, october 4, october 6
		for obj in reader:
			atsept27 = False
			atsept28 = False
			atoct4 = False
			atoct6 = False
			d = obj
			tweet_text = d['full_text']
			user_handle = "@" + d['user']['screen_name']
			tweet_date = d["created_at"]
			date = tweet_date[4:10]

			# Each user associated with the text of the tweet, date and time of tweet, attrs of tweet and attrs of user
			user_attrs = [tweet_text, tweet_date, d['entities'], d['user']]

			# if date == "Sep 27":
			# 	i += 1
			# 	atsept27 = True
			# 	sept27_dict = update_dict(sept27_dict, user_handle, user_attrs)
			# elif date == "Sep 28":
			# 	i += 1
			# 	sept27_dict = None
			# 	atsept28 = True
			# 	sept28_dict = update_dict(sept28_dict, user_handle, user_attrs)
			if date == "Oct 04":
				i += 1
				# sept28_dict = None
				atoct4 = True
				oct4_dict = update_dict(oct4_dict, user_handle, user_attrs)
			elif date == "Oct 06":
				i += 1
				oct4_dict = None
				atoct6 = True
				oct6_dict = update_dict(oct6_dict, user_handle, user_attrs)


			# if atsept27 and ((i % 10000) == 0):
			# 	filename = "sept27_data_subset_" + str(j) + ".pickle"
			# 	with open(filename, "wb") as handle:
			# 		pickle.dump(sept27_dict, handle, protocol = 2)
			# 	sept27_dict = {}
			# 	j += 1
			# if atsept28 and ((i % 10000) == 0):
			# 	filename = "sept28_data_subset_" + str(j) + ".pickle"
			# 	with open(filename, "wb") as handle:
			# 		pickle.dump(sept28_dict, handle, protocol = 2)
			# 	sept28_dict = {}
			# 	j += 1
			if atoct4 and ((i % 10000) == 0):
				filename = "oct4_data_subset_" + str(j) + ".pickle"
				with open(filename, "wb") as handle:
					pickle.dump(oct4_dict, handle, protocol = 2)
				oct4_dict = {}
				j += 1
			if atoct6 and ((i % 10000) == 0):
				filename = "oct6_data_subset_" + str(j) + ".pickle"
				with open(filename, "wb") as handle:
					pickle.dump(oct6_dict, handle, protocol = 2)
				oct6_dict = {}
				j += 1


		# filename = "sept27_dict.pickle"
		# with open(filename, "wb") as handle:
		# 	pickle.dump(sept27_dict, handle, protocol = 2)
		# filename = "sept28_dict.pickle"
		# with open(filename, "wb") as handle:
		# 	pickle.dump(sept28_dict, handle, protocol = 2)
		# filename = "oct4_dict.pickle"
		# with open(filename, "wb") as handle:
		# 	pickle.dump(oct4_dict, handle, protocol = 2)
		# filename = "oct6_dict.pickle"
		# with open(filename, "wb") as handle:
		# 	pickle.dump(oct6_dict, handle, protocol = 2)

def update_dict(dictionary, user_handle, user_attrs):
	if user_handle in dictionary:
		dictionary[user_handle].append(user_attrs)
	else:
		dictionary[user_handle] = []
		dictionary[user_handle].append(user_attrs)
	return dictionary


if __name__ == "__main__":
	parseData()