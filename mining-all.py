#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime

from apriori import apriori

if __name__ == "__main__":
	
	start_t = datetime.now()
	print("-- start | " + start_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " --")
	
	file_name = "trafic_data"
	minsup = 0.80
	minconf = 0.4
	
	input_file = "./traffic_data/" + file_name + ".json"
	output_file_json = "./traffic_data/" + file_name + "_rules.json"
	output_file_csv = "./traffic_data/" + file_name + "_rules.csv"
	
	f = codecs.open(input_file,"r","utf-8")
	data = json.load(f)
	
	item_data = []
	print "loading file"
	for d in data:
		item_data.append( d[u"items"] )
	
	result = apriori(item_data, minsup=minsup, minconf=minconf)		
	
	print "writing data json"
	output_json = codecs.open(output_file_json, "w", "utf-8")
	json.dump(result, output_json, indent = 4, ensure_ascii = False)
	output_json.close()
	
	print "writing data csv"
	output_csv = codecs.open(output_file_csv, "w", "shift-jis")
	
	header_txt = "\"" + str( len(result) ) + " rules, minsup=" + str( minsup ) + ",minconf=" + str(minconf) + "\"\n"
	output_csv.write(header_txt)
	
	row_txt = "X,Y,support,confidence,lift\n"
	output_csv.write(row_txt)
	
	for row in result:
		row_data = ""
		
		X_txt = ""
		X_txt += "\"[" + row["X"][0]
		for x in row["X"][1:]:
			X_txt += ( "," + x )
		X_txt += "]\""
		
		Y_txt = ""
		Y_txt += "\"[" + row["Y"][0]
		for y in row["Y"][1:]:
			Y_txt += ( "," + y )
		Y_txt += "]\""
		
		row_data += ( X_txt + "," + Y_txt + "," + str(row["support"]) + "," + str(row["confidence"]) + "," + str(row["lift"]) + "\n")
		output_csv.write(row_data)
	output_csv.close()
	
	f.close()
	
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")