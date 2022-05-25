import time
import requests, re, json, shutil, urllib.request
from bs4 import BeautifulSoup as bs
from urllib.error import URLError, HTTPError
import os
import sys
import copy


json_path = "/home/akash/ashok/ipl/points_table.csv"
f = open(json_path)
point_table_all = json.load(f)
"""
json_path_2 = "/home/akash/ashok/ipl/match_output.csv"
f = open(json_path_2)
match_dict_all = json.load(f)
"""
def index_adding(point_table_ind):

	point_table_ind_with_index = {}
	count = 0
	for key in point_table_ind.keys():
		count += 1
		point_table_ind_with_index[count] = {}
		point_table_ind_with_index[count][key] = point_table_ind[key]

	#print(point_table_ind_with_index)
	return point_table_ind_with_index


def point_table_sort(point_table_ind):
	#print('1')
	#print(point_table_ind)
	point_table_ind = index_adding(point_table_ind)

	#print(point_table_ind)
	for i in range(1,10):
		
		for j in range(i,10):

			team_1 = list(point_table_ind[j].keys())[0]
			#print(team_1)
			
			win_1 = int(point_table_ind[j][team_1]['pts'])
			#print(win_1)

			team_2 = list(point_table_ind[j+1].keys())[0]
			#print(team_2)
			win_2 = int(point_table_ind[j+1][team_2]['pts'])
			#print(win_2)
			#exit()
			if(win_1<win_2):

				cache = point_table_ind[j]
				point_table_ind[j] = point_table_ind[j+1]
				point_table_ind[j+1] = cache

	#print('\n')
	#print(point_table_ind)






#print(point_table_all['1'])
#print('\n')
#index_adding(point_table_all['1'])
point_table_sorted_all = {}
for i in range(len(point_table_all.keys())):
	point_table_sorted = point_table_sort(point_table_all[str(i+1)])
	point_table_sorted_all[str(i+1)] = point_table_sorted