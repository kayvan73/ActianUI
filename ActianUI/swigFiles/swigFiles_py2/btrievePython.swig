////////////////////////////////////////////////////////////
//
// Copyright (C) 2016 - Actian Corp.
//
////////////////////////////////////////////////////////////

%module btrievePython

#if !defined(_WIN32) && !defined(_WIN64) && !defined(__linux__) && !defined(__APPLE__)
   #error Please define one of the above.
#endif

%inline %{

   static int buffer_view_attach(Py_buffer *view, PyObject *obj, char **buffer, Py_ssize_t *size)
   {
      // Not all objects support writeable so don't use it.  Doing this
      // is not without risk.  We do write to some objects.  Experimentation
      // shows this currently isn't a problem, but it might become one in
      // the future.
      // if (PyObject_GetBuffer(obj, view, PyBUF_ANY_CONTIGUOUS | PyBUF_WRITEABLE) == -1) {
      if (PyObject_GetBuffer(obj, view, PyBUF_ANY_CONTIGUOUS) == -1) {
          return -1;
      }
      *buffer = (char*)view->buf;
      *size = view->len;
      return 0;
   }
%}

#if defined(_WIN32) || defined(_WIN64)
%extend BtrieveClient {
   %{
   #include <Windows.h>
   #include "btrieveCpp.h"
   %}

   Btrieve::StatusCode FileCreate(BtrieveFileAttributes *btrieveFileAttributes, const char *fileName, Btrieve::CreateMode createMode, Btrieve::LocationMode locationMode = Btrieve::LOCATION_MODE_NO_PREFERENCE)
   {
      wchar_t fileNameW[256] = L"";
      char fileNameA[256] = "";

      if (MultiByteToWideChar(CP_UTF8, 0, fileName, -1, fileNameW, 256) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      if (WideCharToMultiByte(CP_ACP, 0, fileNameW, -1, fileNameA, 256, NULL, NULL) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      return self->FileCreate(btrieveFileAttributes, fileNameA, createMode, 
         locationMode);
   }

   Btrieve::StatusCode FileCreate(BtrieveFileAttributes *btrieveFileAttributes, BtrieveIndexAttributes *btrieveIndexAttributes, const char *fileName, Btrieve::CreateMode createMode, Btrieve::LocationMode locationMode = Btrieve::LOCATION_MODE_NO_PREFERENCE)
   {
      wchar_t fileNameW[256] = L"";
      char fileNameA[256] = "";

      if (MultiByteToWideChar(CP_UTF8, 0, fileName, -1, fileNameW, 256) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      if (WideCharToMultiByte(CP_ACP, 0, fileNameW, -1, fileNameA, 256, NULL, NULL) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      return self->FileCreate(btrieveFileAttributes, btrieveIndexAttributes, fileNameA, createMode, 
         locationMode);
   }

   Btrieve::StatusCode FileOpen(BtrieveFile *btrieveFile, const char *fileName, const char *ownerName, Btrieve::OpenMode openMode, Btrieve::LocationMode locationMode = Btrieve::LOCATION_MODE_NO_PREFERENCE)
   {
      wchar_t fileNameW[256] = L"";
      char fileNameA[256] = "";

      if (MultiByteToWideChar(CP_UTF8, 0, fileName, -1, fileNameW, 256) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      if (WideCharToMultiByte(CP_ACP, 0, fileNameW, -1, fileNameA, 256, NULL, NULL) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      return self->FileOpen(btrieveFile, fileNameA, ownerName, openMode, locationMode);
   }

   Btrieve::StatusCode FileDelete(const char *fileName)
   {
      wchar_t fileNameW[256] = L"";
      char fileNameA[256] = "";

      if (MultiByteToWideChar(CP_UTF8, 0, fileName, -1, fileNameW, 256) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      if (WideCharToMultiByte(CP_ACP, 0, fileNameW, -1, fileNameA, 256, NULL, NULL) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      return self->FileDelete(fileNameA);
   }

   Btrieve::StatusCode FileRename(const char *existingFileName, const char *newFileName)
   {
      wchar_t existingFileNameW[256] = L"";
      char existingFileNameA[256] = "";
      wchar_t newFileNameW[256] = L"";
      char newFileNameA[256] = "";

      if (MultiByteToWideChar(CP_UTF8, 0, existingFileName, -1, existingFileNameW, 256) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      if (WideCharToMultiByte(CP_ACP, 0, existingFileNameW, -1, existingFileNameA, 256, NULL, NULL) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      if (MultiByteToWideChar(CP_UTF8, 0, newFileName, -1, newFileNameW, 256) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      if (WideCharToMultiByte(CP_ACP, 0, newFileNameW, -1, newFileNameA, 256, NULL, NULL) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      return self->FileRename(existingFileNameA, newFileNameA);
   }

   Btrieve::StatusCode SetCurrentDirectory(const char *currentDirectory)
   {
      wchar_t currentDirectoryW[256] = L"";
      char currentDirectoryA[256] = "";

      if (MultiByteToWideChar(CP_UTF8, 0, currentDirectory, -1, currentDirectoryW, 256) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      if (WideCharToMultiByte(CP_ACP, 0, currentDirectoryW, -1, currentDirectoryA, 256, NULL, NULL) == 0)
      {
         return Btrieve::STATUS_CODE_INVALID_OPTION;
      }

      return self->FileDelete(currentDirectoryA);
   }

   PyObject *GetCurrentDirectory(Btrieve::DiskDrive diskDrive)
   {
      Btrieve::StatusCode statusCode;
      char currentDirectoryA[256] = "";
      wchar_t currentDirectoryW[256] = L"";
      PyObject *currentDirectoryObject;

      if ((statusCode = self->GetCurrentDirectory(diskDrive, currentDirectoryA, 256)) != Btrieve::STATUS_CODE_NO_ERROR)
      {
         return Py_None;
      }

      if (MultiByteToWideChar(CP_ACP, 0, currentDirectoryA, -1, currentDirectoryW, 256) == 0)
      {
         // TODO: Set last status code.
         return Py_None;
      }

      if ((currentDirectoryObject = PyUnicode_FromWideChar(currentDirectoryW, -1)) == NULL)
      {
         // TODO: Set last status code.
         return Py_None;
      }

      return currentDirectoryObject;
   }
}

%extend BtrieveFileInformation {
   %{
   #include "btrieveCpp.h"
   %}

   PyObject *GetReferentialIntegrityFileName()
   {
      Btrieve::StatusCode statusCode;
      char fileNameA[256] = "";
      wchar_t fileNameW[256] = L"";
      PyObject *fileNameObject;

      if ((statusCode = self->GetReferentialIntegrityFileName(fileNameA, 256)) != Btrieve::STATUS_CODE_NO_ERROR)
      {
         return Py_None;
      }

      if (MultiByteToWideChar(CP_ACP, 0, fileNameA, -1, fileNameW, 256) == 0)
      {
         // TODO: Set last status code.
         return Py_None;
      }

      if ((fileNameObject = PyUnicode_FromWideChar(fileNameW, -1)) == NULL)
      {
         // TODO: Set last status code.
         return Py_None;
      }

      return fileNameObject;
   }

   PyObject *GetSegmentFileName(int segmentFileNumber)
   {
      Btrieve::StatusCode statusCode;
      char fileNameA[256] = "";
      wchar_t fileNameW[256] = L"";
      PyObject *fileNameObject;

      if ((statusCode = self->GetSegmentFileName(segmentFileNumber, fileNameA, 256)) != Btrieve::STATUS_CODE_NO_ERROR)
      {
         return Py_None;
      }

      if (MultiByteToWideChar(CP_ACP, 0, fileNameA, -1, fileNameW, 256) == 0)
      {
         // TODO: Set last status code.
         return Py_None;
      }

      if ((fileNameObject = PyUnicode_FromWideChar(fileNameW, -1)) == NULL)
      {
         // TODO: Set last status code.
         return Py_None;
      }

      return fileNameObject;
   }
}
#endif

%extend BtrieveBulkCreatePayload {
   %{
   #include "btrieveCpp.h"
   %}

   Btrieve::StatusCode AddRecord(PyObject *recordObject)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;

      Py_buffer view;
      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         Btrieve::StatusCode status = self->AddRecord(record, (int)recordSize);
         PyBuffer_Release(&view);
         return status;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      return Btrieve::STATUS_CODE_INVALID_OPTION;
   }
}

%extend BtrieveBulkRetrieveResult {
   %{
   #include "btrieveCpp.h"
   %}

   int GetRecord(int recordNumber, PyObject *recordObject)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         int count = self->GetRecord(recordNumber, record, (int)recordSize);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      // TODO: Set last status code.
      return -1;
   }
}

%extend BtrieveFile {
   %{
   #include "btrieveCpp.h"
   %}

   int GetNumerator(Btrieve::Index index, PyObject *keyObject, int denominator)
   {
      char *key = NULL;
      Py_ssize_t keySize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, keyObject, &key, &keySize) == 0)
      {
         int numerator = self->GetNumerator(index, key, (int)keySize, denominator);
         PyBuffer_Release(&view);
         return numerator;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of keyObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int GetPercentage(Btrieve::Index index, PyObject *keyObject)
   {
      char *key = NULL;
      Py_ssize_t keySize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, keyObject, &key, &keySize) == 0)
      {
         int percentage = self->GetPercentage(index, key, (int)keySize);
         PyBuffer_Release(&view);
         return percentage;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of keyObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int KeyRetrieve(Btrieve::Comparison comparison, Btrieve::Index index, PyObject *keyObject)
   {
      char *key = NULL;
      Py_ssize_t keySize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, keyObject, &key, &keySize) == 0)
      {
         int count = self->KeyRetrieve(comparison, index, key, (int)keySize);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of keyObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int KeyRetrieveFirst(Btrieve::Index index, PyObject *keyObject)
   {
      char *key = NULL;
      Py_ssize_t keySize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, keyObject, &key, &keySize) == 0)
      {
         int count = self->KeyRetrieveFirst(index, key, (int)keySize);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of keyObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int KeyRetrieveLast(Btrieve::Index index, PyObject *keyObject)
   {
      char *key = NULL;
      Py_ssize_t keySize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, keyObject, &key, &keySize) == 0)
      {
         int count = self->KeyRetrieveLast(index, key, (int)keySize);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of keyObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int KeyRetrieveNext(PyObject *keyObject)
   {
      char *key = NULL;
      Py_ssize_t keySize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, keyObject, &key, &keySize) == 0)
      {
         int count = self->KeyRetrieveNext(key, (int)keySize);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of keyObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int KeyRetrievePrevious(PyObject *keyObject)
   {
      char *key = NULL;
      Py_ssize_t keySize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, keyObject, &key, &keySize) == 0)
      {
         int count = self->KeyRetrievePrevious(key, (int)keySize);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of keyObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   Btrieve::StatusCode RecordAppendChunk(PyObject *chunkObject)
   {
      char *chunk = NULL;
      Py_ssize_t chunkSize = 0;
      Py_buffer view;
      if (buffer_view_attach(&view, chunkObject, &chunk, &chunkSize) == 0)
      {
         Btrieve::StatusCode status = self->RecordAppendChunk(chunk, (int)chunkSize);
         PyBuffer_Release(&view);
         return status;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of chunkObject");
#endif

      return Btrieve::STATUS_CODE_INVALID_OPTION;
   }

   Btrieve::StatusCode RecordCreate(PyObject *recordObject)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         Btrieve::StatusCode status = self->RecordCreate(record, (int)recordSize);
         PyBuffer_Release(&view);
         return status;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      return Btrieve::STATUS_CODE_INVALID_OPTION;
   }

   int RecordRetrieveByCursorPosition(Btrieve::Index index, long long cursorPosition, PyObject *recordObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         int count = self->RecordRetrieveByCursorPosition(index, cursorPosition, record, (int)recordSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrieveByFraction(Btrieve::Index index, int numerator, int denominator, PyObject *recordObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         int count = self->RecordRetrieveByFraction(index, numerator, denominator, record, (int)recordSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrieveByPercentage(Btrieve::Index index, int percentage, PyObject *recordObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         int count = self->RecordRetrieveByPercentage(index, percentage, record, (int)recordSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrieveChunk(int length, PyObject *chunkObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *chunk = NULL;
      Py_ssize_t chunkSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, chunkObject, &chunk, &chunkSize) == 0)
      {
         int count = self->RecordRetrieveChunk(length, chunk, (int)chunkSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of chunkObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrieveChunk(int offset, int length, PyObject *chunkObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *chunk = NULL;
      Py_ssize_t chunkSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, chunkObject, &chunk, &chunkSize) == 0)
      {
         int count = self->RecordRetrieveChunk(offset, length, chunk, (int)chunkSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of chunkObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrieve(Btrieve::Comparison comparison, Btrieve::Index index, PyObject *keyObject, PyObject *recordObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *key = NULL;
      Py_ssize_t keySize = 0;
      char *record = NULL;
      Py_ssize_t recordSize = 0;

      Py_buffer kview;
      if (buffer_view_attach(&kview, keyObject, &key, &keySize) == 0)
      {
         Py_buffer rview;
         if (buffer_view_attach(&rview, recordObject, &record, &recordSize) == 0)
         {
            int count = self->RecordRetrieve(comparison, index, key, (int)keySize,
                                             record, (int)recordSize, lockMode);
            PyBuffer_Release(&rview);
            PyBuffer_Release(&kview);
            return count;
         }
         else
         {
            PyBuffer_Release(&kview);

#ifdef DEBUG
            PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif
         }
      }
      else
      {
#ifdef DEBUG
         PyErr_SetString(PyExc_TypeError, "failed to get buffer view of keyObject");
#endif
      }

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrieveFirst(Btrieve::Index index, PyObject *recordObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         int count = self->RecordRetrieveFirst(index, record, (int)recordSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrieveLast(Btrieve::Index index, PyObject *recordObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         int count = self->RecordRetrieveLast(index, record, (int)recordSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrieveNext(PyObject *recordObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         int count = self->RecordRetrieveNext(record, (int)recordSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordRetrievePrevious(PyObject *recordObject, Btrieve::LockMode lockMode = Btrieve::LOCK_MODE_NONE)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         int count = self->RecordRetrievePrevious(record, (int)recordSize, lockMode);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   Btrieve::StatusCode RecordUpdate(PyObject *recordObject)
   {
      char *record = NULL;
      Py_ssize_t recordSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, recordObject, &record, &recordSize) == 0)
      {
         Btrieve::StatusCode status = self->RecordUpdate(record, (int)recordSize);
         PyBuffer_Release(&view);
         return status;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of recordObject");
#endif

      return Btrieve::STATUS_CODE_INVALID_OPTION;
   }

   int RecordUpdateChunk(PyObject *chunkObject)
   {
      char *chunk = NULL;
      Py_ssize_t chunkSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, chunkObject, &chunk, &chunkSize) == 0)
      {
         int count = self->RecordUpdateChunk(chunk, (int)chunkSize);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of chunkObject");
#endif

      // TODO: Set last status code.
      return -1;
   }

   int RecordUpdateChunk(int offset, PyObject *chunkObject)
   {
      char *chunk = NULL;
      Py_ssize_t chunkSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, chunkObject, &chunk, &chunkSize) == 0)
      {
         int count = self->RecordUpdateChunk(offset, chunk, (int)chunkSize);
         PyBuffer_Release(&view);
         return count;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of chunkObject");
#endif

      // TODO: Set last status code.
      return -1;
   }
}

%extend BtrieveFilter {
   %{
   #include "btrieveCpp.h"
   %}

   Btrieve::StatusCode SetComparisonConstant(PyObject *constantObject)
   {
      char *constant = NULL;
      Py_ssize_t constantSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, constantObject, &constant, &constantSize) == 0)
      {
         Btrieve::StatusCode status = self->SetComparisonConstant(constant, (int)constantSize);
         PyBuffer_Release(&view);
         return status;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of constantObject");
#endif

      return Btrieve::STATUS_CODE_INVALID_OPTION;
   }
}

%extend BtrieveIndexAttributes {
   %{
   #include "btrieveCpp.h"
   %}

   Btrieve::StatusCode SetACSUserDefined(const char *ACSName, PyObject *ACSMapObject)
   {
      char *ACSMap = NULL;
      Py_ssize_t ACSMapSize = 0;
      Py_buffer view;

      if (buffer_view_attach(&view, ACSMapObject, &ACSMap, &ACSMapSize) == 0)
      {
         Btrieve::StatusCode status = self->SetACSUserDefined(ACSName, ACSMap, ACSMapSize);
         PyBuffer_Release(&view);
         return status;
      }

#ifdef DEBUG
      PyErr_SetString(PyExc_TypeError, "failed to get buffer view of ACSMapObject");
#endif

      return Btrieve::STATUS_CODE_INVALID_OPTION;
   }
}

#if defined(_WIN32) || defined(_WIN64)
%ignore BtrieveClient::FileCreate;
%ignore BtrieveClient::FileDelete;
%ignore BtrieveClient::FileOpen;
%ignore BtrieveClient::FileRename;
%ignore BtrieveClient::GetCurrentDirectory;
%ignore BtrieveClient::SetCurrentDirectory;
%ignore BtrieveFileInformation::GetReferentialIntegrityFileName;
%ignore BtrieveFileInformation::GetSegmentFileName;
#endif

%ignore BtrieveBulkCreatePayload::AddRecord;
%ignore BtrieveBulkRetrieveResult::GetRecord;
%ignore BtrieveFile::GetNumerator;
%ignore BtrieveFile::GetPercentage;
%ignore BtrieveFile::KeyRetrieve;
%ignore BtrieveFile::KeyRetrieveFirst;
%ignore BtrieveFile::KeyRetrieveLast;
%ignore BtrieveFile::KeyRetrieveNext;
%ignore BtrieveFile::KeyRetrievePrevious;
%ignore BtrieveFile::RecordAppendChunk;
%ignore BtrieveFile::RecordCreate;
%ignore BtrieveFile::RecordRetrieve;
%ignore BtrieveFile::RecordRetrieveByCursorPosition;
%ignore BtrieveFile::RecordRetrieveByFraction;
%ignore BtrieveFile::RecordRetrieveByPercentage;
%ignore BtrieveFile::RecordRetrieveChunk;
%ignore BtrieveFile::RecordRetrieveFirst;
%ignore BtrieveFile::RecordRetrieveLast;
%ignore BtrieveFile::RecordRetrieveNext;
%ignore BtrieveFile::RecordRetrievePrevious;
%ignore BtrieveFile::RecordUpdate;
%ignore BtrieveFile::RecordUpdateChunk;
%ignore BtrieveFilter::SetComparisonConstant;
%ignore BtrieveIndexAttributes::SetACSUserDefined;

%include "btrieveSwig.swig"

