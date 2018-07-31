#!/usr/bin/env python2.7
#print "Start simulator (SITL)"
#import dronekit_sitl
#sitl = dronekit_sitl.start_default()
#connection_string = sitl.connection_string()
#use the above lines if you want to simulate a connection
#since i am using real pixhawk, i dont want those

# Import DroneKit-Python
from dronekit import connect, VehicleMode
from time import sleep
import os
import sys
#import subprocess #we need to start our imgRec script in the background once connection is established in this script


import flightTable_py2_access as flightTb

print(os.getcwd())
curdir = os.getcwd()
if (curdir == '/home/pi/Desktop/ActianUI/ActianUI/flightAnalysis/psql_fullReport'):
    os.chdir('../../btrieveFiles')
elif (curdir == '/home/pi/Desktop/ActianUI/ActianUI'):
    os.chdir('./btrieveFiles')
else :
    os.chdir('../btrieveFiles')
print(os.getcwd())

#test that you can connect to the table
data = flightTb.select_all_flightData()
print(data)

# Connect to the Vehicle.
connection_string = '/dev/ttyS0'
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, baud=57600, wait_ready=True)

# Get some vehicle attributes (state)
print(" Get some vehicle attribute values:")
print(" Global Location: %s" % vehicle.location.global_frame)
#print(vehicle.location.global_frame.lat) 
#print('testing that its an integer')
#print(1 + vehicle.location.global_frame.lat) 
#print(vehicle.location.global_frame.lon)
#print(vehicle.location.global_frame.alt)

#these are other values from pixhawk you have access to but arent as relevant at the moment
#print " Local Location: %s" % vehicle.location.local_frameprint 
#print " GPS: %s" % vehicle.gps_0
#print " Attitude: %s" % vehicle.attitude
#print " Battery: %s" % vehicle.battery
#print " Last Heartbeat: %s" % vehicle.last_heartbeat
#print " Is Armable?: %s" % vehicle.is_armable
#print " System status: %s" % vehicle.system_status.state
#print " Mode: %s" % vehicle.mode.name    # settable

print( "=======================================") 
print( "Now recroding flight Data" )
print( "=======================================")
#print( "starting imgRec script in background")
#print( "=======================================")
#subprocess.call(['/home/pi/Desktop/flightTests/analyzeImgs.py', '&'])
for i in range(180):
    print ("...................")
    print (" Global Location (relative altitude): %s" % vehicle.location.global_frame)
    flightTb.insertRecord(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon)
    sleep(1) 

# Close vehicle object before exiting script
vehicle.close()
flightTb.closeTable()

# Shut down simulator
#sitl.stop()
print("Completed")
