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

json_path_2 = "/home/akash/ashok/ipl/match_output.csv"
f = open(json_path_2)
match_dict_all = json.load(f)

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
#exit()

def print_match_results(match,team_short):
	print("\n")
	print(f'    vs         results')
	print("-----------------------")
	for key in match.keys():
		teams = match[key]["teams"]
		result = match[key]["result"]
		print(teams)
		print(result)
		#exit()
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

	match_dict_favour  = {}
	favour_cases = 0

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
					

					print('****************************************************************************************')

					print_point_table(pt_ind,team_short)
					
					print_match_results(match_dict_all[key],team_short)

					playoff_count_without_nrr += 1
					favour_cases += 1

					match_dict_favour[favour_cases] = match_dict_all[key]

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
					favour_cases += 1
					match_dict_favour[favour_cases] = match_dict_all[key]
					break
				else:
					no_playoffs += 1

				
			index += 1
			if(index==11):
				break

		count += 1


	print("total possibilites :",count)
	print("cases where nrr is not required - ",playoff_count_without_nrr)
	print("cases where nrr is required - ",playoff_count_with_nrr)
	print("cases where not qualified for playoffs - ",no_playoffs)
	print(f'probablity of {team} getting into playoffs - {(playoff_count_without_nrr+playoff_count_with_nrr)/count}')
	
	return match_dict_favour




#team = "Royal Challengers Bangalore"
#team  = 'Lucknow Super Giants'
#team  = 'Mumbai Indians'
#team  = 'Chennai Super Kings'
#team = 'Sunrisers Hyderabad'
#team = 'Kolkata Knight Riders'
#team = 'Delhi Capitals'
team = 'Punjab Kings'
#team = 'Rajasthan Royals'
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
match_dict_favour = probability_find(team,point_table_all,match_dict_all,team_short)
print("------------------------------")
#print(match_dict_favour)
#print(len(match_dict_favour.keys()))
print(team)
#exit()
def print_match_results_merge(match,team_short):
	print("\n")
	print(f'    vs         results')
	print("-----------------------")
	for key in match.keys():
		teams = match[key]["teams"]
		result = match[key]["result"]
		#print(teams)
		#print(result)
		#exit()
		if(len(result)==1):
			str_print2 = team_short[teams[0]]+" vs "+team_short[teams[1]]+"       "+result[0]
		else:
			str_print2 = team_short[teams[0]]+" vs "+team_short[teams[1]]+"       "+result[0]+" or "+ result[1]
		print(str_print2)



def result_merge(match_dict_favour,team_short):
	merge_dict = match_dict_favour[1]
	#print(merge_dict)
	

	for key1 in match_dict_favour.keys():

		match_ind = match_dict_favour[key1]
		for key in match_ind.keys():
			#print(type(merge_dict[key]["result"]))
			#print(isinstance(merge_dict[key]["result"]	, str))
			teams = match_ind[key]["teams"]
			result = match_ind[key]["result"]
			"""
			print("-------------------")
			print("teams",teams)
			print("result",result)
			print("merge_dict[key]_result_",merge_dict[key]["result"])
			"""
			if(isinstance(merge_dict[key]["result"]	, str)):

				#print('str')
				merge_dict[key]["result"] = []
				merge_dict[key]["result"].append(team_short[result])

			elif(team_short[result] not in merge_dict[key]["result"]):
				merge_dict[key]["result"].append(team_short[result])
			#print("merge_dict[key]_result_3",merge_dict[key]["result"])
		#exit()
	print(merge_dict)
	print_match_results_merge(merge_dict,team_short)
	return merge_dict

def team_check(match_dict_favour,team_short):
	print('------------------------------------------------------')
	for key in match_dict_favour.keys():
		print(key)
		if(match_dict_favour[key]['70']['result']=='Sunrisers Hyderabad'):
			print('----------')
			print(match_dict_favour[key])
			#exit()


team_check(match_dict_favour,team_short)

#merge_dict = result_merge(match_dict_favour,team_short)