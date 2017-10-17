import numpy as np
import pyigl as igl
import glob
import os
import sys

pose_path = '/scratch/zj495/pose4900/'
npz_path = '/scratch/zj495/pose_npz/'

poses = sorted([os.path.basename(p) for p in glob.iglob(pose_path+'*.obj')])

for pose in poses:
    V, TC, CN = igl.eigen.MatrixXd(), igl.eigen.MatrixXd(), igl.eigen.MatrixXd()
    F, FTC, FCN = igl.eigen.MatrixXi(),igl.eigen.MatrixXi(),igl.eigen.MatrixXi()
    igl.readOBJ(pose_path + pose, V, TC, CN, F, FTC, FCN)

    seams, bnds, folds = igl.eigen.MatrixXi(),igl.eigen.MatrixXi(),igl.eigen.MatrixXi()
    igl.seam_edges(V,TC,F,FTC,seams, bnds, folds)

    np.savez_compressed(npz_path + pose+'.npz', V=V, F=F, seams=seams, bnds=bnds)
