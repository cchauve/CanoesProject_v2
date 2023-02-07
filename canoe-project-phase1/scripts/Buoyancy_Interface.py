"""
A script mainly for setting up the interface of each graphing model,
everything should be in one function (as this script will be bulky enough)
Any method these scripts use should be outsourced to seperate python files, unless it's small and meaningfull addition.
"""
import plotly.graph_objects as go
import numpy as np

from ipywidgets import interact, fixed, interact_manual #, interactive
import ipywidgets as widgets
from IPython.display import display

import scripts.models.cubeModel as cm
import scripts.models.canoeModel as canoe 
import scripts.models.graphics as graphics
import scripts.Buoyancy_Equilibrium as eq

GLOBAL_WaterDensity = 997     #(kg / m^3)
GLOBAL_Gravity      = 9.80665 #(m/s^2)

#https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html A way to stop the flickering of the graphs, near the bottom of the webpage
def CubeGraph():
    """
    Ultimate UI call for the canoe Graph,
    set up sliders, labels, and ui position. As well as calling the the method to display everything
    """
    stepSize = 0.05
    length = widgets.FloatSlider(
        min = 0.01,                                  
        max = 2,                          
        step = stepSize,                                 
        value = 1,                              
        description = "length (m): ",                      
        continuous_update = False
    )
    
    width  = widgets.FloatSlider(
        min = 0.01,                                
        max = 2,                               
        step = stepSize,                              
        value = 1,                                 
        description = "width (m): ",                            
        continuous_update = False
    )
    
    height = widgets.FloatSlider(
        min = 0.01,                                
        max = 2,                          
        step = stepSize,                            
        value = 1,                          
        description = "height (m): ",        
        continuous_update = False
    )
    
    density = widgets.FloatSlider(
        min = 0.1,                         
        max = GLOBAL_WaterDensity * 1.05,                              
        value = 750 ,                                
        step = stepSize,                                 
        description = "density: ",                            
        continuous_update = False
    )
    
    density.style.handle_color = "#141414"
    
    ui = widgets.TwoByTwoLayout(
        top_left = length, 
        top_right = width, 
        bottom_left = height, 
        bottom_right = density
    )
    
    out = widgets.interactive_output(
        WaterLevelCubeGraph,                           
        {"length": length,                                    
         "width": width,                                   
         "height": height,                                     
         "density": density,              
         "resolution": fixed(64)}
    )
    display(ui, out)

def CanoeBuoyancy(widgetLengthScale, widgetWidthScale, widgetHeightScale, widgetNames):
    """
    Ultimate UI call for the canoe Graph,
    set up sliders, labels, and ui position. As well as calling the the method to display everything
    """   
    "STARTS THE INTERACTABLE GRAPH"
    im = interact_manual.options(manual_name = "refresh")
    args = {"lengthScale":widgetLengthScale, "widthScale": widgetWidthScale, "heightScale":widgetHeightScale, "canoe_type":widgetNames}
    im(GenerateBoatGraph, **args)
    
def figureSetup(traces, width, height, showlegend = False, xRange = None, yRange = None):
    """
    A helper method to condense the figure setup and remove duplicate code
    """
    fig = go.Figure()
    n=0
    for i in range(0, len(traces)):
        fig.add_trace(traces[i])
        fig.data[i].visible = True
    fig.update_layout(
        showlegend = showlegend,
        width = width,
        height = height
    )
    fig.update_yaxes()
    fig.update_xaxes(range = xRange, title_text = "meters") #tickprefix = "m" but looks cluttered
    fig.update_yaxes(range = yRange, title_text = "meters",scaleanchor = "x", scaleratio = 1)
    
    return fig
    
def WaterLevelCubeGraph(length = 5, width = 5, height = 5, density = 0.5, resolution = 64):
    """ 
    A small interactive graph for a simple cube in water, water level is interactive.
    Takes a length, depth, height, density, and resolution.
    resolution is how many slides you want for the graph. Higher numbers are more laggy.
    """
    #Variable set up
    waterHeight = cm.CalcEquilibrium(height, 0, GLOBAL_WaterDensity)
    gravityForce = cm.CalcWeight(length, width, height, density, GLOBAL_Gravity)
    buoyancyForce = cm.CalcBouyancy(length, width, height, height, GLOBAL_WaterDensity, GLOBAL_Gravity)
    maximumForce = max(buoyancyForce, gravityForce ) #To cap the arrows height
    arrowX, arrowY = (np.sqrt(length**2 + height**2)*1.2), 0
    stepsize = height / resolution
    
    #plot setup
    traceCube = cm.GetCubeTrace(length, height, waterHeight)
    traceWater = cm.GetWaterTrace(length, waterHeight)
    traceArrow = graphics.GetTrace(arrowX, arrowY, [0,1], 5, 1)
    xRange = [length  * (-1/4), length * (5/4 + 1)]
    yRange = [height  * (-5/4), height * 5/4]
    
    fig = figureSetup([traceCube, traceWater, traceArrow], width = 800, height = 500, xRange = xRange, yRange = yRange)
    
    #widget set up
    waterLevelWidget = widgets.FloatSlider(min = 0, 
                                           max = height, 
                                           step = stepsize, 
                                           description = "depth (m)", layout = widgets.Layout(width = "50%"))
    
    waterLevelWidget.style.handle_color = "lightblue"
    @interact(waterLevel = waterLevelWidget)
    def update(waterLevel):
        with fig.batch_update():
            fig.data[0].x, fig.data[0].y = cm.GetCubeDiagram(length, height, waterLevel)
            fig.data[1].x, fig.data[1].y = cm.GetWaterDiagram(length, waterLevel)

            buoyancyForce = cm.CalcBouyancy(length, width, height, waterLevel, GLOBAL_WaterDensity, GLOBAL_Gravity)
            totalForce = buoyancyForce - gravityForce
            arrowMagnitude = (totalForce / (maximumForce)) * height * 1.2
            fig.data[2].x, fig.data[2].y = graphics.GetArrow(arrowX, arrowY, [0,1], arrowMagnitude, arrowMagnitude/2)
            
            titleString  = "Cuboid weight: " 
            titleString += "{:.2f}".format(cm.CalcWeight(length, width, height, density, gravity = GLOBAL_Gravity)) + "(N)"
            titleString += " Depth: " + "{:.2f}".format(waterLevel) + "(m)"
            titleString += " Total force: " + "{:.2f}".format(totalForce) + "(N)"
            fig.update_layout(
                title = titleString
            )
        return fig


