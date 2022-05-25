import json
"""    
# Data to be written
dictionary ={
    "name" : "sathiyajith",
    "rollno" : 56,
    "cgpa" : 8.6,
    "phonenumber" : "9976770500"
}

json_path = "/home/akash/ashok/ipl/test.csv"
with open(json_path, "w") as outfile:
    json.dump(dictionary, outfile)
"""
json_path = "/home/akash/ashok/ipl/points_table.csv"
f = open(json_path)

data = json.load(f)

print(data['1'])