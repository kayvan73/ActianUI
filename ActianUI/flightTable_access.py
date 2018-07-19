import os
import sys
from datetime import datetime
from time import strftime
import struct
sys.path.insert(0, '/usr/local/psql/swigFiles')  #need these to talk to btrieve2
import btrievePython as btrv
os.chdir('/usr/local/psql/data/DEMODATA')
btrieveFileName = 'FlightTable.mkd'
recordFormat = '<iBdBdBBBBB'
#i = integer (for the IDENTITY, 4bytes)
#B = null byte(goes in between columns, 1byte)
#d = double (8bytes)
#BBH = unsigned short integer +Byte+Byte(for the TIME datatype - look at lindas example for clarification)
recordLength = 27
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
# Create the file:
rc = btrieveClient.FileCreate(btrieveFileAttributes, btrieveIndexAttributes,
btrieveFileName, btrv.Btrieve.CREATE_MODE_OVERWRITE)
# Allocate a file object:
btrieveFile = btrv.BtrieveFile()
# Open the file:
rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
     print('File open successful!\n')
else:
     print('File open failed - status: ', rc, '\n')


#SELECT * FROM FlightTable.mkd
def select_all_flightData():
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

def insertRecord_flightTable(lat, lng):
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
   flightData = select_all_flightData()
   print(flightData)
   closeTable()