def GenerateBoatGraph(lengthScale, widthScale, heightScale, canoe_type):
    """ 
    An interactive graph with a slider for weight. Shows where the equilibrium of the boat is depending on weight, 
    along with a side view of said boat with a line at equilibrium level.
    """
    #variable set up
    symmetry = 2
    resolution = 4
    XX, YY, ZZ = canoe.GetCanoe([lengthScale, widthScale, heightScale], canoe_type, resolution)
    length = 0
    height = 0
    for i in range(0, len(XX)):
        for j in range(0, len(XX[0])):
            if (XX[i][j] > length): length = XX[i][j]
            if (ZZ[i][j] > height): height = ZZ[i][j] 
    
    heightNormalArea = eq.GenerateVectorList(XX,YY,ZZ)
    maxWeight = abs(eq.CalculateForce(heightNormalArea, height) / GLOBAL_Gravity)
    stepsize = maxWeight/(64)
    
    xLine, zLine = getCanoeBorder(XX,ZZ)
    
    #plot setup
    xRange = [ (0.5-0.75) * length, (0.75+0.5)*length]
    yRange = [-1.1 * height, 1.1 * height]
    levelTrace = go.Scatter(
        x = [-0.5*length, 1.5*length], 
        y = [0, 0],
        visible = False,
        line = dict(color = "#1991df", width = 3)
    )
    sideTrace = go.Scatter(
        x = xLine, 
        y = zLine, 
        visible = False, 
        line = dict(color = "#141414", width = 3)
    )
    
    #Change the list order for traces to change render order
    fig = figureSetup([sideTrace, levelTrace], width = 1080, height = 720, xRange = xRange, yRange = yRange) 
    
    #widget setup
    massWidget = widgets.FloatSlider(min = 0, max = maxWeight*1.4, step = stepsize, description = "mass (kg)", value = maxWeight)
    massWidget.style.handle_color = "#141414"
    
    @interact(mass = massWidget) 
    def update(mass):
        with fig.batch_update():
            waterLevel = eq.BinarySearch(heightNormalArea, weight = mass * GLOBAL_Gravity ,symmetryMultiplier = symmetry)
            fig.data[0].y = np.subtract(zLine, waterLevel)
            
            fig.update_layout(
                title = "water level(m): " + "{:.4f}".format(waterLevel)
            )
        return fig
    return None

def getCanoeBorder(X,Z):
    """ Takes in two array grids (same size)
    returns the border of two array grids in a list, counter clockwise
    """
    arrayD = [len(X), len(X[0])]
    xLine = []
    zLine = []
    listInit = lambda a: [[0]*a, [0]*a]
    arrayGrab = lambda a,b: [X[a][b], Z[a][b]]
    arrayAppend = lambda a,b: [xLine + a, zLine + b]
    
    x0, z0 = listInit(arrayD[0])
    x1, z1 = listInit(arrayD[1])
    
    index_b = 0
    for i in range(0, arrayD[0]):
        index_a = i
        x0[i], z0[i] = arrayGrab(index_a, index_b)
    xLine, zLine = arrayAppend(x0, z0)
    
    index_a = arrayD[0]-1
    for i in range(0, arrayD[1]):
        index_b = i
        x1[i], z1[i] = arrayGrab(index_a, index_b)
    xLine, zLine = arrayAppend(x1, z1)

    index_b = arrayD[1]-1
    for i in range(0, arrayD[0]):
        index_a = arrayD[0]-1-i
        x0[i], z0[i] = arrayGrab(index_a, index_b)
    xLine, zLine = arrayAppend(x0, z0)

    index_a = 0
    for i in range(0, arrayD[1]):
        index_b = arrayD[1]-1-i
        x1[i], z1[i] = arrayGrab(index_a, index_b)
    xLine, zLine = arrayAppend(x1, z1)
    return xLine,zLine
    
