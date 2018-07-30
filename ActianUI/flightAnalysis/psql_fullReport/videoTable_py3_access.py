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



#print(os.getcwd())
#sys.path.insert(1, '../../swigFiles/swigFiles_py3')  #need these to talk to btrieve2
sys.path.insert(1, '../swigFiles/swigFiles_py3')  #need these to talk to btrieve2
import btrievePython as btrv
#os.chdir('../../btrieveFiles')
os.chdir('../btrieveFiles')
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

btrieveFileName = 'VideoRecordings.mkd'
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


def select_all():
    selectALL = []
    #recordFormat = '<iII'
    record = struct.pack(recordFormat, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
    print(readLength)
    while (readLength > 0):
        humanReadable_record = (struct.unpack(recordFormat, record))
        readLength = btrieveFile.RecordRetrieveNext(record, 0)
        selectALL.append(humanReadable_record)
    return (selectALL)


def get_videos():
    record = struct.pack(recordFormat, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
    print(readLength)
    maxBlobSize = 10000000
    blobArray = []
    while (readLength > 0):
        humanReadable_record = (struct.unpack(recordFormat, record))
        print(humanReadable_record)
        readLength = btrieveFile.RecordRetrieveNext(record, 0)
        #print(readLength)
        #selectALL.append(humanReadable_record)
        blob = bytes(maxBlobSize)
        rc = btrieveFile.RecordRetrieveChunk(recordLength, maxBlobSize, blob)
        blobArray.append(base64.b64encode(blob))  #NOTE the binary image data NEEDS to be ascii encoded to prevent corruption
    #print(rc)
    assert(rc >= 0)
    return (blobArray)



def get_last():
    # =============================
    # if you are trying to get a specific record based on index
    identifier=1
    record = struct.pack(recordFormat, identifier, 0, 0)
    rc = btrieveFile.KeyRetrieve(btrv.Btrieve.COMPARISON_EQUAL, btrv.Btrieve.INDEX_1, record)
    print(rc)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)
    unPacked = struct.unpack(recordFormat, record)
    print('the record we are looking at is: ')
    print(' ==================================')
    print(unPacked)
    print(' ==================================')
    # ===================================
    # my method of record retireval
    #record = struct.pack(recordFormat,  0, 0, bytes(8))
    #readLength = btrieveFile.RecordRetrieveLast(btrv.Btrieve.INDEX_1, record, 0)
    #unpacked_record = struct.unpack(recordFormat, record)
    # ===================================

    maxBlobSize = 10000000
    blob = bytes(maxBlobSize)
    rc = btrieveFile.RecordRetrieveChunk(recordLength, maxBlobSize, blob)
    #print(rc)
    assert(rc >= 0)

    print(type(blob))

    #myvol = imageio.volread(blob, format='mp4')
    #savedvid = imageio.volwrite('NOBYTES.mp4', myvol, format='mp4')
    # a volume is NOT a gernal blob of data - CANT use this

    #myvid = imageio.mimread(blob, format='mp4', memtest=False)
    

    # ============================
    # this method works but is slow
    reader = imageio.get_reader(blob, format='mp4')
    #fps = reader.get_meta_data()
    #print(fps)
    writer=imageio.get_writer('NOBYTES.mp4', fps=5.0)
    for frame in reader:
        print('in loop')
        writer.append_data(frame)
    writer.close()
    # ============================
    
    #im = Image.open(io.BytesIO(blob))
    #print(im.format)
    #print(im.size)
    #print(im.mode)
    #im.save('DONT_NEED_BYTES.jpg', 'JPEG')
    return (unPacked)


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
    vidlocation = '/home/pi/Desktop/jsVidTest/myMovie.mp4'
    realPath = os.path.realpath(vidlocation)
    print('the path of the video is: ' + str(realPath))
    blobFile = open(realPath, mode='rb')
    vidBlob = blobFile.read()
    blobFile.close()
    #insertRecord(vidBlob)
    Data = select_all()
    print(Data)
    #lastRow = get_last()
    #print(lastRow)
    closeTable()





