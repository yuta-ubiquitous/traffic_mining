#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime

from apriori import apriori

if __name__ == "__main__":
	
	start_t = datetime.now()
	print("-- start | " + start_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " --")
	
	file_name = "trafic_data"
	minsup = 0.4
	minconf = 0.7
	item_data = [	
					["tsuna","konbu","sake"],
					["tarako","tsuna"],
					["tarako","sake","ume"],
					["tsuna","konbu","sake"],
					["tsuna","sake"]
				]
	
	result = apriori(item_data, minsup=minsup, minconf=minconf)
	
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")