#-*- coding:utf-8 -*-

if __name__ == "__main__":
	
	print("start apriori mining")
	
	test_data = [["b","c","d"],["a","b"],["a","d","e"],["b","c","d"],["b","d"]]
	
	test_set = set()
	for T in test_data:
		for item in T:
			test_set.add(item)
	print test_set
	
	test_set = sorted(test_set)
	
	# not nessesary
	print test_set
	Oms = []
	for T in test_data:
		t = [one_set in T for one_set in test_set]
		Oms.append(t)
		print t
	print ""
	
	N = 5.
	minsup = 0.4
	
	C_0 = {}
	for item in test_set:
		C_0[item] = 0
	
	for T in test_data:
		for one_set in test_set:
			if one_set in T:
				C_0[one_set] += 1
	print C_0
	
	F_k = []
	
	F_0 = []
	for one_set in test_set:
		if(C_0[one_set]/N >= minsup):
			F_0.append([one_set])
	print F_0
	
	F_k.append(F_0)
	
	for k in range( len(test_set) ):
		C_kp1 = set()
		for i in range(len(F_k[k]))[:-1]:
			for j in range(len(F_k[k]))[i + 1:]:
				 c = []
				 c.extend(F_k[k][i])
				 c.extend(F_k[k][j])
				 c.sort()
				 C_kp1.add( tuple(set(c)) )
		print "C_" + str(k+1), [_ for _ in C_kp1]
		
		F_kp1 = []
		for c in C_kp1:
			count = 0
			for T in test_data:
				true_count = 0
				for c_i in c:
					if(c_i in T):
						true_count += 1
				if(true_count == len(c) ):
					count += 1
			if(count/N >= minsup):
				F_kp1.append(list(c))
		print "F_" + str(k+1), F_kp1
		
		if( len(F_kp1) == 0):
			break
		else:
			F_k.append(F_kp1)
	
	print "\nfrequent patterns"
	num = 0
	for F in F_k:
		for f in F:
			num += 1
			for f_item in f:
				print f_item,
			print ""
	print str(num),"patterns"
			
		