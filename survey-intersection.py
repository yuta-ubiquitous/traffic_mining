#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime
import math

from apriori import apriori

if __name__ == "__main__":
	
	start_t = datetime.now()
	print "*** survey-intersection.py ***"
	print("-- start | " + start_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " --")
	
	file_name = "trafic_data_intersection"
	
	input_file = "./traffic_data/" + file_name + ".json"
	output_file = u"./traffic_data/survey_intersection.csv"
	
	f = codecs.open(input_file,"r","utf-8")
	data = json.load(f)
	f.close()
	
	all_rule_list = []
	
	intersection_dict = {}
	for T in data:
		if( intersection_dict.has_key(T["intersection"]) ):
			intersection_dict[ T["intersection"] ] += 1
		else:
			intersection_dict[ T["intersection"] ] = 1
	
	print "writing data csv"
	output_csv = codecs.open(output_file,"w","utf-8")
	
	row_txt = u"交差点名,事故数\n"
	output_csv.write(row_txt)
	
	for key,value in intersection_dict.items():
		row_txt = key + u"," + str( value ) + u"\n"
		output_csv.write(row_txt)
		
	output_csv.close()
	
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")