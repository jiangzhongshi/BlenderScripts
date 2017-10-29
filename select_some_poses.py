import os
import shutil
import sys
import glob
import random
import tarfile
import multiprocessing

def random_sample(population, num):
    num = min(num, len(population))
    return random.sample(population, num)

def extract_one_tar_sample(pose):
    with tarfile.open(pose, 'r:gz') as tar:
        tar.extractall(out_path + model ,
             random_sample(tar.getmembers(),3))

if __name__ == '__main__':
    argv = sys.argv[sys.argv.index("--") + 1:]
    in_path = argv[0]
    out_path = argv[1]
    model_path = os.listdir(in_path)
    #print(model_path)
    #exit(1)
    for model in model_path[1:]:
        if not os.path.isdir(out_path+model):
            os.makedirs(out_path + model)
        pose_files =glob.glob(in_path + model + '/*.tar.gz') # random_sample(glob.glob(in_path + model+'/*.tar.gz'),20)

        mp = multiprocessing.Pool(int(argv[2]))
        mp.map(extract_one_tar_sample, pose_files)
