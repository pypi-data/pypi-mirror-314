from utils import *
import argparse
import os
from icecream import ic
from PIL import Image
import cv2
import imageio

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a set of images into one video',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('imgsDir', type=str, help='The path of the images dir')
    parser.add_argument('--outPath', type=str, default=None, help='The path of the output mp4 video file')
    parser.add_argument('--fps', type=int, default=25, help='The fps of the output video')
    
    args = parser.parse_args()
    imgsDir = args.imgsDir
    outPath = args.outPath
    fps = args.fps
    
    imgW, imgH = None, None
    imgs = []
    imgPaths = getFilePathsInDir(imgsDir)
    for i in range(len(imgPaths)):
        img = Image.open(imgPaths[i])
        imgs.append(np.array(img))
        if i == 0:
            imgW, imgH = img.size
    if outPath is None:
        outPath = os.path.join(imgsDir,'video.mp4')
    imageio.mimwrite(outPath, imgs, fps=fps, quality=8, macro_block_size=1)

    