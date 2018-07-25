#!/usr/bin/env python2.7
import io
from PIL import Image
import os
import sys
from datetime import datetime
from time import strftime
import struct
#print(os.getcwd())
sys.path.insert(1, '../../swigFiles/swigFiles_py2')  #need these to talk to btrieve2
import btrievePython as btrv
os.chdir('../../PSQL')
#btrieveFileName = 'BigBoi.mkd'
btrieveFileName = 'ImgTest.mkd'
recordFormat = '<iB8s'
#recordFormat = '<iB4s4sBdBd'
#i = integer (for the IDENTITY, 4bytes)
#B = null byte(goes in between columns, 1byte)
#d = double (8bytes)
#s = char
recordLength = 13
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


# Allocate a file object:
btrieveFile = btrv.BtrieveFile()
# Open the file:
rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
     print('File open successful!\n')
else:
     print('File open failed - status: ', rc, '\n')


def get_last():
    # =============================
    # if you are trying to get a specific record based on index
    #identifier=1
    #record = struct.pack(recordFormat, identifier, 0, bytes(8))
    #rc = btrieveFile.KeyRetrieve(btrv.Btrieve.COMPARISON_EQUAL, btrv.Btrieve.INDEX_1, record)
    #assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)
    # ==================================
    # my method of record retireval
    record = struct.pack(recordFormat,  0, 0, bytes(8))
    readLength = btrieveFile.RecordRetrieveLast(btrv.Btrieve.INDEX_1, record, 0)
    #unpacked_record = struct.unpack(recordFormat, record)
    # ===================================

    maxBlobSize = 1024 * 1024
    blob = bytes(maxBlobSize)
    rc = btrieveFile.RecordRetrieveChunk(recordLength, maxBlobSize, blob)
    assert(rc >= 0)
    
    bytesob = io.BytesIO(blob)
    im = Image.open(bytesob)
    print(im.format)
    print(im.size)
    print(im.mode)
    im.save('DONT_NEED_BYTES.jpg', 'JPEG')
    return (unpacked_record)


def insertRecord(imglocation, lat, lng):
    record = struct.pack(recordFormat, 0, 0, bytes(8))
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
    #insertRecord('../javascriptUI/heroImages/m1.jpg', 345, 678)
    #Data = select_all()
    #print(Data)
    lastRow = get_last()
    print(lastRow)
    closeTable()





