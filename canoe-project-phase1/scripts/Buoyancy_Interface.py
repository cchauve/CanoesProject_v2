"""
A script mainly for setting up the interface of each graphing model,
everything should be in one function (as this script will be bulky enough)
Any method these scripts use should be outsourced to seperate python files, unless it's small and meaningfull addition.
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    widgetMaker = lambda min_size, max_size, value, subdivisions, de: widgets.FloatSlider(
        min = min_size,
        max = max_size,
        step = (max_size-min_size)/subdivisions,
        value = value,
        description = de,
        continuous_update = False)
    length = widgetMaker(0.01, 2, 1, 64, "length (m): ")
    width = widgetMaker(0.01, 2, 1, 64, "width (m): ")
    height = widgetMaker(0.01, 2, 1, 64, "height (m): ")
    density = widgetMaker(0.1, GLOBAL_WaterDensity * 1.05, 750, 256, "density: ")
     
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

def CanoeBuoyancy(widgetLength, widgetWidth, widgetHeight, widgetNames):
    """
    Ultimate UI call for the canoe Graph,
    Takes in the widgets from the Bezier Surface Interface script and will run the Bouyancy model of the canoe.
    """   

    im = interact_manual.options(manual_name = "refresh")
    args = {"length":widgetLength, "width": widgetWidth, "height":widgetHeight, "canoe_type":widgetNames}
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

    #helper lambda setup
    f2str = lambda x:  "{:.2f}".format(x)
    title_str = lambda weight, depth, force: "Cuboid weight: " + f2str(weight) + "(N)" + " Depth: " + f2str(depth) + "(m)" + " Total Force: " + f2str(force) + "(N)"

    @interact(waterLevel = waterLevelWidget)
    def update(waterLevel):
        with fig.batch_update():
            fig.data[0].x, fig.data[0].y = cm.GetCubeDiagram(length, height, waterLevel)
            fig.data[1].x, fig.data[1].y = cm.GetWaterDiagram(length, waterLevel)

            buoyancyForce = cm.CalcBouyancy(length, width, height, waterLevel, GLOBAL_WaterDensity, GLOBAL_Gravity)
            totalForce = buoyancyForce - gravityForce
            arrowMagnitude = (totalForce / (maximumForce)) * height * 1.2
            fig.data[2].x, fig.data[2].y = graphics.GetArrow(arrowX, arrowY, [0,1], arrowMagnitude, arrowMagnitude/2)
            
            titleString  = title_str(cm.CalcWeight(length, width, height, density, gravity = GLOBAL_Gravity),waterLevel,totalForce) 
            fig.update_layout(
                title = titleString
            )
        return fig


def GenerateBoatGraph(length, width, height, canoe_type):
    """ 
    An interactive graph with a slider for weight. Shows where the equilibrium of the boat is depending on weight, 
    along with a side view of said boat with a line at equilibrium level.
    """
    #variable set up
    symmetry = 2
    resolution = 5
    XX, YY, ZZ = canoe.GetCanoe(length, width, height, canoe_type, resolution)
    #for the sideTrace canoe outline
    xLine, zLine, maxWaterLevel = getCanoeBorder(XX,ZZ)

    f2str = lambda x:  "{:.4f}".format(x)
    titleStr = "Length: " + f2str(length) + "(m)\tWidth: " + f2str(width) + "(m)\tHeight: " + f2str(height) +"(m)" 

    heightNormalArea = eq.GenerateVectorList(XX,YY,ZZ)
    maxWeight = abs(eq.CalculateForce(heightNormalArea, maxWaterLevel * 1.5) / GLOBAL_Gravity)
    stepsize = maxWeight/(128)
    
    #for the mass vs level graph
    graphResolution = 128
    massData = np.linspace(0, maxWeight, num = graphResolution, endpoint = True)
    waterLevelData = np.linspace(0, 1, num = graphResolution, endpoint = True)
    for i in range(graphResolution):
        waterLevelData[i] = eq.BinarySearch(heightNormalArea, weight = massData[i] * GLOBAL_Gravity ,symmetryMultiplier = symmetry)
    
    #plot setup
    xRange = [ (0.5-0.75) * length, (0.75+0.5)*length]
    yRange = [-1.1 * height, 1.1 * height]

    scatter = lambda X,Y, line_color:go.Scatter(
        x = X,
        y = Y,
        visible = True,
        line = dict(color = line_color, width = 3)
    )

    levelTrace = scatter([-0.5*length, 1.5*length], [0,0], "#1991df")
    sideTrace = scatter(xLine, zLine, "#141414")
    massLevelTrace = scatter(massData, waterLevelData, "#141414")
    massLevelInteractiveTrace = scatter([maxWeight,maxWeight], [0, waterLevelData[graphResolution-1]], "#1991df")

    """
    MAKE SUBGRAPH ON THE SIDE THAT SHOWS THE MASS vs WaterHeight
    """

    #Change the list order for traces to change render order
    fig = make_subplots(
        rows = 2, cols = 1,
        subplot_titles=("Graphic", "Mass versus Waterlevel")
    )
    fig.update_layout(width = 1280, height = 720, title_text="bouyancy graph")
    fig.update_xaxes(range = xRange, row = 1, col = 1)
    fig.update_yaxes(range = yRange, row = 1, col = 1, scaleanchor ="x", scaleratio = 1)

    fig.add_trace(sideTrace,  row = 1, col = 1)                 #data 0
    fig.add_trace(levelTrace, row = 1, col = 1)                 #data 1
    fig.add_trace(massLevelTrace, row = 2, col = 1)             #data 2
    fig.add_trace(massLevelInteractiveTrace, row = 2, col = 1)  #data 3
    
    #widget setup
    massWidget = widgets.FloatSlider(min = 0, max = maxWeight, step = stepsize, description = "Mass (kg)", value = maxWeight)
    massWidget.style.handle_color = "#141414"
    
    @interact(mass = massWidget) 
    def update(mass):
        with fig.batch_update():
            waterLevel = eq.BinarySearch(heightNormalArea, weight = mass * GLOBAL_Gravity ,symmetryMultiplier = symmetry)
            fig.data[0].y = np.subtract(zLine, waterLevel)
            fig.data[3].x = [mass,mass]
            fig.data[3].y = [0, waterLevel]
            
            fig.update_layout(
                title = "Bottom of the Canoe to Water Level(m): " + "{:.4f}".format(waterLevel) + "\t" + titleStr
            )
        return fig
    return None

def getCanoeBorder(X,Z):
    """ Takes in two array grids (same size)
    returns the border of two array grids in a list, counter clockwise
    """
    minWall = [100,100,100,100] #find a nicer value to use...
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
        if (z0[i] < minWall[0]): minWall[0] = z0[i]

    xLine, zLine = arrayAppend(x0, z0)
    
    index_a = arrayD[0]-1
    for i in range(0, arrayD[1]):
        index_b = i
        x1[i], z1[i] = arrayGrab(index_a, index_b)
        if (z1[i] < minWall[1]): minWall[1] = z1[i]
    xLine, zLine = arrayAppend(x1, z1)

    index_b = arrayD[1]-1
    for i in range(0, arrayD[0]):
        index_a = arrayD[0]-1-i
        x0[i], z0[i] = arrayGrab(index_a, index_b)
        if (z0[i] < minWall[2]): minWall[2] = z0[i]
    xLine, zLine = arrayAppend(x0, z0)

    index_a = 0
    for i in range(0, arrayD[1]):
        index_b = arrayD[1]-1-i
        x1[i], z1[i] = arrayGrab(index_a, index_b)
        if (z1[i] < minWall[3]): minWall[3] = z1[i]
    xLine, zLine = arrayAppend(x1, z1)
    return xLine, zLine, minWall[1]
    
