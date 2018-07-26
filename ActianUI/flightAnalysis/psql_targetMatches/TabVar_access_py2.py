#!/usr/bin/env python2.7


# =================================
#this is last working version to extract blobs
# =================================


import io
from PIL import Image
import os
import sys
from datetime import datetime
from time import strftime
import struct
#print(os.getcwd())
sys.path.insert(1, '../../swigFiles/swigFiles_py3')  #need these to talk to btrieve2
import btrievePython as btrv
#os.chdir('../../PSQL')
#btrieveFileName = 'BigBoi.mkd'
#btrieveFileName = '../../PSQL/TomsLesson.mkd'
#recordFormat = '<iBII'
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

#start session (ie start up the db server)
#instantiate file
#try to open file
#if not open, cthen create file and add
#       1) index segment and attributes
#       2) file attributes
#       3) file name
# (make sure there are assertions at each step)
#now open file
#btrieveFileName = 'TomsLesson2.btr'
btrieveFileName = 'RealPathTest.mkd'
recordFormat = '<III'
recordLength = 12
#the above settings are for when you want to construct entire table in 
#btrieve and then go back into pcc to do ddf building

#recordFormat = '<IBII'
#recordLength = 13
#this is for if you wan


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


def select_all():
    selectALL = []
    #recordFormat = '<iBs50BdBdBBBBB'
    #record = struct.pack(recordFormat, 0, 0, 0, 0)
    record = struct.pack(recordFormat, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
    print(readLength)
    while (readLength > 0):
        humanReadable_record = (struct.unpack(recordFormat, record))
        readLength = btrieveFile.RecordRetrieveNext(record, 0)
        selectALL.append(humanReadable_record)
    return (selectALL)


def get_last():
    # =============================
    # if you are trying to get a specific record based on index
    identifier=1
    #record = struct.pack(recordFormat, identifier, 0, 0, 0)
    record = struct.pack(recordFormat, identifier, 0, 0)
    #record = struct.pack(recordFormat, identifier, 0, recordLength, 82248)
    rc = btrieveFile.KeyRetrieve(btrv.Btrieve.COMPARISON_EQUAL, btrv.Btrieve.INDEX_1, record)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)
    #unPacked = struct.unpack(recordFormat, record)
    #print('the record we are looking at is: ')
    #print('===============')
    #print('===============')
    # ==================================
    # my method of record retireval
    #record = struct.pack(recordFormat,  0, 0, bytes(8))
    #readLength = btrieveFile.RecordRetrieveLast(btrv.Btrieve.INDEX_1, record, 0)
    #unpacked_record = struct.unpack(recordFormat, record)
    # ===================================

    maxBlobSize = 1024 * 1024
    blob = bytes(maxBlobSize)
    rc = btrieveFile.RecordRetrieveChunk(recordLength, maxBlobSize, blob)
    print(rc)
    assert(rc >= 0)
    
    #bytesob = io.BytesIO(blob)
    im = Image.open(io.BytesIO(blob))
    print(im.format)
    print(im.size)
    print(im.mode)
    #im.save('DONT_NEED_BYTES.jpg', 'JPEG')
    #return (unpacked_record)


def insertRecord(imglocation):
    realPath = os.path.realpath(imglocation)
    print('the path of the image is: ' + str(realPath))
    blobFile = open(realPath, mode='rb')
    blob = blobFile.read()
    blobFile.close()

    blobSize = len(blob)
    #blobOffset = recordLength

    #record = struct.pack(recordFormat, 0, 0, recordLength, blobSize)
    record = struct.pack(recordFormat, 0, recordLength, blobSize)
    rc = btrieveFile.RecordCreate(record)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print(' Insert successful!')
    else:
         print(' Insert failed - status: ', rc)

    # Now we want to append the image data
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

# the code below is a total hack. i want to keep all my btrieve files in 
# one PSQL folder, but that means in scripts i have to change dirs to the files
# and then at the end of the script change back ---------- actually why do i have to
# change back? - gonna comment this out for now
#os.chdir('../dataCollection/psql_targetMatches')


if __name__ == '__main__':
    os.chdir('../../PSQL')
    #insertRecord('../../javascriptUI/heroImages/m1.jpg')
    Data = select_all()
    print(Data)
    #lastRow = get_last()
    #print(lastRow)
    closeTable()




