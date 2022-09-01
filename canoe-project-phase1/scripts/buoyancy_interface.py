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
import scripts.models.rotatingCubeModel as rcm # TO DEPRECATE
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
    length = widgets.FloatSlider(min = 0.01, max = 2, step = stepSize, value = 1, description = "length (m): ", continuous_update = False)
    width  = widgets.FloatSlider(min = 0.01, max = 2, step = stepSize, value = 1, description = "width (m): ", continuous_update = False)
    height = widgets.FloatSlider(min = 0.01, max = 2, step = stepSize, value = 1, description = "height (m): ", continuous_update = False)
    
    density = widgets.FloatSlider(min = 0.1, max = GLOBAL_WaterDensity * 1.05, value = 750 , step = stepSize, description = "density: ", continuous_update = False)
    density.style.handle_color = "#141414"
    
    ui = widgets.TwoByTwoLayout(top_left = length, top_right = width, bottom_left = height, bottom_right = density)
    out = widgets.interactive_output(WaterLevelCubeGraph, {"length": length, "width": width, "height": height, "density": density, "resolution": fixed(64)})
    display(ui, out)

def CanoeGraph():
    """
    Ultimate UI call for the canoe Graph,
    set up sliders, labels, and ui position. As well as calling the the method to display everything
    """
    stepSize = 0.05
    
    length = widgets.FloatSlider(min = 0.01, max = 5, step = stepSize, value = 4  , description = "length (m)", continuous_update = False)
    width  = widgets.FloatSlider(min = 0.01, max = 1.5, step = stepSize, value = 0.5, description = "width (m)" , continuous_update = False)
    height = widgets.FloatSlider(min = 0.01, max = 1.5, step = stepSize, value = 0.5  , description = "height (m)", continuous_update = False)

    curveDef = widgets.FloatSlider(min = 0.01, max = 2, step = stepSize, value = 0.5, description = "curve definition", continuous_update = False, orientation = "vertical")
    canoeType = widgets.IntSlider(min = 1, max = 3, description = "Canoe Type", layout=widgets.Layout(width='85%'))

    ui = widgets.GridspecLayout(4, 2, width = "50%", height = "275px")
    ui[0, 0] = length
    ui[1, 0] = width
    ui[2, 0] = height
    ui[0:2, 1] = curveDef
    ui[3, :] = canoeType
    
    out = widgets.interactive_output(GenerateBoatGraph, {"length": length, "width": width, "height": height, "c": curveDef, "canoe_type": canoeType, "resolution": fixed(50)})
    display(ui, out)

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
    waterLevelWidget = widgets.FloatSlider(min = 0, max = height, step = stepsize, description = "depth (m)", layout = widgets.Layout(width = "50%"))
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
            
            titleString =  "Cuboid weight:" + "{:.2f}".format(cm.CalcWeight(length, width, height, density, gravity = GLOBAL_Gravity)) + "(N)"
            titleString += " Depth: " + "{:.2f}".format(waterLevel) + "(m)"
            titleString += " Total force: " + "{:.2f}".format(totalForce) + "(N)"
            fig.update_layout(
                title = titleString
            )
        return fig


def GenerateBoatGraph(length, width, height, c, canoe_type, resolution = 32):
    """ 
    An interactive graph with a slider for weight. Shows where the equilibrium of the boat is depending on weight, 
    along with a side view of said boat with a line at equilibrium level.
    """
    #variable set up
    mass = 100
    X, Y, Z = canoe.GetXYZ(width, height, length, c, canoe_type, resolution = 32)
    heightNormalArea = eq.GenerateVectorList(X,Y,Z)
    maxWeight = abs(eq.CalculateForce(heightNormalArea, 0) / GLOBAL_Gravity)
    stepsize = maxWeight/resolution
    
    #plot setup
    levelTrace = canoe.GetLevelTrace(0, length)
    sideTrace = canoe.GetSideTrace(height, length, c, canoe_type, resolution)
    sideData = [0]*2 #set up to retrieve side data
    sideData = canoe.GetSideData(height, length, c, canoe_type, resolution)
    xRange = [-length * 1.1, length * 1.1] 
    yRange = [-height * 1.1, height * 1.1]
    
    fig = figureSetup([sideTrace, levelTrace], width = 700, height = 500, xRange = xRange, yRange = yRange) #Change the list order for traces to change render order
    
    #widget setup
    massWidget = widgets.FloatSlider(min = 0, max = maxWeight, step = stepsize, description = "mass (kg)", value = maxWeight)
    massWidget.style.handle_color = "#141414"
    
    @interact(mass = massWidget) 
    def update(mass):
        with fig.batch_update():
            
            level = eq.BinarySearch(heightNormalArea, mass * GLOBAL_Gravity)
            fig.data[0].y = np.add(sideData[1], level)
            
            fig.update_layout(
                title = "Canoe top to water (m): " + "{:.4f}".format(level)
            )
        return fig
    return None

