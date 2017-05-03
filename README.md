# RideSharing
Pre-processing.py is a script which was used to only cosider the usefull column and data from the big csv file downloaded from the internet.

pre.csv is the new csv file obtained from the pre-processing.py script which only contains the required data.

python.py is the script using mySqldb which is a python module to enter all the csv data into a preconstructed database.

grid.py is the main python script for accesing values from db on a time basis and contatcting graph hopper and finally implementing our algorithm to produce a graph which gives the distance with ride sharing and without ridesharing.

sqlcreate.txt contains the sql create table synatx with which we created the table
