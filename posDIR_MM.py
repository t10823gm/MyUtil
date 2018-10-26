# -*- coding: utf-8 -*-
"""
Folders were created for each imaging position

Author: Gembu MARYU
"""

from os.path import join, relpath, splitext, exists
from os import makedirs, getcwd, rename
import shutil
from glob import glob
import sys

### Editable variable
path = "20180331_HELB"

#path=sys.argv[0]
ROOT_DIR = getcwd()
#print ROOT_DIR
#print join(ROOT_DIR, path)

files = [relpath(x, path)

for x in glob(join(path, "*"))]
#print files

for file in files:
    ext = splitext(file)
    if ext[1] == ".tif" or ext[1] == ".TIF":
        fn = file.split("_")
        pi = fn[-2] # position infomation
        pn = pi[1:]
        dn = "Pos"+ pn # directoly name
        ti = fn[-1] # time infomation
        tn = ti.split('.')[0]
        tn = tn[1:]

        if exists(join(ROOT_DIR, path, dn)) == True:
            #print 'Hi'
            shutil.move(join(ROOT_DIR, path, file), join(ROOT_DIR, path, dn, file))
        else:
            print "omg"
            makedirs(join(path, dn))
            shutil.move(join(ROOT_DIR, path, file), join(ROOT_DIR, path, dn, file))

        file1 = join(ROOT_DIR, path, dn, file)
        file2 = join(ROOT_DIR, path, dn, fn[0]+'_'+fn[1]+'_'+fn[2]+'_'+'t'+'{0:03d}'.format(int(tn))+'.TIF')
        rename(file1, file2)