"""
===================================
      T O   D E P R E C A T E
===================================

def EquilibriumCubeGraph(length = 5, depth = 5, height = 5, resolution = 64):
    
    An interactive graph with slider for weight. Shows where the equilibrium of the cube is.
    Subgraph on the side plotting weight vs equilibrium.
         
    fig = go.Figure()
    
    fig.update_layout(
        showlegend = False,
        width = 500,
        height = 700
    )
    fig.update_xaxes(range = [length  * (-1/4), length * 5/4])
    fig.update_yaxes(range = [height  * (-5/4), height * 5/4], scaleanchor = "x", scaleratio = 1)
    
    ##initial plot
    waterHeight = cm.CalcEquilibrium(height, 0, GLOBAL_WaterDensity)
    
    traceCube = cm.GetCubeTrace(length, height, waterHeight)
    traceWater = cm.GetWaterTrace(length, waterHeight)
    
    fig.add_trace(traceCube)
    fig.add_trace(traceWater)
    
    fig.data[0].visible = True
    fig.data[1].visible = True
    #fig.show()
    
    maximum_density = GLOBAL_WaterDensity
    stepsize = maximum_density/resolution
    
    @interact(density = (0, maximum_density, stepsize))
    def update(density):
        with fig.batch_update():
            waterHeight = cm.CalcEquilibrium(height, density, GLOBAL_WaterDensity)
            
            fig.data[0].x, fig.data[0].y = cm.GetCubeDiagram(length, height, waterHeight)
            fig.data[1].x, fig.data[1].y = cm.GetWaterDiagram(length, waterHeight)
            
            waterMass = cm.CalcBouyancy(length, depth, height, waterHeight, GLOBAL_WaterDensity, 1)
            cubeMass = cm.CalcWeight(length, depth, height, density, 1)
            fig.update_layout(
                title = "Cube Mass: " + "{:.4f}".format(cubeMass) + " Equilibrium level: " + "{:.4f}".format(waterHeight)
            )
        return fig
    return None
    
def RotatedCubeGraph(length = 1, depth = 1, height = 1, density = 500, resolution = 32):
    
    An interactive graph with slider for water level. 
    length, depth, height, density. Rotation will be in degrees (will be converted to radians in script) 
    resolution of normals 
   
    fig = go.Figure()
    fig.update_layout(
        showlegend = False,
        width = 500,
        height = 700
    )
    maxRange = np.multiply([-1,1],max(length,height) * np.sqrt(2)*1.5)
    fig.update_xaxes(range = maxRange)
    fig.update_yaxes(range = maxRange, scaleanchor = "x", scaleratio = 1)
    
    theta = 0
    
    traceCube, traceWater = rcm.GetTrace(length, height, theta)
    fig.add_trace(traceCube)
    fig.add_trace(traceWater)
    fig.data[0].visible = True
    fig.data[1].visible = True
    
    @interact(theta = (0, np.pi, np.pi/resolution))
    def update(theta):
        with fig.batch_update():
            X_cube, Y_cube, X_water, Y_water = rcm.GetDiagram(length, height, theta)
            fig.data[0].x, fig.data[0].y = X_cube, Y_cube
            fig.data[1].x, fig.data[1].y = X_water, Y_water
            
            volume = rcm.GetArea(X_water, Y_water) * depth
            fig.update_layout(
                title = "Displaced Water Volume: " + "{:.4f}".format(volume)
            )
        return fig
    
    return None
"""