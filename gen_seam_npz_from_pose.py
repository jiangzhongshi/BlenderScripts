import numpy as np
import pyigl as igl
import glob
import os
import sys
import multiprocessing
sys.path.append(os.path.expanduser('~/Workspace/libigl/python/'))
from iglhelpers import e2p,p2e

argv = sys.argv[sys.argv.index("--") + 1:]
obj_path = argv[0]
npz_path = argv[1]
#pose_path = '/scratch/zj495/pose4900/'
#npz_path = '/scratch/zj495/pose_npz/'

def obj_to_npz_w_seam_bnd_L(pose):
    if os.path.isfile(npz_path + pose +'.npz'):
        return
    V, TC, CN = igl.eigen.MatrixXd(), igl.eigen.MatrixXd(), igl.eigen.MatrixXd()
    F, FTC, FCN = igl.eigen.MatrixXi(),igl.eigen.MatrixXi(),igl.eigen.MatrixXi()
    igl.readOBJ(obj_path + pose, V, TC, CN, F, FTC, FCN)

    #assert F.cols()==3, obj_path+pose
    if F.cols()!= 3:
        print("bad:"+pose)
        os.remove(obj_path+pose)
        return
    seams, bnds, folds = igl.eigen.MatrixXi(),igl.eigen.MatrixXi(),igl.eigen.MatrixXi()
    igl.seam_edges(V,TC,F,FTC,seams, bnds, folds)

    L_igl = igl.eigen.SparseMatrixd()
    M, Minv =  igl.eigen.SparseMatrixd(),igl.eigen.SparseMatrixd()
    igl.cotmatrix(V,F,L_igl)
    igl.massmatrix(V,F,igl.MASSMATRIX_TYPE_BARYCENTRIC,M)
    igl.invert_diag(M,Minv)
    L_igl = Minv*L_igl

    V, F, seams, bnds = e2p(V), e2p(F), e2p(seams), e2p(bnds)
    if seams.size + bnds.size ==0:
        print("!!!empty seambnd"+filename)
        return
    seam_verts = set(
        [F[e[i],e[i+1]] for e in seams for i in (0,2)] +
        [F[e[0],(e[1]+i)%3] for e in bnds for i in (0,1)] )
    assert len(seam_verts) !=0, filename + "empty seamvert"
    vdist = [min(np.linalg.norm(vrow - V[s]) for s in seam_verts) if i not in seam_verts else 0 for i,vrow in enumerate(V)]

    np.savez_compressed(npz_path + pose + '.npz', V=V, F=F, seams=seams, bnds=bnds, L = e2p(L_igl), vdist=vdist)

if __name__ == '__main__':
    poses = sorted([os.path.basename(p) for p in glob.iglob(obj_path+'*.obj')])
    if len(argv) > 2:
        p = multiprocessing.Pool(int(argv[2]))
        p.map(obj_to_npz_w_seam_bnd_L, poses)
    else:
        obj_to_npz_w_seam_bnd_L(poses[0])
