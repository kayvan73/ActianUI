import os
import sys
import struct
sys.path.insert(0, '/usr/local/psql/btrieveTests')
import btrievePython as btrv
os.chdir('/usr/local/psql/data/DEMODATA')


#SELECT * FROM TargetData.mkd
def select_all_targetData():
    btrieveFileName = 'TargetData.mkd'
    recordFormat = '<iB50sBdBd'
    recordLength = 73
    keyFormat = '<i'
    btrieveClient = btrv.BtrieveClient(0x4232, 0)
    btrieveFile = btrv.BtrieveFile()
    
    rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
         print('File open successful!\n')
    else:
         print('File open failed - status: ', rc, '\n')


    selectALL = []
    record = struct.pack(recordFormat, 0, 0, ''.ljust(50).encode('UTF-8'), 0, 0, 0, 0)
    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
    print(readLength)
    while (readLength > 0):
        humanReadable_record = (struct.unpack(recordFormat, record))
        readLength = btrieveFile.RecordRetrieveNext(record, 0)
        selectALL.append(humanReadable_record)
    return (selectALL)


##SELECT * FROM targetImages.mkd
#def select_all_targetImages():
#    btrieveFileName = 'TargetImages.mkd'
#    recordFormat = '<iB50s'
#    recordLength = 55
#    keyFormat = '<i'
#    btrieveClient = btrv.BtrieveClient(0x4232, 0)
#    btrieveFile = btrv.BtrieveFile()
#    
#    rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
#    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
#         print('File open successful!\n')
#    else:
#         print('File open failed - status: ', rc, '\n')
#
#
#    selectALL = []
#    record = struct.pack(recordFormat, 0, 0, ' '.ljust(50).encode('UTF-8'))
#    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
#    print(readLength)
#    while (readLength > 0):
#        humanReadable_record = (struct.unpack(recordFormat, record))
#        readLength = btrieveFile.RecordRetrieveNext(record, 0)
#        selectALL.append(humanReadable_record)
#    return (selectALL)
#
#
##SELECT * FROM targetCoordinates.mkd
#def select_all_targetGPS():
#    btrieveFileName = 'TargetGPS.mkd'
#    recordFormat = '<iBdBd'
#    recordLength = 22
#    keyFormat = '<i'
#    btrieveClient = btrv.BtrieveClient(0x4232, 0)
#    btrieveFile = btrv.BtrieveFile()
#    
#    rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
#    if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
#         print('File open successful!\n')
#    else:
#         print('File open failed - status: ', rc, '\n')
#
#
#    selectALL = []
#    record = struct.pack(recordFormat, 0, 0, 0, 0, 0)
#    readLength = btrieveFile.RecordRetrieveFirst(btrv.Btrieve.INDEX_1, record, 0)
#    print(readLength)
#    while (readLength > 0):
#        humanReadable_record = (struct.unpack(recordFormat, record))
#        readLength = btrieveFile.RecordRetrieveNext(record, 0)
#        selectALL.append(humanReadable_record)
#    return (selectALL)


if __name__ == '__main__':
   #imageLocs = select_all_targetImages()
   #print(imageLocs)
   flightData = select_all_targetData()
   print(flightData)





