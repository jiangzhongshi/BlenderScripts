import pyigl as igl
import glob
import os
import numpy as np
import sys
sys.path.append(os.path.expanduser('/home/zj495/Workspace/'))
from iglhelpers import p2e,e2p
import tables
import multiprocessing
import random
argv = sys.argv
argv = argv[argv.index("--") + 1:]

npz_path=argv[0]# os.environ['SLURM_JOBTMP'] + '/in/'
out_path =argv[1]# os.environ['SLURM_JOBTMP'] + '/out/'
#npz_path = '/scratch/zj495/pose_npz/'
#out_path = '/scratch/zj495/pose_npz_8channel/'

npz_list = [os.path.basename(p) for p in glob.glob(npz_path+'*.npz')]


def append_normal_curvature(filename):
    with np.load(npz_path + filename) as frame:
        N = igl.eigen.MatrixXd()
        V,F = p2e(np.ascontiguousarray(frame['V'])),p2e(np.ascontiguousarray(frame['F']))
        igl.per_vertex_normals(V,F,igl.PER_VERTEX_NORMALS_WEIGHTING_TYPE_DEFAULT, N)
        PD1,PD2 = igl.eigen.MatrixXd(), igl.eigen.MatrixXd()
        PV1,PV2 = igl.eigen.MatrixXd(), igl.eigen.MatrixXd()
        H,K = igl.eigen.MatrixXd(), igl.eigen.MatrixXd()
        igl.principal_curvature(V,F,PD1,PD2,PV1,PV2)
        H = 0.5*(PV1+PV2)
        K = np.array(PV1)*np.array(PV2)
        # do not overwrite 'DiA', 'F', 'vdist', 'Di', 'V'
        np.savez_compressed(out_path + filename,
                           V=frame['V'], F = frame['F'],
                          Di = frame['Di'], DiA = frame['DiA'],
                          vdist = frame['vdist'], N = N, H=H, K=K)
        #with tables.open_file(+ '.h5', 'a', driver='H5FD_CORE') as h5file:
        #    for name in frame: # natural append
        #        h5file.create_array(h5file.root, name, frame[name])
        #    h5file.create_array(h5file.root, "N", e2p(N))
        #    h5file.create_array(h5file.root, "H", e2p(H))
        #    h5file.create_array(h5file.root, "K", K)

def append_vdist_to_npz(filename):
    with np.load(filename) as npl:
        if 'vdist' in npl:
            print('AE:'+filename)
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


def append_Laplacian(filename):
    with np.load(npz_path + filename) as frame:

        if 'vdist' not in frame:
            V, F, seams, bnds = frame['V'], frame['F'], frame['seams'], frame['bnds']
            if seams.size + bnds.size ==0:
                print("!!!empty seambnd"+filename)
                return
            seam_verts = set(
                [F[e[i],e[i+1]] for e in seams for i in (0,2)] +
                [F[e[0],(e[1]+i)%3] for e in bnds for i in (0,1)] )
            assert len(seam_verts) !=0, filename + "empty seamvert"
            vdist = [min(np.linalg.norm(vrow - V[s]) for s in seam_verts) if i not in seam_verts else 0 for i,vrow in enumerate(V)]
        else:
            vdist = frame['vdist']
        V,F = p2e(np.ascontiguousarray(frame['V'])),       p2e(np.ascontiguousarray(frame['F']))
        L_igl = igl.eigen.SparseMatrixd()
        M, Minv =  igl.eigen.SparseMatrixd(),igl.eigen.SparseMatrixd()
        igl.cotmatrix(V,F,L_igl)
        igl.massmatrix(V,F,igl.MASSMATRIX_TYPE_BARYCENTRIC,M)
        igl.invert_diag(M,Minv)
        L_igl = Minv*L_igl

        np.savez_compressed(out_path + filename,
                           V=frame['V'], F = frame['F'],
                            vdist = vdist, L = e2p(L_igl).tocsr())
    os.remove(npz_path + filename)

if __name__ == '__main__':
    p = multiprocessing.Pool(1)
    random.shuffle(npz_list)
    p.map(append_Laplacian, npz_list)


