import pandas as pd
import json
import datetime
import math

#importing and processing json file-----------------------------------------------------------------------------
e = {}
with open('neighbor-districts-modified.json') as f:
    d = json.load(f)

for key in d.keys():
    string = key
    for i in range(len(string)):
        if (string[i] == '/'):
            index =i
            break
    string = string[0:index]    
    # string = string.replace("_district", "")
    # string = string.replace("_", " ")
    e[string] = d[key]

for i in e:
    for j in e[i]:
        string = j
        for k in range(len(string)):
            if (string[k] == '/'):
                index =k
                break
        string = string[0:index]    
        # string = string.replace("_district", "")
        # string = string.replace("_", " ")
        val_index = e[i].index(j)
        e[i].remove(j)
        e[i].insert(val_index,string)    

neighbour_dict = {}        
for i in sorted(e):
    neighbour_dict[i] = sorted(e[i])      
#print (neighbour_dict)    

# with open('m.json', 'w') as s:
#     json.dump(neighbour_dict, s, sort_keys=True, indent=4)

id_count = 101
for i in neighbour_dict:
    neighbour_dict[i].insert(0,id_count) 
    id_count += 1;

# json file editing complete------------------------------------------------------------------------

#Data From api.covid19india.org -----------------------------------------------------------------------------
#Importing raw_data1 and raw_data2 and concating them
raw1 = pd.read_csv("raw_data1.csv") 
raw2 = pd.read_csv("raw_data2.csv") 
raw = pd.concat([raw1, raw2])
raw = raw.reset_index()

#Correcting District Names as per the new merged districts - Telangana, Delhi, Mumbai
raw.loc[raw['Detected State']== "Telangana",'Detected District'] = "Telangana"
raw.loc[raw['Detected State']== "Delhi",'Detected District'] = "Delhi"
raw.loc[raw['Detected State']== "Mumbai",'Detected District'] = "Mumbai"
raw.loc[raw['Detected State']== "Goa",'Detected District'] = "Goa"

