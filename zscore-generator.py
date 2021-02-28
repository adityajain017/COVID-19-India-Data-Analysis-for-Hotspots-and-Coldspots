import pandas as pd
import math
import json

#importing dataframes from Q2
df_o = pd.read_csv("cases-overall.csv")
df_m = pd.read_csv("cases-month.csv")
df_w = pd.read_csv("cases-week.csv")
#importing dataframes from Q4
dfno = pd.read_csv("neighbor-overall.csv") 
dfso = pd.read_csv("state-overall.csv")
dfnm = pd.read_csv("neighbor-month.csv") 
dfsm = pd.read_csv("state-month.csv")
dfnw = pd.read_csv("neighbor-week.csv") 
dfsw = pd.read_csv("state-week.csv")

#Overall----------------------------------------------------------------------------
#defining lists
mean_list = []
st_list = []
li =[]
li2 =[]
li2 = df_o['cases'].astype(int)
li= df_o['districtid'].astype(str)
#creating dictionary for random fetch of data
res ={li[i]: li2[i] for i in range(len(li))}

#dataframe for zscore
dfzo = dfno.copy()
dfzo['districtid']= dfzo['districtid'].astype(str)
dfzo[['statemean','statestdev']] = dfso[['statemean','statestdev']]

#Calculating Zscore for neigbhor
zslist =[]
for i, rows in dfzo.iterrows():
  if(int(rows['neighborstdev']) == 0):
      zslist.append(int(0))
  else:
    value = (res[str(rows['districtid'])] - int(rows['neighbormean']))/rows['neighborstdev']
    zslist.append(round(value,2))

dfzo['neighborhoodzscore'] = zslist

# Calculating Zscore for state
zslist =[]
for i, rows in dfzo.iterrows():
  if(int(rows['statestdev']) == 0):
      zslist.append(int(0))
  else:
    value = (res[str(rows['districtid'])] - int(rows['statemean']))/rows['statestdev']
    zslist.append(round(value,2))

dfzo['statezscore'] = zslist
#dropping irrelavent columns
dfzo.drop(dfzo.columns[[2,3,4,5]], axis = 1, inplace = True)  
#exporting to csv
dfzo.to_csv("zscore-overall.csv", index = False)
# dfzo.head()

#monthly---------------------------------------------------------------------------------------
#defining lists
mean_list = []
st_list = []
li =[]
li2 =[]
li2 = df_m['cases'].astype(int)
li= df_m['districtid'].astype(str) + df_m['monthid'].astype(str)
#creating dictionary for random fetch of data
res ={li[i]: li2[i] for i in range(len(li))}

#dataframe for zscore
dfzm = dfnm.copy()
dfzm['districtid']= dfzm['districtid'].astype(str)
dfzm[['statemean','statestdev']] = dfsm[['statemean','statestdev']]

#Calculating Zscore for neigbhor
zslist =[]
for i, rows in dfzm.iterrows():
  stre = str(rows['districtid']) + str(rows['monthid'])
  if(int(rows['neighborstdev']) == 0):
      zslist.append(int(0))
  else:
    value = (res[stre] - int(rows['neighbormean']))/rows['neighborstdev']
    zslist.append(round(value,2))

dfzm['neighborhoodzscore'] = zslist

# Calculating Zscore for state
zslist =[]
for i, rows in dfzm.iterrows():
  stre = str(rows['districtid']) + str(rows['monthid'])
  if(int(rows['statestdev']) == 0):
      zslist.append(int(0))
  else:
    value = (res[stre] - int(rows['statemean']))/rows['statestdev']
    zslist.append(round(value,2))

dfzm['statezscore'] = zslist
#dropping irrelavent columns
dfzm.drop(dfzm.columns[[2,3,4,5]], axis = 1, inplace = True)  
#exporting to csv
dfzm.to_csv("zscore-month.csv", index = False)
# dfzm.head()

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

#dataframe for zscore
dfzw = dfnw.copy()
dfzw['districtid']= dfzw['districtid'].astype(str)
dfzw[['statemean','statestdev']] = dfsw[['statemean','statestdev']]

#Calculating Zscore for neigbhor
zslist =[]
for i, rows in dfzw.iterrows():
  stre = str(rows['districtid']) + str(rows['weekid'])
  if(int(rows['neighborstdev']) == 0):
      zslist.append(int(0))
  else:
    value = (res[stre] - int(rows['neighbormean']))/rows['neighborstdev']
    zslist.append(round(value,2))

dfzw['neighborhoodzscore'] = zslist

# Calculating Zscore for state
zslist =[]
for i, rows in dfzw.iterrows():
  stre = str(rows['districtid']) + str(rows['weekid'])
  if(int(rows['statestdev']) == 0):
      zslist.append(int(0))
  else:
    value = (res[stre] - int(rows['statemean']))/rows['statestdev']
    zslist.append(round(value,2))

dfzw['statezscore'] = zslist
#dropping irrelavent columns
dfzw.drop(dfzw.columns[[2,3,4,5]], axis = 1, inplace = True)  
#exporting to csv
dfzw.to_csv("zscore-week.csv", index = False)
dfzo.head()