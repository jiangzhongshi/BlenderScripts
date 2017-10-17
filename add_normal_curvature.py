import pyigl as igl
import glob
import os
import numpy as np
import sys
sys.path.append(os.path.expanduser('/home/zj495/Workspace/'))
from iglhelpers import p2e,e2p
import tables

npz_path= '/state/partition1/zj495/npz_complete/'
out_path = '/state/partition1/zj495/16_Arissa_npz_complete/'
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

def append_Laplacian(filename):
    with np.load(npz_path + filename) as frame:
        V,F = p2e(np.ascontiguousarray(frame['V'])), 
                p2e(np.ascontiguousarray(frame['F']))
        
        L_igl = igl.eigen.SparseMatrixd()
        M, Minv =  igl.eigen.SparseMatrixd(),igl.eigen.SparseMatrixd()
        igl.cotmatrix(V,F,L_igl)
        igl.massmatrix(V,F,igl.MASSMATRIX_TYPE_BARYCENTRIC,M)
        igl.invert_diag(M,Minv)
        L_igl = Minv*L_igl

        # do not overwrite 'DiA', 'F', 'vdist', 'Di', 'V'
        np.savez_compressed(out_path + filename, 
                           V=frame['V'], F = frame['F'],
                          Di = frame['Di'], DiA = frame['DiA'],
                            vdist = frame['vdist'], N = frame['N'], H=frame['H'], 
                            K=frame['K'], L = e2p(L_igl).tocsr())
    os.remove(npz_path + filename)
    
if __name__ == '__main__':
    for f in npz_list:
        try:
            append_Laplacian(f)
        except:
            print(f)
    
