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
import scripts.visualization as vs
import scripts.models.graphics as graphics
import scripts.buoyancy_equilibrium as eq

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

def CanoeGraph():
    """
    Ultimate UI call for the canoe Graph,
    set up sliders, labels, and ui position. As well as calling the the method to display everything
    """
    stepSize = 0.05
    widgetLength = widgets.FloatSlider(
        min   = 4, 
        max   = 10, 
        step  = stepSize, 
        value = 7.687, 
        description = "length (m)", 
        continuous_update = False
    )
    
    widgetWidth = widgets.FloatSlider(
        min   = 0.1, 
        max   = 3, 
        step  = stepSize, 
        value = 1.250, 
        description = "width (m)", 
        continuous_update = False
    )
    
    widgetHeight = widgets.FloatSlider(
        min   = 0.1, 
        max   = 3, 
        step  = stepSize, 
        value = 1.135, 
        description = "height (m)", 
        continuous_update = False
    )
    
    widgetNames = widgets.Dropdown(
        options = [("Nootkan-Style Canoe", 1), ("Haida-Dugout Canoe", 2)],
        value = 1,
        description = "Canoe type: "
    )
    
    "STARTS THE INTERACTABLE GRAPH"
    widgets.interact_manual(
        GenerateBoatGraph, 
        length     = widgetLength, 
        width      = widgetWidth, 
        height     = widgetHeight, 
        canoe_type = widgetNames
    )
    

    #ui = widgets.GridspecLayout(4, 2, width = "50%", height = "275px")
    #ui[0, 0] = length
    #ui[1, 0] = width
    #ui[2, 0] = height
    #ui[3, :] = canoeType
    
    #out = widgets.interactive_output(GenerateBoatGraph, 
    #                                 {"length": length, 
    #                                  "width": width, 
    #                                  "height": height, 
    #                                  "canoe_type": canoeType, 
    #                                  "resolution": fixed(50)})
    #display(ui, out)

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
    fig.update_yaxes(range = yRange, title_text = "meters",scaleanchor = "x", scaleratio = 1, )
    
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


def GenerateBoatGraph(length, width, height, canoe_type, resolution = 4):
    """ 
    An interactive graph with a slider for weight. Shows where the equilibrium of the boat is depending on weight, 
    along with a side view of said boat with a line at equilibrium level.
    """
    #variable set up
    mass = 100
    symmetry = 2
    
    X, Y, Z = canoe.GetCanoe(width, height, length, canoe_type, resolution)
    #arrayDimensions = [len(X), len(X[0])]
    heightNormalArea = eq.GenerateVectorList(X,Y,Z)
    
    maxWeight = abs(eq.CalculateForce(heightNormalArea, 0)*2 / GLOBAL_Gravity)
    stepsize = maxWeight/resolution
    
    xLine, zLine = getCanoeBorder(X,Z)
    xRange = [-0.5 * length, 1.5 * length]
    yRange = [-1.1 * height, 1.1 * height]
    #plot setup
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
    fig = figureSetup([sideTrace, levelTrace], width = 700, height = 500, xRange = xRange, yRange = yRange) 
    
    #widget setup
    massWidget = widgets.FloatSlider(min = 0, max = maxWeight, step = stepsize, description = "mass (kg)", value = maxWeight)
    massWidget.style.handle_color = "#141414"
    
    @interact(mass = massWidget) 
    def update(mass):
        with fig.batch_update():
            
            level = eq.BinarySearch(heightNormalArea, mass * GLOBAL_Gravity, symmetryMultiplier = symmetry)
            fig.data[0].y = np.add(zLine, level)
            
            fig.update_layout(
                title = "Canoe top to water (m): " + "{:.4f}".format(level)
            )
        return fig
    return None

def getCanoeBorder(X,Z):
    arrayDimensions = [len(X), len(X[0])]
    size = (arrayDimensions[0] + arrayDimensions[1] - 1)*2
    xLine = [0]*(size)
    zLine = [0]*(size)
    for i in range(0, arrayDimensions[0]-1):
        xLine[i] = X[i][0]
        zLine[i] = Z[i][0]
        
    offset = arrayDimensions[0] - 1
    for i in range(0, arrayDimensions[1]-1):
        xLine[i + offset] = X[arrayDimensions[0]-1][i]
        zLine[i + offset] = Z[arrayDimensions[0]-1][i]
        
    offset += arrayDimensions[1] - 1
    for i in range(0, arrayDimensions[0]-1):
        xLine[i + offset] = X[arrayDimensions[0]-1-i][arrayDimensions[1]-1]
        zLine[i + offset] = Z[arrayDimensions[0]-1-i][arrayDimensions[1]-1]
        
    offset += arrayDimensions[0]-1
    for i in range(0, arrayDimensions[1]-1):
        xLine[i + offset] = X[0][arrayDimensions[1]-1-i]
        zLine[i + offset] = Z[0][arrayDimensions[1]-1-i]
    
    return X,Z
        
        
    