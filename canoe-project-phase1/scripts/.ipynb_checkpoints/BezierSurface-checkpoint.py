from math import sqrt, isnan
import numpy as np

"""
This script is for generating the surface points of the bezier surface.
"""
def GetSurface(P, U, V, n):
    """
    Takes in P, U, V as 2D arrays of vectors (Both the same size), n resolution of each "tile" since this can be rectangular.
    P,U,V = [
        [[x,y,z], [x,y,z]],
        [[x,y,z], [x,y,z]]
    ]
    P - is points
    U is direction along the i'th direction P[j][i]
    V is direction along the j'th direction P[j][i]
    (P).-> (U) -  -  -  (P).->(U)
       |                   |
       v (V)               v(V)
       |                   |
    (P).-> (U) -   -  - (O).->(U)
       |                   |
       v (V)               v(V)
    """
    uTiles = 2 #len(P[0])
    vTiles = 3 #len(P)
    #adding one for the included endpoint, all numbers repeat mod 1
    S,T = np.meshgrid(np.linspace(0, 1, n+1, endpoint = True), np.linspace(0, 1, n+1, endpoint = True)) 
    print(X)
    #XX, YY = function that partitions the grid into section
    for i in range(0, uTiles - 1):
        for j in range(0, vTiles - 1):
            #to avoid methods with 5+ inputs, we will keep the 4 fold nested for loop.
            # S,T[j][i]
            # U goes in i'th direction
            # V goes in j'th direction
            # for loop in range [0, 1, 2, ... n - 1]
            uOffset = i*n
            vOffset = j*n
            
            for u in range(0, n):
                point00, point01, point10, point11 = P[j][i], P[j][i + 1], P[j + 1][i], P[j + 1][i + 1]
                
                v0Handle = Interpolate2(, )
                v1Handle = 
                for v in range(0, n):
                    
            
            
    #return XX, YY
    
def Interpolation4(A,B,C,D, t):
    A0 = np.multiply(A, -1*t**3 + 3*t**2 - 3*t + 1)
    B0 = np.multiply(B,  3*t**3 - 6*t**2 + 3*t
    C0 = np.multiply(C, -3*t**3 + 3*t**2
    D0 = np.multiply(D,  3*t**3)
    return A0 + B0 + C0 + D0 #arrays can add onto eachother nicely.

def Interpolation2(A, B, t):
    A0 = np.multiply(A, -t + 1)
    B0 = np.multiply(B,  t)
    return A0 + B0
    