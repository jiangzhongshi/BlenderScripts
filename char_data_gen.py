import sys
import os
sys.path.append('..')
sys.path.append(os.path.expanduser('~/Workspace/SurfaceNN/src'))

import utils.mesh as mesh
import utils.graph as graph


sys.path.append('../..')

import numpy as np
import itertools
import pyigl as igl
from iglhelpers import p2e,e2p

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
                seam_vert_ind[V_id] = 1
    return seam_vert_ind

def rotate_data(V,F):
    angle = np.random.rand()*2*np.pi
    rot_mat = np.array([[np.cos(angle),np.sin(angle)],[ -np.sin(angle), np.cos(angle)]])
    rot_V = np.array(V)
    rot_V[:,0:3:2] = np.matmul(V[:,0:3:2],rot_mat)
    D, DA = mesh.dirac(rot_V, F)
    return (rot_V, F, D, DA)


if __name__ == '__main__':
    '''
    import glob
    for i, filename in enumerate(glob.glob(os.path.expanduser(
        '~/Workspace/SurfaceNN/src/seam_predict/data_plus/*.npz'))):
        print(filename)
        npfile = np.load(filename)

        seam_id = npfile['seam_id']
        V = npfile['V']
        F = npfile['F']
        for k in range(10):
            V, F, D, DA = rotate_data(V,F)
            np.savez(filename+str(k)+'npz', V=V, F=F, Di=D, DiA=DA, seam_id=seam_id)
     '''
     import glob
     V,UV, NV = igl.eigen.MatrixXd(),igl.eigen.MatrixXd(),igl.eigen.MatrixXd()
     F, TF, FN = igl.eigen.MatrixXi(),igl.eigen.MatrixXi(),igl.eigen.MatrixXi()
     for i, filename in enumerate(glob.iglob('/mnt/ssd/tmp/zhjiang/0_out/*.obj')):
         igl.readOBJ(filename, V,UV,NV, F, TF, FN)
         seam_verts = get_seam_verts(F,TF,V.rows())
         npz_path = filename[:23] + 'npz' + filename[26:]+'.npz'
         V = e2p(V)
         F = e2p(F)
         D, DA = mesh.dirac(V, F)
         np.savez(npz_path,V = (V), F= (F),Di = D, DiA = DA, seam_verts = seam_verts)


