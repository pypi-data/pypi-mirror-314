import numpy as np
import argparse
import os
import torch
from icecream import ic
import glob
from pathlib import Path
from tqdm import tqdm
def readDat(file_path, toTensor=False):
    "basic & core func"
    dat = np.fromfile(file_path,dtype='<f')
    if toTensor:
        dat = torch.from_numpy(dat)
    return dat

def saveDat(dat,file_path):
    "basic & core func"
    dat.tofile(file_path,format="<f")

def nc_to_tensor(location, opt = None, variable = None):
    import netCDF4 as nc
    f = nc.Dataset(location)
    
    channels = []
    for a in f.variables:
        if variable is not None and a != variable:
            continue
        full_shape = f[a].shape # 256 256 256
        
        if(opt is None or opt['extents'] is None):
            d = f[a]
        else:
            #print(f"Loading data with extents {opt['extents']}")
            ext = opt['extents'].split(',')
            ext = [eval(i) for i in ext]
            d = np.array(f[a][ext[0]:ext[1],ext[2]:ext[3],ext[4]:ext[5]])
        channels.append(d)
    d = np.stack(channels) 
    d = torch.tensor(d).unsqueeze(0) # 1, 1, 256, 256, 256
    return d, full_shape

def list_variables(location): # list all variables in the .nc file
    import netCDF4 as nc
    f = nc.Dataset(location)
    for a in f.variables:
        print("variable:", a, "\tshape:", f[a].shape)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default="/home/dullpigeon/SSD/VolumeData/Mantle-Vis-2021-selected", help='path to the directory containing the .nc files')
    parser.add_argument('-ls', action='store_true', default=False, help='list all variables in the .nc file')
    parser.add_argument('--outputDir', type=str, default="/home/dullpigeon/SSD/VolumeData/mantle", help='path to the output .raw file, None to save in the same directory as the .nc file')
    parser.add_argument('--variable', type=str, default="temperature anomaly", help='which variable in .nc to extract, None to extract all and stack together')

    args = parser.parse_args()
    nc_dir = args.d
    show_vars = args.ls
    outputDir = args.outputDir
    variable = args.variable
    
    os.makedirs(outputDir, exist_ok=True)
    
    nc_files = sorted(glob.glob(os.path.join(nc_dir, "*.nc")))
    # print(nc_files)
    # base_name = Path(nc_files[0]).stem
    # print(base_name)
    
  
    if args.ls:
        list_variables(nc_files[0])
        exit()
    for nc_filePath in tqdm(nc_files):
        d,_ = nc_to_tensor(nc_filePath, variable=variable)
        d = d.squeeze().numpy()
        # d = d.flatten("F")
        d = d.flatten()
        if outputDir is None:
            savePath = nc_filePath.replace(".nc", ".raw")
            saveDat(d,savePath)
        else:
            savePath = os.path.join(outputDir, Path(nc_filePath).stem + ".raw")
            saveDat(d,savePath)
