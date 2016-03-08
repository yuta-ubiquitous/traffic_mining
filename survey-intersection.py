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
	output_file_1 = u"./traffic_data/intersection/survey_intersection.csv"
	output_file_2 = u"./traffic_data/intersection/survey_intersection_histgram.csv"
	max_num = 0
	
	f = codecs.open(input_file,"r","utf-8")
	data = json.load(f)
	f.close()
	
	all_rule_list = []
	
	intersection_dict = {}
	for T in data:
		if( intersection_dict.has_key(T["intersection"]) ):
			intersection_dict[ T["intersection"] ] += 1
			if(intersection_dict[ T["intersection"] ] > max_num):
				max_num = intersection_dict[ T["intersection"] ]
		else:
			intersection_dict[ T["intersection"] ] = 1
	
	print "output " + output_file_1
	output_csv = codecs.open(output_file_1,"w","utf-8")
	
	row_txt = u"交差点名,事故数\n"
	output_csv.write(row_txt)
	
	for key,value in intersection_dict.items():
		row_txt = key + u"," + str( value ) + u"\n"
		output_csv.write(row_txt)
		
	output_csv.close()
	
	print "output " + output_file_2
	output_csv = codecs.open(output_file_2,"w","utf-8")
	
	row_txt = u"事故数,交差点数\n"
	output_csv.write(row_txt)

	for i in range( max_num + 1 ):
		counter = 0
		for key, value in intersection_dict.items():
			if(value == i):
				counter += 1
		
		row_txt = str( i ) + u"," + str( counter ) + u"\n"
		output_csv.write(row_txt)
	output_csv.close()
	
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")