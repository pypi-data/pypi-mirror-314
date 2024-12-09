import numpy as np
from utils import *
import argparse
from skimage.transform import resize
from icecream import ic
from tqdm import tqdm
from scipy.interpolate import RegularGridInterpolator
from icecream import ic
# Get insight from: https://medium.com/vitrox-publication/rotation-of-voxels-in-3d-space-using-python-c3b2fc0afda1
from scipy.ndimage import rotate
RotateAlongXaix = lambda angle: np.array([[1, 0, 0],
                                          [0, np.cos(angle), -np.sin(angle)],
                                          [0, np.sin(angle), np.cos(angle)]])
RotateAlongYaix = lambda angle: np.array([[np.cos(angle), 0, np.sin(angle)],
                                          [0, 1, 0],
                                          [-np.sin(angle), 0, np.cos(angle)]])
RotateAlongZaix = lambda angle: np.array([[np.cos(angle), -np.sin(angle), 0],
                                          [np.sin(angle), np.cos(angle), 0],
                                          [0, 0, 1]])

def getRodriguesMatrix(axis, theta):
    v_length = np.linalg.norm(axis)
    if v_length==0:
        raise ValueError("length of rotation axis cannot be zero.")
    if theta==0.0:
        return np.identity(3)
    v = np.array(axis) / v_length
    # rodrigues rotation matrix
    W = np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]])
    rot3d_mat = np.identity(3) + W * np.sin(theta) + np.dot(W, W) * (1.0 - np.cos(theta))
    return rot3d_mat


def rotationVol(VolArray, axis, angle=90):
    # if angle%90 != 0:
    #     raise ValueError("angle must be a multiple of 90")
    if axis in [0, 'x', 'X']:
        axis = [1, 0, 0]
    elif axis in [1, 'y', 'Y']:
        axis = [0, 1, 0]
    elif axis in [2, 'z', 'Z']:
        axis = [0, 0, 1]
    else:
        raise ValueError("axis must be 0, 1, 2 or 'x', 'y', 'z'")
    
    # R = RotateAlongXaix(np.radians(angle))
    R = getRodriguesMatrix(axis, np.radians(angle))
    trans_mat_inv = np.linalg.inv(R)
    # trans_mat_inv = R
    Xdim, Ydim, Zdim = VolArray.shape
    x = np.linspace(0, Xdim-1, Xdim)
    y = np.linspace(0, Ydim-1, Ydim)
    z = np.linspace(0, Zdim-1, Zdim)
    xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')
    coord = np.array([xx - Xdim//2, yy - Ydim//2, zz - Zdim//2])
    coord_prime = np.tensordot(trans_mat_inv, coord, axes=((1), (0)))
    xx_prime = coord_prime[0] + Xdim//2
    yy_prime = coord_prime[1] + Ydim//2
    zz_prime = coord_prime[2] + Zdim//2
    
    x_valid1 = xx_prime >= 0
    x_valid2 = xx_prime < Xdim
    y_valid1 = yy_prime >= 0
    y_valid2 = yy_prime < Ydim
    z_valid1 = zz_prime >= 0
    z_valid2 = zz_prime < Zdim
    
    
    valid_voxel = x_valid1 * x_valid2 * y_valid1 * y_valid2 * z_valid1 * z_valid2

    x_valid_idx, y_valid_idx, z_valid_idx = np.where(valid_voxel > 0)
    vol_transformed = np.zeros_like(VolArray)
    # vol_transformed = np.zeros((Xdim, Ydim, Zdim))
    # print(VolArray.shape)
    # print((z, y, x))
    data_w_coor = RegularGridInterpolator((x, y, z), VolArray)
    interp_points = np.array([xx_prime[x_valid_idx, y_valid_idx, z_valid_idx],
                              yy_prime[x_valid_idx, y_valid_idx, z_valid_idx],
                              zz_prime[x_valid_idx, y_valid_idx, z_valid_idx]]).T

    interp_result = data_w_coor(interp_points)
    vol_transformed[x_valid_idx, y_valid_idx, z_valid_idx] = interp_result
    
    return vol_transformed
    
def Rectangle2Cube(vol):
    x, y, z = vol.shape
    if x == y and y == z:
        return vol
    else:
        max_dim = max(x, y, z)
        new_vol = np.zeros((max_dim, max_dim, max_dim))
        padding_x = (max_dim - x) // 2
        padding_y = (max_dim - y) // 2
        padding_z = (max_dim - z) // 2
        new_vol = np.pad(vol, ((padding_x, max_dim - x - padding_x), (padding_y, max_dim - y - padding_y), (padding_z, max_dim - z - padding_z)), 'constant')
        # new_vol[padding_x:-padding_x-1, padding_y:-padding_y-1, padding_z:-padding_z-1] = vol
        # new_vol[:, 7:-padding_y, padding_z:-padding_z] = vol
        return new_vol
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the diff image in a dir folder compared with GT',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('volPath', type=str, help='The volume data dir/file path')
    parser.add_argument('-d','--dims', type=int, nargs=3, default=[1024,1024,1080], help='The space dims of original volume data')
    parser.add_argument('--operations', type=str, nargs='+', help='The operations to perform on the volume data')

    args = parser.parse_args()
    volPath = args.volPath
    dims = args.dims
    operations = args.operations
    # print(f"volPath: {volPath}", f"dims: {dims}", f"operations: {operations}")
    # exit()
    if os.path.isdir(volPath):
        volPaths = getFilePathsInDir(volPath)    
    else:
        volPaths = [volPath]
    #* rotate
    for volPath in volPaths:
        v = readDat(volPath) # 1x 2 x 3   v.reshape(3,2,1).tranpose(2,1,0)
        v = v.reshape(dims[2],dims[1],dims[0]).transpose(2,1,0) # do not use reshape(dims)
        trans_v = rotate(v, 90, axes=(0, (0 + 1) % 3), reshape=False, mode='nearest')
        trans_v = rotate(trans_v, 90, axes=(1, (1 + 1) % 3), reshape=False, mode='nearest')
        trans_v = trans_v.flatten("F")
        saveDat(trans_v, volPath.replace(".raw", "_rotated.raw"))
