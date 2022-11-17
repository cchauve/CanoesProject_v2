import scripts.BezierSurface as bs
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from ipywidgets import interact, fixed, interact_manual #, interactive
import ipywidgets as widgets
from IPython.display import display


def Canoe():
    stepSize = 0.05
    length = widgets.FloatSlider(min = 4, 
                                 max = 10, 
                                 step = stepSize, 
                                 value = 7.687, 
                                 description = "length (m)", 
                                 continuous_update = False)
    
    width = widgets.FloatSlider(min = 0.1, 
                                max = 3, 
                                step = stepSize, 
                                value = 1.250, 
                                description = "width (m)", 
                                continuous_update = False)
    height = widgets.FloatSlider(min = 0.1, 
                                 max = 3, 
                                 step = stepSize, 
                                 value = 1.135, 
                                 description = "height (m)", 
                                 continuous_update = False)
    
    name   = widgets.Dropdown(options = [("Nootkan-Style Canoe", 1), ("Haida-Dugout Canoe", 2)],
                              value = 1,
                              description = "Canoe type: ")
    
    #ui = widgets.HBox([length, width, height, name])
    #out = widgets.interactive_output(CanoeGraph, {"length": length, "width": width, "height": height, "name": name})
    
    #display(ui, out)
    
    widgets.interact_manual(CanoeGraph,
                            length = widgets.FloatSlider(min = 4, 
                                                         max = 10, 
                                                         step = stepSize, 
                                                         value = 7.687, 
                                                         description = "length (m)", 
                                                         continuous_update = False),
                            width = widgets.FloatSlider(min = 0.1, 
                                                        max = 3, 
                                                        step = stepSize, 
                                                        value = 1.250, 
                                                        description = "width (m)", 
                                                        continuous_update = False),
                            height = widgets.FloatSlider(min = 0.1, 
                                                         max = 3, 
                                                         step = stepSize, 
                                                         value = 1.135, 
                                                         description = "height (m)", 
                                                         continuous_update = False),
                            name   = widgets.Dropdown(options = [("Nootkan-Style Canoe", 1), ("Haida-Dugout Canoe", 2)],
                                                      value = 1,
                                                      description = "Canoe type: "))
    

def CanoeGraph(length, width, height, name):
    if   (name == 1):
        P, U, V = GetCanoeA(length, width, height)
    elif (name == 2):
        P, U, V = GetCanoeB()
    else:
        P, U, V = GetCanoeA(length, width, height)
        
    XX, YY, ZZ = bs.GetSurface(P,U,V, 4)
    YY_mirror = np.multiply(YY, -1)
    
    #colorscale = [[0, 'rgb(101, 77, 62 )'],[1, 'rgb(101, 77, 62 )']]
    myColor = np.ones(shape = XX.shape)
    #myColor = (["rgb(101, 77, 62 )"] * len(XX[1])) * len(XX)
    
    #remove axis labels
    trace1 = go.Surface(x=XX, y=YY       , z=ZZ, surfacecolor=myColor, showscale = False, contours ={
        "z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}
    })
    trace2 = go.Surface(x=XX, y=YY_mirror, z=ZZ, surfacecolor=myColor, showscale = False, contours ={
        "z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}
    })
    
    axisDictionary = dict(title = '', showbackground = False, showgrid = False, showline = False, showticklabels = False)
    fig = go.Figure(data = [trace1, trace2])
    fig.update_layout(scene = dict( aspectmode= "data",
                                    xaxis = axisDictionary,
                                    yaxis = axisDictionary,
                                    zaxis = axisDictionary))
    fig.show()

    
