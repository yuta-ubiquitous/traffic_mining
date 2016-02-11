#-*- coding:utf-8 -*-

import sys
import itertools

def apriori(item_data, minsup=0.0, minconf=0.0, liftcut=False, frequent_pattern=False, log=True):	
	
	if log: print("start apriori mining")
	
	N = float(len(item_data))
	
	if log: print "N :",N,"minsup :",minsup,"minconf :",minconf
	if log: print "make C_0"
	
	C_0 = set()
	for T in item_data:
		for item in T:
			C_0.add(item)
	
	C_0 = sorted(C_0)
				
	# show pattern times
	# for one_set in set_data:
	# 	print one_set, C_0[one_set]
	
	F_k = []
	
	if log: print "make F_0"
	F_0 = []
	
	item_counter0 = {}
	for item in C_0:
		item_counter0[item] = 0.0
	
	for T in item_data:
		for item in T:
			item_counter0[item] += 1.0
	
	for item in C_0:
		if(item_counter0[item]/N >= minsup):
			F_0.append( [item] )

	F_k.append(F_0)
	
	for k in range(len(C_0)):
		C_kp1 = set()
		
		set_items = set()
		for f in F_k[k]:
			for item in f:
				set_items.add(item)
		
		for X_kp1 in list(itertools.combinations(set_items, k + 2 ) ):
			isAllClear = True
			for X_k in list(itertools.combinations(X_kp1, k + 1 ) ):
				F_tuple = tuple( sorted( tuple(F) for F in F_k[k] ) )
				
				if( tuple( sorted(X_k) ) in F_tuple):
					pass
				else:
					isAllClear = False
					break
			if( isAllClear ):
				C_kp1.add( tuple( sorted(X_kp1) ) )
		
		'''
		for i in range(len(F_k[k]))[:-1]:
			for j in range(len(F_k[k]))[i + 1:]:
				 c = []
				 c.extend(F_k[k][i])
				 c.extend(F_k[k][j])
				 c.sort()
				 C_kp1.add( tuple(set(c)) )
		'''
		# print "C_" + str(k+1), [_ for _ in C_kp1]
		
		F_kp1 = []
		
		for i, c in enumerate(C_kp1):
			
			if log:
				log_c = "C_" + str(k+1) + " " + str(i+1) + "/" + str(len(C_kp1))
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
		
		if log:	
			if(len(C_kp1) == 0):
				print "C_" + str(k+1) + " " + "0/0"
			else:
				print ""
		
		if log: print "F_" + str(k+1),len(F_kp1)
		
		if( len(F_kp1) == 0):
			break
		else:
			F_k.append(F_kp1)
			
	if log: print "frequent patterns"
	
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
			
	if log: print str(num),"patterns"
	
	if frequent_pattern:
		result_freq = []
		for pattern,num in freq_dict.items():
			json_data = {}
			json_data["pattern"] = pattern
			json_data["support"] = num/N
			result_freq.append(json_data)
		return result_freq
	
	# confidense
	rule_dict = []
	
	for i, F in enumerate(F_k):
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
						
						# debug - duplicate 
						isDuplicate = False
						for rule in rule_dict:
							if(tuple(sorted(rule["X"])) == X and tuple(sorted(rule["Y"])) == Y):
								isDuplicate = True
								break
						if(isDuplicate):
							continue
						
						supX = float( freq_dict[X] ) / N
						supY = float( freq_dict[Y] ) / N
						supXY = float( freq_dict[ tuple( sorted(f) ) ] ) / N
						confXY = supXY / supX
						liftXY = confXY / supY
						
						if(liftcut):
							if(liftXY <= 1.0):
								continue
						if(confXY >= minconf):
							rule_dict.append({"X":list(X), "Y":list(Y), "support":supXY, "confidence":confXY, "lift":liftXY})
							
	if log: print str( len(rule_dict) ) + " rules"
	if log: print "apriori finish!!"
	return rule_dict