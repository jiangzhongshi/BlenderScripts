import os
import shutil
import sys
import glob
import random
import tarfile

def random_sample(population, num):
    num = min(num, len(population))
    return random.sample(population, num)

if __name__ == '__main__':
    argv = sys.argv[sys.argv.index("--") + 1:]
    in_path = argv[0]
    out_path = argv[1]
    model_path = os.listdir(in_path)
    for model in model_path:
        os.makedirs(out_path + model)
        pose_files = random_sample(glob.glob(in_path + model+'/*.tar.gz'),20)
        for pose in pose_files:
            with tarfile.open(pose, 'r:gz') as tar:
                tar.extractall(out_path + model ,
                     random_sample(tar.getmembers(),3))
