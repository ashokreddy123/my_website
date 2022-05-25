import time
import requests, re, json, shutil, urllib.request
from bs4 import BeautifulSoup as bs
from urllib.error import URLError, HTTPError
import os
import sys
import copy

def schedule_scrap():

	link="https://www.cricbuzz.com/cricket-series/4061/indian-premier-league-2022/matches"
	page = requests.get(link)

	soup = bs(page.content, 'html.parser')

	
	match_count = 0
	match_dict = {}
	for data in soup.findAll('a',class_="text-hvr-underline"):

		match_count += 1

		#print(data.span.text)
		teams = [data.span.text.split(' vs ')[0], data.span.text.split(' vs ')[1].split(',')[0]]
		#print(teams)
		#print("--------------------")
		

		match_dict[str(match_count)] = {}
		match_dict[str(match_count)]['teams'] = teams
		match_dict[str(match_count)]['result'] = 'NA' 

		if(match_count>=70):
			break
	
	result_count = 0
	for data in soup.findAll('a',class_="cb-text-complete"):

		result_count += 1

		#print(data.text)

		result = data.text.split(' won ')[0]
		#print(result)
		#print('-------------------')
		match_dict[str(result_count)]['result'] = result 
		
	print("result_count ",result_count)

	return match_dict,result_count

def point_table_scrap():

	link="https://www.cricbuzz.com/cricket-series/4061/indian-premier-league-2022/points-table"
	page = requests.get(link)

	soup = bs(page.content, 'html.parser')

	points_table = {}
	
	team_count = 0
	match_dict = {}
	for data in soup.findAll('tr',class_=""):
		
		for data2 in data.findAll('td',class_="cb-srs-pnts-name"):
			team_count += 1
			#print('****************************')

			if(data2 != []):
				#print(data)
				#print(data2.text)
				team_name = data2.text
				team_name = team_name.split('(')[0]
				team_name = team_name.replace(u'\xa0', '')
				points_table[team_name] = {}

				values = []
				for data3 in data.findAll('td',class_="cb-srs-pnts-td"):
					#print(data3)
					values.append(data3.text)
				

				points_table[team_name]['mat'] = int(values[0])
				points_table[team_name]['won'] = int(values[1])
				points_table[team_name]['lost'] = int(values[2])
				points_table[team_name]['tied'] = int(values[3])
				points_table[team_name]['NR'] = int(values[4])
				points_table[team_name]['pts'] = int(values[5])
				points_table[team_name]['nrr'] = values[6]
				#print('--------------------------')
		
	return points_table

