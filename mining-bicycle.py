#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime
import math

from apriori import apriori

def output_process(result, path, length, minsup):
	print "writing data json"
	output_json = codecs.open(path + ".json","w","utf-8")
	json.dump(result, output_json, indent = 4, ensure_ascii = False)
	output_json.close()
	
	print "writing data csv"
	output_csv = codecs.open(path +  ".csv", "w", "shift-jis")
	header_txt = "\"" + str(length) + " accident, " +str( len(result) ) + " patterns, minsup=" + str( minsup ) + "\"\n"
	output_csv.write(header_txt)
	row_txt = u"patterns,support,潜在率\n"
	output_csv.write(row_txt)
	
	for pattern in result:
		pattern_txt = ""
		pattern_txt += "\"" + pattern["pattern"][0]
		for item in pattern["pattern"][1:]:
			pattern_txt += ( "," + item )
		pattern_txt += "\""
		row_data = ( pattern_txt + "," + str( pattern["support"] ) + "," + str( pattern["potential"] ) + "\n")
		output_csv.write(row_data)		
	output_csv.close()

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
	file_name_car_car = "乗用車-乗用車"
	result_car_car = apriori(T_car_car, minsup=minsup, frequent_pattern=True)
	
	# car_bicycle
	file_name_car_bicycle = "乗用車-自転車"
	result_car_bicycle = apriori(T_car_bicycle, minsup=minsup, frequent_pattern=True)
	
	for pattern in result_car_car:
		isExist = False
		for com_pattern in result_car_bicycle:
			if( pattern["pattern"] == com_pattern["pattern"]):
				isExist = True
				pattern["potential"] = pattern["support"] / com_pattern["support"]
				break
				
		if(not isExist):
			pattern["potential"] = 99999
	output_process(result_car_car, output_path + file_name_car_car, len(T_car_car), minsup)
		
	for pattern in result_car_bicycle:
		isExist = False
		for com_pattern in result_car_car:
			if( pattern["pattern"] == com_pattern["pattern"]):
				isExist = True
				pattern["potential"] = pattern["support"] / com_pattern["support"]
				break
				
		if(not isExist):
			pattern["potential"] = 99999
	output_process(result_car_bicycle, output_path + file_name_car_bicycle, len(T_car_bicycle), minsup)
	
	# end process
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")