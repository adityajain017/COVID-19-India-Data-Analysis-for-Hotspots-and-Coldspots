import json 
import pandas as pd
import datetime
import math

#importing files ------------------------------------------------------------------------
df_o = pd.read_csv("cases-overall.csv")
df_m = pd.read_csv("cases-month.csv")
df_w = pd.read_csv("cases-week.csv")
#with open('neighbor-districts.json') as f:
#    data1 = json.load(f)

#imporiting and processing json file-----------------------------------------------------------------------------
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
    
#Assigning IDs to the districts --------------------------------------------------------------------    
#data = {}
#for i in sorted(data1):
#    data[i] = sorted(data1[i])

data = neighbour_dict.copy()

#inserting id number to each district
id_count = 101
for i in data:
    data[i].insert(0,str(id_count)) 
    id_count += 1;
    
#replacing district names with their id number
for i in data:
    for j in data[i]:
        for k in data:
            if(j==k):
                index = data[i].index(j)
                data[i].remove(j)
                data[i].insert(index,data[k][0])
                           
#replacing dictionary key names with their id numbers
data2 = {}
for i in data:
    stri = data[i][0]
    data2[stri] = data[i]
    data2[stri].remove(stri)
      
neigh = data2.copy()
#debugging
#with open('sorted_file.json', 'w') as s:
#    json.dump(neigh, s, sort_keys=True, indent=4)
#print(neigh)

#end of IDs assigning---------------------------------------------------------------------------------------------------------

#overall--------------------------------------------------------------------------------
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
  j = str(df_o.iloc[i,0])
  for k in range(len(neigh[j])):
    stre = str(neigh[j][k])
    num+=1
    try:
      sum+= int(res[stre])
    except (KeyError):
      continue
  mean = round(sum / num,2)
  mean_list.append(mean)
      
new_df_o = df_o[['districtid','overallid']]
new_df_o['neighbormean'] = mean_list


#computing Standard deviation
for i in range(len(df_o)):
  st=0.00
  sum =0.00
  num=0
  j = str(df_o.iloc[i,0])
  for k in range(len(neigh[j])):
    stre = str(neigh[j][k])
    num+=1
    try:
      sum+= (int(res[stre]) - int(new_df_o.iloc[i,2]))**2
    except (KeyError):
      continue
  st = round(math.sqrt(sum / num),2)
  st_list.append(st)

new_df_o['neighborstdev'] = st_list
new_df_o.to_csv("neighbor-overall.csv", index = False)
# new_df_o.head(30)

#monthly-------------------------------------------------------------------------------------
#defining lists
mean_list = []
st_list = []
li =[]
li2 =[]
li2 = df_m['cases'].astype(int)
li= df_m['districtid'].astype(str) + df_m['monthid'].astype(str)
#creating dictionary for random fetch of data
res ={li[i]: li2[i] for i in range(len(li))}
res['1012']

#Computing mean
for i in range(len(df_m)):
  mean=0.00
  sum =0
  num=0
  j = str(df_m.iloc[i,0])
  for k in range(len(neigh[j])):
    stre = str(neigh[j][k]) + str(df_m.iloc[i,1])
    num+=1
    try:
      sum+= int(res[stre])
    except (KeyError):
      continue
  mean = round(sum / num,2)
  mean_list.append(mean)
      
new_df_m = df_m[['districtid','monthid']]
new_df_m['neighbormean'] = mean_list

#computing Standard deviation
for i in range(len(df_m)):
  st=0.00
  sum =0.00
  num=0
  j = str(df_m.iloc[i,0])
  for k in range(len(neigh[j])):
    stre = str(neigh[j][k]) + str(df_m.iloc[i,1])
    num+=1
    try:
      sum+= (int(res[stre]) - int(new_df_m.iloc[i,2]))**2
    except (KeyError):
      continue
  st = round(math.sqrt(sum / num),2)
  st_list.append(st)

new_df_m['neighborstdev'] = st_list
new_df_m.to_csv("neighbor-month.csv", index = False)
#new_df_m.head(36)

#weekly-------------------------------------------------------------------------------------
#defining lists
mean_list = []
st_list = []
li =[]
li2 =[]
li2 = df_w['cases'].astype(int)
li= df_w['districtid'].astype(str) + df_w['weekid'].astype(str)
#creating dictionary for random fetch of data
res ={li[i]: li2[i] for i in range(len(li))}
#debugging
# res['1012']

#Computing mean
for i in range(len(df_w)):
  mean=0.00
  sum =0
  num=0
  j = str(df_w.iloc[i,0])
  for k in range(len(neigh[j])):
    stre = str(neigh[j][k]) + str(df_w.iloc[i,1])
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
new_df_w['neighbormean'] = mean_list

#computing Standard deviation
for i in range(len(df_w)):
  st=0.00
  sum =0.00
  num=0
  j = str(df_w.iloc[i,0])
  for k in range(len(neigh[j])):
    stre = str(neigh[j][k]) + str(df_w.iloc[i,1])
    num+=1
    try:
      sum+= (int(res[stre]) - int(new_df_w.iloc[i,2]))**2
    except (KeyError):
      continue
  if (num==0):
    st =0
    st_list.append(mean)
  else:
    st = round(math.sqrt(sum / num),2)
    st_list.append(st)

new_df_w['neighborstdev'] = st_list
new_df_w.to_csv("neighbor-week.csv", index = False)
# new_df_w.head(36)

