#config: utf-8

import os
import glob
import hashlib
import struct
import re

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

def MakeFileInfo(endian):
    for i in filelist:
        i = i.replace('\\','/')
        filesize = os.path.getsize(i)
        filename = os.path.basename(i)
        hashValue = hashlib.md5(filename.encode('utf-8')).hexdigest()
        filesizebytes = filesize.to_bytes(4,endian)
        index = i.find('resource')
        filePath = i[index:len(i)]
        print(i)
        print(filesize)
        print(filesizebytes)
        f.write('\t["filePath":"{0}", "fileSize":{1}, "hash":{2}],\n'.format(filePath, filesize, hashValue))
        barray.extend(filePath.encode('utf-8'))
        barray.extend(filesizebytes)
        barray.extend(hashValue.encode('utf-8'))
    f.write('}')
    f.close()
    fb.write(barray)
    fb.close()

MakeFileInfo('little')