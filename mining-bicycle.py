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
	
	T_car_bicycle = []
	T_car_car = []
	for T in data:
		if( T[u"被害車種"] == u"乗用車" ):
			T_car_car.append( T[u"items"] )
		elif( T[u"被害車種"] == u"自転車" ):
			T_car_bicycle.append( T[u"items"] )
	
	# Start mining
	
	# car_car
	output_file_name = "乗用車-乗用車"
	result = apriori(T_car_car, minsup=minsup, frequent_pattern=True)
	
	result_json = []
	for pattern,support in result.items():
		json_data = {}
		json_data["pattern"] = pattern
		json_data["support"] = support/float( len(T_car_car) )
		result_json.append(json_data)
	
	print "writing data json"
	car_car_output_json = codecs.open(output_path + output_file_name + ".json","w","utf-8")
	json.dump(result_json, car_car_output_json, indent = 4, ensure_ascii = False)
	car_car_output_json.close()
	
	print "writing data csv"
	output_csv = codecs.open(output_path + output_file_name +  ".csv", "w", "shift-jis")
	header_txt = "\"" + str(len(T_car_car)) + " accident, " +str( len(result) ) + " patterns, minsup=" + str( minsup ) + "\"\n"
	output_csv.write(header_txt)
	row_txt = "patterns,support\n"
	output_csv.write(row_txt)
	
	for pattern,support in result.items():
		pattern_txt = ""
		pattern_txt += "\"" + pattern[0]
		for item in pattern[1:]:
			pattern_txt += ( "," + item )
		pattern_txt += "\""
		row_data = ( pattern_txt + "," + str( support/float( len(T_car_car) ) ) + "\n")
		output_csv.write(row_data)		
	output_csv.close()
	
	# car_bicycle
	output_file_name = "乗用車-自転車"
	result = apriori(T_car_bicycle, minsup=minsup, frequent_pattern=True)
	
	result_json = []
	for pattern,support in result.items():
		json_data = {}
		json_data["pattern"] = pattern
		json_data["support"] = support/float(len(T_car_bicycle))
		result_json.append(json_data)
	
	print "writing data json"
	car_bicycle_output_json = codecs.open(output_path + output_file_name + ".json","w","utf-8")
	json.dump(result_json, car_bicycle_output_json, indent = 4, ensure_ascii = False)
	car_bicycle_output_json.close()
	
	print "writing data csv"
	output_csv = codecs.open(output_path + output_file_name +  ".csv", "w", "shift-jis")
	header_txt = "\"" + str(len(T_car_bicycle)) + " accident, " +str( len(result) ) + " patterns, minsup=" + str( minsup ) + "\"\n"
	output_csv.write(header_txt)
	row_txt = "patterns,support\n"
	output_csv.write(row_txt)
	
	for pattern,support in result.items():
		pattern_txt = ""
		pattern_txt += "\"" + pattern[0]
		for item in pattern[1:]:
			pattern_txt += ( "," + item )
		pattern_txt += "\""
		
		row_data = ( pattern_txt + "," + str( support/float(len(T_car_bicycle)) ) + "\n")
		output_csv.write(row_data)
	output_csv.close()
	
	# end process
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")