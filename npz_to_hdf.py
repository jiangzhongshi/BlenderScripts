import numpy as np
import h5py
import scipy
import os
import sys
import argparse
import glob

parser = argparse.ArgumentParser(description='Change folder of npz to a single hdf5')
parser.add_argument('--npz-folder', default='@')
parser.add_argument('--output-hdf5', default='new_hdf5.h5')
parser.add_argument('--ver', default='Nov10')

#hf = h5py.File('name-of-file.h5','w')
#npf = np.load('1000_rejected_000036.obj0.obj.npz',encoding='latin1')

def write_h5_sparse(hf, name, SpM):
    sp_g = hf.create_group(name)

    sp_g.attrs['format'] = SpM.format
    sp_g.attrs['shape'] = SpM.shape
    sp_g.create_dataset('data', data = SpM.data)
    if SpM.format in ('csc', 'csr', 'bsr'):
        sp_g.create_dataset('indices', data = SpM.indices)
        sp_g.create_dataset('indptr', data = SpM.indptr)
    elif SpM.format == 'coo':
        sp_g.create_dataset('row', data = SpM.row)
        sp_g.create_dataset('col', data = SpM.col)
def read_h5_sparse(hf, name):
    sp_g = hf[name]
    form = sp_g.attrs['format']
    shape = sp_g.attrs['shape']
    data = sp_g['data']
    if form in ('csc', 'csr', 'bsr'):
        return scipy.sparse.csr_matrix((data, sp_g['indices'], sp_g['indptr']), shape=shape)
    elif form == 'coo':
        return scipy.sparse.csr_matrix((data, (sp_g['row'], sp_g['col'])), shape = shape)

def npz_to_hdf(npzf, hf):
    for name, arr in npf.items():
        if name in hf:
            del hf[name]
        if arr.dtype == 'O':
            arr = arr.item()
        if scipy.sparse.issparse(arr):
            write_h5_sparse(hf, name, arr)
        else:
            hf.create_dataset(name, data=arr)

if __name__ == '__main__':
    argv = parser.parse_args()
    npz_names = sorted([n for n in glob.glob(argv.npz_folder+'/*.npz')])
    with h5py.File(argv.output_hdf5) as hf:
        for npz_path in npz_names:
            npz_name = os.path.basename(npz_path)
            if npz_name in hf:
                try:
                    if hf[npz_name].attrs['ver'] == argv.ver:
                        continue
                except:
                    del hf[npz_name]
            with np.load(npz_path) as npf:
                np_g = hf.create_group(npz_name)
                npz_to_hdf(npf, np_g)
                np_g.attrs['ver'] = argv.ver
                print('Finish:{}'.format(npz_name))


