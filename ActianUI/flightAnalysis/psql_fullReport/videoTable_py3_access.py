#!/usr/bin/env python3

import base64
import io
#from PIL import Image
import os
import sys
from datetime import datetime
from time import strftime
import struct
import imageio
#import visvis as vv


#I have the below code so that no matter where i run this file 
#it will be able to import the correct files form the correct places
print(os.getcwd())
curdir = os.getcwd()
if (curdir == '/home/pi/Desktop/ActianUI/ActianUI/flightAnalysis/psql_fullReport'):
    sys.path.insert(1, '../../swigFiles/swigFiles_py3')  #need these to talk to btrieve2
    import btrievePython as btrv
    os.chdir('../../btrieveFiles')
elif (curdir == '/home/pi/Desktop/ActianUI/ActianUI'):
    sys.path.insert(1, './swigFiles/swigFiles_py3')  #need these to talk to btrieve2
    import btrievePython as btrv
    os.chdir('./btrieveFiles')
else :
    sys.path.insert(1, '../swigFiles/swigFiles_py3')  #need these to talk to btrieve2
    import btrievePython as btrv
    os.chdir('../btrieveFiles')
print(os.getcwd())


#there are two I terms because the header of the blob files
#is comprised of 2 intergers - one for the offset of the 
#blob from where the record currently is (should be the length of
#the record so that the blob is stored right after the record
#the 2nd integer signifies the size of the blob
#recordFormat = '<iB4s4sBdBd'
#i = integer (for the IDENTITY, 4bytes)
#I = unsigned int
#B = null byte(goes in between columns, 1byte)
#d = double (8bytes)
#s = char

#btrieveFileName = 'VideoRecordings.mkd'
btrieveFileName = 'Videos.mkd'
recordFormat = '<iII'
#the B's in between columns are so the file is SQL compliant
#identity, lat, lng, title, blobOffset, blobSize
recordLength = 12
#the above settings are for when you want to construct entire table in 
#btrieve and then go back into pcc to do ddf building



btrieveClient = btrv.BtrieveClient(0x4232, 0)
assert(btrieveClient != None)

btrieveFile = btrv.BtrieveFile()
assert(btrieveFile != None)

rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)

# Create the Btrieve image file if necessary.
if (rc == btrv.Btrieve.STATUS_CODE_FILE_NOT_FOUND):
    print('creating new table')
    btrieveKeySegment = btrv.BtrieveKeySegment()
    assert(btrieveKeySegment != None)

    rc = btrieveKeySegment.SetField(0, 4, btrv.Btrieve.DATA_TYPE_AUTOINCREMENT)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)

    btrieveIndexAttributes = btrv.BtrieveIndexAttributes()
    assert(btrieveIndexAttributes != None)

    rc = btrieveIndexAttributes.AddKeySegment(btrieveKeySegment)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)

    rc = btrieveIndexAttributes.SetModifiable(False)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)

    btrieveFileAttributes = btrv.BtrieveFileAttributes()
    assert(btrieveFileAttributes != None)

    rc = btrieveFileAttributes.SetFixedRecordLength(recordLength)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)

    rc = btrieveFileAttributes.SetVariableLengthRecordsMode(btrv.Btrieve.VARIABLE_LENGTH_RECORDS_MODE_YES)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)

    rc = btrieveClient.FileCreate(btrieveFileAttributes, btrieveIndexAttributes, btrieveFileName, btrv.Btrieve.CREATE_MODE_NO_OVERWRITE)
    #print(rc)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)

    rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)
    
print('File Open Successfull!')


def select_fixedRecords():
    fixedRecords = []
    #recordFormat = '<iII'
    record = struct.pack(recordFormat, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
    print(readLength)
    while (readLength > 0):
        unpacked_record = (struct.unpack(recordFormat, record))
        readLength = btrieveFile.RecordRetrieveNext(record, 0)
        fixedRecords.append(unpacked_record)
    return (fixedRecords)


def select_range(lowerRange, upperRange):

    maxBlobSize = 6000000
    blobArray = []
    fixedRecords = []
    for i in range(lowerRange, upperRange+1):   #need the +1 othwise python will NOT iterate through upperRange
        record = struct.pack(recordFormat, i, 0, 0) #NOTE the i term in the packing
        rc = btrieveFile.KeyRetrieve(btrv.Btrieve.COMPARISON_EQUAL, btrv.Btrieve.INDEX_1, record)
        #print(rc)
        assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)
        blob = bytes(maxBlobSize)
        rc = btrieveFile.RecordRetrieveChunk(recordLength, maxBlobSize, blob)
        blobArray.append(base64.b64encode(blob))  #NOTE the binary image data NEEDS to be ascii encoded to prevent corruption
        unpacked_record = (struct.unpack(recordFormat, record))
        print(unpacked_record)
        fixedRecords.append(unpacked_record)

    return (blobArray)  #NOTE that i return a dict 



