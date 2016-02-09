#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime
import math

from apriori import apriori

def hubeny(lon1, lat1, lon2, lat2):
	
	x1 = lon1 * math.pi / 180.0
	y1 = lat1 * math.pi / 180.0
	x2 = lon2 * math.pi / 180.0
	y2 = lat2 * math.pi / 180.0
	
	a = 6378137.000
	b = 6356752.314245
	e = math.sqrt( (a**2 - b**2) / a**2 )
	dy = y1 - y2
	dx = x1 - x2
	mu_y = (y1 + y2)/2.0
	W = math.sqrt(1.0 - e**2 * math.sin(mu_y) ** 2)
	M = a * (1 - e**2) / W**3
	N = a / W
	d = math.sqrt( (dy*M)**2 + (dx*N*math.cos(mu_y))**2 )
	return d

if __name__ == "__main__":
	
	start_t = datetime.now()
	print "*** intersection.py ***"
	print("-- start | " + start_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " --")
	
	file_name = "trafic_data_intersection"
	minsup = 0.2
	minconf = 0.5
	minaccidents = 10
	
	input_file = "./traffic_data/" + file_name + ".json"
	
	f = codecs.open(input_file,"r","utf-8")
	data = json.load(f)
	f.close()
	
	intersection_set = set()
	for T in data:
		intersection_set.add( T["intersection"] )
	
	print str( len(intersection_set) ) + " intersections"
	
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
		result = apriori(item_data, minsup=minsup, minconf=minconf, liftcut=True)	
	
		print "writing data json"
		output_json = codecs.open("./traffic_data/intersection/" + intersection_name + ".json", "w", "utf-8")
		json.dump(result, output_json, indent = 4, ensure_ascii = False)
		output_json.close()
		
		print "writing data csv"
		output_csv = codecs.open("./traffic_data/intersection/" + intersection_name + ".csv", "w", "shift-jis")
		
		header_txt = "\"" + str(accident_count) + " accident, " +str( len(result) ) + " rules, minsup=" + str( minsup ) + ",minconf=" + str(minconf) + "\"\n"
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
	
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")