def one_match_prediction(points_table,match_dict,point_table_count,point_table_all,match_dict_all,matches_done):
	match_count = 1
	
	#print(match_dict[str(match_count)]['result'])
	
	while(True):

		if(match_dict[str(match_count)]['result'] == 'NA'):


			
			#print(match_dict[str(match_count)])
			#points_table_1 = points_table+"_"+str(point_table_count)
			#points_table+"_"+str(point_table_count) = copy.deepcopy(points_table)

			team_1 = match_dict[str(match_count)]['teams'][0]
			team_2 = match_dict[str(match_count)]['teams'][1]
			#print('-------------')
			#print(match_count)
			#print(team_1,team_2)
			#------------------------------------
			points_table_1 = copy.deepcopy(points_table)
			match_dict_1 = copy.deepcopy(match_dict)



			match_dict_1[str(match_count)]['result'] = team_1
			print("team1",team_1)
			print("team2",team_2)
			points_table_1[team_1]['mat'] += 1
			points_table_1[team_1]['won'] += 1
			points_table_1[team_1]['pts'] += 2

			points_table_1[team_2]['mat'] += 1
			points_table_1[team_2]['lost'] += 1

			#---------------------------------------------------------
			points_table_2 = copy.deepcopy(points_table)
			match_dict_2 = copy.deepcopy(match_dict)

			match_dict_2[str(match_count)]['result'] = team_2

			points_table_2[team_2]['mat'] += 1
			points_table_2[team_2]['won'] += 1
			points_table_2[team_2]['pts'] += 2

			points_table_2[team_1]['mat'] += 1
			points_table_2[team_1]['lost'] += 1

			if(match_count==70):
				point_table_count += 1
				match_futute_list = [str(num) for num in list(range(matches_done+1,70+1))]

				point_table_all[point_table_count] = points_table_1

				res_1 = {key: match_dict_1[key] for key in match_futute_list} 
				#print('-----------')
				#print(res_1['70']['result'])             
				match_dict_all[point_table_count] = res_1

				point_table_count += 1
				point_table_all[point_table_count] = points_table_2
				res_2 = {key: match_dict_2[key] for key in match_futute_list}
				#print(res_2['70']['result'])
				match_dict_all[point_table_count] = res_2
				"""
				print("_____________________________**************************_____________________________________________")
				print(point_table_count)
				print("_________________________________________________________________________________________________")
				print(points_table_1)
				print("_________________________________________________________________________________________________")
				print(points_table_2)
				"""
				return point_table_count,point_table_all,match_dict_all


			break
		match_count += 1

		

	"""
	point_table_count += 1
	point_table_all[point_table_count] = points_table_1
	point_table_count += 1
	point_table_all[point_table_count] = points_table_2
	"""

	point_table_count,point_table_all,match_dict_all = one_match_prediction(points_table_1,match_dict_1,point_table_count,point_table_all,match_dict_all,matches_done)
	point_table_count,point_table_all,match_dict_all = one_match_prediction(points_table_2,match_dict_2,point_table_count,point_table_all,match_dict_all,matches_done)

	return point_table_count,point_table_all,match_dict_all


def point_table_prediction(points_table,match_dict,matches_done):
	point_table_count = 0
	point_table_all = {}
	match_dict_all = {}
	point_table_count,point_table_all,match_dict_all = one_match_prediction(points_table,match_dict,point_table_count,point_table_all,match_dict_all,matches_done)
	print('\n')
	
	#print(point_table_count)
	

	return point_table_all,match_dict_all
	


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
	#print('*******************************')
	#print(point_table_ind)

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
	return point_table_ind


def print_match_results(match,team_short):
	print("\n")
	print(f'    vs         results')
	print("-----------------------")
	for key in match.keys():
		teams = match[key]["teams"]
		result = match[key]["result"]

		str_print2 = team_short[teams[0]]+" vs "+team_short[teams[1]]+"       "+team_short[result]
		print(str_print2)



def print_point_table(pt_ind,team_short):

	print('prediction table')
	print('--------------------')
	print(f'team    mat     won     lost    pts')
	for key in pt_ind.keys():
		team = list(pt_ind[key].keys())[0]
		str_print = team_short[team]+"     "+str(pt_ind[key][team]['mat'])+"       "+str(pt_ind[key][team]['won'])+"       "+str(pt_ind[key][team]['lost'])+"      "+str(pt_ind[key][team]['pts'])
		print(str_print)
		#print(f'{team} - {pt_ind[key][team]['mat']}')
		#print(f'{pt_ind[key][team]} {pt_ind[key][team]['mat']} {pt_ind[key][team]['won']} {pt_ind[key][team]['lost']} {pt_ind[key][team]['pts']}')
	print('--------------------')

