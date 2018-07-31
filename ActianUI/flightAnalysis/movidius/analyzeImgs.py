#!/usr/bin/env python2.7
from time import sleep
import sys


print(os.getcwd())
curdir = os.getcwd()
if (curdir == '/home/pi/Desktop/ActianUI/ActianUI/flightAnalysis/movidius'):
    sys.path.insert(1, '../psql_fullReport')  #need these to talk to btrieve2
    import targetTable_py2_access as targetTb
    import flightTable_py2_access as flightTb
    os.chdir('../../btrieveFiles')
elif (curdir == '/home/pi/Desktop/ActianUI/ActianUI'):
    sys.path.insert(1, './flightAnalysis/psql_fullReport')  #need these to talk to btrieve2
    import targetTable_py2_access as targetTb
    import flightTable_py2_access as flightTb
    os.chdir('./btrieveFiles')
else :
    sys.path.insert(1, '../flightAnalysis/psql_fullReport')  #need these to talk to btrieve2
    import targetTable_py2_access as targetTb
    import flightTable_py2_access as flightTb
    os.chdir('../btrieveFiles')
print(os.getcwd())



#just to test that the import and the function in that import work
#data = targetTb.select_all()
#print(data)

for i in range(4):
    sleep(20)
    print('inserting')
    img = '../../javascriptUI//heroImages/m' + str(i) + '.jpg'
    GPS = flightTb.get_last()
    targetTb.insertRecord(img, GPS[2], GPS[4], GPS[7], GPS[8], GPS[9])

    
targetTb.closeTable()    
flightTb.closeTable()
