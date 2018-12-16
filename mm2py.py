import pandas as pd
import xlrd
import numpy as np
from matplotlib import pyplot as plt

"""
Metamorphで解析したデータをPythonで図示する時に使用する．
MMから出力されるファイルには1ポジションのデータのみが入っていることを想定している．
"""
def loadExcelFile(input_file_name):
    input_book = pd.ExcelFile(input_file_name) 
    input_sheet_name = input_book.sheet_names
    num_sheet = len(input_sheet_name)
    print('Number of Sheet: ', num_sheet)
    df = input_book.parse(input_sheet_name[0])
    df.columns = [c.replace(' ', '_') for c in df.columns]
    print('Channel Info:', np.unique(np.asarray(df['Image_Name'])))
    return df

def channelSpliter(df, channel):
    for ch in np.unique(np.asarray(df['Image_Name'])):
        if channel != ch:
            #delete other color data from dataframe
            ch_df = df[df['Image_Name'] != ch]
    return ch_df

def subcellularSpliter(df, nuc_odd_even): # sc: 1 or 2
    df['Region_binary'] = np.asarray(df['Region_Label'])%2 
    for rl in np.unique(np.asarray(df['Region_Label'])):
        if nuc_odd_even == 1:
            nuc_df = df[df['Region_binary'] != 0 ]
            cyt_df = df[df['Region_binary'] != 1]
    return nuc_df, cyt_df

def normalizeAtStimulus(FC_ratio, timepoint):
    nmFC_ratio = FC_ratio.copy()
    for i in range(nmFC_ratio.shape[1]):
        nmFC_ratio[:, i] = nmFC_ratio[:, i]/np.mean(nmFC_ratio[0:timepoint, i])
    return nmFC_ratio
