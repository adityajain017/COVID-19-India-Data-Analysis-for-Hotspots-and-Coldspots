import pandas as pd
import json
import datetime
import math

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
raw.loc[raw['Detected State']== "Assam",'Detected District'] = "Assam"

#renaming the duplicate districts in raw
#renaming the duplicate districts in raw
raw.loc[raw['Detected District'] == "Aurangabad", 'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Bilaspur",'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Pratapgarh",'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Hamirpur",'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Balrampur",'Detected District'] = raw['Detected District'] + raw['Detected State']
raw.loc[raw['Detected District']=="Bijapur",'Detected District'] = raw['Detected District'] + raw['Detected State']

#Dropping Columns
raw.drop(raw.columns[[0,1,2,4,5,6,7,9,10]], axis=1, inplace = True)
raw.drop(raw.iloc[:, 2:12], inplace = True, axis = 1) 
raw.columns =['Date', 'District','cases']

#Changing Data type to date
raw['Date'] = pd.to_datetime(raw['Date'], format='%d/%m/%Y')

#Removing rows before 15th March 2020
raw = raw[(raw.Date>"14/03/2020" )& (raw.Date<"26/04/2020")]

#Grouping them to get total cases w.r.t to date and district
draw =pd.DataFrame({'Confirmed' : raw.groupby(['Date','District']).sum()['cases']}).reset_index() 

#Sorting by date
draw.sort_values(by=['Date'],inplace=True)
#raw files process end ------------------------------------------------------------------------------------------------

#processing data from district.csv ---------------------------------------------------------------------------------------------
#Importing data from district.csv present in other csv sheet section at https://api.covid19india.org/documentation/csv/
dframe = pd.read_csv("districts.csv") 

#Correcting district names for Telangana and Goa in district.csv data
dframe.loc[dframe['State']== "Telangana",'District'] = "Telangana"
dframe.loc[dframe['State']== "Goa",'District'] = "Goa"
dframe.loc[dframe['State']== "Assam",'District'] = "Assam"

#dropping columns
dframe.drop(dframe.columns[[4,5,6,7]], axis=1, inplace = True)
dframe['Date'] = pd.to_datetime(dframe['Date'], format='%Y-%m-%d')
dframe = dframe[dframe.Date<"2020/09/06"]

#renaming the duplicate districts in dframe
dframe.loc[dframe['District']=="Aurangabad",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Bilaspur",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Pratapgarh",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Hamirpur",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Balrampur",'District'] = dframe['District'] + dframe['State']
dframe.loc[dframe['District']=="Bijapur",'District'] = dframe['District'] + dframe['State']

#dropping state column
dframe.drop('State',axis=1, inplace = True)

#Group By statement to correct multiple Goa district on same date (due to merging)
dframe =pd.DataFrame({'Confirmed' : dframe.groupby(['Date','District']).sum()['Confirmed']}).reset_index() 

#Sorting
dframe.sort_values(by=['District','Date'], inplace=True)

#fixing cummalative data to normal data
dframe.loc[dframe['District'] == dframe['District'].shift(), 'newnumber'] = (dframe.Confirmed - dframe.Confirmed.shift())
dframe.loc[dframe.newnumber.isna(),'newnumber'] = dframe.Confirmed
dframe['Confirmed'] = dframe['newnumber']
dframe.drop("newnumber", axis =1, inplace = True)

# Merging raw data and district file data 
dframe = pd.concat([draw,dframe])
dframe.sort_values(by=['District','Date'], inplace=True)

#Correcting the cummalative data for 26 April 2020 after mergig with raw data
draw_sum = pd.DataFrame({'Confirmed' : draw.groupby('District').sum().Confirmed}).reset_index() 

for i in range(len(dframe)):
  if(dframe.iat[i,0] == datetime.date(2020, 4, 26)):
    for j in range(len(draw_sum)):
      if (dframe.iloc[i,1] == draw_sum.iloc[j,0]):
        dframe.iat[i,2] = dframe.iat[i,2] - draw_sum.iat[j,1]
        break
  
#Assigning District id-------------------------------------------------------------------------------------
#Removing Rows where District is Unknown
dframe = dframe[dframe.District!="Unknown"]

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

#debugging - Will print the name of districts that were not matched with neighbor_district data
#dframe[dframe.districtid=="NA"].groupby('District').count()

#Removing NA from district id:
dframe = dframe[dframe.districtid!="NA"]

#debugging - Will Return total number of cases between 15 March and 5 Sept after cleaning
# dframe.Confirmed.sum()
#--------------------------------------------------------------------------------------------------
#Calculating Overall Results
overall_df = pd.DataFrame({'cases' : dframe.groupby('districtid').sum()['Confirmed']}).reset_index()

overall_df['overallid'] = 1
overall_df = overall_df[["districtid", "overallid", "cases"]]

#Exporting to CSV
overall_df.to_csv('cases-overall.csv', index = False)
# overall_df.count()

#-----------------------------------------------------------------------------------------------------
#Calculating monthly results
m_df = dframe.copy()
m_df['monthid'] = pd.DatetimeIndex(dframe['Date']).month
m_df['monthid'] = m_df['monthid']-2
w_df = m_df.copy()
m_df = pd.DataFrame({'cases' : m_df.groupby(['monthid','districtid']).sum()['Confirmed']}).reset_index()
m_df = m_df[['districtid', 'monthid', 'cases']]
m_df.sort_values(by=['districtid','monthid'], inplace = True)

#Exporting to CSV
m_df.to_csv('cases-month.csv', index = False) 
# m_df.head()

#------------------------------------------------------------------------------------------------------
#Calculating weekly results
w_df.sort_values(by=['Date'], inplace=True)
w_df['day'] = pd.DatetimeIndex(w_df['Date']).day
w_df['Date'] = pd.to_datetime(w_df['Date'], errors='coerce')
w_df['weekid'] = w_df['Date'].dt.week - 11
w_df['weekday'] = w_df['Date'].dt.dayofweek 

w_df = w_df.reset_index()
w_df.loc[w_df['weekday'] ==6, 'weekid'] = w_df['weekid'] +1
w_df.drop('index',axis = 1, inplace = True)
w_df = pd.DataFrame({'cases' : w_df.groupby(['weekid','districtid']).sum()['Confirmed']}).reset_index()

w_df = w_df[['districtid', 'weekid', 'cases']]
w_df.sort_values(by=['districtid','weekid'], inplace = True)

#Exporting to CSV
w_df.to_csv('cases-week.csv', index = False) 
# w_df.head(25)
#------------------------------------------------------------------------------------------------------
# dframe.dtypes  
# dframe.head()
# dframe.tail()
# dframe[dframe.districtid=="NA"].groupby('District').count()
    