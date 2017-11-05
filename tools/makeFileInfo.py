#config: utf-8

import os
import glob
import hashlib
import struct
import re
import ctypes

class FileInfoBigEndian(ctypes.BigEndianStructure):
    _fields_ = (
        ('filePath', ctypes.c_char * 256),
        ('fileSize', ctypes.c_uint32),
        ('hashValue', ctypes.c_uint32),
    )

class FileInfoLittleEndian(ctypes.LittleEndianStructure):
    _fields_ = (
        ('filePath', ctypes.c_char * 256),
        ('fileSize', ctypes.c_uint32),
        ('hashValue', ctypes.c_uint32),
    )

basePath = os.path.join(os.path.abspath(__file__), '../')
refpath = os.path.normpath(os.path.join(basePath, '../resource'))
resourcePath = os.path.normpath(os.path.join(basePath, '../resource/**/*.*'))

def GetFileList(dirPath):
    globlist = glob.glob(dirPath)
    return globlist


outJsonPath = os.path.join(basePath, 'fileinfo.json')
outbinPath = os.path.join(refpath, 'fileinfo.bin')

f = open(outJsonPath, 'w')
fb = open(outbinPath, 'wb')
barray = bytearray()
f.write('{\n')
filelist = GetFileList(resourcePath)
fileInfoList = list()
hashlist = list()
def MakeFileInfo(endian):
    print(filelist)
    for i in filelist:
        line = i
        i = i.replace('\\','/')
        fileSize = os.path.getsize(i)
        filename = os.path.basename(i)
        hashValue = hashlib.md5(i.encode('utf-8')).hexdigest()
        hashInt = int(hashValue, 16)
        hashInt32 = hashInt % pow(2, 32);
        
        index = i.find('resource')
        filePath = i[index:len(i)]
        filePath = filePath.replace("resource/", "")
        fileSizeBytes = fileSize.to_bytes(4, endian)
        print(i)
        print('FileSize:{0}'.format(fileSize))
        print('HashInt32:{0}'.format(hashInt32))
        ret = hashInt32 in hashlist
        #同じハッシュ値が見つかったらアサート
        assert ret == False, 'Hash Hit file:{0} hash:{1}'.format(filePath, hashInt32)
        hashlist.append(hashInt32)
        f.write('\t["filePath":"{0}", "fileSize":{1}, "hash":{2}]'.format(filePath, fileSize, hashInt32))
        if line == filelist[-1]:
            f.write("\n")
        else:
            f.write(",\n")

        if endian == 'little':
            fileinfo = FileInfoLittleEndian(filePath.encode('utf-8'), fileSize, hashInt32)
        else:
            fileinfo = FileInfoBigEndian(filePath.encode('utf-8'), fileSize, hashInt32)
        
        fileInfoList.append(fileinfo)
    f.write('}')
    f.close()

    #バイナリファイル出力
    for i in fileInfoList:
        fb.write(i)
    fb.close()

MakeFileInfo('little')