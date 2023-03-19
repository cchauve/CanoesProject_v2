import scripts.models.canoeModel as canoe 
import plotly.graph_objects as go
import numpy as np

from ipywidgets import interact_manual 
import ipywidgets as widgets

def GetWidgets():
    """
    Returns the widgets needed for interactability.\\
    return [widgetLength, widgetWidth, widgetHeight, widgetNames]
    """
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


def Canoe(widgetLength, widgetWidth, widgetHeight, widgetNames):
    """
    Ultimate UI call for the canoe Graph,\\
    Takes in the widgets respective widgets from GetWidgets and runs displays the 3d mesh of the canoe.
    """ 
    im = interact_manual.options(manual_name = "refresh")
    args = {"length":widgetLength, "width": widgetWidth, "height":widgetHeight, "canoe_type":widgetNames}
    im(CanoeGraph, **args)


def CanoeGraph(length, width, height, canoe_type):
    """ 
    Displays the canoe graph\\
    takes a length, width, height and canoe type(integer).\\
    Will display the canoe type with the respective properties.
    """
    f2str = lambda x:  "{:.4f}".format(x)
    titleStr = "Length: " + f2str(length) + "(m)\twidth: " + f2str(width) + "(m)\theight: " + f2str(height) +"(m)" 
    color = "#734e32"
        
    x, y, z, dx, dy, dz = Canoe_To_List(length, width, height, canoe_type, 4)
    
    mesh = lambda X,Y,Z: go.Mesh3d(
        x = X, y = Y, z = Z,
        i = dx, j = dy, k = dz,
        color = color,
        lighting = dict(diffuse = 1, ambient = 0.5, fresnel = 5, roughness = 0.7),
        lightposition = dict(x = length/2, y = width + 5, z = height + 3)
    )
    normal_meshTrace = mesh(x, y                , z)
    mirror_meshTrace = mesh(x, np.multiply(y,-1), z)

    fig = go.Figure(data=[normal_meshTrace, mirror_meshTrace])
    axisDictionary = dict(title = '', showbackground = False, showgrid = False, showline = False, showticklabels = False)
    sceneDictionary = dict( aspectmode= "data", xaxis = axisDictionary, yaxis = axisDictionary, zaxis = axisDictionary)
    fig.update_layout(scene = sceneDictionary, title = titleStr,  width = 1280, height = 720)
    fig.show()
    

def Canoe_To_List(length, width, height, canoe_type, res):
    """
    A helper script that will take our surface array of points\\
    from the canoe script and transforms them into a list for\\
    the go.Mesh3d, along with the triangulizations\\
    returns point_x, point_y, point_z, dx, dy, dz
    """
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