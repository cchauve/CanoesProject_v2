import plotly.graph_objects as go
import numpy as np
import scripts.visualization as vs
GLOBAL_WaterDensity = 997     #(kg / m^3)
GLOBAL_Gravity      = 9.80665 #(m/s^2)

def GetSideTrace(height, length, c, type, resolution):
    """
    Gets the side profile of our canoe and returns the scatter plot trace of it
    """
    X_side, Z_side = GetSideData(height, length, c, type, resolution)
    sideTrace = go.Scatter(
        visible = False,
        line = dict(color = "#141414", width = 3),
        x = X_side, 
        y = Z_side
    )
    return sideTrace

def GetSideData(height, length, c, type, resolution):
    """
    Gets the data of the side trace.
    """
    if type==3:
        a, b = np.linspace(0.01, np.pi-0.01, resolution), np.linspace(np.pi/2, (3/2)*np.pi, resolution)
    else:
        a, b = np.linspace(0.0, 2*np.pi, resolution), np.linspace(np.pi/2, (3/2)*np.pi, resolution)
    
    X_side = vs.x_coordinates(length, a)
    Z_side = vs.z_coordinates(height, c, a, b, type)
    
    return X_side, Z_side

def GetXYZ(width, height, length, c, type, resolution = 32):
    """
    Gets the Surface of our canoe, in X,Y,Z form
    """
    a, b = vs.get_eta_theta(type)
    
    X = vs.x_coordinates(length, a)
    Y = vs.y_coordinates(width , c, a, b, type)
    Z = vs.z_coordinates(height, c, a, b, type)
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