def probability_find(team,point_table_all,match_dict_all,team_short):

	count = 0
	playoff_count_without_nrr = 0
	playoff_count_with_nrr = 0
	no_playoffs = 0


	for key in point_table_all.keys():
		#print(key)
		#exit()

		pt_ind = point_table_all[key]

		team_4 = list(pt_ind['4'].keys())[0]
		pts_team_4 = pt_ind['4'][team_4]['pts']

		team_5 = list(pt_ind['5'].keys())[0]
		pts_team_5 = pt_ind['5'][team_5]['pts']

		index = 1
		while(True):
			
			if(team==list(pt_ind[str(index)].keys())[0]):
				
				team_pts = pt_ind[str(index)][team]['pts']
				#print("team_pts",team_pts)
				if(team_pts>pts_team_5):
					playoff_count_without_nrr += 1
					print('****************************************************************************************')

					print_point_table(pt_ind,team_short)
					
					print_match_results(match_dict_all[key],team_short)
					break

				elif(team_pts==pts_team_5 and team_pts==pts_team_4):
					#print('test2')
					
					cache = pt_ind['4']
					pt_ind['4'] = pt_ind[str(index)]
					pt_ind[str(index)] = cache
					#print('****************************************************************************************')
					#print_point_table(pt_ind,team_short)
					#print_match_results(match_dict_all[key],team_short)

					playoff_count_with_nrr += 1
					break
				else:
					no_playoffs += 1

				
			index += 1
			if(index==11):
				break

		count += 1
	print("\n")
	print('-------------------------------')
	print("total possibilites :",count)
	print("cases where nrr is not required - ",playoff_count_without_nrr)
	print("cases where nrr is required - ",playoff_count_with_nrr)
	print("cases where not qualified for playoffs - ",no_playoffs)
	print(f'probablity of {team_short[team]} getting into playoffs - {(playoff_count_without_nrr+playoff_count_with_nrr)/count}')



#----------------------------------------------------------------------------------------------------------
points_table = point_table_scrap()
print(points_table)
#exit()
match_dict,matches_done = schedule_scrap()

print(match_dict)
point_table_all,match_dict_all = point_table_prediction(points_table,match_dict,matches_done)
#exit()
#print('\n')
#print(point_table_all.keys())
#print(point_table_all[1])

point_table_sorted_all = {}
for i in range(len(point_table_all.keys())):
	#print('------------------------')
	#print()
	point_table_sorted = point_table_sort(point_table_all[i+1])
	#print(point_table_sorted)
	#exit()
	point_table_sorted_all[i+1] = point_table_sorted
"""
print('----------------------')
print('\n')
print(match_dict_all['1'])
print('----------------------')
print('\n')
print(match_dict_all['10'])
print('----------------------')
print('\n')
print(match_dict_all['15'])
print('----------------------')
print('\n')
print(match_dict_all['100'])
print('----------------------')
print('\n')
print(match_dict_all['178'])
exit()
#-----------------------------------------------------------------------------------------------------------

print('\n')
print(point_table_sorted_all[1])
print('\n')
print(match_dict_all[1])
print('\n')
print(point_table_sorted_all[10])
print('\n')
print(match_dict_all[10])
"""
json_path = "/home/akash/ashok/ipl/points_table.csv"
with open(json_path, "w") as outfile:
	json.dump(point_table_sorted_all, outfile)

json_path_2 = "/home/akash/ashok/ipl/match_output.csv"
with open(json_path_2, "w") as outfile:
	json.dump(match_dict_all, outfile)

team = "Royal Challengers Bangalore"
#team  = 'Lucknow Super Giants'
#team  = 'Mumbai Indians'
#team  = 'Chennai Super Kings'
#team = 'Sunrisers Hyderabad'
#team = 'Kolkata Knight Riders'
#team = 'Delhi Capitals'
#team = 'Punjab Kings'
#team = 'Rajasthan Royals'

teams = ["Lucknow Super Giants","Gujarat Titans","Rajasthan Royals","Royal Challengers Bangalore","Delhi Capitals",
		"Sunrisers Hyderabad","Punjab Kings","Chennai Super Kings","Kolkata Knight Riders","Mumbai Indians"]

team_short = {"Lucknow Super Giants":"LSG",
			  "Gujarat Titans":"GT",
			  "Rajasthan Royals":"RR",
			  "Royal Challengers Bangalore":"RCB",
			  "Delhi Capitals":"DC",
			  "Sunrisers Hyderabad":"SRH",
			  "Punjab Kings":"PBKS",
			  "Chennai Super Kings":"CSK",
			  "Kolkata Knight Riders":"KKR",
			  "Mumbai Indians":"MI",}



f = open(json_path)
point_table_all = json.load(f)


f = open(json_path_2)
match_dict_all = json.load(f)

probability_find(team,point_table_all,match_dict_all,team_short)
print("done!")