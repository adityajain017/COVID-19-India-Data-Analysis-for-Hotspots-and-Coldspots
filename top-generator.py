#(15 marks) For every month and overall, find the top-5 hotspot and top-5 coldspot districts using
#the z-score values according to both the neighborhood and state methods.
# The output format is: timeid; method; spot; districtid1; : : : ; districtid5 where method indicates
# the comparison method used (neighborhood/state) and spot indicates hot/cold. Call this
# output file top-time.csv and the script/program to generate this top-generator.sh
# where time is week, month, and overall.
import pandas as pd
import math
import json

#top-overall start------------------------------------------------------------------------------------------------------------------------
#importing files
dfo = pd.read_csv("method-spot-overall.csv")
dfsz = pd.read_csv("zscore-overall.csv")

#creating output dataframe 
output = pd.DataFrame(columns=['overallid','method','spot','districitid1','districitid2','districitid3','districitid4','districitid5'])

#creating dictionaries for zscore fetch
neigh_dict ={}
state_dict = {}
for i , row in dfsz.iterrows():
    neigh_dict[row['districtid']] = row['neighborhoodzscore']
    state_dict[row['districtid']] = row['statezscore']
    

#neighbor-overall start ------------------------------------------------------------------
dfno = dfo[dfo.method == "neighborhood"].copy()
dfno.sort_values(by=['districtid'], inplace = True)
dfno = dfno.reset_index(drop=True)

#Adding statezscore to dffso dataframe----------------------
#dfno['neighborhoodzscore'] = dfsz['neighborhoodzscore']
#Adding zscore attribute
for i , row in dfno.iterrows():
    dfno.loc[i,'neighborhoodzscore'] = neigh_dict[row['districtid']]
    
dfno.sort_values(by=['neighborhoodzscore'], ascending= False, inplace = True)
dk = dfno[dfno.neighborhoodzscore != math.inf]

#computing top districts into lists (spotwise)
hotlist = []
coldlist = []
for i in range(5):
  hotlist.append(dk[dk.spot == "hot"].iloc[i,3])

dfno.sort_values(by=['neighborhoodzscore'], inplace = True)
dk = dfno[dfno.neighborhoodzscore != -math.inf]
for i in range(5):
  coldlist.append(dk[dk.spot == "cold"].iloc[i,3])

#Adding rows to output dataframe
output = output.append(pd.Series(['1', 'neighborhood', 'hotspot', hotlist[0], hotlist[1], hotlist[2], hotlist[3], hotlist[4] ], index=output.columns ), ignore_index=True)
output = output.append(pd.Series(['1', 'neighborhood', 'coldspot', coldlist[0], coldlist[1], coldlist[2], coldlist[3], coldlist[4] ], index=output.columns ), ignore_index=True)
#neighbor-overall end ----------------------------------------------------------------------------------

#state-overall start-----------------------------------------------------------------------------------------------------------
dfsso = dfo[dfo.method == "state"].copy()
dfsso.sort_values(by=['districtid'], inplace = True)
dfsso = dfsso.reset_index(drop=True)

#Adding statezscore to dffso dataframe----------------------
#dfsso['statezscore'] = dfsz['statezscore']
#Adding zscore attribute
for i , row in dfsso.iterrows():
    dfsso.loc[i,'statezscore'] = neigh_dict[row['districtid']]

dfsso.sort_values(by=['statezscore'], ascending= False, inplace = True)
dk = dfsso[dfsso.statezscore != math.inf]

#computing top districts into lists (spotwise)
hotlist = []
coldlist = []
for i in range(5):
  hotlist.append(dk[dk.spot == "hot"].iloc[i,3])

dfsso.sort_values(by=['statezscore'], inplace = True)
dk = dfsso[dfsso.statezscore != -math.inf]
for i in range(5):
  coldlist.append(dk[dk.spot == "cold"].iloc[i,3])

#Adding rows to output dataframe
output = output.append(pd.Series(['1', 'state', 'hotspot', hotlist[0], hotlist[1], hotlist[2], hotlist[3], hotlist[4] ], index=output.columns ), ignore_index=True)
output = output.append(pd.Series(['1', 'state', 'coldspot', coldlist[0], coldlist[1], coldlist[2], coldlist[3], coldlist[4] ], index=output.columns ), ignore_index=True)
#state-overall end -----------------------------------------------------------------------

#sorting output
output.sort_values(by=['method','spot'], inplace = True)
#Exporting output dataframe into top-overall.csv
output.to_csv("top-overall.csv", index = False)
#top-overall ends ---------------------------------------------------------------------------------------------------------------------------

#top-month starts -----------------------------------------------------------------------------------------------------------------------
#importing files
dfm = pd.read_csv("method-spot-month.csv")
dfzm = pd.read_csv("zscore-month.csv")

