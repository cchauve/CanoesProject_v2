from math import sqrt, isnan
import numpy as np

"""
This script is for generating the surface points of the bezier surface.
"""
"""
    Takes in P, U, V as 2D arrays of vectors (Both the same size), n resolution of each "tile" since this can be rectangular.
    Returns XX, YY, ZZ 2d arrays of where each point of the grid lies.
    P,U,V = [
        [[x,y,z], [x,y,z]],
        [[x,y,z], [x,y,z]]
    ]
    P - is points
    V is direction along the i'th direction P[i][ ] \/
    U is direction along the j'th direction P[ ][j] ->
    
    (P).-> (U) -  -  -  (P).->(U) -   -   -  
       |                   |
       v (V)   P[0,0]      v(V)          P[0,1]
       |                   |
    (P).-> (U) -   -  - (P).->(U)  -  -   -
       |                   |
       v (V)   P[1,0]      v(V)
    """
def GetSurface(p, u, v, n):
    P = np.array(p)
    U = np.array(u)
    V = np.array(v)
    
    #an intialized point tile. This allows us to simplify some math
    M = [[[0]*3 for i in range(4)] for i in range(4)]
    columns = len(P[0])-1 #columns of P
    rows = len(P)-1       #ros of P,
    
    #adding one for the included endpoint, all numbers repeat mod 1, we sample our t points from this instead of calculating them
    T = np.linspace(0, 1, n+1*0, endpoint = True)
    
    rowsLinspace = np.linspace(0, 1*rows   , n*rows    + 1*0, endpoint = True)
    colsLinspace = np.linspace(0, 1*columns, n*columns + 1*0, endpoint = True)
    XX, YY    = np.meshgrid(colsLinspace, rowsLinspace)
    ZZ, dummy = np.meshgrid(colsLinspace, rowsLinspace)
    
    #FILL IN FROM TOP TO BOTTOM USING THE TOP LINES
    for i in range(0, rows):
        for j in range(0, columns):
            #for each tile, generate the grid in it.
            #Corner points.
            M[0][0] = P[i  ][ j  ]
            M[0][3] = P[i  ][ j+1]
            M[3][0] = P[i+1][ j  ]
            M[3][3] = P[i+1][ j+1]
            #Border points.
            M[0][1] = M[0][0] + U[i  ][ j  ]
            M[0][2] = M[0][3] - U[i  ][ j+1]
            M[3][1] = M[3][0] + U[i+1][ j  ]
            M[3][2] = M[3][3] - U[i+1][ j+1]

            M[1][0] = M[0][0] + V[i  ][ j  ]
            M[2][0] = M[3][0] - V[i+1][ j  ]
            M[1][3] = M[0][3] + V[i  ][ j+1]
            M[2][3] = M[3][3] - V[i+1][ j+1]
            #Center points.
            M[1][1] = M[0][1] + V[i  ][ j  ]
            M[1][2] = M[0][2] + V[i  ][ j+1]
            M[2][1] = M[3][1] - V[i+1][ j  ]
            M[2][2] = M[3][2] - V[i+1][ j+1]
            #print(M)
            for t in range(0, n):
                for s in range(0, n): 
                    point = BSurf(M, T[t],T[s])
                    #print(point)
                    XX[i*n+s][j*n+t] = point[0]
                    YY[i*n+s][j*n+t] = point[1]
                    ZZ[i*n+s][j*n+t] = point[2]
              
    return XX, YY, ZZ
    

"""
Takes in points A,B,C,D
and a interpolation value t in [0,1] range.

Outputs a point in the same dimension
"""
def BCurve(A,B,C,D, t):
    
    A0 = np.multiply(A, Bweights(1,t))
    B0 = np.multiply(B, Bweights(2,t))
    C0 = np.multiply(C, Bweights(3,t))
    D0 = np.multiply(D, Bweights(4,t))
    return A0 + B0 + C0 + D0 #arrays can add onto eachother nicely.

def BSurf(M, t,s):
    point = np.array([0]*3)
    for i in range (0,4):
        point = np.add(point, np.multiply(BCurve(M[i][0], M[i][1], M[i][2], M[i][3], t) , Bweights(i+1, s)))
    return point

def Bweights(weightNumber, t):
    if (weightNumber == 1): return -1*t**3 + 3*t**2 - 3*t + 1
    if (weightNumber == 2): return  3*t**3 - 6*t**2 + 3*t
    if (weightNumber == 3): return -3*t**3 + 3*t**2
    return                          1*t**3

"""
A linear interpolation between A and B
using the interpolation value t in [0,1] range.

Outputs a point in the same dimension
TECHNICALLY NOT NEEDED, MIGHT REMOVE.
"""
def Lerp(A, B, t):
    A0 = np.multiply(A, -t + 1)
    B0 = np.multiply(B,  t)
    return A0 + B0
    