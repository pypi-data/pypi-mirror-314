from utils import *
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='calculate the psnr of volumes, the parameter "eval" and "GT" can either be both file path or dir (but not one file path and one dir). The ext of file name can be anything including .raw or .iw',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('GT', type=str, help='The path of the gt dir/file')
    parser.add_argument('eval', type=str, help='The path of the eval dir/file')
    parser.add_argument('-n', action="store_true", help='whether norm the data to [-1,1] before calculating psnr')
    
    args = parser.parse_args()
    eval_path = args.eval
    GT_path = args.GT
    eval_is_dir = os.path.isdir(eval_path)
    GT_is_dir = os.path.isdir(GT_path)
    if eval_is_dir and GT_is_dir:
        o = VolumeMetrics(GT_dirPath=GT_path, eval_dirPath=eval_path, verbose=True, normBeforeHand=args.n)
        MeanPSNR, PSNR = o.getBatchPSNR()
        for i in range(len(PSNR)):
            print(f"PSNR of {i+1} timestep is {PSNR[i]}")
        print(f"Mean PSNR is {MeanPSNR}")
        print(f"array:\n {PSNR}")
    elif (not eval_is_dir) and (not GT_is_dir):
        o = VolumeMetrics(normBeforeHand=args.n)
        PSNR = o.getPSNRFromFile(GT_path,eval_path)
        print(f"PSNR is {PSNR}")
    else:
        raise ValueError(f"eval and GT should be both dir or both file, but got {eval_path} is dir as {eval_is_dir} and {GT_path} is dir as {GT_is_dir}")