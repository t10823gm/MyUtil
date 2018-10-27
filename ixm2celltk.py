from __future__ import print_function
from os.path import join, relpath, splitext, exists
from os import makedirs, getcwd, rename, listdir
import shutil
from glob import glob
import sys
import os
import string
import argparse


parser = argparse.ArgumentParser(
    prog='ixm2celltk.py',
    usage='python ixm2celltk.py [-h] [-s \'hgoehoge\'] [-d \'fugafuga\'] [-t ]',
    description='change file name from IXM-XLS sytle to CellTK',
    #add_help=True
)

parser.add_argument('-s', '--src', help='full path to the source directory')
parser.add_argument('-d', '--dest', help='full path to the destination directory')
parser.add_argument('-t', '--start_tp',  default=0, type=int, help='start timepint')
parser.add_argument('-w', '--wavelength', help='dictionary about wavelength name',\
                    default={'w1':'w1iRFP', 'w2':'w2mKO', 'w3':'w3mCherry', 'w4':'w4GFP', 'w5':'w5CFP'})
arg = parser.parse_args()


''' params '''
SRC_DIR = arg.src
wavelength = arg.wavelength
start_tp = arg.start_tp
DEST_DIR = arg.dest

''' functions '''
def chars_to_int(chars):
    '''
    For MATLAB image processing script developed by Tobias Lab.
    Split well information into row number and column number (e.g. A3 -> 1_3)
    :param chars: column number in multi-well dish
    :return: converted value
    '''
    chars = chars.upper()
    size = len(chars)
    result = 0
    for pos, c in enumerate(chars):
        i = string.ascii_uppercase.index(c) + 1
        exp = size - pos - 1
        result += i * 26 ** exp
    return resultgit

def cpy_rename(path, DEST_DIR, tp, wavelength, start_tp = 0):
    '''
    Copy TIFF file from external HDD to "CellTK/data" directory after rename
    :param path: path to 'TimePoint_#' directory
    :param SRC_DIR: parent directory of each experimental result
    :param tp: Time point information
    :param wavelength: wavelength data pass as dictionary
    :return: null
    '''
    files = [relpath(x,path)
             for x in glob(join(path, "*"))]
    for file in files:
        #print(file)
        ext = splitext(file)
        if ext[1] == ".tif" or ext[1] == ".TIF":
            # e.g. : 96well-5col-p21-2-1-HGS-PIP_C07_w1.TIF / 96well-5col_A01_s2_w1.TIF
            fn = file.split("_")
            #print(fn)

            w_s = fn[-2] # well info or stage position info
            if w_s[0] == 's':
                #print('multi-position in a well')
                wellinfo = join(DEST_DIR, fn[-3])
                if exists(join(DEST_DIR, fn[-3])) != True:
                    makedirs(wellinfo)
                if exists(join(wellinfo, fn[-2])) != True:
                    makedirs(join(wellinfo, fn[-2]))

                pn = w_s[1:] # number of stage position
                wl = fn[-1]  # wavelength
                wl = wl.split('.')[0]
                afile = w_s[0] + '{0:02d}'.format(int(pn)) + '_' + wavelength[wl] + '_t' + \
                        '{0:03d}'.format(int(tp)+start_tp) + '.TIF'
                #print(join(wellinfo, fn[-2], afile))
                shutil.copy(join(path, file), join(wellinfo, fn[-2], afile))

            else:
                #print('single position in a well')
                if exists(join(DEST_DIR, w_s)) != True:
                    makedirs(join(DEST_DIR, w_s))

                save_dir = join(DEST_DIR, w_s)
                wl = fn[-1]  # wavelength
                wl = wl.split('.')[0]
                total_tp = int(tp) + int(start_tp)
                afile = 's01' + '_' + wavelength[wl] + '_t' + '{0:03d}'.format(total_tp) + '.TIF'
                print('Source : ' + join(path, file))
                print('Save as : ' + join(DEST_DIR, fn[-3], afile))
                shutil.copy(join(path, file), join(save_dir, afile))
    return

for i, n in enumerate(os.listdir(SRC_DIR)):
    path = os.path.join(SRC_DIR, n)
    if os.path.isdir(path):
        tp = n.split('_')[-1] # timepoint
        #print('path is ', path)
        cpy_rename(path, DEST_DIR, tp, wavelength, start_tp)

    if i % 50 == 0:
        print(str(i) + "th point is passed")
