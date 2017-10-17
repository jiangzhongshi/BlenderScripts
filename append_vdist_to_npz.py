import numpy as np
from scipy import sparse
import glob
import os
import sys
from multiprocessing import Pool
import pyigl as igl

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

def append_vdist_to_npz(filename):
    with np.load(filename) as npl:
        if 'vdist' in npl:
            return
        V, F, seams, bnds = npl['V'], npl['F'], npl['seams'], npl['bnds']
        if seams.size + bnds.size ==0:
            print("!!!empty seambnd"+filename)
            return
        Di, DiA = dirac(V, F)
        seam_verts = set(
            [F[e[i],e[i+1]] for e in seams for i in (0,2)] +
            [F[e[0],(e[1]+i)%3] for e in bnds for i in (0,1)] )
        assert len(seam_verts) !=0, filename + "empty seamvert"
        vdist = [min(np.linalg.norm(vrow - V[s]) for s in seam_verts) if i not in seam_verts else 0 for i,vrow in enumerate(V)]
        np.savez_compressed(filename, V=V, F=F, Di=Di, DiA = DiA, seams=seams, bnds=bnds, vdist=vdist)
        print('Done' + filename)

if __name__=='__main__':
    p = Pool(30)
    npz_path = glob.glob('/scratch/zj495/pose_npz_test/*.npz')
    print("npzs to process: {}".format(len(npz_path)))
    #append_vdist_to_npz(npz_path[0])
    p.map(append_vdist_to_npz, npz_path)
