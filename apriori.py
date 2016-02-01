#-*- coding:utf-8 -*-

import json
import codecs
import sys
import itertools

if __name__ == "__main__":
	
	print("start apriori mining")
	
	N = None
	minsup = 0.87
	minconf = 0.6
	
	f = codecs.open('./traffic_data/trafic_data.json','r','utf-8')
	data = json.load(f)
	N = float(len(data))
	
	item_data = []
	
	print "loading file"
	for d in data:
		item_data.append( d[u"items"] )
	
	# item_data = [["b","c","d"],["a","b"],["a","d","e"],["b","c","d"],["b","d"]]
	# N = 5.
	
	print "make set file"
	set_data = set()
	for T in item_data:
		for item in T:
			set_data.add(item)
	
	set_data = sorted(set_data)
	
	print "N :",N,"set_num :",len(set_data),"minsup :",minsup,"minconf :",minconf
	print "make C_0"
	C_0 = {}
	for item in set_data:
		C_0[item] = 0
		
	for T in item_data:
		for one_set in set_data:
			if one_set in T:
				C_0[one_set] += 1
				
	# show pattern times
	# for one_set in set_data:
	# 	print one_set, C_0[one_set]
	
	F_k = []
	
	print "make F_0"
	F_0 = []
	for one_set in set_data:
		if(C_0[one_set]/N >= minsup):
			F_0.append([one_set])
	
	# print F_0
	
	F_k.append(F_0)
	
	for k in range( len(set_data) ):
		
		print "k :",k,
		
		C_kp1 = set()
		for i in range(len(F_k[k]))[:-1]:
			for j in range(len(F_k[k]))[i + 1:]:
				 c = []
				 c.extend(F_k[k][i])
				 c.extend(F_k[k][j])
				 c.sort()
				 C_kp1.add( tuple(set(c)) )
		# print "C_" + str(k+1), [_ for _ in C_kp1]
		
		F_kp1 = []
		for i, c in enumerate(C_kp1):
			
			log_c = "C_" + str(k+1) + " " + str(i) + "/" + str(len(C_kp1) - 1)
			sys.stdout.write("\r" + log_c)
			sys.stdout.flush()
			
			count = 0
			for T in item_data:
				true_count = 0
				for c_i in c:
					if(c_i in T):
						true_count += 1
				if(true_count == len(c) ):
					count += 1
			if(count/N >= minsup):
				F_kp1.append(list(c))
		print ""
		# print "F_" + str(k+1), F_kp1
		
		print "F_" + str(k+1),len(F_kp1)
		
		if( len(F_kp1) == 0):
			break
		else:
			F_k.append(F_kp1)
			
	print "frequent patterns"
	
	freq_dict = {}
	
	num = 0
	for F in F_k:
		for f in F:
			num += 1
			all_count = 0
			for T in item_data:
				t_count = 0
				for f_item in f:
					if(f_item in T):
						t_count += 1
				if(t_count == len(f)):
					all_count += 1
			
			# for f_item in f:
			# 	print f_item,
			# print " " + str(all_count)
			
			freq_dict.update({tuple(sorted(f)):all_count})
			
	print str(num),"patterns"
	
	# print freq_dict
	
	# confidense
	conf_dict = []
	
	for i, F in enumerate(F_k):
		#if(i + 1 == 2):
		#	for f in F:
		#		supX = float( freq_dict[tuple([f[0]])] )
		#		confXY = freq_dict[tuple(f)] / supX
		#		if(confXY >= minconf):
		#			conf_dict.append({"X":f[0], "Y":f[1], "support":supX, "confidense":confXY})
		#		
		#		supY = float( freq_dict[tuple([f[1]])] )
		#		confYX = freq_dict[tuple(f)] / supY
		#		if(confYX >= minconf):
		#			conf_dict.append({"X":f[0], "Y":f[1], "sup":supY, "conf":confYX})
		
		if(i + 1 >= 2):
			for f in F:
				k = i + 1
				for j in range(1, k):
					for X in list(itertools.combinations(f, j) ):
						Y = []
						for item_y in f:
							if(item_y not in X):
								Y.append(item_y)
						X = tuple( sorted(X) )
						Y = tuple( sorted(Y) )
						supX = float( freq_dict[X] )
						confXY = freq_dict[ tuple( sorted(f) ) ] / supX
						
						if(confXY >= minconf):
							conf_dict.append({"X":list(X), "Y":list(Y), "support":supX/N, "confidence":confXY})
		
	print str( len(conf_dict) ) + " rules"
	print "writing data"
	output_json = codecs.open("./traffic_data/trafic_data_rules.json", "w", "utf-8")
	json.dump(conf_dict, output_json, indent = 4, ensure_ascii = False)
	output_json.close()
	
	print "finish!!"