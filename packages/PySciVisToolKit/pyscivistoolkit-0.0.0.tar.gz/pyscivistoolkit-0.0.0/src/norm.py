from utils import *
import argparse

def getGlobalMinMax(dirPath):
    global_min = 1e10
    global_max = -1e10
    paths = getFilePathsInDir(dirPath,ext='.raw')
    for p in paths:
        v = readDat(p)
        global_max = max(global_max,v.max())
        global_min = min(global_min,v.min())
    return global_min,global_max

def GlobalNormalizeDir(dirPath,outMin=0,outMax=1,outDir=None,verbose=True):
    global_min,global_max = getGlobalMinMax(dirPath)
    primeDataPaths = getFilePathsInDir(dirPath,ext='.raw')
    
    in_place_flag = False if outDir != None else True
    if outDir == None:
        outDir = dirPath
    else:
        ensure_dirs(outDir)
    
    for path in tqdm(primeDataPaths,disable=(not verbose),desc="normalizing data"):
        datFileName = os.path.split(path)[-1]
        dat         = readDat(path)
        dat_min,dat_max = global_min,global_max
        zero_to_one_dat = (dat - dat_min)/(dat_max - dat_min)
        normalized_dat  = (outMax - outMin)*zero_to_one_dat + outMin
        normalized_dat = np.array(normalized_dat,dtype="<f")
        if in_place_flag:
            os.remove(path)
        saveDat(normalized_dat,os.path.join(outDir,datFileName))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Normalize the volume scalar data in dir, then save the normalized data in outDir/in-place. The ext of volume data file must be ".raw",formatter_class=argparse.ArgumentDefaultsHelpFormatter')
    parser.add_argument('dirPath', type=str, help='The path of the data dir')
    parser.add_argument('-g', action="store_true", help='whether norm the data globally over all time steps')
    parser.add_argument('--outMin', type=float, default=0.0, help='The min value of the output')
    parser.add_argument('--outMax', type=float, default=1.0, help='The max value of the output')
    parser.add_argument('--not_verbose', action="store_true", help='not verbose output')
    parser.add_argument('--outDir', type=str, default=None, help='The path of the output dir')
    
    args = parser.parse_args()
    dirPath = args.dirPath
    outMin = args.outMin
    outMax = args.outMax
    verbose = not args.not_verbose
    is_global = args.g
    if is_global:
        GlobalNormalizeDir(dirPath,outMin,outMax,outDir=None,verbose=verbose)
    else:
        NormalizeDataInDir(dirPath,outMin,outMax,outDir=None,verbose=verbose)
