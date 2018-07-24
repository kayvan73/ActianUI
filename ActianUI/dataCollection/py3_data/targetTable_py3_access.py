import os
import sys
from datetime import datetime
from time import strftime
import struct
sys.path.append('swigFiles/swigFiles_py3')  #need these to talk to btrieve2
import btrievePython as btrv
currentPath = os.getcwd()
#print(currentPath)
os.chdir('/usr/local/psql/data/DEMODATA')


btrieveFileName = 'TargetTable.mkd'
recordFormat = '<iB50sBdBdBBBBB'
#i = integer (for the IDENTITY, 4bytes)
#B = null byte(goes in between columns, 1byte)
#d = double (8bytes)
#s = char
#BBBB = for the TIME datatype byte for sec,time,hour,PM/AM
recordLength = 78
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
    record = struct.pack(recordFormat, 0, 0, ''.ljust(50).encode('UTF-8'), 0, 0, 0, 0, 0, 0, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
    print(readLength)
    while (readLength > 0):
        humanReadable_record = (struct.unpack(recordFormat, record))
        readLength = btrieveFile.RecordRetrieveNext(record, 0)
        selectALL.append(humanReadable_record)
    return (selectALL)


def get_last():
    record = struct.pack(recordFormat,  0, 0, ''.ljust(50).encode('UTF-8'), 0, 0, 0, 0, 0, 0, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveLast(btrv.Btrieve.INDEX_1, record, 0)
    unpacked_record = struct.unpack(recordFormat, record)
    #print(unpacked_record)
    return (unpacked_record)

def insertRecord(imglocation, lat, lng, hour, minute, sec):
    time = datetime.now()
    print(time)
    record = struct.pack(recordFormat, 0, 0, imglocation.ljust(50).encode('UTF-8'), 0, lat, 0, lng, 0, 0, hour, minute, sec)
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

# ============================
os.chdir(currentPath) 
# ===========================
#this is a real hack. to access the psql db's, i need to 
#chnage directory. sys.path.append / sys.path.isnert only works on importing python
#modules, not other files. thus, after im done, i have to change the path back to orignal


if __name__ == '__main__':
    #insertRecord(345, 678)
    #Data = select_all()
    #print(Data)
    lastRow = get_last()
    print(lastRow)
    closeTable()





