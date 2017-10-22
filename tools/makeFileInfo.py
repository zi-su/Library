#config: utf-8

import os
import glob
import hashlib
import struct
import re
import ctypes

class FileInfoBigEndian(ctypes.BigEndianStructure):
    _fields_ = (
        ('filePath', ctypes.c_char * 512),
        ('fileSize', ctypes.c_uint32),
        ('hashValue', ctypes.c_char * 32),
    )

class FileInfoLittleEndian(ctypes.LittleEndianStructure):
    _fields_ = (
        ('filePath', ctypes.c_char * 512),
        ('fileSize', ctypes.c_uint32),
        ('hashValue', ctypes.c_char * 32),
    )

basePath = os.path.join(os.path.abspath(__file__), '../')
refpath = os.path.normpath(os.path.join(basePath, '../resource'))
resourcePath = os.path.normpath(os.path.join(basePath, '../resource/**/*.*'))

def GetFileList(dirPath):
    globlist = glob.glob(dirPath)
    return globlist


outJsonPath = os.path.join(basePath, 'fileinfo.json')
outbinPath = os.path.join(basePath, 'fileinfo.bin')

f = open(outJsonPath, 'w')
fb = open(outbinPath, 'wb')
barray = bytearray()
f.write('{\n')
filelist = GetFileList(resourcePath)
fileInfoList = list()

def MakeFileInfo(endian):
    for i in filelist:
        i = i.replace('\\','/')
        fileSize = os.path.getsize(i)
        filename = os.path.basename(i)
        hashValue = hashlib.md5(filename.encode('utf-8')).hexdigest()
        index = i.find('resource')
        filePath = i[index:len(i)]
        fileSizeBytes = fileSize.to_bytes(4, endian)
        print(i)
        print(fileSize)
        print(fileSizeBytes)        
        f.write('\t["filePath":"{0}", "fileSize":{1}, "hash":{2}],\n'.format(filePath, fileSize, hashValue))
        if endian == 'little':
            fileinfo = FileInfoLittleEndian(filePath.encode('utf-8'), fileSize, hashValue.encode('utf-8'))
        else:
            fileinfo = FileInfoBigEndian(filePath.encode('utf-8'), fileSize, hashValue.encode('utf-8'))
        
        fileInfoList.append(fileinfo)
    f.write('}')
    f.close()
    for i in fileInfoList:
        fb.write(i)
    fb.close()

MakeFileInfo('little')