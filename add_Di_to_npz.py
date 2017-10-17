import numpy as np
import pyigl as igl
import glob
import os
import sys
sys.path.append(os.path.expanduser('~/Workspace'))
from iglhelpers import p2e, e2p
import scipy.sparse as sparse

def quaternion_matrix(x):
    a, b, c, d = x.tolist()
    return np.array([[a, -b, -c, -d],
                     [b,  a, -d,  c],
                     [c,  d,  a, -b],
                     [d, -c,  b,  a]])

def dirac(V, F):
    V = igl.eigen.MatrixXd(V)
    F = igl.eigen.MatrixXi(F)
    dblAf = igl.eigen.MatrixXd()
    igl.doublearea(V,F,dblAf)
    
    D = np.zeros((4 * F.rows(), 4 * V.rows()))
    DA = np.zeros((4 * V.rows(), 4 * F.rows()))

    dblAv = np.zeros(V.rows())
    for i in range(F.rows()):
        for j in F.row(i):
            dblAv[j] += dblAf[i] / 3

    for i in range(F.rows()):
        for ind, j in enumerate(F.row(i)):
            ind1 = F[i, (ind + 1) % 3]
            ind2 = F[i, (ind + 2) % 3]

            e1 = V.row(ind1)
            e2 = V.row(ind2)

            e = np.array([0, e1[0] - e2[0], e1[1] - e2[1], e1[2] - e2[2]])

            mat = -quaternion_matrix(e) / (dblAf[i])
            D[i * 4:(i + 1) * 4, j * 4: (j + 1) * 4] = mat
            DA[j * 4:(j + 1) * 4, i * 4: (i + 1) * 4] = mat.transpose() * dblAf[i] / dblAv[j]

    D = sparse.csr_matrix(D)
    DA = sparse.csr_matrix(DA)

    return D, DA

npz_path =  '/state/partition1/zj495/pose_npz/pose_npz/'
out_path =  '/state/partition1/zj495/pose_w_D/'

npz_files = sorted([os.path.basename(p) for p in glob.iglob(npz_path+'*.npz')])
existing_npz = sorted([os.path.basename(p) for p in glob.iglob(out_path+'*.npz')])
npz_files = [f for f in npz_files if f not in existing_npz]

def add_Di(npf):
    pose = np.load(npz_path + npf)
    V = pose['V']
    F = pose['F']
    Di, DiA = dirac(V, F)
    vdist = pose['vdist']
    #vdist = [min(np.linalg.norm(vrow - V[s]) for s in seam_verts) if i not in seam_verts else 0 for i,vrow in enumerate(V)]
    np.savez(out_path + npf , V=V, F=F, Di=Di, DiA=DiA, vdist=vdist)
    os.remove(npz_path + npf)

if __name__ == '__main__':
    for f in npz_files:
        add_Di(f)

