import pandas as pd

data = pd.read_csv('2016_Green_Taxi_Trip_Data.csv',usecols=[0,1,2,5,6,7,8,9,10,18])

jfk = data.loc[(data['Pickup_latitude'] >= 40.5413) & (data['Pickup_latitude']<= 40.7413)&
				(data['Pickup_longitude']>= -73.8781)&(data['Pickup_longitude']<= -73.6781)&

				(data['Trip_distance']>0.3)&(data['Passenger_count']<3)]



jfk['Lpep_dropoff_datetime'] = pd.to_datetime(jfk['Lpep_dropoff_datetime'])
jfk['lpep_pickup_datetime'] = pd.to_datetime(jfk['lpep_pickup_datetime'])

jfk['Trip_time'] = jfk['Lpep_dropoff_datetime'] - jfk['lpep_pickup_datetime']

jfk = jfk.loc[(jfk['Trip_time']>pd.Timedelta('00:02:00'))&(jfk['Trip_time']<pd.Timedelta('05:00:00'))]
jfk.to_csv('pre_processed.csv')
print jfk