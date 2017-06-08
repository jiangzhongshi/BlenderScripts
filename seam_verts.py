#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 22:41:12 2017

@author: zhongshi
"""

import pyigl as igl

def get_verts_on_seam(F, FTC, nv = None):
    if nv == None:
        nv = F.maxCoeff()+1
        
    V2uv = igl.eigen.MatrixXi(nv, 1)
    for i in range(0, V2uv.rows()):
        V2uv[i] = -1
    seam_verts = set()
    for i in range(0, FTC.rows()):
        for j in range(0,3):
            uv_id = FTC[i,j]
            V_id = F[i,j]
            if V2uv[V_id] == -1:
                V2uv[V_id] = uv_id
            else:
                if V2uv[V_id] != uv_id:
                    seam_verts.add(V_id)
    return seam_verts

if __name__ == "__main__":
    import tcpviewer
    
    TUTORIAL_SHARED_PATH = "/Users/zhongshi/Desktop/"
    
    # Read a mesh
    V, TC, CN = igl.eigen.MatrixXd(), igl.eigen.MatrixXd(), igl.eigen.MatrixXd()
    F, FTC, FN = igl.eigen.MatrixXi(), igl.eigen.MatrixXi(), igl.eigen.MatrixXi()
    
    igl.readOBJ(TUTORIAL_SHARED_PATH + "animal_low.obj", V,TC,CN, F,FTC,FN)
    
    seam_verts = get_verts_on_seam(F,FTC)
            
    viewer = tcpviewer.TCPViewer()
    viewer.data.set_mesh(V,F)
    for i in seam_verts:
        viewer.data.add_points(igl.eigen.MatrixXd([[V[i,0],V[i,1],V[i,2]]]), igl.eigen.MatrixXd([[1, 0, 0]]))
    
    viewer.launch()