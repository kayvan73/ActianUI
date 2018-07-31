#!/usr/bin/env python2.7
from time import sleep
import sys

import flightTable_py3_access as flightTb
import videoTable_py3_access as videoTb
import targetTable_py3_access as targetTb


#just to test that the import and the function in that import work
#data = targetTb.select_all()
#print(data)

for i in range(4):
    sleep(20)  #this is just for testing purpose. IRL the target could be seconds away from each other
    print('Target Located!')

    # ========== lat, lng, and vid clip extraction ==============
    GPS = flightTb.get_last()
    currentVidID = videoTb.getLastRecorID()
    assert(type(currentVidID) == 'int')
    # ========================================================

    # =========== Img Recognition and Blob Creations ==============
    img = '../../javascriptUI//heroImages/m' + str(i) + '.jpg'
    imglocation = '/home/pi/Desktop/img' + str(i) + '.jpg'
    imgID = 'img' + str(i)
    realPath = os.path.realpath(imglocation)
    print('the path of the video is: ' + str(realPath))
    blobFile = open(realPath, mode='rb')
    imgBlob = blobFile.read()
    blobFile.close()
    # ========================================================

    targetTb.insertRecord(GPS[1], GPS[2], imgID, imgBlob, currentVidID-1, currentVidID)

    
targetTb.closeTable()    
flightTb.closeTable()
