#-*- coding:utf-8 -*-

import sys
import itertools

def apriori(item_data, minsup=0.0, minconf=0.0, liftcut=False):	
	print("start apriori mining")
	
	N = float(len(item_data))

	print "make set file"
	set_data = set()
	for T in item_data:
		for item in T:
			set_data.add(item)
	
	set_data = sorted(set_data)
	
	'''
	import time
	for s in set_data:
		print s
		time.sleep(0.1)
	exit()
	'''
	
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
			
		if(len(C_kp1) == 0):
			print "C_" + str(k+1) + " " + "0/0"
		else:
			print ""
		
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
	print str( len(rule_dict) ) + " rules"
	print "apriori finish!!"
	return rule_dict