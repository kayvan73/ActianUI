#!/usr/bin/env python3.5
from time import sleep
import sys
import os

import flightTable_py3_access as flightTb  #its in the same folder

curdir = os.getcwd()
print('current dir is: ' + curdir)
print('adding necceasry packages to interpreters path depending on where you are in repo')
if (curdir == '/home/pi/Desktop/ActianUI/ActianUI/flightAnalysis/movidius'):
    print('in movidius')
    #print(os.path.realpath('../fullReport_psql'))
    #print(sys.path)
    sys.path.append('../fullReport_psql')
    import videoTable_py3_access as videoTb
    sys.path.append('../targetMatches_psql')  #need these to talk to btrieve2
    import store_TargetMatches as targetTb
elif (curdir == '/home/pi/Desktop/ActianUI/ActianUI'):
    print('in home folder')
    sys.path.insert(1, './flightAnalysis/psql_fullReport')  #need these to talk to btrieve2
    import videoTable_py3_access as videoTb
    sys.path.insert(1, '../flightAnalysis/psql_targetMatches')  #need these to talk to btrieve2
    import store_TargetMatches as targetTb
print('your cwd is: ' + os.getcwd())


#just to test that the import and the function in that import work
#data = targetTb.select_all()
#print(data)

vidArray = [[1,2], [3,4], [2,3], [1,2]]  #NOTE that each pair has to be 1 digit apart ie CANT do [2,4] or [1,3]
for i in range(4):
    #sleep(20)  #this is just for testing purpose. IRL the target could be seconds away from each other
    sleep(5) 
    print('Target Located!')

    # ========== lat, lng, and vid clip extraction ==============
    GPS = flightTb.get_last()
    currentVidID = videoTb.get_LastRecordID()
    assert(type(currentVidID) == int)
    # ========================================================

    # =========== Img Recognition and Blob Creations ==============
    imglocation = '/home/pi/Desktop/img' + str(i) + '.jpg'
    imgID = 'img' + str(i)
    realPath = os.path.realpath(imglocation)
    print('the path of the video is: ' + str(realPath))
    blobFile = open(realPath, mode='rb')
    imgBlob = blobFile.read()
    blobFile.close()
    # ========================================================

    targetTb.insertRecord(GPS[1], GPS[2], imgID, imgBlob, currentVidID-1, currentVidID, GPS[4], GPS[5], GPS[6])
    print(targetTb.select_fixedRecords())

    
targetTb.closeTable()    
flightTb.closeTable()
