"""EXPERIMENTAL"""

from matplotlib import pyplot as plt
import numpy as np
import plotly.graph_objs as go



def Weight(t, n : int): 
    #switch case only in python 3.10+ (or in pythons situation Match case)
    if n == 1: return -1*pow(t,3) + 3*pow(t,2) - 3*t+1
    if n == 2: return  3*pow(t,3) - 6*pow(t,2) + 3*t
    if n == 3: return -3*pow(t,3) + 3*pow(t,2)
    if n == 4: return    pow(t,3)

    return 0

def BCurve(A, B, C, D, t):
    return A * Weight(t,1) + B * Weight(t,2) + C * Weight(t,3) + D * Weight(t,4)

def BezierSurface(A, B, C, D, N):
    # Handles are the tangent vector of the surface at that point (might have mixed up t and s, need to rewrite later)
    #                A->B       A -> C
    #     [[point], [tHandle], [sHandle]]
    # A = [[x,y,z], [x,y,z]  , [x,y,z]  ]
    
    N = 32
    t,s = np.meshgrid(np.linspace(0, 1, N), np.linspace(0, 1, N))

    X = np.meshgrid(np.linspace(0, 0, N), np.linspace(0, 0, N))[0]
    Y = np.meshgrid(np.linspace(0, 0, N), np.linspace(0, 0, N))[0]
    Z = np.meshgrid(np.linspace(0, 0, N), np.linspace(0, 0, N))[0]
    surf = [X,Y,Z]

    #   <-----t----->
    # A --------------- B   /\
    # |     |      |    |   |
    # AC--AC_h---BD_h---BD  s
    # |     |      |    |   |
    # C --------------- D  \/
    #

    for d in [0,1,2]:  
        for i in range(0,N):
            for j in range(0,N):
                AC   = BCurve(A[0][d]          , A[0][d] +           A[2][d], C[0][d] +           C[2][d], C[0][d]          , s[i][j])
                AC_h = BCurve(A[0][d] + A[1][d], A[0][d] + A[1][d] + A[2][d], C[0][d] + C[1][d] + C[2][d], C[0][d] + C[1][d], s[i][j]) 
                BD_h = BCurve(B[0][d] + B[1][d], B[0][d] + B[1][d] + B[2][d], D[0][d] + D[1][d] + D[2][d], D[0][d] + D[1][d], s[i][j])
                BD   = BCurve(B[0][d]          , B[0][d] +           B[2][d], D[0][d] +           D[2][d], D[0][d]          , s[i][j])

                surf[d][i][j] = BCurve(AC, AC_h, BD_h, BD, t[i][j]) 
    
    return surf

