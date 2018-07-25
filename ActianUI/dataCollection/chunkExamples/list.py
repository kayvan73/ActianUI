#!/cygdrive/c/Python36/python

#import imageio
import io
import os
import struct
import sys

#sys.path.append("C:\\Program Files\\Actian\\PSQL\\bin")
sys.path.append("/usr/local/psql/swigFiles_py3")
import btrievePython as bp

btrieveFileName = "images.btr"
recordFormat = "<I255s"
recordLength = 259
maxBlobSize = 1024 * 1024
blob = bytes(maxBlobSize)

if (len(sys.argv) != 1):
	sys.exit("Usage: " + os.path.basename(sys.argv[0]))

btrieveClient = bp.BtrieveClient(0x4232, 0)
assert(btrieveClient != None)

btrieveFile = bp.BtrieveFile()
assert(btrieveFile != None)

rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, bp.Btrieve.OPEN_MODE_NORMAL)
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

record = struct.pack(recordFormat, 0, bytes(255))

rc = btrieveFile.RecordRetrieveFirst(bp.Btrieve.INDEX_1, record)

while (rc == recordLength):
    fields = struct.unpack(recordFormat, record)
    print(fields[0], fields[1].decode("utf-8"))
    rc = btrieveFile.RecordRetrieveNext(record)

rc = btrieveClient.FileClose(btrieveFile)
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

