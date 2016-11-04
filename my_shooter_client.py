#!/usr/bin/env python
#coding=utf-8

import hashlib
import os
import sys
import requests
from requests.packages.urllib3 import disable_warnings

#获取文件hash值
def ComputeFileHash(fileFullName):
    ret = ""
    try:
        vfile = open(fileFullName, "rb")
    except IOError:
        print("Cannot read file %s" % fileFullName)

    statinfo = os.stat(fileFullName)
    fLength = statinfo.st_size

    ret = []
    for i in (4096, int(fLength / 3) * 2, int(fLength / 3), fLength - 8192):
        vfile.seek(i, 0)
        bBuf = vfile.read(4096)
        ret.append(hashlib.md5(bBuf).hexdigest())
    vfile.close()
    return ';'.join(ret)


#获取电影文件名和格式
def getMovieName(fileFullName):
    fileinfo= os.path.split(fileFullName)
    movieinfo = os.path.splitext(fileinfo[1])     #电影文件名和格式
    return fileinfo,movieinfo

#获取字幕
def get_subtitleinfo(fileFullName):
    """do api request, parse error, return response."""
    sys.stdout.write("Requesting subtitle info...\n")

    #接口获取字幕信息
    response = requests.post(
        "https://www.shooter.cn/api/subapi.php",
        verify=False,
        params= {
            'filehash': ComputeFileHash(fileFullName),
            'pathinfo': os.path.realpath(fileFullName),
            'format': 'json',
            'lang': "Chn",
        },
    )
    #未找到字幕处理
    if response.text == u'\xff':
        sys.stderr.write("Subtitle not found.\n")
        sys.exit(1)
    return response


def main(fileFullName):
    disable_warnings()
    #判断电影文件是否存在
    if not os.path.isfile(os.path.realpath(fileFullName)):
        sys.stderr.write("File %s not found.\n" % fileFullName)
        sys.exit(1)

    #请求字幕api
    response = get_subtitleinfo(fileFullName)
    sys.stdout.write("Requesting subtitle file...\n")
    subtitles = set([])

    #拆分文件名和格式
    (fileinfo,movieinfo) = getMovieName(fileFullName)
    bname = fileinfo[0]+"/"+movieinfo[0]+".chn"    #电影路径+电影名+".chn"
    for count in xrange(len(response.json())):
        print response.json()
        _basename = bname+str(count+1)+"."       #电影路径+电影名+".chn"+"1"+"."
        #遍历下载字幕
        for fileinfo in response.json()[count]['Files']:
            url = fileinfo['Link']
            #ext = fileinfo['Ext']
            _response = requests.get(url, verify=False)
            #获取字幕文件后缀
            heads= _response.headers
            attachment = heads['Content-Disposition']
            substyle = attachment[-3:]

            subFielName = _basename+substyle        #电影路径+电影名+".chn"+"1"+"."+"格式"
            print subFielName

            #下载字幕
            if _response.ok and _response.text not in subtitles:
                subtitles.add(_response.text)
                fobj = open(subFielName, 'w')
                fobj.write(_response.text.encode("UTF8"))
                fobj.close()

if __name__ == '__main__':
    main(sys.argv[1])
