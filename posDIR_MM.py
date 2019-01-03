# -*- coding: utf-8 -*-
"""
Folders were created for each imaging position

Author: Gembu MARYU
"""
from __future__ import print_function
from os.path import join, relpath, splitext, exists
from os import makedirs, getcwd, rename, listdir
import shutil
from glob import glob
import sys
import os
import string
import argparse
import json


#python posDIR_MM.py -s /home/gembu/CellTK/data/2014_MCF10A -d /home/gembu/CellTK/data/20181214_MCF10A -t 132'
parser = argparse.ArgumentParser(
    prog='posDIR_MM.py',
    usage='python posDIR_MM.py [-s \'hgoehoge\'] [-d \'fugafuga\'] [-t ]',
    description='make subfolder for MetaMorph MDA',
    #add_help=True
)

parser.add_argument('-s', '--src', help='full path to the source directory')
parser.add_argument('-d', '--dest', help='full path to the destination directory')
parser.add_argument('-t', '--start_tp',  default=0, type=int, help='start timepint')
arg = parser.parse_args()

''' params '''
SRC_DIR = arg.src
start_tp = arg.start_tp
DEST_DIR = arg.dest

def cpy_rename(path, DEST_DIR, start_tp = 0):
    '''
    Copy TIFF file from external HDD to "CellTK/data" directory after rename
    :param path: path to 'TimePoint_#' directory
    :param SRC_DIR: parent directory of each experimental result
    :param tp: Time point information
    :return: null
    '''
    files = [relpath(x,path)
             for x in glob(join(path, "*"))]
    
    for i, file in enumerate(files):
        #print(file)
        ext = splitext(file)
        if ext[1] == ".tif" or ext[1] == ".TIF":
            # e.g. : 96well-5col-p21-2-1-HGS-PIP_C07_w1.TIF / 96well-5col_A01_s2_w1.TIF / MCF10A-4_w2GFP-Glass_s1_t84.TIF
            fn = file.split("_")
            #print(fn)
            tp = file.split('_')[-1] # timepoint
            tp = tp.split('.')[0]
            tp = tp[1:]
            w_s = fn[-2] # well info or stage position info
            posinfo = join(DEST_DIR, fn[-2])
            #print(posinfo)
            if exists(join(DEST_DIR, fn[-2])) != True:
                makedirs(posinfo)

            pn = w_s[1:] # number of stage position
            afile = fn[1] + '_t' + '{0:03d}'.format(int(tp)+start_tp) + '.TIF'
            #print(join(posinfo, afile))
            #print(join(path, file))
            shutil.copy(join(path, file), join(posinfo, afile))
        if i % 100 == 0:
            print(str(i) + "th pic is processed")
    return

cpy_rename(SRC_DIR, DEST_DIR, start_tp)
