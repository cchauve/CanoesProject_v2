import scripts.BezierSurface as bs
import plotly.graph_objects as go
import numpy as np

from ipywidgets import interact, fixed, interact_manual #, interactive
import ipywidgets as widgets
from IPython.display import display

"""
NOOTKAN-STYLE CANOE
in metric (m)
"""
def CanoeA():
    """
    UI FOR CANOE GRAPH A
    """
    return 0
    
def CanoeGraphA():
    P, U, V = GetCanoeA()
    XX, YY, ZZ = bs.GetSurface(P,U,V, 8)
    YY_mirror = np.multiply(YY, -1)
    
    
    fig = go.Figure()
    fig.add_trace(go.Surface(x=XX, y=YY, z=ZZ, contours ={
        "z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}
    }))
    fig.add_trace(go.Surface(x=XX, y=YY_mirror, z=ZZ, contours ={
        "z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}
    }))
    
    fig.update_layout(scene = dict(
        aspectmode='data'
    ))
    fig.show()
    
def GetCanoeA():
    P = [
        [[-0.011, -0.07, 0.56] , [0.031, 0, 0.05]],
        [[0.81, -0.29, 0.44]   , [0.76, 0, 0.003]],
        [[3.62, -0.625, 0.438] , [3.648, 0, 0.003]],
        [[5.786, -0.45, 0.522] , [6.58, 0 , 0.031]],
        [[7.037, -0.179, 0.711], [7.217, 0, 0.387]],
        [[7.666, -0.087, 1.135], [7.687, 0, 0.898]]
        ]
    #U is for the inner list direction from p[i][j] to p[i][j+1]
    U = [
        [[-0.0135, -0.0016, -0.162]  , [0.018, 0.0315, -0.1327]],
        [[0.0016, 0.204, -0.274]     , [0.03225, 0.10523, 0]],
        [[0.0135, 0.33256, -0.43211] , [0.0171, 0.41627, 0]],
        [[0.0555, 0.1092, -0.0924]   , [0.4066, 0.16201, -0.18854]],
        [[0.0477, 0.086623, -0.07052], [0.0399, 0.028651, -0.0615]],
        [[0.005, 0.023835, -0.0634]  , [0.0073,0.018603,-0.05214]]
        ]
    #V is for the inner list direction from p[i][j] to p[i+1][j]
    V = [
        [[0.35863, 0.02412, -0.05928], [0.27386, 0, -0.034092]],
        [[0.5837, -0.15418, -0.01687], [0.2287, 0, -0.0004]],
        [[0.7903, 0.0032, 0.01415]   , [1.2589, 0, -0.002416]],
        [[0.6115, 0.09908, 0.04867]  , [0.5394, 0, 0.014912]],
        [[0.1913, 0.05291, 0.06429]  , [0.192, 0, 0.29091]],
        [[0.1947, 0.0002, 0.278]     , [0.1251,0,0.09059]]
        ]
    return P, U, V