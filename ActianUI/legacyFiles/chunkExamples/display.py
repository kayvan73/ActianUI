#!/cygdrive/c/Python36/python

import base64
#import imageio
import io
import os
import struct
import sys
#import visvis
#from matplotlib import pyplot
#from matplotlib import image
from PIL import Image

#sys.path.append("C:\\Program Files\\Actian\\PSQL\\bin")
sys.path.append('/usr/local/psql/swigFiles_py3')
import btrievePython as bp

btrieveFileName = "images.btr"
recordFormat = "<I255s"
recordLength = 259
maxBlobSize = 1024 * 1024
blob = bytes(maxBlobSize)

if (len(sys.argv) != 2):
	sys.exit("Usage: " + os.path.basename(sys.argv[0]) + " identifier")

identifier = int(sys.argv[1])

btrieveClient = bp.BtrieveClient(0x4232, 0)
assert(btrieveClient != None)

btrieveFile = bp.BtrieveFile()
assert(btrieveFile != None)

rc = btrieveClient.FileOpen(btrieveFile, btrieveFileName, None, bp.Btrieve.OPEN_MODE_NORMAL)
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

record = struct.pack(recordFormat, identifier, bytes(255))

rc = btrieveFile.KeyRetrieve(bp.Btrieve.COMPARISON_EQUAL, bp.Btrieve.INDEX_1, record)
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)
# ==================================
# my method of record retireval
#record = struct.pack(recordFormat,  0, bytes(255))
#readLength = btrieveFile.RecordRetrieveLast(bp.Btrieve.INDEX_1, record, 0)
# ===================================

rc = btrieveFile.RecordRetrieveChunk(recordLength, maxBlobSize, blob)
assert(rc >= 0)

#  This was micheals implementation for reading the bytes and displaying the image
#  i trie using this approach but got nasty dependcy erros. tried to solve those by building stuff from 
#  source, but that also failed
#application = visvis.use()
#visvis.title("Identifier" + " = " + str(identifier))
#imageFile = io.BytesIO(blob)
#reader = imageio.get_reader(imageFile)
#axes = visvis.axis("off")
#clim = (0, 255)
#texture = visvis.imshow(reader.get_next_data(), axes=axes, clim=clim)
#application.Run()

#BYTESOBJ = io.BytesIO(blob)
#val = bytesob.getvalue()
#print(type(val))
#print(type(bytesob))
#im = Image.open(BYTESOBJ)
im = Image.open(io.BytesIO(blob))
#fileblob = open(blob, 'rb')
#blober = fileblob.read()
#print(type(blobber))
#im = Image.open(blobber)
print(type(im))
#bytesblob = io.BytesIO(blob)
#im = Image.open(filelob)
print(im.format)
print(im.size)
print(im.mode)
#im.save('DONT_NEED_BYTES.jpg', 'JPEG')

rc = btrieveClient.FileClose(btrieveFile)
assert(rc == bp.Btrieve.STATUS_CODE_NO_ERROR)

