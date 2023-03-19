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
    #XX, YY, ZZ = canoe.GetCanoe(length, width, height, canoe_type, 4)
    f2str = lambda x:  "{:.4f}".format(x)
    titleStr = "Length: " + f2str(length) + "(m)\twidth: " + f2str(width) + "(m)\theight: " + f2str(height) +"(m)" 
    color = "#734e32"
        
    x, y, z, dx, dy, dz = Canoe_To_List(length, width, height, canoe_type, 4)
    
    mesh = lambda X,Y,Z: go.Mesh3d(
        x = X, y = Y, z = Z,
        i = dx, j = dy, k = dz,
        color = color,
        lighting = dict(diffuse = 0.8, ambient = 0.5, fresnel = 5, roughness = 0.6),
        lightposition = dict(x = length/2, y = width + 5, z = height + 3)
    )
    normal_meshTrace = mesh(x, y                , z)
    mirror_meshTrace = mesh(x, np.multiply(y,-1), z)

    fig = go.Figure(data=[normal_meshTrace, mirror_meshTrace])
    axisDictionary = dict(title = '', showbackground = False, showgrid = False, showline = False, showticklabels = False)
    sceneDictionary = dict( aspectmode= "data", xaxis = axisDictionary, yaxis = axisDictionary, zaxis = axisDictionary)
    fig.update_layout(scene = sceneDictionary, title = titleStr,  width = 1280, height = 720)
    fig.show()
    
    """
    YY_mirror = np.multiply(YY, -1) #Since we only generate half a canoe
    myColor = np.ones(shape = XX.shape)

    #remove axis labels
    surface = lambda surf_X,surf_Y,surf_Z:go.Surface(
        x=surf_X,
        y=surf_Y,
        z=surf_Z,
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
    """

def Canoe_To_List(length, width, height, canoe_type, res):
    XX, YY, ZZ = canoe.GetCanoe(length, width, height, canoe_type, res)

    grid_size = len(XX)*len(XX[0])
    grid_XX0 = len(XX[0])
    point_x = [0]*grid_size
    point_y = [0]*grid_size
    point_z = [0]*grid_size
    for i in range(len(XX)):
        for j in range(grid_XX0):
            index = i*grid_XX0 + j
            point_x[index] = XX[i][j]
            point_y[index] = YY[i][j]
            point_z[index] = ZZ[i][j]
    dx = [0]*(grid_size*2)
    dy = [0]*(grid_size*2)
    dz = [0]*(grid_size*2)
    triangle = 0
    for i in range(len(XX)-1):
        for j in range(grid_XX0-1):
            dx[triangle] = i    *grid_XX0 + j
            dy[triangle] = i    *grid_XX0 + j + 1
            dz[triangle] = (i+1)*grid_XX0 + j + 1
            triangle += 1
            dx[triangle] = i    *grid_XX0 + j 
            dy[triangle] = (i+1)*grid_XX0 + j + 1
            dz[triangle] = (i+1)*grid_XX0 + j
            triangle += 1

    return point_x, point_y, point_z, dx, dy, dz