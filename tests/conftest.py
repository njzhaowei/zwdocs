import os
import codecs

def rmfile(pth):
    if os.path.isfile(str(pth)):
        os.remove(str(pth))

def writefile(pth, txt, enc='utf-8'):
    with codecs.open(pth, 'w', enc) as fp:
        fp.write(txt)
        fp.flush()

def readfile(pth, enc='utf-8', default=None):
    rtn = None
    with codecs.open(pth, 'r', enc) as fp:
        rtn = fp.read()
    if rtn.startswith('\ufeff'):# BOM
        rtn = rtn[1:]
    return rtn