# =============================
# if you are trying to get a specific record based on index
# =============================
def get_row(rowNum):

    record = struct.pack(recordFormat, rowNum, 0, 0)
    rc = btrieveFile.KeyRetrieve(btrv.Btrieve.COMPARISON_EQUAL, btrv.Btrieve.INDEX_1, record)
    print(rc)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)
    unPacked = struct.unpack(recordFormat, record)
    print('the record we are looking at is: ')
    print(' ==================================')
    print(unPacked)
    print(' ==================================')

    maxBlobSize = 6000000
    blob = bytes(maxBlobSize)
    rc = btrieveFile.RecordRetrieveChunk(recordLength, maxBlobSize, blob)
    #print(rc)
    assert(rc >= 0)


    #neither volumen NOR mime are how you read video. use below code instead
    # ========== use below code if you want to write mp4 file to drive ========
    # ======= WARNING - it is SLOW =====================
    #reader = imageio.get_reader(blob, format='mp4')
    #fps = reader.get_meta_data()
    #print(fps)
    #writer=imageio.get_writer('NOBYTES.mp4', fps=5.0)
    #for frame in reader:
    #    print('in loop')
    #    writer.append_data(frame)
    #writer.close()
    # ============================
    
    return ({'fixedRecord': unPacked, 'encodedVideo': base64.b64encode(blob)})  #NOTE that i return a dict 


def insertRecord(vidBlob):
    #realPath = os.path.realpath(imglocation
    #print('the path of the image is: ' + str(realPath))
    #blobFile = open(realPath, mode='rb')
    #blob = blobFile.read()
    #blobFile.close()

    blobSize = len(vidBlob)
    blobOffset = recordLength

    #recordFormat = '<iBdBdB30sBII'
    record = struct.pack(recordFormat, 0, blobOffset, blobSize)
    rc = btrieveFile.RecordCreate(record)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print(' Insert successful!')
    else:
         print(' Insert failed - status: ', rc)

    # Now we want to append the image data
    rc = btrieveFile.RecordAppendChunk(vidBlob)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print(' Append Chunk successful!')
    else:
         print(' Append failed - status: ', rc)
    #closeTable()

def fill_db():
    for i in range(4):
        vidlocation = '/home/pi/Desktop/smallvid' + str(i) + '.mp4'
        realPath = os.path.realpath(vidlocation)
        print('the path of the video is: ' + str(realPath))
        blobFile = open(realPath, mode='rb')
        vidBlob = blobFile.read()
        blobFile.close()
        insertRecord(vidBlob)
    


def closeTable():
    rc = btrieveClient.FileClose(btrieveFile)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print('File closed successful!')
    else:
         print('File close failed - status: ', rc)

# the code below is a total hack. i want to keep all my btrieve files in 
# one PSQL folder, but that means in scripts i have to change dirs to the files
# and then at the end of the script change back ---------- actually why do i have to
# change back? - gonna comment this out for now
#os.chdir('../dataCollection/psql_targetMatches')


if __name__ == '__main__':
    #vidlocation = '/home/pi/Desktop/smallvid0.mp4'
    #vidlocation = '/home/pi/Desktop/smallvid1.mp4'
    #vidlocation = '/home/pi/Desktop/smallvid2.mp4'
    #vidlocation = '/home/pi/Desktop/smallvid3.mp4'
    #realPath = os.path.realpath(vidlocation)
    #print('the path of the video is: ' + str(realPath))
    #blobFile = open(realPath, mode='rb')
    #vidBlob = blobFile.read()
    #blobFile.close()
    #insertRecord(vidBlob)
    fill_db()
    Data = select_fixedRecords()
    print(Data)
    #lastRow = get_last()
    #print(lastRow)
    closeTable()





