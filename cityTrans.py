# Web spider for the transportation time between cities from the excel file
# Author: Yuan Wei
# Site: Shanghai Jiao Tong University
# Date: 2018-01
# Email: weiy1991@{sjtu.edu.cn , 163.com}

import os
import sys
import xlrd

# read the excel file
def open_excel(file_name):
	data = xlrd.open_workbook(file_name)
	return data
# end read

# get the data by sheet name
def get_data_by_sheet_name(file_name, col_name_index = 0, sheet_name = "sheet1"):
	data = open_excel(file_name)
	table = data.sheet_by_name(sheet_name)
	nrows = table.nrows
	#print("nrows:", nrows)
	col_names = table.row_values(col_name_index)
	#print("col_names:",col_names)
	#list = []
	#for rownum in range(1, nrows):
	#	row = table.row_values(rownum)
	#	if row:
	#		app = {}
	#		for i in range(len(col_names)):
	#			app[col_names[i]] = row[i]
	#		list.append(app)
	return col_names
# end get

# get the API from the Gaode Map

# end get

# get the API from the 12306 website

# end get

# get the result from the website and write the result to the excel file

# end get


col_names = get_data_by_sheet_name("城市矩阵副本.xlsx", 0, "汽车")
print(col_names[0])
print(col_names[1])
print(col_names[2])

from urllib.parse import quote
from urllib import request
import json
import xlwt

# for driving path planning
amap_web_key = 'cdf8a2cb96be23b86cc5323828aafe9d'  # API Key from the Gaode
driving_path_planning = "http://restapi.amap.com/v3/direction/driving"
location_encode = "http://restapi.amap.com/v3/geocode/geo"

poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"

# key dic
map_key = ['9104487784107981ee3310e4fe08591d',
	   '6c6d2a7c80d63206a1ecacacee2a76c5',
	   '3359c7e74cd6cb20ee63ebcf5eb3ae10',
	   '93d2d194c987f64e8ca39ded9ed03f76',
	   'c68a245f0eb6c0582530ea06bd7a0ea1',
	   'ea47439f693e34ca304b007b1e621838',
	   '7f19af0af77e1097767ad072bd00cfbe']
# end key 


#根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True : #使用while循环不断分页获取数据
       result = getpoi_page(cityname, keywords, i)
       result = json.loads(result)  # 将字符串转换为json
       if result['count'] == '0':
           break
       hand(poilist, result)
       i = i + 1
    return poilist

#将返回的poi数据装入集合返回
def hand(poilist, result):
    #result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)) :
        poilist.append(pois[i])

#单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

#单页获取pois
def getDrivingPath_page(origin, destination, web_key):
    req_url = driving_path_planning + "?key=" + web_key + '&origin=' + origin  + '&destination=' + destination + '&extensions=base&output=jason&strategy=0'
    print(req_url)
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

# get the location of the place 
def getLocation(placeName):
	req_url = location_encode + "?key=" + amap_web_key + '&address=' + quote(placeName)
	data = ''
	#tt = request.urlopen(req_url)
	#print(tt)
	#print(type(tt))
	with request.urlopen(req_url) as f:
		data = f.read()
		data = data.decode('utf-8')
	return data


#获取城市分类数据
#cityname = "珠海"
#classfiled = "大学"
#pois = getpois(cityname, classfiled)

#location = getLocation("四川省绵阳市")
#print(location)


# get the location of each place
dict_city = {}
for i in range(len(col_names)):
	if i > 0:
		print(col_names[i])
		location_result = eval(getLocation(col_names[i]))
		#print(type(location_json))
		location_dic = location_result['geocodes'][0]['location']
		print(location_dic)

		dict_city[col_names[i]] = location_dic

# get the path planning time for the two places
# encode the order of the city
time_cost = {}
# end encode

count = 1
count_web_key = 0
cur_web_key = map_key[0]
for i in range(len(col_names)):
	# get the first location of the place
	if i == 0:
		continue
	#if i > 5:
 	#	break
	location_first = dict_city[col_names[i]]
	for j in range(len(col_names)):
		if j ==0:
			continue

		#if j > 5:
		#	break
		
		count += 1
		# check the key value
		# cur_web_key = ''
		if count > 1900:
			count_web_key += 1
			cur_web_key = map_key[count_web_key]
			#count_web_key += 1
			count = 1 
		# end check

		# get the second location of the  place
		location_second = dict_city[col_names[j]]
		# get the time cost of the two places
		data = getDrivingPath_page(location_first, location_second, cur_web_key)
		# print(data)
		data_dic = eval(data)
		#time_result = data_dic['route']
		#print("time_result:", time_result)
		time_result = data_dic['route']['paths'][0]['duration']
		print("time_result:", time_result)

		time_cost[col_names[i] + '-' + col_names[j]] = time_result

# wirte the time result to the excel file

import xlwt

print("time_cost: ", time_cost)

def open_excel_w(file_name):
	data = xlwt.open_workbook(file_name)
	return data

def write_result_to_excel_file(file_name, sheet_name, index, col, value):	
	data = open_excel_w(file_name)
	table = data.sheet_by_name(sheet_name)
	table.write(0, 0, time_cost[0])

#write_result_to_excel_file('城市矩阵.xlsx', '汽车', 0, 0, 'test')


def write_excel(sheet_name):
	wbk = xlwt.Workbook()
	sheet = wbk.add_sheet(sheet_name)
	for i in range(len(col_names)):
		if i==0:
			continue
		#if i>5:
		#	break
		sheet.write(i, 0, col_names[i])
		for j in range(len(col_names)):
			if j==0:
				sheet.write(0, i, col_names[i])
				continue
			#if j>5:
			#	break
			sheet.write(i,j,time_cost[col_names[i] + '-' + col_names[j]])#第0行第一列写入内容
	wbk.save('result.xls')
write_excel('cars')
# end write
			



#print(dict_city)
#timexml = getdrivingpath_page(1, 2)
#print(timexml)
