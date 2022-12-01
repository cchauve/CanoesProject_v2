import scripts.models.canoeModel as canoe 
import scripts.BezierSurface as bs
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from ipywidgets import interact, fixed, interact_manual #, interactive
import ipywidgets as widgets
from IPython.display import display

def GetWidgets():
    stepSize = 0.05
    widgetLength = widgets.FloatSlider(min = 4, 
                                 max = 10, 
                                 step = stepSize, 
                                 value = 7.687, 
                                 description = "length (m)", 
                                 continuous_update = False)
    
    widgetWidth = widgets.FloatSlider(min = 0.1, 
                                max = 3, 
                                step = stepSize, 
                                value = 1.250, 
                                description = "width (m)", 
                                continuous_update = False)
    
    widgetHeight = widgets.FloatSlider(min = 0.1, 
                                 max = 3, 
                                 step = stepSize, 
                                 value = 1.135, 
                                 description = "height (m)", 
                                 continuous_update = False)
    
    widgetNames   = widgets.Dropdown(options = [("Nootkan-Style Canoe", 1), ("Haida-Dugout Canoe", 2)],
                              value = 1,
                              description = "Canoe type: ")

    return [widgetLength, widgetWidth, widgetHeight, widgetNames]

def Canoe(widgetLength, widgetWidth, widgetHeight, widgetNames):
    """
    Brings up the ui for the Canoe visualizer
    """
    im = interact_manual.options(manual_name = "refresh")
    im(CanoeGraph, length = widgetLength, width = widgetWidth, height = widgetHeight, canoe_type = widgetNames)

def CanoeGraph(length, width, height, canoe_type):
    """ Takes a length, width, height, and name(type) will properly name next push
    Outputs nothing, but displays the canoe graph
    """
    XX, YY, ZZ = canoe.GetCanoe(length, width, height, canoe_type, 4)
    YY_mirror = np.multiply(YY, -1) #Since we only generate half a canoe
    
    myColor = np.ones(shape = XX.shape)
    #remove axis labels
    trace1 = go.Surface(x=XX, 
                        y=YY, 
                        z=ZZ, 
                        surfacecolor=myColor, 
                        showscale = False, 
                        contours ={"z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}})
    trace2 = go.Surface(x=XX, 
                        y=YY_mirror, 
                        z=ZZ, 
                        surfacecolor=myColor, 
                        showscale = False, 
                        contours ={"z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}})
    
    axisDictionary = dict(title = '', showbackground = False, showgrid = False, showline = False, showticklabels = False)
    sceneDictionary = dict( aspectmode= "data", xaxis = axisDictionary, yaxis = axisDictionary, zaxis = axisDictionary)
    fig = go.Figure(data = [trace1, trace2])
    fig.update_layout(scene = sceneDictionary)
    fig.show()
