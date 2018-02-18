# This file is for the web spider of 12306.com of China train website
# Author: Wei Yuan
# Site: Shanghai Jiao Tong University
# Date: 2018-02-09
# Email: weiy1991@{sjtu.edu.cn, 163.com}

import os
#import xlrt
import xlwt
import requests
import re

#url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9002' #根据查看源码查出来的
#response=requests.get(url,verify=False)
#stations=re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response.text)#用正则表达式 来获取车站的拼音和大小写字母的代号信息
#print(dict(stations))

url_train = 'http://trains.ctrip.com/TrainBooking/Search.aspx?from=shanghai&to=beijing&day=2'
#url_train = 'http://trains.ctrip.com/TrainBooking/shanghai-beijing/'
#url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9002' #根据查看源码查出来的
response_train = requests.get(url_train,verify=False)
#stations_train = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response_train.text)#用正则表达式 来获取车站的拼音和大小写字母的代号信息
print(response_train)

