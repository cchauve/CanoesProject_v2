"""
===============================
     T O   D E P R E C A T E
===============================
"""
import plotly.graph_objects as go
import numpy as np
GLOBAL_WaterDensity = 997     #(kg / m^3)
GLOBAL_Gravity      = 9.80665 #(m/s^2)


def rotate(x, y, theta):
    """
    rotates (x,y) around the origin by theta (in radians)
    """
    return x*np.cos(theta)-y*np.sin(theta), x*np.sin(theta) + y*np.cos(theta)

def GetDiagram(length, height, theta):
    """
    Gets the list of points in connecting order for both cube and water
    """
    X0 = [1,1,-1,-1,1]
    Y0 = [1,-1,-1,1,1]
    bound = np.sqrt(length**2 + height**2)*2
    
    X0 = np.multiply(X0, length)
    Y0 = np.multiply(Y0, height)
    
    X1, Y1 = rotate(X0, Y0, theta) #rotates
    
    X2, A = GetIntersection(X1, Y1)
    
    X_cubeP = [0]*5
    Y_cubeP = [0]*5
    X_waterP = [0]*5
    Y_waterP = [0]*5
    
    for i in range(0, 4):
        if (A[i] < 0 and Y1[i+1] <= 0):
            X_waterP = [X2[i], X1[(i+1)%4], X1[(i+2)%4], X2[(i+2)%4], None, -bound, bound]
            Y_waterP = [0    , Y1[(i+1)%4], Y1[(i+2)%4], 0          , None, 0     , 0    ]

            X_cubeP = [X2[i], X2[(i+2)%4], X1[(i+3)%4], X1[i], X2[i]]
            Y_cubeP = [0    , 0          , Y1[(i+3)%4], Y1[i], 0    ]
            return X_cubeP, Y_cubeP, X_waterP, Y_waterP
    return None    
    
def GetIntersection(X1, Y1):
    """
    Retrieves the intersection point of (X1,Y1) with the X axis
    Also gets the activators for whether or not the intersection should be used
    """
    X2 = [0]*4
    A = [0]*4
    for i in range(0, 4):
        if (Y1[i]-Y1[i+1] != 0):
            X2[i] = X1[i]-Y1[i] * (X1[i]-X1[i+1])/(Y1[i]-Y1[i+1])
        A[i] = Y1[i]*Y1[i+1]
    return X2, A

def GetTrace(length, height, theta):
    """
    Gets the Scatter plot of the points and the lines joining them for both the cube and water
    plots
    """
    X_cube , Y_cube, X_water, Y_water = GetDiagram(length, height, theta)
    scatter_cube = go.Scatter(
        visible = False,
        line = dict(color = "#141414", width = 3),
        #name = "w = " + str(waterLevel),
        x = X_cube,
        y = Y_cube
    )
    scatter_water = go.Scatter(
        visible = False,
        line = dict(color = "#1991df", width = 3),
        x = X_water,
        y = Y_water,
    )
    return scatter_cube, scatter_water

def GetArea(X, Y):
    """
    Gets the area of a (X,Y) square (REDUNDANT AS WE CUT A SQUARE IN HALF RESULTING IN HALF THE AREA)
    """
    # 0-------1
    # \       \
    # \       \
    # 3-------2
    U = [X[1] - X[0], X[2] - X[0]]
    V = [Y[1] - Y[0], Y[2] - Y[0]]
    
    A = U[0]*V[1] - U[1]*V[0] #012 trapezoid
    
    U = [X[2] - X[0], X[3] - X[0]]
    V = [Y[2] - Y[0], Y[3] - Y[0]]
    
    B = U[0]*V[1] - U[1]*V[0] #023 trapezoid
    
    return (abs(A) + abs(B))/2.0