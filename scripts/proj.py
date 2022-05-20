import os
import re
import codecs
from pathlib import Path
from datetime import datetime

pkg_name = 'zwdocs'
pkg_desc = 'Personal Document Utilities'
author = 'Zhao Wei'
email = 'yewberry@163.com'
fpenc = 'utf-8'
pkg_info = [
    '__version__', '0.0.0',
    '__title__', pkg_name,
    '__description__', pkg_desc,
    '__url__', 'https://github.com/njzhaowei/%s' % pkg_name,
    '__author__', author,
    '__author_email__', email,
    '__license__', 'Apache 2.0',
    '__copyright__', 'Copyright (c) %s %s. All rights reserved.' % (datetime.now().year, author),
]
rootdir = Path(os.path.abspath(__file__)).parent.parent

pth = rootdir / ('%s/__version__.py' % pkg_name)
print('Setup %s' % pth)
if not pth.exists() or os.stat(pth).st_size == 0:
    Path(pth).parent.mkdir(parents=True, exist_ok=True)
    with codecs.open(str(pth), 'w', fpenc) as fp:
        for i in range(0, len(pkg_info), 2):
            fp.write("%s = '%s'\n"%(pkg_info[i], pkg_info[i+1]))
        fp.flush()

pth = rootdir / ('docs/source/%s'%'conf.py')
print('Setup %s' % pth)
with codecs.open(str(pth), 'r', fpenc) as fp:
    lines = fp.readlines()
    for i,s in enumerate(lines):
        if re.match(r'^project = .*\r?\n?$', s):
            lines[i] = "project = '%s'\n" % pkg_name
        elif re.match(r'^author = .*\r?\n?$', s):
            lines[i] = "author = '%s'\n" % author
        else:
            lines[i] = '%s\n' % s.rstrip()
with codecs.open(str(pth), 'w', fpenc) as fp:
    fp.writelines(lines)

pth = rootdir / 'setup.py'
lines = []
print('Setup %s' % pth)
with codecs.open(str(pth), 'r+', fpenc) as fp:
    lines = fp.readlines()
    for i,s in enumerate(lines):
        if re.match(r'^pkg_name = .*\n$', s):
            lines[i] = "pkg_name = '%s'\n" % pkg_name
            break
    fp.seek(0)
    fp.writelines(lines)
    fp.flush()

pth = rootdir / 'README.md'
print('Setup %s' % pth)
if not pth.exists() or os.stat(pth).st_size == 0:
    with codecs.open(str(pth), 'w', fpenc) as fp:
        fp.write('# %s\n'%pkg_name.upper())
        fp.write('%s  ' % pkg_desc)

pth = rootdir / 'LICENSE'
lines = []
print('Setup %s' % pth)
with codecs.open(str(pth), 'r', fpenc) as fp:
    lines = fp.readlines()
    for i,s in enumerate(lines):
        if re.match(r'^Copyright \(c\) .*\r?\n?$', s):
            lines[i] = "Copyright (c) %s %s\n" %  (datetime.now().year, author)
        else:
            lines[i] = '%s\n' % s.rstrip()
with codecs.open(str(pth), 'w', fpenc) as fp:
    fp.writelines(lines)