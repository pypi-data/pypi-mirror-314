import numpy as np
from utils import *
import argparse
from skimage.transform import resize
from icecream import ic
from tqdm import tqdm

def slideWindowTimeInterpolation(volPaths,ut):
    # get the output paths
    volPaths_baseDir = os.path.dirname(volPaths[0])
    volPaths_baseName = os.path.basename(volPaths[0])[:-8]
    input_samples = len(volPaths) # input samples
    output_samples = int(input_samples * ut) # output samples
    outPaths = [os.path.join(volPaths_baseDir,f"{volPaths_baseName}{i:04d}.dat") for i in range(1,output_samples+1)]

    key_time_indexs = [i for i in range(1,output_samples+1,ut)]

    # read and interpolate the input volumes in a slide window way (to reduce memory usage)
    for jth,i in enumerate(range(1,len(key_time_indexs))):
        index_e = key_time_indexs[i]
        index_s = key_time_indexs[i-1]
        end_vol = readDat(volPaths[jth+1])
        start_vol = readDat(volPaths[jth])
        saveDat(start_vol,outPaths[index_s-1])
        ic(outPaths[index_s-1])
        saveDat(end_vol,outPaths[index_e-1])
        ic(outPaths[index_e-1])
        for index_i in range(index_s+1,index_e):
            d_si = index_i - index_s
            d_ie = index_e - index_i
            d_se = index_e - index_s
            saveDat((d_ie/d_se) * start_vol + (d_si/d_se) * end_vol,outPaths[index_i-1]) 

    if key_time_indexs[-1] != output_samples:
        index_e = key_time_indexs[-1]
        index_s = key_time_indexs[-2]
        start_vol = readDat(volPaths[-2])
        end_vol = readDat(volPaths[-1])
        saveDat(start_vol,outPaths[index_s-1])
        saveDat(end_vol,outPaths[index_e-1])
        for index_i in range(key_time_indexs[-1]+1, output_samples+1):
            d_si = index_i - index_s
            d_ie = index_e - index_i
            d_se = index_e - index_s
            saveDat((d_ie/d_se) * start_vol+ (d_si/d_se) * end_vol,outPaths[index_i-1]) 
    delFilesInDir(volPaths_baseDir,ext=".raw") #delete all raw files
    for p in outPaths:
        os.rename(p,p[:-4]+".raw") # rename all dat files to raw files
        
def Resize(volDir,dims,us):
    volPaths = getFilePathsInDir(volDir)
    for p in tqdm(volPaths,desc="spatial upsampling",disable=False):
        vol = readDat(p)
        vol = vol.reshape(dims[2],dims[1],dims[0]).transpose()
        vol = resize(vol,(int(dims[0]*us),int(dims[1]*us),int(dims[2]*us)),order=3)#
        vol = vol.flatten("F")
        saveDat(vol,p)
    

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the diff image in a dir folder compared with GT',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dirPath', type=str, help='The volume data dir path')
    parser.add_argument('-d','--dims', type=int, nargs='+', help='The space dims of original volume data')
    parser.add_argument('-us',type=float, default=1,help='Upsampling spatial scale factor')
    parser.add_argument('-ut',type=int, default=1,help='Upsampling temporal scale factor')

    args = parser.parse_args()
    dirPath = args.dirPath
    dims = args.dims
    us = args.us
    ut = args.ut
    assert (us >= 1 and ut >= 1), "Not implemented: Upsampling scale factor must be greater than 1"
    
    volPaths = getFilePathsInDir(args.dirPath)
    assert len(volPaths) > 0, "The volume data dir is empty"
    
    volPaths_baseDir = os.path.dirname(volPaths[0])
    volPaths_baseName = os.path.basename(volPaths[0])[:-8]
    volPaths_extName = os.path.basename(volPaths[0])[-8:]
    if "raw" not in volPaths_extName:
        raise Exception("The volume data must be in .raw format")
    
    input_samples = len(volPaths) # input samples
    output_samples = int(input_samples * ut) # output samples
    
    # outPaths = [os.path.join(volPaths_baseDir,f"{volPaths_baseName}{i:04d}.raw") for i in range(1,output_samples+1)]
    
    #* time interpolation first:
    if ut != 1:
        slideWindowTimeInterpolation(volPaths,ut)
    if us != 1:
        Resize(volPaths_baseDir,args.dims,us)
        



# def BL(ymlPath,verbose=True):
#     args = yaml_loader(ymlPath)
#     dataset = Dataset(args)
#     dataset.ReadData()
#     data = dataset.GetSampledData()
#     dims = dataset.dim
#     outDir = args['data_setting']['outputDir']
    
#     for var in tqdm(dataset.vars,desc="LERP",disable=(not verbose)):
#         outVarDir = os.path.join(outDir,var)
#         ensure_dirs(outVarDir,verbose=True)
#         var_data = data[var]
#         for index in range(len(var_data)):
#             var_data[index] = resize(var_data[index],(dims[0],dims[1],dims[2]),order=3).flatten("F")
#         var_data = timeLinearInterpolation(var_data,dataset.total_samples,dataset.sample_time_steps)
#         for t in range(1,len(var_data)+1):
#             save_path = os.path.join(outVarDir,f"{dataset.dataset}-{var}-{t:04d}.dat")
#             save_dat = np.array(var_data[t-1],dtype='<f')
#             save_dat.tofile(save_path,format="<f")