def GetCanoeA(length, width, height):
    "Nootkan Style Canoe"
    a = length - 7.687
    b = width/2 - 0.625
    c = height - 1.135
    P = [
        [[-0.011      ,-0.07  - b/4  , 0.560 + c], [0.031      , 0, 0.05 ]],
        [[ 0.81       ,-0.29  - b/3  , 0.440 + c], [0.76       , 0, 0.003]],
        [[ 3.62  + a/2,-0.625 - b    , 0.438 + c], [3.648 + a/2, 0, 0.003]],
        [[ 5.786 + a  ,-0.45  - b*2/3, 0.522 + c], [6.58  + a  , 0, 0.031]],
        [[ 7.037 + a  ,-0.179 - b*3/4, 0.711 + c], [7.217 + a  , 0, 0.387]],
        [[ 7.666 + a  ,-0.087 - b/4  , 1.135 + c], [7.687 + a  , 0, 0.898]]
        ]
    #U is for the inner list direction from p[i][j] to p[i][j+1]
    U = [
        [[-0.0135 ,-0.0016  ,-0.162]  , [0.018  , 0.0315  ,-0.1327]],
        [[ 0.0016 , 0.204   ,-0.274]  , [0.03225, 0.10523 , 0]],
        [[ 0.0135 , 0.33256 ,-0.43211], [0.0171 , 0.41627 , 0]],
        [[ 0.0555 , 0.1092  ,-0.0924] , [0.4066 , 0.16201 ,-0.18854]],
        [[ 0.0477 , 0.086623,-0.07052], [0.0399 , 0.028651,-0.0615]],
        [[ 0.005  , 0.023835,-0.0634] , [0.0073 , 0.018603,-0.05214]]
        ]
    #V is for the inner list direction from p[i][j] to p[i+1][j]
    V = [
        [[0.35863, 0.02412,-0.05928], [0.27386, 0,-0.034092]],
        [[0.5837 ,-0.15418,-0.01687], [0.2287 , 0,-0.0004]],
        [[0.7903 , 0.0032 , 0.01415], [1.2589 , 0,-0.002416]],
        [[0.6115 , 0.09908, 0.04867], [0.5394 , 0, 0.014912]],
        [[0.1913 , 0.05291, 0.06429], [0.192  , 0, 0.29091]],
        [[0.1947 , 0.0002 , 0.278]  , [0.1251 , 0, 0.09059]]
        ]
    return P, U, V

def GetCanoeB(length, width, height):
    "Haida Style Canoe"
    a = length - 6.4268
    b = width/2 - 0.50708
    c = height - 0.84752
    P = [
        [[0.007417      ,-0.046391 - b/4, 0.77212 + c], [0.050118      , 0, 0.57692 + c/2]],
        [[1.7351 + a*1/4,-0.47607  - b  , 0.47695 + c], [1.7434 + a*1/4, 0, 0.00738]],
        [[4.2141 + a*3/4,-0.50708  - b  , 0.48305 + c], [4.2206 + a*3/4, 0, 0.00738]],
        [[5.2557 + a    ,-0.36251  - b  , 0.61488 + c], [5.26   + a    , 0, 0.16842 + c/4]],
        [[6.4268 + a    ,-0.054097 - b/4, 0.84752 + c], [6.4406 + a    , 0, 0.63492 + c/2]],
        ]
    
    U = [
        [[ 0.000697, 0.049124,-0.05085] ,[0.044547, 0       ,-0.11851]],
        [[ 0.116   ,-0.02094 ,-0.397862],[0.006   , 0.21516 , 0]],
        [[ 0.0053  , 0.02237 ,-0.532096],[0.0011  , 0.090214, 0]],
        [[-0.1482  , 0.18592 ,-0.28189] ,[0.0304  , 0.046367,-0.0065]],
        [[ 0.0053  , 0.019512,-0.07584] ,[0.0041  , 0.021945,-0.07558]],
        ]
    
    V = [
        [[0.904683,-0.303729,-0.2168] ,[0.707182, 0,-0.57627]],
        [[0.5388  ,-0.02837 ,-0.02648],[1.4813  , 0,-0.017136]],
        [[0.5377  , 0.02269 , 0.04749],[0.9418  , 0, 0.014674]],
        [[0.3491  , 0.10417 , 0.05709],[0.0041  , 0, 0.14552]],
        [[0.3539  , 0.079448, 0.06641],[0.1553  , 0, 0.34577]],
        ]
    return P, U, V