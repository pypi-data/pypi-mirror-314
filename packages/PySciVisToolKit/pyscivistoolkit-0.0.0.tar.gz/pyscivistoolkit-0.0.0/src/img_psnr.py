from utils import *
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='calculate the lpips and ssim of images, the parameter "eval" and "GT" can either be both file path or dir (but not one file path and one dir). The ext of file name can be anything including .raw or .iw',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('GT', type=str, help='The path of the gt dir/file')
    parser.add_argument('eval', type=str, help='The path of the eval dir/file')


    args = parser.parse_args()
    eval_path = args.eval
    GT_path = args.GT
    eval_is_dir = os.path.isdir(eval_path)
    GT_is_dir = os.path.isdir(GT_path)
    if eval_is_dir and GT_is_dir:
        o = ImageMetrics(GT_dirPath=GT_path, eval_dirPath=eval_path, verbose=True)
        MeanPSNR, PSNR = o.getBatchPSNR()
        for i in range(len(PSNR)):
            print(f"PSNR of {i+1} timestep is {PSNR[i]}")
        print(f"Mean PSNR is {MeanPSNR}")
        print('\n')
        #MeanSSIM, SSIM = o.getBatchSSIM()
        #for i in range(len(SSIM)):
        #    print(f"SSIM of {i+1} timestep is {SSIM[i]}")
        #print(f"Mean SSIM is {MeanSSIM}")
        #print('\n')
        print(f"array:\n {PSNR}")
    elif (not eval_is_dir) and (not GT_is_dir):
        o = ImageMetrics()
        PSNR = o.getPSNRFromFile(GT_path,eval_path)
        print(f"PSNR is {PSNR}")
        #print('\n')
        #SSIM = o.getSSIMFromFile(GT_path,eval_path)
        #print(f"SSIM is {SSIM}")
    else:
        raise ValueError(f"eval and GT should be both dir or both file, but got {eval_path} is dir as {eval_is_dir} and {GT_path} is dir as {GT_is_dir}")
