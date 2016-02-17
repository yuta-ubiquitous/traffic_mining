#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime
import math

from apriori import apriori

if __name__ == "__main__":
	
	start_t = datetime.now()
	print "*** mining-age.py ***"
	print("-- start | " + start_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " --")
	
	file_name = "trafic_data_age"
	minsup = 0.05
	
	input_file = "./traffic_data/" + file_name + ".json"
	output_path = "./traffic_data/age/"
	
	f = codecs.open(input_file,"r","utf-8")
	data = json.load(f)
	f.close()
	
	age_set = set()
	for T in data:
		age_set.add(T[u"age"])
	
	T_dict = {}
	for age in age_set:
		T_list = []
		for T in data:
			if( T[u"age"] == age ):
				T_list.append( T["items"] )
		T_dict[age] = T_list
	
	# Start mining
	# car_car
	result_dict = {}
	for age in age_set:
		result_dict[age] = apriori(T_dict[age], minsup=minsup, frequent_pattern=True)
	
	for age in age_set:
		other_age_list = [a for a in age_set if(not age == a)]
		for com_age in other_age_list:
			for pattern in result_dict[age]:
				isExist = False
				for com_pattern in result_dict[com_age]:
					if( pattern["pattern"] == com_pattern["pattern"] ):
						isExist = True
						pattern[com_age] = pattern["support"] / com_pattern["support"]
						break
				if(not isExist):
					pattern[com_age] = 99999
		
		path = output_path + u"年齢" + age
		print "writing " + age + " data json"
		output_json = codecs.open(path + ".json","w","utf-8")
		json.dump(result_dict[age], output_json, indent = 4, ensure_ascii = False)
		output_json.close()
		
		print "writing " + age + " data csv"
		output_csv = codecs.open(path +  ".csv", "w", "shift-jis")
		header_txt = "\"" + str( len(T_dict[age]) ) + " accident, " +str( len(result_dict[age]) ) + " patterns, minsup=" + str( minsup ) + "\"\n"
		output_csv.write(header_txt)
		
		row_txt = u"patterns,support"
		for a in other_age_list:
			row_txt += "," + u"増加率_" + a
		row_txt += "\n"
		output_csv.write(row_txt)
		
		for pattern in result_dict[age]:
			pattern_txt = ""
			pattern_txt += "\"" + pattern["pattern"][0]
			for item in pattern["pattern"][1:]:
				pattern_txt += ( "," + item )
			pattern_txt += "\""
			row_data = pattern_txt + "," + str( pattern["support"] )
			
			for v in other_age_list:
				row_data += "," + str( pattern[v] )
			row_data += "\n"
			output_csv.write(row_data)		
		output_csv.close()
		
	# all
	pattern_set = set()
	for age in age_set:
		for pattern in result_dict[age]:
			pattern_set.add(pattern["pattern"])
	
	pattern_dict = []
	for pattern in pattern_set:
		p_dict = {}
		p_dict["pattern"] = pattern
		for age in age_set:
			isExist = False
			for com_pattern in result_dict[age]:
				if( pattern == com_pattern["pattern"] ):
					p_dict[age] = com_pattern["support"]
					isExist = True
					break
			if( not isExist ):
				p_dict[age] = 0.0
		pattern_dict.append(p_dict)
		
	print "writing all data csv"
	path = output_path + "all"
	output_csv = codecs.open(path +  ".csv", "w", "shift-jis")
	
	row_txt = u"patterns"
	for age in age_set:
		row_txt += "," + u"support_" + age
	row_txt += "\n"
	output_csv.write(row_txt)
	
	for pattern in pattern_dict:
		pattern_txt = ""
		pattern_txt += "\"" + pattern["pattern"][0]
		for item in pattern["pattern"][1:]:
			pattern_txt += ( "," + item )
		pattern_txt += "\""
		row_data = pattern_txt
		
		for age in age_set:
			support = pattern[age]
			row_data += "," + str( support )
		row_data += "\n"
		output_csv.write(row_data)		
	output_csv.close()
	
	# end process
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")