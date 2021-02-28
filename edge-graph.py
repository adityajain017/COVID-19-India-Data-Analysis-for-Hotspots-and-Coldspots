import json
import csv

with open('neighbor-districts-modified.json') as f:
    data1 = json.load(f)

#to replace if error in program    
#with open('sorted_file.json', 'w') as s:
#    json.dump(data, s, sort_keys=True, indent=4)
#
#with open('sorted_file.json') as f:
#    data = json.load(f)

data = {}

for i in sorted(data1):
    data[i] = sorted(data1[i])

#debugging    
#with open('sorted_file.json', 'w') as s:
#    json.dump(data, s, sort_keys=True, indent=4)
    
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
      
#print(data2)
#list having edge pairs
edge_set = []  
#loop to obtain edge pairs
for i in data2: 
    for j in data2[i]:
#            stri = "(" + i + "," + j + ")"
        edge_set.append((i,j))
        



#print(edge_set)
#with open('data.json' , 'w') as f:
#    json.dump(edge_set,f)

#exporting edge_set list to csv file
li = ["1,23","45,6"]
# writing the data into the file 
with open('edge-graph.csv', 'w+', newline ='') as f:     
    w = csv.writer(f) 
    w.writerows(edge_set) 
#    for i in edge_set:
 #       w.writerow([i])     
