import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='root',
    db='ridesharing')
cursor = mydb.cursor()
count=1
csv_data = csv.reader(file('pre.csv'))
for row in csv_data:
	cursor.execute('INSERT INTO cabs(VendorID, pickup_datetime, dropoff_datetime,Pickup_longitude,Pickup_latitude,Dropoff_longitude,Dropoff_latitude,Passenger_count,Trip_distance,Total_amount,Trip_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',row)
#close the connection to the database.
cursor.close()
mydb.commit()
print "Done"
