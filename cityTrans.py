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

col_names = get_data_by_sheet_name("城市矩阵.xlsx", 0, "汽车")
print(col_names) 
