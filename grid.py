import csv
import MySQLdb
import json
import urllib2
import requests
import time
import math

start_time = time.clock()
mydb = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='root',
                       db='ridesharing')

#global distance_final
distance_final = 0.0
cursor = mydb.cursor()
cX =-74.254085
cY = 40.487688
gridDict = dict()
m= 2 #218
n= 2 #218
lat_long = []

def getGridID(inputX,inputY):
    gX = int((68*(inputX - cX) / m ))
    gY = int((68*(inputY - cY) / n ))
    #print gX,gY
    gridID = str(gX) +" "+str(gY)
    #print "gridID", gridID
    return gridID



def to_json(inp_list):
    final_dictionary = dict()
    vehicles_dict_list = []
    vehicle_type_dict_list = []
    services_dict_list = []
    vehicle_type_dict_list.append({})
    vehicle_type_dict_list[0]['type_id'] = 'vehicle_type_1'
    vehicle_type_dict_list[0]['profile'] = 'car'
    vehicle_type_dict_list[0]['capacity'] = [3]
    length_val = 10
    if len(inp_list)/3 < 10 and len(inp_list)<10:
        length_val = len(inp_list)
    elif len(inp_list)/3<10 and len(inp_list)>=10:
        length_val = len(inp_list)/3
    for i in range (0,length_val):
        vehicles_dict_list.append({})
        vehicles_dict_list[i]['vehicle_id'] = str(inp_list[i][2])
        vehicles_dict_list[i]['start_address'] = {'location_id':'v ' + str(i+1),'lon':inp_list[i][4],'lat': inp_list[i][5]}
        vehicles_dict_list[i]['type_id'] = vehicle_type_dict_list[0]['type_id']
    for i in range (0,len(inp_list)):
        services_dict_list.append({})
        services_dict_list[i]['id'] =  str(inp_list[i][2])
        services_dict_list[i]['name'] = 'constname'
        services_dict_list[i]['address'] = {'location_id': 'location_id ' + str(i+1), 'lon':inp_list[i][0],'lat':inp_list[i][1]}
        services_dict_list[i]['size'] = [int(str(inp_list[i][3]))]
    final_dictionary['services'] = services_dict_list
    final_dictionary['vehicle_types'] = vehicle_type_dict_list
    final_dictionary['vehicles'] = vehicles_dict_list
    with open('/Users/aravindachanta/Desktop/input.json', 'w') as fp:
        json.dump(final_dictionary, fp)
        return length_val

def addToDict(no,gridID):
    gridDict.setdefault(gridID, [])
    gridDict[gridID].append(no)

def computeAdj(k):
    x,y=k.split(" ")
    x=int(x)
    y=int(y)
    adjList=[str(x-1)+" "+str(y+1),str(x-1)+" "+str(y),str(x-1)+" "+str(y-1),str(x)+" "+str(y+1),str(x)+" "+str(y-1),str(x+1)+" "+str(y+1),str(x+1)+" "+str(y),str(x+1)+" "+str(y-1)]
    #print adjList
    return adjList

def updateDict():
    for k,v in gridDict.items():
        if(len(v)%3 == 1):
            adjList=[]
            adjList = computeAdj(k)
            print adjList
            for eachItem in adjList:
                #print eachItem
                if eachItem in gridDict.keys():
                    if(len(gridDict[eachItem])%3 == 1):
                        gridDict[eachItem].append(v[0])
                        v.remove(v[0])
                        gridDict[k] = v
                        break 



def command_execution():
    url = "https://graphhopper.com/api/1/vrp/optimize?key=697b7a3c-49e7-44db-912e-e475711256bd"
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    r = requests.post(url, data=open('/Users/aravindachanta/Desktop/input.json', 'rb'), headers=headers)
    json_data = r.json()
    job = json_data ['job_id']
    print job
    time.sleep(1)
    url1 = "https://graphhopper.com/api/1/vrp/solution/"+job+"?key=697b7a3c-49e7-44db-912e-e475711256bd"
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    f = requests.get(url1,headers=headers)
    out = f.json()
    with open('/Users/aravindachanta/Desktop/output.json', 'w') as fp:
    	json.dump(out, fp)

