#-*- coding:utf-8 -*-

import os
import codecs
import json
import sys

# MAX_ROW = 8870
MAX_ROW = 0

if __name__ == "__main__":

	print "start traffic_mining"
	
	output_name = "./traffic_data/trafic_data_sub.json"
	h24 = codecs.open("traffic_data/h24.csv", "r", "utf-8")
	h25 = codecs.open("traffic_data/h25.csv", "r", "utf-8")
	h26 = codecs.open("traffic_data/h26.csv", "r", "utf-8")
	
	f = [h24,h25,h26]
	
	row_counter = 0
	row_label = []
	dict_list = []
	output_dict = []
	
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
			if(MAX_ROW == 0):
				continue
			elif(row_counter > MAX_ROW):
				break
	
	for data in dict_list:
		sys.stdout.write("\r" + str(data[u"id"]))
		sys.stdout.flush()
		
		item_dict = {}
		
		item_dict["id"] = data["id"]
		item_dict["latitude"] = float(data[u"地点緯度"])
		item_dict["longitude"] = float(data[u"地点経度"])
		
		if(item_dict["latitude"] == 0 or item_dict["longitude"] == 0):
			print "\n" + "id " + str( data["id"] ) + " : detect null position item"
			continue
		
		item_list = []
		
		
		'''
		key = u"事故類型_１"
		item_list.append( key + u":" + data[key] )
		'''
		
		key = u"事故類型_２"
		for item in data[key].split(u"・"):
			item_list.append( key + u":" + item )
		
		'''
		key = u"死者数"
		item_list.append( u"死者" + u":" + (u"あり" if int( data[key] ) > 0 else u"なし" ) )
		
		key = u"重傷者数"
		item_list.append( u"重傷者" + u":" + (u"あり" if int( data[key] ) > 0 else u"なし" ) )
		
		key = u"軽傷者数"
		item_list.append( u"軽傷者" + u":" + (u"あり" if int( data[key] ) > 0 else u"なし" ) )
		
		key = u"路線"
		item_list.append( key + u":" + data[key] )
		
		key = u"昼夜"
		item_list.append( key + u":" + data[key] )
		
		key = u"道路形状"
		for item in data[key].split(u"・"):
			item_list.append( key + u":" + item )
		'''	
		
		key = u"年齢_１当"
		item_list.append( key + u":" + str( int( data[key] ) / 10 * 10 ) + u"歳代" )
		
		key = u"年齢_２当"
		if( data[u"事故類型_１"] == u"車両相互" ):
			item_list.append( key + u":" + str( int( data[key] ) / 10 * 10 ) + u"歳代" )
		
		'''	
		key = u"当事者種_1"
		for item in data[key].split(u"　"):
			item_list.append( key + u":" + item )
		
		key = u"当事者種_2"
		for item in data[key].split(u"　"):
			item_list.append( key + u":" + item )
		
		key = u"法令違反_1"
		for item1 in data[key].split(u"　"):
			for item2 in item1.split(u"・"):
				item_list.append( key + u":" + item2 )
		
		key = u"法令違反_2"
		for item1 in data[key].split(u"　"):
			for item2 in item1.split(u"・"):
				item_list.append( key + u":" + item2 )
		
		key = u"事故内容"
		item_list.append( key + u":" + data[key] )
		'''
		
		key = u"発生時分"
		# 年/月/日
		item = data[key].split(u" ")
		time0 = item[0].split(u"/")
		# item_list.append( key + u"_年" + u":" + time0[0] )
		# 気象庁による区分
		# 春 3-5月  
		# 夏 6-8月
		# 秋 9-11月
		# 冬 12-2月
		month = int(time0[1])
		season = ""
		if(month >= 3 and month <= 5):
			season = u"春"
		elif(month >= 6 and month <= 8):
			season = u"夏"
		elif(month >= 9 and month <= 11):
			season = u"秋"
		elif(month == 12 or month <= 2):
			season = u"冬"		
		item_list.append( key + u"_季節" + u":" + season )
		
		# 時:分
		time1 = item[1].split(u":")
		# 未明 0-2時
		# 明け方 3-5時
		# 朝 6-8時
		# 昼前 9-11時
		# 昼過ぎ 12-14時
		# 夕方 15-17時
		# 夜の初め頃 18-20時
		# 夜遅く 21-23時
		hour = int(time1[0])
		timezone = ""
		if(hour >= 0 and hour <= 2):
			timezone = u"未明"
		elif(month >= 3 and month <= 5):
			timezone = u"明け方"
		elif(month >= 6 and month <= 8):
			timezone = u"朝"
		elif(month >= 9 and month <= 11):
			timezone = u"昼前"
		elif(month >= 12 and month <= 14):
			timezone = u"昼過ぎ"
		elif(month >= 15 and month <= 17):
			timezone = u"夕方"
		elif(month >= 18 and month <= 20):
			timezone = u"夜の初め頃"
		elif(month >= 21 and month <= 23):
			timezone = u"夜遅く"
		item_list.append( key + u"_時間帯" + u":" + timezone )
		
		key = u"曜日"
		item_list.append( key + u":" + data[key] )
		
		'''
		key = u"天候"
		item_list.append( key + u":" + data[key] )
		
		key = u"路面状態"
		item_list.append( key + u":" + data[key] )
		
		key = u"信号機"
		item_list.append( key + u":" + data[key] )
		
		key = u"道路線形"
		item_list.append( key + u":" + data[key] )
		
		key = u"衝突地点"
		for item in data[key].split(u"・"):
			item_list.append( key + u":" + item )
		
		key = u"中央分離帯"
		item_list.append( key + u":" + data[key] )
		
		key = u"歩車道区分"
		for item in data[key].split(u"　"):
			item_list.append( key + u":" + item )
		
		key = u"危険速度_1"
		item_list.append( key + u":" + data[key] )
		
		key = u"危険速度_2"
		if( data[u"事故類型_１"] == u"車両相互" ):
			item_list.append( key + u":" + data[key] )
		
		key = u"用途別_１当"
		for item in data[key].split(u"・"):
			item_list.append( key + u":" + item )
		
		key = u"用途別_２当"
		if( data[u"事故類型_１"] == u"車両相互" ):
			for item in data[key].split(u"・"):
				item_list.append( key + u":" + item )
		
		key = u"車両形状_１当"
		for item in data[key].split(u"　"):
			item_list.append( key + u":" + item )
			
		key = u"車両形状_２当"
		if( data[u"事故類型_１"] == u"車両相互" ):
			for item in data[key].split(u"　"):
				item_list.append( key + u":" + item )
		
		key = u"行動類型_１当"
		for item in data[key].split(u"・"):
			item_list.append( key + u":" + item )
		
		key = u"行動類型_２当"
		if( data[u"事故類型_１"] == u"車両相互" ):
			for item in data[key].split(u"・"):
				item_list.append( key + u":" + item )
		
		key = u"車両損壊_１当"
		item_list.append( key + u":" + data[key] )
		
		key = u"車両損壊_２当"
		if( data[u"事故類型_１"] == u"車両相互" ):
			item_list.append( key + u":" + data[key] )
			
		key = u"１当進行方向"
		item_list.append( key + u":" + data[key] )
		
		key = u"２当進行方向"
		if( data[u"事故類型_１"] == u"車両相互" ):
			item_list.append( key + u":" + data[key] )
		'''
		
		item_dict["items"] = item_list
		
		# add preprocess data
		output_dict.append(item_dict)
	
	print ""
	
	# output preprocess data to json file
	print "writing data"
	output_json = codecs.open(output_name, "w", "utf-8")
	json.dump(output_dict, output_json, indent = 4, ensure_ascii = False)
	output_json.close()
	
	print "finish!!"