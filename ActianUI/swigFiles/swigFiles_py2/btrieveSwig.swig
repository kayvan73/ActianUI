////////////////////////////////////////////////////////////
//
// Copyright (C) 2016 - Actian Corp.
//
////////////////////////////////////////////////////////////

%apply (char *STRING, int LENGTH) { (char *chunk, int chunkSize) };
%apply (char *STRING, int LENGTH) { (char *key, int keySize) };
%apply (char *STRING, int LENGTH) { (char *record, int recordSize) };
%apply (char *STRING, int LENGTH) { (const char *chunk, int chunkLength) };
%apply (char *STRING, int LENGTH) { (const char *constant, int constantLength) };
%apply (char *STRING, int LENGTH) { (const char *key, int keyLength) };
%apply (char *STRING, int LENGTH) { (const char *record, int recordLength) };
%apply (char *STRING, int LENGTH) { (char *record, int recordLength) };
%apply (char *STRING, int LENGTH) { (const char *ACSMap, int ACSMapLength) };

#define LINKAGE

%include "btrieveCpp.h"

%{
   #include "btrieveCpp.h"
%}