#creating output dataframe 
month_output = pd.DataFrame(columns=['monthid','method','spot','districitid1','districitid2','districitid3','districitid4','districitid5'])

#neighbor-month start ------------------------------------------------------------------
dfnm = dfm[dfm.method == "neighborhood"].copy()
#dfnm.sort_values(by=['districtid'], inplace = True)
#dfnm = dfnm.reset_index(drop=True)
#Adding neighborhoodzscore to dfnm dataframe----------------------
dfzm['districtid'] = dfzm['districtid'].astype(str)
dfzm['monthid'] = dfzm['monthid'].astype(str)


dictionary ={}
for i, row in dfzm.iterrows():
    dictionary[row['districtid'] + row['monthid']] = row['neighborhoodzscore']

#print(dictionary)
for i, rows in dfnm.iterrows():
    dfnm.loc[i,'neighborhoodzscore'] = dictionary[str(rows['districtid']) + str(rows['monthid'])]

dfnm = dfnm[dfnm.neighborhoodzscore != math.inf] 
dfnm = dfnm[dfnm.neighborhoodzscore != -math.inf]   
for k in range(1,8):
    dk = dfnm[dfnm.monthid == k].copy()
    dkh = dk[dk.spot == "hot"].copy()
    dkh.sort_values(by=['neighborhoodzscore'], ascending= False, inplace = True)
    dkh = dkh.reset_index(drop=True)
    hotlist = []
    coldlist = ["","","","",""]
    for i in range(5):
      hotlist.append(dkh.iloc[i,3])
    
    dkc = dk[dk.spot == "cold"].copy()
    dkc.sort_values(by=['neighborhoodzscore'], inplace = True)
    dkc = dkc.reset_index(drop=True)
    for i in range(len(dkc)):
      coldlist[i] = (dkc.iloc[i,3])
      if(i==4):
            break
    #Adding rows to output dataframe
    month_output = month_output.append(pd.Series([k, 'neighborhood', 'hotspot', hotlist[0], hotlist[1], hotlist[2], hotlist[3], hotlist[4] ], index=month_output.columns ), ignore_index=True)
    month_output = month_output.append(pd.Series([k, 'neighborhood', 'coldspot', coldlist[0], coldlist[1], coldlist[2], coldlist[3], coldlist[4] ], index=month_output.columns ), ignore_index=True)

#print(month_output.head(25))
#month_output.to_csv('month_output.csv', index = False)
#neighbor-month end ------------------------------------------------------------------

#state-month start -----------------------------------------------------------------------------------
dfns = dfm[dfm.method == "state"].copy()
dfns= dfns.reset_index(drop=True)
#print(dfns.head(12))

#Adding statezscore to dfns dataframe----------------------
dictionarys ={}
for i, row in dfzm.iterrows():
    dictionarys[row['districtid'] + row['monthid']] = row['statezscore']

#print(dictionarys)
for i in range(len(dfns)):
    dfns.loc[i,'statezscore'] = dictionarys[str(dfns.loc[i,'districtid']) + str(dfns.loc[i,'monthid'])]

dfns = dfns[dfns.statezscore != math.inf]    
dfns = dfns[dfns.statezscore != -math.inf]    
for k in range(1,8):
    dk = dfns[dfns.monthid == k].copy()
    dkh = dk[dk.spot == "hot"].copy()
    dkh.sort_values(by=['statezscore'], ascending= False, inplace = True)
    dkh = dkh.reset_index(drop=True)
    hotlist = []
    coldlist = ["","","","",""]
    for i in range(5):
      hotlist.append(dkh.iloc[i,3])
    
    dkc = dk[dk.spot == "cold"].copy()
    dkc.sort_values(by=['statezscore'], inplace = True)
    dkc = dkc.reset_index(drop=True)
    for i in range(len(dkc)):
      coldlist[i] = (dkc.iloc[i,3])
      if(i==4):
            break
    #Adding rows to output dataframe
    month_output = month_output.append(pd.Series([k, 'state', 'hotspot', hotlist[0], hotlist[1], hotlist[2], hotlist[3], hotlist[4] ], index=month_output.columns ), ignore_index=True)
    month_output = month_output.append(pd.Series([k, 'state', 'coldspot', coldlist[0], coldlist[1], coldlist[2], coldlist[3], coldlist[4] ], index=month_output.columns ), ignore_index=True)

#print(month_output.head(25))
#state-month end ------------------------------------------------------------------
#sorting output
month_output.sort_values(by=['monthid','method','spot'], inplace = True)
#Exporting month_output dataframe into top-overall.csv
month_output.to_csv("top-month.csv", index = False)
#top-month end -----------------------------------------------------------------------------------------------------------------------

