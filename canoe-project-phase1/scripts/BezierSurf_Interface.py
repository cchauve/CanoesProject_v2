import scripts.models.canoeModel as canoe 
import scripts.BezierSurface as bs
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from ipywidgets import interact, fixed, interact_manual #, interactive
import ipywidgets as widgets
from IPython.display import display

def GetWidgets():
    widgetMaker = lambda min_size,max_size,de: widgets.FloatSlider(
        min=min_size,
        max=max_size,
        step=(max_size-min_size)/128,
        value=(max_size+min_size)/2,
        continuous_update=False,
        description=de)

    widgetLength = widgetMaker(4,10,"length (m)")
    widgetWidth  = widgetMaker(0.5,1.5,"width (m)")
    widgetHeight = widgetMaker(0.25,1.25,"height (m)")

    canoeOptions = [("Nootkan-Style Canoe", 1), ("Haida-Dugout Canoe", 2), ("Kutenai Canoe",3)]
    widgetNames = widgets.Dropdown(options = canoeOptions, value = 3, description = "Canoe type: ")
    return [widgetLength, widgetWidth, widgetHeight, widgetNames]

"""
    Brings up the ui for the Canoe visualizer
"""
def Canoe(widgetLength, widgetWidth, widgetHeight, widgetNames):
    
    im = interact_manual.options(manual_name = "refresh")
    args = {"length":widgetLength, "width": widgetWidth, "height":widgetHeight, "canoe_type":widgetNames}
    im(CanoeGraph, **args)

""" Plots the canoe_type, with the given scaling
scale      - [float, float, float]
canoe_type - integer 

"""
def CanoeGraph(length, width, height, canoe_type):
    """ Takes a length, width, height, and name(type) will properly name next push
    Outputs nothing, but displays the canoe graph
    """
    XX, YY, ZZ = canoe.GetCanoe(length, width, height, canoe_type, 8)
    f2str = lambda x:  "{:.4f}".format(x)
    titleStr = "Length: " + f2str(length) + "(m)\twidth: " + f2str(width) + "(m)\theight: " + f2str(height) +"(m)" 
        
    YY_mirror = np.multiply(YY, -1) #Since we only generate half a canoe
    myColor = np.ones(shape = XX.shape)
    
    #remove axis labels
    surface = lambda X,Y,Z:go.Surface(
        x=X,
        y=Y,
        z=Z,
        surfacecolor=myColor,
        showscale= False,
        contours={"z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}}
    ) 
    trace1 = surface(XX,YY,ZZ)
    trace2 = surface(XX,YY_mirror,ZZ)
    
    axisDictionary = dict(title = '', showbackground = False, showgrid = False, showline = False, showticklabels = False)
    sceneDictionary = dict( aspectmode= "data", xaxis = axisDictionary, yaxis = axisDictionary, zaxis = axisDictionary)
    fig = go.Figure(data = [trace1, trace2])
    fig.update_layout(scene = sceneDictionary, title = titleStr,  width = 1080, height = 720)
    fig.show()
