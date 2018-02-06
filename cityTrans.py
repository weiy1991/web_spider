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


col_names = get_data_by_sheet_name("城市矩阵.xlsx", 0, "汽车")
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
def getDrivingPath_page(origin, destination):
    req_url = driving_path_planning + "?key=" + amap_web_key + '&origin=104.679114,31.467450' + '&destination=108.393135,31.160711' + '&extensions=base&output=jason&strategy=0'
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
cityname = "珠海"
classfiled = "大学"
#pois = getpois(cityname, classfiled)

location = getLocation("四川省绵阳市")
print(location)


dict_city = {}
for i in range(len(col_names)-1):
	if i > 0:
		print(col_names[i])
		location_result = eval(getLocation(col_names[i]))
		#print(type(location_json))
		location_dic = location_result['geocodes'][0]['location']
		print(location_dic)

		dict_city[col_names[i]] = location_dic


print(dict_city)
#timeXML = getDrivingPath_page(1, 2)
#print(timeXML)