#top-week starts -----------------------------------------------------------------------------------------------------------------------
#importing files
dfw = pd.read_csv("method-spot-week.csv")
dfzw = pd.read_csv("zscore-week.csv")

#creating output dataframe 
week_output = pd.DataFrame(columns=['weekid','method','spot','districitid1','districitid2','districitid3','districitid4','districitid5'])

#neighbor-week start ------------------------------------------------------------------
dfnw = dfw[dfw.method == "neighborhood"].copy()

#Adding neighborhoodzscore to dfnw dataframe----------------------
dfzw['districtid'] = dfzw['districtid'].astype(str)
dfzw['weekid'] = dfzw['weekid'].astype(str)


dictionary1 ={}
for i, row in dfzw.iterrows():
    dictionary1[row['districtid'] + row['weekid']] = row['neighborhoodzscore']

#print(dictionary1)
for i, row in dfnw.iterrows():
    dfnw.loc[i,'neighborhoodzscore'] = dictionary1[str(row['districtid']) + str(row['weekid'])]

dfnw = dfnw[dfnw.neighborhoodzscore != math.inf]    
dfnw = dfnw[dfnw.neighborhoodzscore != -math.inf]    
for k in range(1,26):
    dk = dfnw[dfnw.weekid == k].copy()
    dkh = dk[dk.spot == "hot"].copy()
    dkh.sort_values(by=['neighborhoodzscore'], ascending= False, inplace = True)
    dkh = dkh.reset_index(drop=True)
    hotlist = []
    coldlist = ["","","","",""]
    for i in range(5):
      hotlist.append(dkh.iloc[i,3])
    
    dkc = dk[dk.spot == "cold"].copy()
    dkc.sort_values(by=['neighborhoodzscore'], inplace = True)
    dkc = dkc.reset_index(drop=True)
    for i in range(len(dkc)):
      coldlist[i] = (dkc.iloc[i,3])
      if(i==4):
            break
    #Adding rows to output dataframe
    week_output = week_output.append(pd.Series([k, 'neighborhood', 'hotspot', hotlist[0], hotlist[1], hotlist[2], hotlist[3], hotlist[4] ], index=week_output.columns ), ignore_index=True)
    week_output = week_output.append(pd.Series([k, 'neighborhood', 'coldspot', coldlist[0], coldlist[1], coldlist[2], coldlist[3], coldlist[4] ], index=week_output.columns ), ignore_index=True)

#print(week_output.head(25))
#week_output.to_csv('week_output.csv', index = False)
#neighbor-week end ------------------------------------------------------------------

#state-week start -----------------------------------------------------------------------------------
dfws = dfw[dfw.method == "state"].copy()
dfws= dfws.reset_index(drop=True)
#print(dfws.head(12))

#Adding statezscore to dfns dataframe----------------------
dictionarys2 ={}
for i, row in dfzw.iterrows():
    dictionarys2[row['districtid'] + row['weekid']] = row['statezscore']

#print(dictionarys)
for i in range(len(dfws)):
    dfws.loc[i,'statezscore'] = dictionarys2[str(dfws.loc[i,'districtid']) + str(dfws.loc[i,'weekid'])]

dfws = dfws[dfws.statezscore != math.inf]    
dfws = dfws[dfws.statezscore != -math.inf]    
for k in range(1,26):
    dk = dfws[dfws.weekid == k].copy()
    dkh = dk[dk.spot == "hot"].copy()
    dkh.sort_values(by=['statezscore'], ascending= False, inplace = True)
    dkh = dkh.reset_index(drop=True)
    hotlist = []
    coldlist = ["","","","",""]
    for i in range(5):
      hotlist.append(dkh.iloc[i,3])
    
    dkc = dk[dk.spot == "cold"].copy()
    dkc.sort_values(by=['statezscore'], inplace = True)
    dkc = dkc.reset_index(drop=True)
    for i in range(len(dkc)):
      coldlist[i] = (dkc.iloc[i,3])
      if(i==4):
            break
    #Adding rows to output dataframe
    week_output = week_output.append(pd.Series([k, 'state', 'hotspot', hotlist[0], hotlist[1], hotlist[2], hotlist[3], hotlist[4] ], index=week_output.columns ), ignore_index=True)
    week_output = week_output.append(pd.Series([k, 'state', 'coldspot', coldlist[0], coldlist[1], coldlist[2], coldlist[3], coldlist[4] ], index=week_output.columns ), ignore_index=True)

#print(week_output.head(25))
#neighbor-week end ------------------------------------------------------------------
#sorting output
week_output.sort_values(by=['weekid','method','spot'], inplace = True)
#Exporting month_output dataframe into top-overall.csv
week_output.to_csv("top-week.csv", index = False)
#top-week end -----------------------------------------------------------------------------------------------------------------------


#print(hotlist)
#print(coldlist)





