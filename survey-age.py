#-*- coding:utf-8 -*-

import json
import codecs
from datetime import datetime
import math

from apriori import apriori

if __name__ == "__main__":
	
	start_t = datetime.now()
	print "*** survey-age.py ***"
	print("-- start | " + start_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " --")
	
	h22 = codecs.open("traffic_data/h22.csv", "r", "utf-8")
	h23 = codecs.open("traffic_data/h23.csv", "r", "utf-8")
	h24 = codecs.open("traffic_data/h24.csv", "r", "utf-8")
	h25 = codecs.open("traffic_data/h25.csv", "r", "utf-8")
	h26 = codecs.open("traffic_data/h26.csv", "r", "utf-8")
	
	output_file = "./traffic_data/age/age-histgram.csv"
	
	f = [h22,h23,h24,h25,h26]
	
	row_counter = 0
	row_label = []
	dict_list = []
	
	for hxx in f:
		isThrough = False
		for row in hxx:
			if(row_counter == 0):
				row_label = row.split(",")
				isThrough = True
			elif(not isThrough):
				isThrough = True
			else:
				dict = {}
				dict["id"] = row_counter
				for key, value in zip( row_label, row.split(",") ):
					dict[key.replace("\r\n", "")] = value.replace("\r\n", "")
				dict_list.append(dict)
				
			row_counter += 1
	
	max_age = 0
	for data in dict_list:
		key = u"年齢_１当"
		if(int( data[key] ) > max_age):
			max_age = int( data[key] )
		
		key = u"年齢_２当"
		if(int( data[key] ) > max_age):
			max_age = int( data[key] )	
			
	# output preprocess data to json file
	print "output " + output_file
	output_csv = codecs.open(output_file,"w","utf-8")
	
	row_txt = u"年齢,加害者数,被害者数\n"
	output_csv.write(row_txt)
	
	for age_i in range(max_age + 1):
		perpetrator_counter = 0
		victim_counter = 0
		
		for data in dict_list:
			key = u"年齢_１当"
			if( age_i == int( data[key] ) ):
				perpetrator_counter += 1
			
			key = u"年齢_２当"
			if( age_i == int( data[key] ) ):
				victim_counter += 1
				
		row_txt = str( age_i ) + u"," + str( perpetrator_counter ) + u"," + str( victim_counter ) + u"\n"
		output_csv.write(row_txt)
	output_csv.close()
	
	end_t = datetime.now()
	between_t = end_t - start_t
	print("-- finish!! | " + end_t.strftime("%Y-%m-%dT%H:%M:%SZ") + " | " + str(between_t.seconds) + "[sec] --")