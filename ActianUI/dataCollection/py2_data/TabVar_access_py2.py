#!/usr/bin/env python2.7
import io
from PIL import Image
import os
import sys
from datetime import datetime
from time import strftime
import struct
print(os.getcwd())
sys.path.insert(1, '../../swigFiles/swigFiles_py2')  #need these to talk to btrieve2
import btrievePython as btrv
os.chdir('../../PSQL')
btrieveFileName = 'BigBoi.mkd'
recordFormat = '<iB8sBdBd'
#i = integer (for the IDENTITY, 4bytes)
#B = null byte(goes in between columns, 1byte)
#d = double (8bytes)
#s = char
#BBBB = for the TIME datatype byte for sec,time,hour,PM/AM
recordLength = 31
keyFormat = '<i'


# Create a session:
btrieveClient = btrv.BtrieveClient(0x4232, 0) # ServiceAgent=B2
# Specify FileAttributes for the new file:
btrieveFileAttributes = btrv.BtrieveFileAttributes()
rc = btrieveFileAttributes.SetFixedRecordLength(recordLength)
# Specify Key 0 as an autoinc:
btrieveKeySegment = btrv.BtrieveKeySegment()
rc = btrieveKeySegment.SetField(0, 4, btrv.Btrieve.DATA_TYPE_AUTOINCREMENT)
btrieveIndexAttributes = btrv.BtrieveIndexAttributes()
rc = btrieveIndexAttributes.AddKeySegment(btrieveKeySegment)
rc = btrieveIndexAttributes.SetDuplicateMode(False)
rc = btrieveIndexAttributes.SetModifiable(True)

#================================
# These 2 lines below "Create the file:" will completly delte and and recreate the table
# ONLY use them if you are looking to clear the table
#===============================
# Create the file:
#rc = btrieveClient.FileCreate(btrieveFileAttributes, btrieveIndexAttributes,
#btrieveFileName, btrv.Btrieve.CREATE_MODE_OVERWRITE)

# Allocate a file object:
btrieveFile = btrv.BtrieveFile()
# Open the file:
rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
     print('File open successful!\n')
else:
     print('File open failed - status: ', rc, '\n')


#SELECT * FROM FlightTable.mkd
def select_all():
    selectALL = []
    #recordFormat = '<iBs50BdBdBBBBB'
    record = struct.pack(recordFormat, 0, 0, bytes(8), 0, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
    print(readLength)
    while (readLength > 0):
        humanReadable_record = (struct.unpack(recordFormat, record))
        readLength = btrieveFile.RecordRetrieveNext(record, 0)
        selectALL.append(humanReadable_record)
    #closeTable()
    return (selectALL)


def get_last():
    #record = struct.pack(recordFormat,  0, 0, bytes(8), 0, 0, 0, 0)
    identifier=5
    record = struct.pack(recordFormat, identifier, 0, bytes(8), 0, 0, 0, 0)
    rc = btrieveFile.KeyRetrieve(btrv.Btrieve.COMPARISON_EQUAL, btrv.Btrieve.INDEX_1, record)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)
    #readLength = btrieveFile.RecordRetrieveLast(btrv.Btrieve.INDEX_1, record, 0)
    unpacked_record = struct.unpack(recordFormat, record)

    maxBlobSize = 1024 * 1024
    blob = bytes(maxBlobSize)
    rc = btrieveFile.RecordRetrieveChunk(recordLength, maxBlobSize, blob)
    assert(rc >= 0)
    
    bytesob = io.BytesIO(blob)
    im = Image.open(bytesob)
    #print(im.format)
    #print(im.size)
    #print(im.mode)
    im.save('DONT_NEED_BYTES.jpg', 'JPEG')
    return (unpacked_record)


def insertRecord(imglocation, lat, lng):
    #time = datetime.now()
    #print(time)
    record = struct.pack(recordFormat, 0, 0, bytes(8), 0, lat, 0, lng)
    #PCC interprets the 4bytes of the TIME datayte as PM/AM, sec, min, hour
    rc = btrieveFile.RecordCreate(record)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print(' Insert successful!')
    else:
         print(' Insert failed - status: ', rc)
    # Now we want to append the image data
    realPath = os.path.realpath(imglocation)
    print(realPath)
    blobFile = open(realPath, mode='rb')
    blob = blobFile.read()
    blobFile.close()
    rc = btrieveFile.RecordAppendChunk(blob)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print(' Append Chunk successful!')
    else:
         print(' Append failed - status: ', rc)
         #closeTable()
         #break
    #closeTable()
    


def closeTable():
    rc = btrieveClient.FileClose(btrieveFile)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print('File closed successful!')
    else:
         print('File close failed - status: ', rc)


if __name__ == '__main__':
    insertRecord('../javascriptUI/heroImages/m1.jpg', 345, 678)
    #Data = select_all()
    #print(Data)
    lastRow = get_last()
    print(lastRow)
    closeTable()