def output(length_val):
    global distance_final
    print "helllll"
    with open("/Users/aravindachanta/Desktop/Output.json") as json_file:
    	json_data = json.load(json_file)
    	j = 0
    	no_of_vehicles = len(json_data ['solution']['routes'])
    	while(j<no_of_vehicles):
            i = 0
            aList = []
            length_of_vehicle = len(json_data ['solution']['routes'][j]['activities'])
            distance_final = distance_final + json_data ['solution']['routes'][j]['activities'][length_of_vehicle-2]['distance']
            print "Individual Distance: ", json_data ['solution']['routes'][j]['activities'][length_of_vehicle-2]['distance'] * 0.00062137
            aList.append(json_data['solution']['routes'][j]['vehicle_id'])
            aList.append("picks up ->")
            while (i <= length_of_vehicle-3):
            	temp = json_data ['solution']['routes'][j]['activities'][i+1]['id']
                aList.append(temp)
                i = i+1
                print (aList)
            j = j+1
        length_of_unassigned = len(json_data['solution']['unassigned']['details'])
    for k in range(0,length_of_unassigned):
        aList = []
        aList.append(lat_long[length_val][2])
        length_val+=1
        aList.append(json_data['solution']['unassigned']['details'][k]['id'])
    #print(aList)
    #print "length:", length_of_unassigned
    print "Distance without ridesharing: " ,distance
    print "Total Distance with ride sharing: ", distance_final * 0.00062137
    #print "Cost without ride sharing: ",cost
    #print "Total cost with ride sharing: ", json_data['solution']['costs']


sqlstmt = "SELECT Trip_distance,record_no,Dropoff_latitude, Dropoff_longitude,Passenger_count,Total_amount from cabs where STR_TO_DATE(pickup_datetime,'%y/%d/%m %T') BETWEEN str_to_date('16/5/4 20:00','%y/%d/%m %T') AND str_to_date('16/5/4 20:20','%y/%d/%m %T')";
distance = 0.0
cost = 0.0
try:
    # Execute the SQL command
    cursor.execute(sqlstmt)
    #print "1"
except:
   	print "Error: unable to fecth data"
results = cursor.fetchall()
for row in results:
    distance = distance + float(row[0])
    no = row[1]
    inputY = float(row[2])
    inputX = float(row[3])
    #passenger = row[4]
    cost = cost + float(row[5])
    #print inputX
    #print inputY
    gridID=getGridID(inputX,inputY)
    #print(gridID)
    addToDict(no,gridID)
for k,v in gridDict.items():
    print k,v
updateDict()

i = 1;
for k,v in gridDict.items():
    print k,v
for k,v in gridDict.items():
    lat_long=[]
    if (len(v) != 0):
        for ids in v:
            sqlstmt1 = "SELECT Dropoff_latitude, Dropoff_longitude,Passenger_count,Total_amount, Pickup_latitude,Pickup_longitude from cabs where record_no = "+str(ids) 
            try:
                # Execute the SQL command
                cursor.execute(sqlstmt1)
                #print "1"
            except:
                print "Error: unable to fecth data"
            row1 = cursor.fetchone()
            #print "fdfw", row1
            inputY = float(row1[0])
            inputX = float(row1[1])
            passenger = row1[2]
            pickupY = float(row1[4])
            pickupX = float(row1[5])
            lat_long.append((inputX,inputY,ids,passenger,pickupX,pickupY))
        print "Loop: ",i, k,v
        i+=1
        length_val = to_json(lat_long)
        command_execution()
        output(length_val)
end_time = time.clock()
print "Time for processing: ", end_time - start_time 
