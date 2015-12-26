#-*- coding:utf-8 -*-

import json
import codecs
import sys

if __name__ == "__main__":
	
	print("start apriori mining")
	
	N = None
	minsup = 0.5
	
	f = codecs.open('./traffic_data/trafic_data.json','r','utf-8')
	data = json.load(f)
	N = float(len(data))
	
	item_data = []
	
	print "loading file"
	for d in data:
		item_data.append( d[u"items"] )
	
	# item_data = [["b","c","d"],["a","b"],["a","d","e"],["b","c","d"],["b","d"]]
	
	print "make set file"
	set_data = set()
	for T in item_data:
		for item in T:
			set_data.add(item)
	
	set_data = sorted(set_data)
	
	print "N :",N,"set_num :",len(set_data),"minsup :",minsup
	C_0 = {}
	for item in set_data:
		C_0[item] = 0
	
	print "count up items"
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
			
			log_c = "C_" + str(k+1) + " " + str(i) + "/" + str(len(C_kp1))
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
	num = 0
	for F in F_k:
		for f in F:
			num += 1
			for f_item in f:
				print f_item,
			print ""
	print str(num),"patterns"		