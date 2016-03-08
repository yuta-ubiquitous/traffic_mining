#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime
import math

from apriori import apriori

if __name__ == "__main__":
	
	start_t = datetime.now()
	print "*** mining-bicycle.py ***"
	print("-- start | " + start_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " --")
	
	file_name = "trafic_data_bicycle"
	minsup = 0.2
	
	input_file = "./traffic_data/" + file_name + ".json"
	output_path = "./traffic_data/bicycle/"
	
	f = codecs.open(input_file,"r","utf-8")
	data = json.load(f)
	f.close()
	
	vehicle_set = set()
	for T in data:
		vehicle_set.add(T[u"被害車種"])
	
	T_dict = {}
	for vehicle in vehicle_set:
		T_list = []
		for T in data:
			if( T[u"被害車種"] == vehicle ):
				T_list.append( T["items"] )
		T_dict[vehicle] = T_list
	
	# Start mining
	# car_car
	result_dict = {}
	for vehicle in vehicle_set:
		result_dict[vehicle] = apriori(T_dict[vehicle], minsup=minsup, frequent_pattern=True)
	
	for vehicle in vehicle_set:
		other_vehicle_list = [v for v in vehicle_set if(not vehicle == v)]
		for com_vehicle in other_vehicle_list:
			for pattern in result_dict[vehicle]:
				isExist = False
				for com_pattern in result_dict[com_vehicle]:
					if( pattern["pattern"] == com_pattern["pattern"] ):
						isExist = True
						pattern[com_vehicle] = pattern["support"] / com_pattern["support"]
						break
				if(not isExist):
					pattern[com_vehicle] = 99999
		
		path = output_path + u"乗用車-" + vehicle
		print "writing " + vehicle + " data json"
		output_json = codecs.open(path + ".json","w","utf-8")
		json.dump(result_dict[vehicle], output_json, indent = 4, ensure_ascii = False)
		output_json.close()
		
		print "writing " + vehicle + " data csv"
		output_csv = codecs.open(path +  ".csv", "w", "shift-jis")
		header_txt = "\"" + str( len(T_dict[vehicle]) ) + " accident, " +str( len(result_dict[vehicle]) ) + " patterns, minsup=" + str( minsup ) + "\"\n"
		output_csv.write(header_txt)
		
		row_txt = u"patterns,support"
		for v in other_vehicle_list:
			row_txt += "," + u"増加率_" + v
		row_txt += "\n"
		output_csv.write(row_txt)
		
		for pattern in result_dict[vehicle]:
			pattern_txt = ""
			pattern_txt += "\"" + pattern["pattern"][0]
			for item in pattern["pattern"][1:]:
				pattern_txt += ( "," + item )
			pattern_txt += "\""
			row_data = pattern_txt + "," + str( pattern["support"] )
			
			for v in other_vehicle_list:
				row_data += "," + str( pattern[v] )
			row_data += "\n"
			output_csv.write(row_data)		
		output_csv.close()
	
	# all patterns
	output_all = "./traffic_data/bicycle/all.csv"
	
	pattern_set = set()
	for vehicle in vehicle_set:
		for pattern in result_dict[vehicle]:
			pattern_set.add(pattern["pattern"])
	
	print "output " + output_all
	output_csv = codecs.open(output_all, "w", "shift-jis")
	
	header_txt = u"patterns,length"
	for vehicle in vehicle_set:
		header_txt += u"," + vehicle + u"-support"
	header_txt += "\n"
	output_csv.write(header_txt)
	
	for pattern in pattern_set:
		pattern_txt = ""
		pattern_txt += "\"" + pattern[0]
		for item in pattern[1:]:
			pattern_txt += ( "," + item )
		pattern_txt += "\""
		output_csv.write(pattern_txt)
		
		length_txt = "," + str( len( pattern ) )
		output_csv.write(length_txt)
		
		for vehicle in vehicle_set:
			counter = 0
			for v_pattern in T_dict[vehicle]:
				equal_counter = 0
				for item in pattern:
					if(item in v_pattern):
						equal_counter += 1
				
				if( equal_counter == len(pattern) ):
					counter += 1
			output_csv.write( "," + str( float(counter) / float( len(T_dict[vehicle]) ) ) )
		output_csv.write("\n")
	output_csv.close()

	# end process
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")