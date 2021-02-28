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

#dataframe for hotspot/coldspot
dfzo = dfno.copy()
dfzo['districtid']= dfzo['districtid'].astype(str)
dfzo[['statemean','statestdev']] = dfso[['statemean','statestdev']]

#Calculating spot for neigbhor
dfzon = dfzo.copy()
dfzon['method'] = "neighborhood"
zslist =[]
for i, rows in dfzon.iterrows():
  if (res[str(rows['districtid'])] > (int(rows['neighbormean']) + rows['neighborstdev'])):
    zslist.append("hot")
  elif(res[str(rows['districtid'])] < (int(rows['neighbormean']) - rows['neighborstdev'])):
    zslist.append("cold")
  else:
    zslist.append("NA")

dfzon['spot'] = zslist
dfzon = dfzon[dfzon.spot!="NA"]
#dropping irrelavent columns
dfzon.drop(dfzon.columns[[2,3,4,5]], axis = 1, inplace = True)  
dfzon = dfzon[['overallid','method','spot', 'districtid']]
dfzon.sort_values(by=['districtid'], inplace=True)
#exporting to csv
#dfzon.to_csv("neighborhood-spot-overall.csv", index = False)
# dfzon.head()

#Calculating spot for state
dfzos = dfzo.copy()
dfzos['method'] = "state"
zslist =[]
for i, rows in dfzos.iterrows():
  if (res[str(rows['districtid'])] > (int(rows['statemean']) + rows['statestdev'])):
    zslist.append("hot")
  elif(res[str(rows['districtid'])] < (int(rows['statemean']) - rows['statestdev'])):
    zslist.append("cold")
  else:
    zslist.append("NA")

dfzos['spot'] = zslist
dfzos = dfzos[dfzos.spot!="NA"]
#dropping irrelavent columns
dfzos.drop(dfzos.columns[[2,3,4,5]], axis = 1, inplace = True)  
dfzos = dfzos[['overallid','method','spot', 'districtid']]
dfzos.sort_values(by=['districtid'], inplace=True)

#Merging both neighbor and state dataframes
dfzos = pd.concat([dfzon, dfzos])
#sorting output file
dfzos.sort_values(by=['method','spot'], inplace = True)
#exporting to csv
dfzos.to_csv("method-spot-overall.csv", index = False)
# dfzos.head()

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

#dataframe for calculating spot
dfzm = dfnm.copy()
dfzm['districtid']= dfzm['districtid'].astype(str)
dfzm[['statemean','statestdev']] = dfsm[['statemean','statestdev']]

#Calculating spot for neigbhor
dfzmn = dfzm.copy()
dfzmn['method'] = "neighborhood"
zslist =[]
for i, rows in dfzmn.iterrows():
  stre = str(rows['districtid']) + str(rows['monthid'])
  if (res[stre] > (int(rows['neighbormean']) + rows['neighborstdev'])):
    zslist.append("hot")
  elif(res[stre] < (int(rows['neighbormean']) - rows['neighborstdev'])):
    zslist.append("cold")
  else:
    zslist.append("NA")

dfzmn['spot'] = zslist
dfzmn = dfzmn[dfzmn.spot!="NA"]
#dropping irrelavent columns
dfzmn.drop(dfzmn.columns[[2,3,4,5]], axis = 1, inplace = True)  
dfzmn = dfzmn[['monthid','method','spot', 'districtid']]
#exporting to csv
#dfzmn.to_csv("neighborhood-spot-month.csv", index = False)
# dfzmn.head(35)

#Calculating spot for state
dfzms = dfzm.copy()
dfzms['method'] = "state"
zslist =[]
for i, rows in dfzms.iterrows():
  stre = str(rows['districtid']) + str(rows['monthid'])
  if (res[stre] > (int(rows['statemean']) + rows['statestdev'])):
    zslist.append("hot")
  elif(res[stre] < (int(rows['statemean']) - rows['statestdev'])):
    zslist.append("cold")
  else:
    zslist.append("NA")

dfzms['spot'] = zslist
dfzms = dfzms[dfzms.spot!="NA"]
#dropping irrelavent columns
dfzms.drop(dfzms.columns[[2,3,4,5]], axis = 1, inplace = True)  
dfzms = dfzms[['monthid','method','spot', 'districtid']]

#Merging both neighbor and state dataframes
dfzms = pd.concat([dfzmn, dfzms])
#sorting output file
dfzms.sort_values(by=['monthid','method','spot'], inplace = True)
#exporting to csv
dfzms.to_csv("method-spot-month.csv", index = False)
#dfzms.head(35)

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

#dataframe for calcualting spot
dfzw = dfnw.copy()
dfzw['districtid']= dfzw['districtid'].astype(str)
dfzw[['statemean','statestdev']] = dfsw[['statemean','statestdev']]

#Calculating spot for neigbhor
dfzwn = dfzw.copy()
dfzwn['method'] = "neighborhood"
zslist =[]
for i, rows in dfzwn.iterrows():
  stre = str(rows['districtid']) + str(rows['weekid'])
  if (res[stre] > (int(rows['neighbormean']) + rows['neighborstdev'])):
    zslist.append("hot")
  elif(res[stre] < (int(rows['neighbormean']) - rows['neighborstdev'])):
    zslist.append("cold")
  else:
    zslist.append("NA")

dfzwn['spot'] = zslist
dfzwn = dfzwn[dfzwn.spot!="NA"]
#dropping irrelavent columns
dfzwn.drop(dfzwn.columns[[2,3,4,5]], axis = 1, inplace = True)  
dfzwn = dfzwn[['weekid','method','spot', 'districtid']]
#exporting to csv
#dfzwn.to_csv("neighborhood-spot-week.csv", index = False)
dfzwn.head(35)

#Calculating spot for state
dfzws = dfzw.copy()
dfzws['method'] = "state"
zslist =[]
for i, rows in dfzws.iterrows():
  stre = str(rows['districtid']) + str(rows['weekid'])
  if (res[stre] > (int(rows['statemean']) + rows['statestdev'])):
    zslist.append("hot")
  elif(res[stre] < (int(rows['statemean']) - rows['statestdev'])):
    zslist.append("cold")
  else:
    zslist.append("NA")

dfzws['spot'] = zslist
dfzws = dfzws[dfzws.spot!="NA"]
#dropping irrelavent columns
dfzws.drop(dfzws.columns[[2,3,4,5]], axis = 1, inplace = True)  
dfzws = dfzws[['weekid','method','spot', 'districtid']]

#Merging both neighbor and state dataframes
dfzws = pd.concat([dfzwn, dfzws])

#sorting output file
dfzws.sort_values(by=['weekid','method','spot'], inplace = True)
#exporting to csv
dfzws.to_csv("method-spot-week.csv", index = False)
dfzws.head(35)