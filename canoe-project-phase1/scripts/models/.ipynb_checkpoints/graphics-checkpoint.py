import numpy as np
import plotly.graph_objects as go

def GetArrow(x, y, direction, magnitude, arrowSize, arrowAngle = 0.7):
    """ returns the polygon points for the arrow
    takes and x and y origin, direction [x0,y0], magnitude, and arrow size
    """
    normalizedD = np.multiply(direction , 1/np.sqrt(direction[0]**2 + direction[1]**2))
    rotatedN   = np.multiply(Rotate(normalizedD, np.pi - arrowAngle), arrowSize)
    reRotatedN = np.multiply(Rotate(normalizedD, np.pi + arrowAngle), arrowSize)
    
    tip = np.add([x, y],np.multiply(normalizedD, magnitude))
    X = [x, tip[0], tip[0] + rotatedN[0], tip[0] + reRotatedN[0], tip[0]]
    Y = [y, tip[1], tip[1] + rotatedN[1], tip[1] + reRotatedN[1], tip[1]]
    
    return X, Y

def Rotate(vector, theta):
    """
    rotates [x,y] around the origin by theta (in radians)
    """
    x, y = vector[0], vector[1]
    return [x*np.cos(theta)-y*np.sin(theta), x*np.sin(theta) + y*np.cos(theta)]

def GetTrace(x, y, direction, magnitude, arrowSize, arrowAngle = 0.7):
    """
    Gets the scatter plot trace of the arrow. Takes and x y position of origin, direction (doesnt need to be normalized)
    an arrow size, and arrow angle in radians the angle from left to right of the point /\
    """
    X , Y = GetArrow(x,y, direction, magnitude, arrowSize, arrowAngle)
    scatter_Arrow = go.Scatter(
        visible = False,
        line = dict(color = "#141414", width = 3),
        mode = "lines",
        x = X,
        y = Y
    )
    
    return scatter_Arrow
    