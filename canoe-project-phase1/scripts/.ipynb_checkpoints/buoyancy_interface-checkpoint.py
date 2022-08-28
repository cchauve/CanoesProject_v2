"""
A script mainly for setting up the interface of each graphing model,
everything should be in one function (as this script will be bulky enough)
Any method these scripts use should be outsourced to a seperate python file to their respective file, unless its small and meaningfull.

WILL SWITCH TO WHAT HARUTO IS USING IN THE FUTURE
"""
import plotly.graph_objects as go
import numpy as np
import ipywidgets as widgets
from ipywidgets import *
import decimal

import scripts.models.cubeModel as cm
import scripts.models.rotatingCubeModel as rcm
#import scripts.buoyancy_equilibrium as eq #not being used yet
#import plot_funcs as pf

GLOBAL_WaterDensity = 997     #(kg / m^3)
GLOBAL_Gravity      = 9.80665 #(m/s^2)

def WaterLevelCubeGraph(length = 5, depth = 5, height = 5, density = 0.5, resolution = 64):
    """ 
    A small interactive graph for a simple cube in water, water level is interactive.
    Takes a length, depth, height, density, and resolution.
    resolution is how many slides you want for the graph. Higher numbers are more laggy.
    """
    fig = go.Figure()
    waterHeight = cm.CalcEquilibrium(height, 0, GLOBAL_WaterDensity)
    
    traceCube = cm.GetCubeTrace(length, height, waterHeight)
    traceWater = cm.GetWaterTrace(length, waterHeight)
    fig.add_trace(traceCube)
    fig.add_trace(traceWater)
    
    fig.update_layout(
        showlegend = False,
        width = 500,
        height = 700
    )
    
    fig.update_xaxes(range = [length  * (-1/4), length * 5/4])
    fig.update_yaxes(range = [height  * (-5/4), height * 5/4], scaleanchor = "x", scaleratio = 1)
    
    
    stepsize = height / resolution
    @interact(waterHeight = (0, height, stepsize))
    def update(waterHeight):
        with fig.batch_update():
            fig.data[0].x, fig.data[0].y = cm.GetCubeDiagram(length, height, waterHeight)
            fig.data[1].x, fig.data[1].y = cm.GetWaterDiagram(length, waterHeight)

            fig.data[0].visible = True #cube trace visible
            fig.data[1].visible = True #water trace visible

            buoyancyForce = cm.CalcBouyancy(length, depth, height, waterHeight, GLOBAL_WaterDensity, GLOBAL_Gravity)
            gravityForce = cm.CalcWeight(length, depth, height, density, GLOBAL_Gravity)
            totalForce = buoyancyForce - gravityForce
            
            fig.update_layout(
                title = "Water depth at: " + "{:.4f}".format(waterHeight) + " Total force: " + "{:.4f}".format(totalForce)
            )
            
        return fig
        
    return None
    
"""
EVERYTHING BELOW IS TO BE IMPLEMENTED 
"""
    
def EquilibriumCubeGraph(length = 5, depth = 5, height = 5, resolution = 64):
    """
    An interactive graph with slider for weight. Shows where the equilibrium of the cube is.
    Subgraph on the side plotting weight vs equilibrium.
    """     
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

def RotatedCubeGraph(length = 5, depth = 5, height = 5, density = 0.5,resolution = 32):
    """
    An interactive graph with slider for water level. 
    length, depth, height, density. Rotation will be in degrees (will be converted to radians in script) 
    resolution of normals 
    """
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
    
    @interact(theta = (0, np.pi))
    def update(theta):
        with fig.batch_update():
            X_cube, Y_cube, X_water, Y_water = rcm.GetDiagram(length, height, theta)
            fig.data[0].x, fig.data[0].y = X_cube, Y_cube
            fig.data[1].x, fig.data[1].y = X_water, Y_water
        return fig
    
    return None

def GenerateBoatGraph(width, height, length, c, a, b, type, resolution = 32):
    """ 
    An interactive graph with a slider for weight. Shows where the equilibrium of the boat is depending on weight, 
    along with a side view of said boat with a line at equilibrium level.
    """
    #X = pf.x_coordinates(length, a)
    #Y = pf.y_coordinates(width , c, a, b, type)
    #Z = pf.z_coordinates(height, c, a, b, type)
    
    #heightNormal = eq.GenerateVectorList(X,Y,Z)
    
    return None
    