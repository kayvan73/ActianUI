#!/usr/bin/env python2.7
import os
import sys
from datetime import datetime
from time import strftime
import struct
sys.path.insert(0, '../../swigFiles/swig_py2')  #need these to talk to btrieve2
import btrievePython as btrv
os.chdir('../../btrieveFiles')
btrieveFileName = 'FullFlightReport.mkd'
recordFormat = '<iBdBdBBBBB'
#i = integer (for the IDENTITY, 4bytes)
#B = null byte(goes in between columns, 1byte)
#d = double (8bytes)
#BBH = unsigned short integer +Byte+Byte(for the TIME datatype - look at lindas example for clarification)
recordLength = 27
keyFormat = '<i'


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

    rc = btrieveClient.FileCreate(btrieveFileAttributes, btrieveIndexAttributes, btrieveFileName, btrv.Btrieve.CREATE_MODE_NO_OVERWRITE)
    #print(rc)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)

    rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
    assert(rc == btrv.Btrieve.STATUS_CODE_NO_ERROR)
    
print('File Open Successfull!')


#SELECT * FROM FlightTable.mkd
def select_all():
    selectALL = []
    #id, nullByte, lng, nullByte, lat, nullByte, hourByte, minuteByte, secondByte, time
    #recordFormat = '<iBdBdBBBBB'
    record = struct.pack(recordFormat, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
    print(readLength)
    while (readLength > 0):
        humanReadable_record = (struct.unpack(recordFormat, record))
        readLength = btrieveFile.RecordRetrieveNext(record, 0)
        selectALL.append(humanReadable_record)
    return (selectALL)


def get_last():
    record = struct.pack(recordFormat, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveLast(btrv.Btrieve.INDEX_1, record, 0)
    unpacked_record = struct.unpack(recordFormat, record)
    #print(unpacked_record)
    return (unpacked_record)


def insertRecord(lat, lng):
    time = datetime.now()
    print(time)
    record = struct.pack(recordFormat, 0, 0, lat, 0, lng, 0, 1, time.second, time.minute, time.hour) 
    #PCC interprets the 4bytes of the TIME datayte as PM/AM, sec, min, hour
    rc = btrieveFile.RecordCreate(record)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print(' Insert successful!')
    else:
         print(' Insert failed - status: ', rc)


def closeTable():
    rc = btrieveClient.FileClose(btrieveFile)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print('File closed successful!')
    else:
         print('File close failed - status: ', rc)


if __name__ == '__main__':
     
    #imageLocs = select_all_targetImages()
    #print(imageLocs)
    #insertRecord_flightTable(345, 678)
    flightData = select_all()
    print(flightData)
    #lastRow = get_last() 
    #print(lastRow)
    closeTable()





