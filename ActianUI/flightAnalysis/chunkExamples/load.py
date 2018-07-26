#!/usr/bin/env python2.7

import os
import struct
import sys
import io

#sys.path.append("C:\\Program Files\\Actian\\PSQL\\bin")
sys.path.append("/usr/local/psql/swigFiles_py3")
import btrievePython as bp

btrieveFileName = "images.btr"
recordFormat = "<I255s"
recordLength = 259

if (len(sys.argv) != 2):
	sys.exit("Usage: " + os.path.basename(sys.argv[0]) + " fileName")

fileName = sys.argv[1]

btrieveClient = bp.BtrieveClient(0x4232, 0)
assert(btrieveClient != None)

btrieveFile = bp.BtrieveFile()
assert(btrieveFile != None)

rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, bp.Btrieve.OPEN_MODE_NORMAL)

# Create the Btrieve image file if necessary.
if (rc == bp.Btrieve.STATUS_CODE_FILE_NOT_FOUND):
    btrieveKeySegment = bp.BtrieveKeySegment()
    assert(btrieveKeySegment != None)

    rc = btrieveKeySegment.SetField(0, 4, bp.Btrieve.DATA_TYPE_AUTOINCREMENT)
    assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

    btrieveIndexAttributes = bp.BtrieveIndexAttributes()
    assert(btrieveIndexAttributes != None)

    rc = btrieveIndexAttributes.AddKeySegment(btrieveKeySegment)
    assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

    rc = btrieveIndexAttributes.SetModifiable(False)
    assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

    btrieveFileAttributes = bp.BtrieveFileAttributes()
    assert(btrieveFileAttributes != None)

    rc = btrieveFileAttributes.SetFixedRecordLength(recordLength)
    assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

    rc = btrieveFileAttributes.SetVariableLengthRecordsMode(bp.Btrieve.VARIABLE_LENGTH_RECORDS_MODE_YES)
    assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

    rc = btrieveClient.FileCreate(btrieveFileAttributes, btrieveIndexAttributes, btrieveFileName, bp.Btrieve.CREATE_MODE_NO_OVERWRITE)
    assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)
    #print(rc)

    rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, bp.Btrieve.OPEN_MODE_NORMAL)
    assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

# Btrieve image file is open.

rc = btrieveClient.TransactionBegin(bp.Btrieve.TRANSACTION_MODE_EXCLUSIVE)
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

record = struct.pack(recordFormat, 0, fileName.encode("utf-8"))

rc = btrieveFile.RecordCreate(record)
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

realPath = os.path.realpath(fileName)
blobFile = open(realPath, mode="rb")
print(type(blobFile))
#blobBytes = io.BytesIO(realPath)
#print(type(blobBytes))
blob = blobFile.read()
blobFile.close()

#rc = btrieveFile.RecordAppendChunk(blob)
#assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

rc = btrieveClient.TransactionEnd()
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

rc = btrieveClient.FileClose(btrieveFile)
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)
