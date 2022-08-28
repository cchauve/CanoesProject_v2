import plotly.graph_objects as go
import numpy as np
GLOBAL_WaterDensity = 997     #(kg / m^3)
GLOBAL_Gravity      = 9.80665 #(m/s^2)


def rotate(x, y, theta):
    return x*np.cos(theta)-y*np.sin(theta), x*np.sin(theta) + y*np.cos(theta)

def GetDiagram(length, height, theta):
    X0 = [1,1,-1,-1,1]
    Y0 = [1,-1,-1,1,1]
    
    X0 = np.multiply(X0, length)
    Y0 = np.multiply(Y0, height)
    
    X1 = np.subtract(np.multiply(X0, np.cos(theta)), np.multiply(Y0, np.sin(theta))) #rotates
    Y1 = np.add(     np.multiply(X0, np.sin(theta)), np.multiply(Y0, np.cos(theta)))
    
    X2, A = GetIntersection(X1, Y1)
    
    X_cubeP = [0]*5
    Y_cubeP = [0]*5
    X_waterP = [0]*5
    Y_waterP = [0]*5
    if (A[0] < 0 and Y1[1] <= 0):
        X_waterP = [X2[0], X1[1], X1[2], X2[2], X2[0]]
        Y_waterP = [0    , Y1[1], Y1[2], 0    , 0    ]
        
        X_cubeP = [X2[0], X2[2], X1[3], X1[0], X2[0]]
        Y_cubeP = [0    , 0    , Y1[3], Y1[0], 0    ]
        
    if (A[1] < 0 and Y1[2] <= 0):
        X_waterP = [X2[1], X1[2], X1[3], X2[3], X2[1]]
        Y_waterP = [0    , Y1[2], Y1[3], 0    , 0    ]
                                
        X_cubeP = [X2[1], X2[3], X1[0], X1[1], X2[1]]
        Y_cubeP = [0    , 0    , Y1[0], Y1[1], 0    ]
    
    if (A[2] < 0 and Y1[3] <= 0):
        X_waterP = [X2[2], X1[3], X1[0], X2[0], X2[2]]
        Y_waterP = [0    , Y1[3], Y1[0], 0    , 0    ]
                    
        X_cubeP = [X2[2], X2[0], X1[1], X1[2], X2[2]]
        Y_cubeP = [0    , 0    , Y1[1], Y1[2], 0    ]
    
    if (A[3] < 0 and Y1[4] <= 0):
        X_waterP = [X2[3], X1[0], X1[1], X2[1], X2[3]]
        Y_waterP = [0    , Y1[0], Y1[1], 0    , 0    ]
                    
        X_cubeP = [X2[3], X2[1], X1[2], X1[3], X2[3]]
        Y_cubeP = [0    , 0    , Y1[2], Y1[3], 0    ]
    
    
    return X_cubeP, Y_cubeP, X_waterP, Y_waterP

def GetIntersection(X1, Y1):
    X2 = [0]*4
    A = [0]*4
    for i in range(0, 4):
        if (Y1[i]-Y1[i+1] != 0):
            X2[i] = X1[i]-Y1[i] * (X1[i]-X1[i+1])/(Y1[i]-Y1[i+1])
        A[i] = Y1[i]*Y1[i+1]
    return X2, A

def GetTrace(length, height, theta):
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