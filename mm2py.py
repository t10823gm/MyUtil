import pandas as pd
import xlrd
import numpy as np
from matplotlib import pyplot as plt

"""
MetamorphのRegion measurementで出力した結果をPythonで図示，解析する際に使用する．
FRET analysis, KTR analysisでは挙動を確認した．
"""
#### Data Import ###
def loadExcelFile(input_file_path):
    '''
    Load single excel file
    '''
    input_book = pd.ExcelFile(input_file_path) 
    input_sheet_name = input_book.sheet_names
    num_sheet = len(input_sheet_name)
    print('Number of Sheet: ', num_sheet)
    df = input_book.parse(input_sheet_name[0])
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[df['Image_Name'] != 'Image Name'] # for multi-postion measurement
    print('Channel Info:', np.unique(np.asarray(df['Image_Name'])))
    return df

def loadExcelFiles(xlsxlist):
    '''
    Load multiple excel file
    xlsxlist: List of exelfiles path 
        e.g. ['Pos1.xlsx', 'Pos2.xlsx', 'Pos3.xlsx', 'Pos4.xlsx']
    return: concatenated dataframe
    '''
    for i, x in enumerate(xlsxlist):
        if i == 0:
            df = loadExcelFile(x)
        else:
            tmp_df = loadExcelFile(x)
            df = pd.concat([df, tmp_df], join='outer')
    return df

### Dataframe handling###
def getDataFromDf(df):
    timepoints = np.array(np.unique(df['Image_Plane']), dtype=np.float32)
    cell_serial = np.arange(1, int(df.shape[0]/len(timepoints))+1,1) #multi-positionの時は通し番号
    df['Cell_Serial'] = np.repeat(cell_serial, len(timepoints))
    #print(int(nuc_df.shape[0]/len(timepoints)))
    intdata = np.reshape(np.asarray(df['Average_Intensity']), [len(cell_serial), len(timepoints)]).T
    return timepoints, cell_serial, intdata, df

def channelSpliter(df, channel):
    '''
    Extract data of channel of interest
    df: loaded dataframe
    ch_df: 
    '''
    for ch in np.unique(np.asarray(df['Image_Name'])):
        if channel != ch:
            #delete other color data from dataframe
            ch_df = df[df['Image_Name'] != ch]
    return ch_df

def subcellularSpliter(df, nuc_odd_even): # sc: 1 or 2
    '''
    Divide 
    nuc_odd_even: select 1 when nuc region is assigned odd number

    '''
    df['Region_binary'] = np.asarray(df['Region_Label'])%2 
    for rl in np.unique(np.asarray(df['Region_Label'])):
        if nuc_odd_even == 1:
            nuc_df = df[df['Region_binary'] != 0 ]
            cyt_df = df[df['Region_binary'] != 1]
    return nuc_df, cyt_df


### Data handling ###
def normalizeAtStimulus(FC_ratio, timepoint):
    '''
    Normalize intensity before stimulation
    timepoint: int

    '''
    nmFC_ratio = FC_ratio.copy()
    for i in range(nmFC_ratio.shape[1]):
        nmFC_ratio[:, i] = nmFC_ratio[:, i]/np.mean(nmFC_ratio[0:timepoint, i])
    return nmFC_ratio

def arrayMeanSd(array):
    '''
    calculation of mean intensity and standard deviation
    
    '''
    array = np.array(array, dtype=np.float32)
    array_mean = np.nanmean(array, axis=1)
    #array_mean = np.array(np.mean(array, axis=1), dtype=np.float32) 
    array_sd = np.nanstd(array, axis=1)
    #array_sd = np.array(np.std(array, axis=1), dtype=np.float32)
    return array_mean, array_sd

def getTargetIndex(df, column_name, keyword):
    search_array = np.asarray(df[column_name])
    index = np.where(search_array == keyword)
    return index

def deleteDataFromArray(array, cell_serial, del_region_list):
    mod_serial = cell_serial.copy()
    mod_array = array.copy()
    for i in del_region_list:
        idx = np.where(mod_serial == i)
        mod_serial = np.delete(mod_serial,  idx)
        mod_array = np.delete(mod_array, idx, axis=1)
    return mod_array, mod_serial

def extractDataFromArray(array, cell_serial, ext_region_list):
    mod_serial = cell_serial.copy()
    del_reg = list(set(cell_serial) - set(ext_region_list))
    mod_array, mod_serial = deleteDataFromArray(array, cell_serial, del_reg)
    return mod_array, mod_serial

### Plot ###
def plotShadedErrorBar(timepoints, array_mean, array_sd):
    plt.plot(timepoints, array_mean)
    print(array_mean-array_sd)
    print(array_mean+array_sd)
    plt.fill_between(timepoints, array_mean-array_sd, array_mean+array_sd, alpha=0.5)
    return

def plotIndividualCell(array, cell_serial, figsize_tuple, tablesize_list):
    plt.figure(figsize=figsize_tuple)
    for i, reg in enumerate(cell_serial):
        plt.subplot(tablesize_list[0], tablesize_list[1], i+1)
        plt.plot(range(array.shape[0]), array[:,i], label=reg)
        plt.grid(linestyle='--')
        plt.title(reg)
    plt.tight_layout()
    return




### Delete in future ###
def deleteFromDf(df, del_reg, KTR=False):
    """
    del_reg : list of region for deletion
    KTR : KTR analysis
    """
    mod_df = df.copy()
    print(df.shape)
    for i in del_reg:
        mod_df = mod_df[mod_df['Region_Label'] != i]
        if KTR==True:
            # in KTR analysis, paired region is also delete
            mod_df = mod_df[mod_df['Region_Label'] != i+1 ]
    print(df.shape)
    return mod_df

def extractFromDf(df, ext_reg, KTR=False):
    """
    ext_reg : list of region for deletion
    KTR : KTR analysis
    """
    timepoints = np.unique(np.asanyarray(df['Image_Plane']))
    region_id = np.arange(1, int(df.shape[0]/len(timepoints))+1,1)
    del_reg = list(set(region_id) - set(ext_reg))
    mod_df = deleteFromDf(df, del_reg, KTR)
    return mod_df
