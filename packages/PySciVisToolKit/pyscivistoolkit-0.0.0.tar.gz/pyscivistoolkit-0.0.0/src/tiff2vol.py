from utils import *
import tifffile
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the diff image in a dir folder compared with GT',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tifPath', type=str, help='The dir path of images')
    parser.add_argument('--outPath',type=str, default=None,help='Output volume path, if None, generate within "filePath" dir with name "OutputVol.raw"') 

    args = parser.parse_args()
    tifPath = args.tifPath
    tiff_stack = tifffile.imread(tifPath)
    
    volume = np.array(tiff_stack)
    volume = volume.flatten("F")
    saveDat(volume,"./output.raw")
    print(volume.dtype)
    print(volume.shape) 