#renaming the duplicate districts in raw
raw.loc[raw['Detected District'] == "Aurangabad", 'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Bilaspur",'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Pratapgarh",'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Hamirpur",'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Balrampur",'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Bijapur",'Detected District'] = raw['Detected District'] + raw['Detected State']

#Dropping Columns
raw.drop(raw.columns[[0,1,2,3,4,5,6,7,10]], axis=1, inplace = True)
raw.drop(raw.iloc[:, 2:13], inplace = True, axis = 1) 
raw.columns =['District','State']

#Group By statement
raw = pd.DataFrame({'count' : raw.groupby( [ 'District','State'] ).size()}).reset_index()
#lists for renaming the states 
#lis = ['Andaman and Nicobar Islands',	'Andhra Pradesh',	'Arunachal Pradesh',	'Assam',	'Bihar',	'Chandigarh',	'Chhattisgarh',	'Dadra and Nagar Haveli',	'Daman and Diu',	'Delhi',	'Goa',	'Gujarat',	'Haryana', 'Himachal Pradesh',	'Jammu and Kashmir', 'Jharkhand',	'Karnataka',	'Kerala',	'Lakshadweep',	'Madhya Pradesh',	'Maharashtra',	'Manipur',	'Meghalaya',	'Mizoram',	'Nagaland',	'Odisha',	'Puducherry',	'Punjab',	'Rajasthan',	'Sikkim',	'Tamil Nadu',	'Telangana',	'Tripura',	'Uttar Pradesh',	'Uttarakhand',	'West Bengal']
#lic = ['AN',	'AP',	'AR',	'AS',	'BR',	'CH',	'CT',	'DN',	'DD',	'DL',	'GA',	'GJ',	'HR',	'HP',	'JK',	'JH',	'KA',	'KL',	'LD',	'MP',	'MH',	'MN',	'ML',	'MZ',	'NL',	'OR',	'PY',	'PB',	'RJ',	'SK',	'TN',	'TG',	'TR',	'UP',	'UT',	'WB']
#full =[]
#dictst = { lic[i] : lis[i] for i in range(len(lis))}
#dictst['LA'] = "Ladakh"
## replacing statecodes with statenames
#for i, row in raw.iterrows():
#  string = row['State']
#  if string in dictst:
#    full.append(dictst[string])
#  else: 
#    full.append("NA")
#raw['State'] = full
raw = raw[raw.State != 'NA']

raw = raw[['State', 'District']]

#-------------------------------------------------------------------------------------------------------------------------------------

#Importing data from district.csv present in other csv sheet section at https://api.covid19india.org/documentation/csv/
dframe = pd.read_csv("districts.csv") 

#renaming the duplicate districts in dframe
dframe.loc[dframe['District']=="Aurangabad",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Bilaspur",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Pratapgarh",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Hamirpur",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Balrampur",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Bijapur",'District'] = dframe['District'] + dframe['State']

#dropping columns
dframe.drop(dframe.columns[[0,3,4,5,6,7]], axis=1, inplace = True)
dframe = pd.DataFrame({'c' : dframe.groupby(['State','District']).size()}).reset_index()
dframe = dframe[['State','District']]
dframe = pd.concat([raw, dframe]) 
dframe = pd.DataFrame({'c' : dframe.groupby(['State','District']).size()}).reset_index()

#Data Cleaning---------------------------------------------------------------

#Removing Rows where District is Unknown
dframe = dframe[dframe.District!="Unknown"]
# len(data[data.District=="Unknown"])

#Computing District Ids
count = 101
d_id =[]
for i in dframe['District']:
  flag =1
  for j in neighbour_dict:
    if (i.lower()==j):
      d_id.append(neighbour_dict[j][0])
      flag =0
      break
  if (flag): 
      d_id.append("NA")

#Adding attribute district id
dframe['districtid'] = d_id

# Removing data that can't be cleaned
dframe = dframe[dframe.districtid!="NA"]
# dframe.sort_values(by=['District'], inplace = True)
dframe.drop(dframe.columns[[1, 2]], axis = 1, inplace = True)  
neigh = neighbour_dict
std = dframe.copy()

#Creating Dictionaries dict1 and dict2
from collections import defaultdict

dict1 = defaultdict(list)
count =0
for i, row in std.iterrows():
  dict1[row['State']].append(row['districtid'])
# print(dict1)

dict2 = {}
count =0
for i, row in std.iterrows():
  dict2[row['districtid']] = (row['State'])
# print(dict2)

#importing dataframes from Q2
df_o = pd.read_csv("cases-overall.csv")
df_m = pd.read_csv("cases-month.csv")
df_w = pd.read_csv("cases-week.csv")

#overall------------------------------------------------------------------------
#Adding State Name
lis =[]
for i, row in df_o.iterrows():
  try:
    lis.append(dict2[row['districtid']])
  except (KeyError):
    lis.append("NA")  
    continue
df_o['State'] = lis

#defining lists
mean_list = []
st_list = []
li =[]
li2 =[]
li2 = df_o['cases'].astype(int)
li= df_o['districtid'].astype(str)
#creating dictionary for random fetch of data
res ={li[i]: li2[i] for i in range(len(li))}
# df_o['districtid'] = pd.to_numeric(df_o['districtid'])

#Computing mean
for i in range(len(df_o)):
  mean=0.00
  sum =0
  num=0
  j = str(df_o.iat[i,3])
  for k in range(len(dict1[j])):
    stre = str(dict1[j][k])
    if (stre != str(df_o.iat[i,0])):
        num+=1
        try:
          sum+= int(res[stre])
        except (KeyError):
          continue
  if (num ==0):
    mean =0
    mean_list.append(mean)
  else:
    mean = round(sum / num,2)
    mean_list.append(mean)
      
new_df_o = df_o[['districtid','overallid']]
new_df_o['statemean'] = mean_list


#computing Standard deviation
for i in range(len(df_o)):
  st=0.00
  sum =0.00
  num=0
  j = str(df_o.iat[i,3])
  for k in range(len(dict1[j])):
    stre = str(dict1[j][k])
    if (stre != str(df_o.iat[i,0])):
        num+=1
        try:
          sum+= (int(res[stre]) - int(new_df_o.iat[i,2]))**2
        except (KeyError):
          continue
  if (num ==0):
    st =0
    st_list.append(st)
  else:
    st = round(math.sqrt(sum / num),2)
    st_list.append(st)
  

new_df_o['statestdev'] = st_list
new_df_o.to_csv("state-overall.csv", index = False)
# df_o[df_o.State == "NA"]
# new_df_o.head(35)

#monthly-------------------------------------------------------------------------------------
#Adding State Name
lis =[]
for i, row in df_m.iterrows():
  try:
    lis.append(dict2[row['districtid']])
  except (KeyError):
    lis.append("NA")  
    continue
df_m['State'] = lis

#defining lists
mean_list = []
st_list = []
li =[]
li2 =[]
li2 = df_m['cases'].astype(int)
li= df_m['State'].astype(str) +df_m['districtid'].astype(str) + df_m['monthid'].astype(str)
#creating dictionary for random fetch of data
res ={li[i]: li2[i] for i in range(len(li))}
# res['1012']

#Computing mean
for i in range(len(df_m)):
  mean=0.00
  sum =0
  num=0
  j = str(df_m.iat[i,3])
  for k in range(len(dict1[j])):
    if (str(dict1[j][k]) != str(df_m.iat[i,0])):
        stre = str(df_m.iat[i,3]) + str(dict1[j][k]) + str(df_m.iat[i,1])
        num+=1
        try:
          sum+= int(res[stre])
        except (KeyError):
          continue
  if (num ==0):
    mean =0
    mean_list.append(mean)
  else:
    mean = round(sum / num,2)
    mean_list.append(mean)
      
new_df_m = df_m[['districtid','monthid']]
new_df_m['statemean'] = mean_list

#computing Standard deviation
for i in range(len(df_m)):
  st=0.00
  sum =0.00
  num=0
  j = str(df_m.iat[i,3])
  for k in range(len(dict1[j])):
    if (str(dict1[j][k]) != str(df_m.iat[i,0])):
        stre = str(df_m.iat[i,3]) + str(dict1[j][k]) + str(df_m.iat[i,1])
        num+=1
        try:
          sum+= (int(res[stre]) - int(new_df_m.iat[i,2]))**2
        except (KeyError):
          continue
  if (num ==0):
    st =0
    st_list.append(st)
  else:
    st = round(math.sqrt(sum / num),2)
    st_list.append(st)

new_df_m['statestdev'] = st_list
new_df_m.to_csv("state-month.csv", index = False)
# new_df_m.head(36)

#weekly-------------------------------------------------------------------------------------
#Adding State Name
lis =[]
for i, row in df_w.iterrows():
  try:
    lis.append(dict2[row['districtid']])
  except (KeyError):
    lis.append("NA")  
    continue
df_w['State'] = lis

#defining lists
mean_list = []
st_list = []
li =[]
li2 =[]
li2 = df_w['cases'].astype(int)
li= df_w['State'].astype(str) + df_w['districtid'].astype(str) + df_w['weekid'].astype(str)
#creating dictionary for random fetch of data
res ={li[i]: li2[i] for i in range(len(li))}
#debugging
# res['1012']

#Computing mean
for i in range(len(df_w)):
  mean=0.00
  sum =0
  num=0
  j = str(df_w.iat[i,3])
  for k in range(len(dict1[j])):
    if (str(dict1[j][k]) != str(df_w.iat[i,0])):
        stre = str(df_w.iat[i,3]) + str(dict1[j][k]) + str(df_w.iat[i,1])
        num+=1
        try:
          sum+= int(res[stre])
        except (KeyError):
          continue
  if (num==0):
    mean =0
    mean_list.append(mean)
  else:
    mean = round(sum / num,2)
    mean_list.append(mean)
      
new_df_w = df_w[['districtid','weekid']]
new_df_w['statemean'] = mean_list

#computing Standard deviation
for i in range(len(df_w)):
  st=0.00
  sum =0.00
  num=0
  j = str(df_w.iat[i,3])
  for k in range(len(dict1[j])):
    if (str(dict1[j][k]) != str(df_w.iat[i,0])):
        stre = str(df_w.iat[i,3]) + str(dict1[j][k]) + str(df_w.iat[i,1])
        num+=1
        try:
          sum+= (int(res[stre]) - int(new_df_w.iat[i,2]))**2
        except (KeyError):
          continue
  if (num==0):
    st =0
    st_list.append(st)
  else:
    st = round(math.sqrt(sum / num),2)
    st_list.append(st)

new_df_w['statestdev'] = st_list
new_df_w.to_csv("state-week.csv", index = False)
# new_df_w.head(36)
