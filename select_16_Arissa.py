import os
import shutil
import sys
import glob
import random
import tarfile

def random_sample(population, num):
    num = min(num, len(population))
    return random.sample(population, num)

in_path = '/state/partition1/zj495/16_Arissa/'
out_path = '/state/partition1/zj495/16_Arissa_out/'
#in_path = '/scratch/zj495/Mixamo/'
#out_path = '/scratch/zj495/poses/'
model = '16_Arissa'
pose_files = glob.glob(in_path+'/*.tar.gz')
for pose in pose_files:
    with tarfile.open(pose, 'r:gz') as tar:
        tar.extractall(out_path,
                 random_sample(tar.getmembers(),3))
