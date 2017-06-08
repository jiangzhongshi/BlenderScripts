#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 23:28:48 2017

@author: zhongshi
"""

import pyigl as igl

import tcpviewer

TUTORIAL_SHARED_PATH = "/Users/zhongshi/Desktop/"

# Read a mesh
V = igl.eigen.MatrixXd()
F = igl.eigen.MatrixXi()

igl.readOBJ(TUTORIAL_SHARED_PATH + "animal_low.obj", V, F)

gamma = set()

D = []
n = V.rows()
sF = F.rows()

DblArea = igl.eigen.VectorXd()
igl.doublearea(V,F,DblArea)
AM = DblArea.sum()/2

t = 5 * AM / sF

# cot matrix
L = igl.eigen.SparseMatrixd()
igl.cotmatrix(V,F,L)

M = igl.eigen.SparseMatrixd()
igl.massmatrix(V,F,igl.MASSMATRIX_TYPE_BARYCENTRIC,M)

u0 = igl.eigen.MatrixXd([0 for i in range(1,n)])
for i in gamma:
    u0[i] = 1
    
Q = M - t*L
B = M*u0

'''
        b = unique(reshape(outline(F),[],1));
         bc = -1*ismember(out,gamma);
         [uD,pre.D] = min_quad_with_fixed(Q,B,b,bc,[],[],pre.D);
                 [uN,pre.N] = min_quad_with_fixed(Q,B,[],[],[],[],pre.N);

      u = 0.5*(uN+uD);
      
  % Evaluate the vector field X
  G = grad(V,F);
  Div = div(V,F);
  grad_u = reshape(G*u,size(F,1),size(V,2));
  grad_u_norm = sqrt(sum(grad_u.^2,2));
  
  % normalize grad_u
  normalized_grad_u = bsxfun(@rdivide,grad_u,grad_u_norm);
  % correct any zero-norm gradients
  normalized_grad_u(grad_u_norm == 0,:) = 0;
  % reverse direction
  X = -normalized_grad_u;

  % Solve the Poisson equation 
  % divergence of X
  div_X = Div*X(:);
  
  [phi,pre.poisson] = ...
  min_quad_with_fixed(-L,div_X,[],[],[],[],pre.poisson);
  D = phi;
  % "Note that ???? is unique only up to an additive constant and should be
  % shifted such that the smallest distance value is zero."
  D = D - min(D(:));
'''

