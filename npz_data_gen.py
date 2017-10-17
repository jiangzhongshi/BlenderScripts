import sys
import os
import gc
sys.path.append('..')
sys.path.append(os.path.expanduser('~/Workspace/SurfaceNN/src'))

import utils.mesh as mesh
import utils.graph as graph

import numpy as np
import itertools
import pyigl as igl
from iglhelpers import p2e,e2p
import glob

def get_seam_verts(F,TF, nv):
    V2uv = -np.ones(nv)
    seam_vert_ind = np.zeros(nv)
    for i in range(TF.rows()):
        for j in range(TF.cols()):
            uv_id = TF[i,j]
            V_id = F[i,j]
            if V2uv[V_id] == -1:
                V2uv[V_id] = uv_id
            elif V2uv[V_id] != uv_id:
                seam_vert_ind[V_id] = 1 # 1 means on the seam
    return seam_vert_ind

def rotate_data(V,F):
    angle = np.random.rand()*2*np.pi
    rot_mat = np.array([[np.cos(angle),np.sin(angle)],[ -np.sin(angle), np.cos(angle)]])
    rot_V = np.array(V)
    rot_V[:,0:3:2] = np.matmul(V[:,0:3:2],rot_mat)
    D, DA = mesh.dirac(rot_V, F)
    return (rot_V, F, D, DA)


if __name__ == '__main__':
     argv = sys.argv
     argv = argv[argv.index("--") + 1:]  # get all args after "--"
     input_path = '/mnt/ssd/tmp/zhjiang/'+argv[0]
     for i, filename in enumerate(glob.iglob(input_path + '_out/*.obj')):
         try:
             V,UV, NV = igl.eigen.MatrixXd(),igl.eigen.MatrixXd(),igl.eigen.MatrixXd()
             F, TF, FN = igl.eigen.MatrixXi(),igl.eigen.MatrixXi(),igl.eigen.MatrixXi()
             igl.readOBJ(filename, V,UV,NV, F, TF, FN)
             seam_verts = get_seam_verts(F,TF,V.rows())
             V = e2p(V)
             F = e2p(F)
             D, DA = mesh.dirac(V, F)
             npz_path = input_path + '_npz/' + filename.split('/')[-1]+'.npz'
             np.savez(npz_path,V = V, F= F,Di = D, DiA = DA, seam_verts = seam_verts)
             os.remove(filename)
             gc.collect()
         except:
             print('except: '+ npz_path)
             shutil.move(filename, input_path+'_problem')
             continue


