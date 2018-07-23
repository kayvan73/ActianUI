import os
import sys
import struct
import btrievePython as btrv
btrieveFileName = "Test_Table.mkd"
recordFormat = "<iB32sBBBH"
recordLength = 42
keyFormat = "<i"
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
if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
     print('\nFile "' + btrieveFileName + '" created successfully!')
else:
     print('\nFile "' + btrieveFileName + '" not created; error: ', rc)
# Allocate a file object:
btrieveFile = btrv.BtrieveFile()
# Open the file:
rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, btrv.Btrieve.OPEN_MODE_NORMAL)
if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
     print('File open successful!\n')
else:
     print('File open failed - status: ', rc, '\n')
# Insert records:
iinserting = True
while iinserting:
     new_name = input('Insert name (Q to quit): ' )
     if new_name.lower() == 'q':
          iinserting = False
     else:
          record = struct.pack(recordFormat, 0, 0, new_name.ljust(32).encode('UTF-8'), 0, 22, 1, 2018)
          rc = btrieveFile.RecordCreate(record)
          if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
               print(' Insert successful!')
          else:
               print(' Insert failed - status: ', rc)
# Get Record count:
btrieveFileInfo = btrv.BtrieveFileInformation()
rc = btrv.BtrieveFile.GetInformation(btrieveFile, btrieveFileInfo)
print('\nTotal Records inserted =', btrieveFileInfo.GetRecordCount())
# Close the file:
rc = btrieveClient.FileClose(btrieveFile)
if (rc == btrv.Btrieve.STATUS_CODE_NO_ERROR):
     print('File closed successful!')
else:
     print('File close failed - status: ', rc)
