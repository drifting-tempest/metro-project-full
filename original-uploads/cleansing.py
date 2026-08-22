#goal- Check if two sta input exist and if it is in teh same line
##import json
##fh=open("odpt_Railway.json",encoding="utf-8")
##data= json.load(fh)
##for rail in data:
##    for item in rail["odpt:stationOrder"]:
##        titctype=item["odpt:stationTitle"]
##        print({titctype['en']},({titctype['ja']}))

##import json# shows file list and dic names
##
### Load your file
##with open('odpt_Railway.json', 'r', encoding='utf-8') as f:
##    data = json.load(f)
##
### 1. Print the type of the main object
##print(f"Top level is a: {type(data)}") 
##
### 2. Look at the keys of the first item
##first_item = data[0]
##print(f"The first dictionary has these keys: {list(first_item.keys())}")
##
### 3. Check the type of a specific field
##print(f"The type of 'odpt:stationOrder' is: {type(first_item['odpt:stationOrder'])}")

""" 
import json #make the dictionary
x=[]
with open('C:\\Users\\ssr\\Desktop\\S.J\\Metro\\dataset\\odpt_Railway.json', encoding='utf-8') as f:
    data = json.load(f)

for i in data:
    titctype=i["odpt:railwayTitle"]
    print({titctype['en']})
f.close() """

##the=[]   
##for rail in data:
##    print(rail["odpt:railwayTitle"][5])
##        #print(["odpt:stationTitle"])
##    for item in rail["odpt:stationOrder"]:
##        x=(item["odpt:stationTitle"]['en'])
##        the.append(x)
##        print(the)

import json     #prints the final list of sta. line wise
fh = open("dataset/odpt_Railway.json", encoding="utf-8")
data= json.load(fh)

for railway in data:
    station_names = []
    for station in railway["odpt:stationOrder"]:
        station_names.append(station["odpt:stationTitle"]["en"])
    #print(station_names)
print(railway["odpt:stationOrder"])