#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime
import math

from apriori import apriori

if __name__ == "__main__":
	
	start_t = datetime.now()
	print "*** mining-intersection.py ***"
	print("-- start | " + start_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " --")
	
	file_name = "trafic_data_intersection"
	minsup = 0.2
	minconf = 0.75
	minaccidents = 10
	
	input_file = "./traffic_data/" + file_name + ".json"
	output_file = u"./traffic_data/" + file_name + u"/全ての交差点"
	
	item_relation = {
		u"発生時分_季節":[u"発生時分_時間帯",u"発生時分",u"曜日"],
		u"発生時分_時間帯":[],
		u"発生時分":[u"発生時分_時間帯"],
		u"曜日":[u"発生時分_時間帯"]
	}
	
	f = codecs.open(input_file,"r","utf-8")
	data = json.load(f)
	f.close()
	
	all_rule_list = []
	
	intersection_set = set()
	for T in data:
		intersection_set.add( T["intersection"] )
	
	print str( len(intersection_set) ) + " intersections"
	
	# Start mining
	for intersection_name in intersection_set:
		
		print "processing " + intersection_name + " intersection"
		
		item_data=[]
		accident_count = 0
		
		for T in data:
			if(T["intersection"] == intersection_name):
				accident_count += 1
				item_data.append( T[u"items"] )
		print "accident num : " + str(accident_count)
		if(accident_count <= minaccidents):
			print "num is little"
			continue
		
		# start apriori
		result = apriori(item_data, minsup=minsup, minconf=minconf, liftcut=True, log=False)	
	
		'''
		output_json = codecs.open("./traffic_data/" + file_name + "/" + intersection_name + ".json", "w", "utf-8")
		json.dump(result, output_json, indent = 4, ensure_ascii = False)
		output_json.close()
		
		output_csv = codecs.open("./traffic_data/" + file_name + "/" + intersection_name + ".csv", "w", "shift-jis")
		
		header_txt = "\"" + str(accident_count) + " accident, " +str( len(result) ) + " rules, minsup=" + str( minsup ) + ",minconf=" + str(minconf) + "\"\n"
		output_csv.write(header_txt)
		
		row_txt = "X,Y,support,confidence,lift\n"
		output_csv.write(row_txt)
		
		for row in result:
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
			
			row_data = ( X_txt + "," + Y_txt + "," + str(row["support"]) + "," + str(row["confidence"]) + "," + str(row["lift"]) + "\n")
			output_csv.write(row_data)
		output_csv.close()
		'''
		
		for row in result:
			
			"発生時分_季節:冬", 
			"発生時分_時間帯:6-11", 
			"発生時分:平日"
			
			"発生時分_季節:夏", 
			"発生時分_時間帯:朝", 
			"曜日:金"
			
			isNotMatch = False
			for _ in row["Y"]:
				y = _.split(":")[0]
				for ry in item_relation[y]:
					for __ in row["X"]:
						x = __.split(":")[0]
						if(ry == x):
							isNotMatch = True
			
			if(not isNotMatch):
				row["intersection"] = intersection_name
				row["number of transaction"] = accident_count * row["support"]
				row["number of accidents"] = accident_count
				all_rule_list.append(row)
	
	print "writing data json"
	all_output_json = codecs.open(output_file + ".json","w","utf-8")
	json.dump(all_rule_list, all_output_json, indent = 4, ensure_ascii = False)
	all_output_json.close()
	
	print "writing data csv"
	all_output_csv = codecs.open(output_file + ".csv","w","shift-jis")
	header_txt = "\"" + str(len(data)) + " accident, " +str( len(all_rule_list) ) + " rules, minsup=" + str( minsup ) + ",minconf=" + str(minconf) + "\"\n"
	all_output_csv.write(header_txt)
	
	row_txt = "X,Y,number of transaction,intersection,number of accidents,support,confidence,lift\n"
	all_output_csv.write(row_txt)
	
	for row in all_rule_list:
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
		
		row_data = ( X_txt + "," + Y_txt + "," + str(row["number of transaction"]) + "," + row["intersection"] + "," + str(row["number of accidents"]) + "," + str(row["support"]) + "," + str(row["confidence"]) + "," + str(row["lift"]) + "\n")
		all_output_csv.write(row_data)
	all_output_csv.close()
	
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")