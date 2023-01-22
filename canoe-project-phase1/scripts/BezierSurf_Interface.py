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
    widgetMaker = lambda de: widgets.FloatSlider(
        min=0.05,
        max=2.0,
        step=0.05,
        value=1,
        continuous_update=False,
        description=de)

    widgetLengthScale = widgetMaker("length scale")
    widgetWidthScale  = widgetMaker("width scale")
    widgetHeightScale = widgetMaker("height scale")

    canoeOptions = [("Nootkan-Style Canoe", 1), ("Haida-Dugout Canoe", 2), ("Kutenai Canoe",3)]
    widgetNames = widgets.Dropdown(options = canoeOptions, value = 3, description = "Canoe type: ")
    return [widgetLengthScale, widgetWidthScale, widgetHeightScale, widgetNames]

"""
    Brings up the ui for the Canoe visualizer
"""
def Canoe(widgetLengthScale, widgetWidthScale, widgetHeightScale, widgetNames):
    
    im = interact_manual.options(manual_name = "refresh")
    args = {"lengthScale":widgetLengthScale, "widthScale": widgetWidthScale, "heightScale":widgetHeightScale, "canoe_type":widgetNames}
    im(CanoeGraph, **args)

""" Plots the canoe_type, with the given scaling
scale      - [float, float, float]
canoe_type - integer 

"""
def CanoeGraph(lengthScale, widthScale, heightScale, canoe_type):
    """ Takes a length, width, height, and name(type) will properly name next push
    Outputs nothing, but displays the canoe graph
    """

    XX, YY, ZZ = canoe.GetCanoe([lengthScale, widthScale, heightScale], canoe_type, 8)
    length = 0
    height = 0
    width = 0
    for i in range(0, len(XX)):
        for j in range(0, len(XX[0])):
            if (XX[i][j] > length): length = XX[i][j]
            if (ZZ[i][j] > height): height = ZZ[i][j] 
            if (abs(YY[i][j]) > width): width = abs(YY[i][j])
    width *= 2 #since we only measured from the middle out.
    f2str = lambda x:  "{:.4f}".format(x)
    titleStr = "Length: " + f2str(length) + "(m)\twidth: " + f2str(width) + "(m)\theight: " + f2str(height) +"(m)" 
    """
    DEBUG
    P, V, U = canoe.GetCanoeKutenai()
    n_rows = len(P)
    n_cols = len(P[0])

    s_size = n_rows*n_cols
    sX = [0]*s_size
    sY = [0]*s_size
    sZ = [0]*s_size
    u_size = (n_rows-1)*n_cols*2
    uX = [0]*u_size
    uY = [0]*u_size
    uZ = [0]*u_size

    v_size = n_rows*(n_cols-1)*2
    vX = [0]*v_size
    vY = [0]*v_size
    vZ = [0]*v_size
    
    for i in range(n_rows):
        for j in range(n_cols):
            vector = P[i][j]
            posIndex = i*(n_cols)+j
            sX[posIndex] = vector[0]
            sY[posIndex] = vector[1]
            sZ[posIndex] = vector[2]

            if (i < n_rows - 1):
                vectorIndex = i*(n_cols*2) + j*2
                uX[vectorIndex] = vector[0] + U[i][j][0][0]
                uY[vectorIndex] = vector[1] + U[i][j][0][1]
                uZ[vectorIndex] = vector[2] + U[i][j][0][2]

                vector = P[i+1][j]
                uX[vectorIndex+1] = vector[0] + U[i][j][1][0]
                uY[vectorIndex+1] = vector[1] + U[i][j][1][1]
                uZ[vectorIndex+1] = vector[2] + U[i][j][1][2]
            if (j < n_cols - 1):
                vector = P[i][j]
                vectorIndex = i*((n_cols-1)*2)+j*2
                vX[vectorIndex] = vector[0] + V[i][j][0][0]
                vY[vectorIndex] = vector[1] + V[i][j][0][1]
                vZ[vectorIndex] = vector[2] + V[i][j][0][2]

                vector = P[i][j+1]
                vX[vectorIndex+1] = vector[0] + V[i][j][1][0]
                vY[vectorIndex+1] = vector[1] + V[i][j][1][1]
                vZ[vectorIndex+1] = vector[2] + V[i][j][1][2]
    
    trace3 = go.Scatter3d(x = sX, y= sY, z = sZ, mode= 'markers')
    trace4 = go.Scatter3d(x = uX, y= uY, z = uZ, mode= 'markers')
    trace5 = go.Scatter3d(x = vX, y= vY, z = vZ, mode= 'markers')
    """


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
    #fig = go.Figure(data = [trace1, trace2])
    fig = go.Figure(data = [trace1, trace2])
    fig.update_layout(scene = sceneDictionary, title = titleStr,  width = 1080, height = 720)
    fig.show()
