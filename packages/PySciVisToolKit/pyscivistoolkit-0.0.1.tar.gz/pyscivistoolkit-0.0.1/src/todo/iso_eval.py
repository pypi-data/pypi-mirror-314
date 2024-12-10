from utils import *
import argparse
import os
#* our inhouse code takes in a path like path/to/volume/xxx-[t:4d].raw format
#* the t will be iterated from 1 to t
def extract_prefix(volDir):
    #* input a volDir, output (dir + the prefix of the volume file name)
    file = getFilePathsInDir(volDir)[0]
    prefix = os.path.basename(file)[:-8]
    res = os.path.join(volDir,prefix)
    return res
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='calculate the CD of volumes, the parameter "eval" and "GT" can either be both file path or dir (but not one file path and one dir). The ext of file name can be anything including .raw or .iw',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('GT', type=str, help='The path of the gt dir/file')
    parser.add_argument('eval', type=str, help='The path of the eval dir/file')
    parser.add_argument('-iso', type=float, default=0.0, help='iso values for marching cube')
    parser.add_argument('--dims', type=int, nargs='+', help='The space dims of the volume data')
    parser.add_argument('--t', type=int, default=1, help='Total timesteps of the volume data')
    args = parser.parse_args()
    eval_path = args.eval
    GT_path = args.GT
    dims = args.dims
    t = args.t
    iso = args.iso
    #* isosurface generation
    eval_is_dir = os.path.isdir(eval_path)
    GT_is_dir = os.path.isdir(GT_path)
    
    iso_tmp_a_dir = r"/home/dullpigeon/Softwares/PythonToolBox/iso_tmp/iso_a"
    iso_tmp_b_dir = r"/home/dullpigeon/Softwares/PythonToolBox/iso_tmp/iso_b"
    IsoSurfaceGenerationCodeDir = r"/home/dullpigeon/Softwares/InHouseCode/IsosurfaceGeneration/build/IsosurfaceGeneration"
    
    ensure_dirs(iso_tmp_a_dir)
    ensure_dirs(iso_tmp_b_dir)
    delFilesInDir(iso_tmp_a_dir)
    delFilesInDir(iso_tmp_b_dir)
    
    print("generating isosurface for gt...")
    if GT_is_dir:
        print(extract_prefix(GT_path))
        iso_cmd_a = f"{IsoSurfaceGenerationCodeDir} {extract_prefix(GT_path)} {iso_tmp_a_dir+'/a-'} {dims[0]} {dims[1]} {dims[2]} {iso} {args.t}"
        runCmd(iso_cmd_a)
    else:
        print("Make sure the input GT file path is only the prefix")
        iso_cmd_a = f"{IsoSurfaceGenerationCodeDir} {GT_path} {iso_tmp_a_dir+'/a-'} {dims[0]} {dims[1]} {dims[2]} {iso} {1}"
        runCmd(iso_cmd_a)
    
    print("generating isosurface for eval...")
    if eval_is_dir:
        print(extract_prefix(eval_path))
        iso_cmd_b = f"{IsoSurfaceGenerationCodeDir} {extract_prefix(eval_path)} {iso_tmp_b_dir+'/b-'} {dims[0]} {dims[1]} {dims[2]} {iso} {args.t}"
        runCmd(iso_cmd_b)
    else:
        print("Make sure the input eval file path is only the prefix")
        iso_cmd_b = f"{IsoSurfaceGenerationCodeDir} {eval_path} {iso_tmp_b_dir+'/b-'} {dims[0]} {dims[1]} {dims[2]} {iso} {1}"
        runCmd(iso_cmd_b)
    
    if eval_is_dir and GT_is_dir:
        o = SurfaceMetrics(GT_dirPath=iso_tmp_a_dir, eval_dirPath=iso_tmp_b_dir, verbose=True)
        MeanCD, CDs = o.getBatchCD()
        for i in range(len(CDs)):
            print(f"CD of {i+1} timestep at iso {args.iso} is {CDs[i]}")
        print(f"Mean CD at iso {args.iso} is {MeanCD}")
        print('\n')
        print(f"array:\n {CDs}")
    elif (not eval_is_dir) and (not GT_is_dir):
        o = SurfaceMetrics(GT_dirPath=iso_tmp_a_dir, eval_dirPath=iso_tmp_b_dir, verbose=True)
        MeanCD, CDs = o.getBatchCD()
        print(f"CD at iso {args.iso} is {MeanCD}")
    else:
        raise ValueError(f"eval and GT should be both dir or both file, but got {eval_path} is dir as {eval_is_dir} and {GT_path} is dir as {GT_is_dir}")