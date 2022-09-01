import plotly.graph_objects as go
import numpy as np
import scripts.visualization as vs
GLOBAL_WaterDensity = 997     #(kg / m^3)
GLOBAL_Gravity      = 9.80665 #(m/s^2)

def GetSideTrace(height, length, c, canoe_type, resolution):
    """
    Gets the side profile of our canoe and returns the scatter plot trace of it
    """
    X_side, Z_side = GetSideData(height, length, c, canoe_type, resolution)
    sideTrace = go.Scatter(
        visible = False,
        line = dict(color = "#141414", width = 3),
        x = X_side, 
        y = Z_side
    )
    return sideTrace

def GetSideData(height, length, c, canoe_type, resolution):
    """
    Gets the data of the side trace.
    """
    X_side, Y_side, Z_side = GetXYZ(1, height, length, c, canoe_type, resolution)
        
    X = [0]*resolution
    Z = [0]*resolution
    
    if (canoe_type == 1):
        for i in range(0, resolution):
            X[i] = X_side[int(resolution/2)][i]
            Z[i] = Z_side[i][int(resolution/2)]
    else:
        for i in range(0, resolution):
            X[i] = X_side[int(resolution/2)][i]
            Z[i] = Z_side[int(resolution/2)][i]
    
    return X, Z
    
def GetXYZ(width, height, length, c, canoe_type, resolution = 32):
    """
    Gets the Surface of our canoe, in X,Y,Z form
    """
    a, b = vs.get_eta_theta(canoe_type)
    
    X = vs.x_coordinates(length, a)
    Y = vs.y_coordinates(width , c, a, b, canoe_type)
    Z = vs.z_coordinates(height, c, a, b, canoe_type)
    return X, Y, Z

def GetLevelTrace(level, length):
    """
    Gets the trace of where the water level is
    """
    sideTrace = go.Scatter(
        visible = False,
        line = dict(color = "#1991df", width = 3),
        x = [-2*length, 2*length], 
        y = [level, level]
    )
    return sideTrace

