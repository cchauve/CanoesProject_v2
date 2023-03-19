import plotly.graph_objects as go
import numpy as np #Might need this later
import scripts.BezierCurve as bc

from ipywidgets import interact, fixed, interact_manual 
import ipywidgets as widgets
from IPython.display import display
    
def CurveGraph():
    """ Displays the 3 point Bezier Curve graph
    There are also widgets available for the user.
    """
    ##DATA PREP WORK
    resolution = 32
    xPoints = [0, 2.5, 5]
    yPoints = [0, 2.5, 5]
    points  = [[xPoints[0],yPoints[0]],[xPoints[1],yPoints[1]],[xPoints[2],yPoints[2]]]
    
    xInterp = [xPoints[0]*0.5 + xPoints[1]*0.5, 
               xPoints[0]*0.25 + xPoints[1]*0.5 + xPoints[2]*0.25, 
               xPoints[1]*0.5 + xPoints[2]*0.5]
    
    yInterp = [yPoints[0]*0.5 + yPoints[1]*0.5, 
               yPoints[0]*0.25 + yPoints[1]*0.5 + yPoints[2]*0.25, 
               yPoints[1]*0.5 + yPoints[2]*0.5] 
    
    xx = [0]*resolution
    yy = [0]*resolution
    
    ##PLOT CREATION
    scatter = lambda name, mode ,line_color, width: go.Scatter(
        name = name,
        visible = True,
        mode = mode,
        line = dict(color = line_color, width = width)
    )
    pointPlot = scatter("1st Interpolation Line", "markers+lines+text", "#2eb089", 3)
    pointPlot.marker = dict(color = "#2eb089", size = 7)
    pointPlot.text = ["P1", "P2", "P3"]
    pointPlot.textposition = "bottom center"

    curvePlot = scatter("Bézier Curve", "lines", "#141414", 5)

    interpolatedPlot = scatter("2nd Interpolation Line", "markers+lines", "#20808c", 3)
    interpolatedPlot.marker = dict(color = "#c134d1", size = 7)
    
    fig = go.Figure()
    fig.add_trace(curvePlot)
    fig.add_trace(pointPlot)
    fig.add_trace(interpolatedPlot)
    fig.update_layout(width = 700, height = 500, plot_bgcolor = 'rgba(0,0,0,0)')
    standard = dict(range = [-0.5,5.5], zeroline = False, showgrid = False, visible = False, scaleratio = 1)
    fig.update_xaxes(standard)
    fig.update_yaxes(standard, scaleanchor = "x", )
    
    #WIDGET AND UPDATE FUNCTIONS FOR GRAPHS
    xWidget, yWidget, tWidget = GetCurvePlotWidgets()
    
    @interact(xData = xWidget, yData = yWidget, t = tWidget)
    def update(xData, yData, t):
        with fig.batch_update():
            points[0] = [xData, yData]
            xPoints[0] = xData
            yPoints[0] = yData
            for i in range(0, resolution):
                xx[i], yy[i] = bc.CurvePoint(points, i/(resolution-1))
            
            xInterp[0], yInterp[0] = bc.CurvePoint([points[0],points[1]],t)
            xInterp[2], yInterp[2] = bc.CurvePoint([points[1],points[2]],t)
            xInterp[1], yInterp[1] = bc.CurvePoint([[xInterp[0], yInterp[0]],[xInterp[2], yInterp[2]]],t)
            
            fig.data[0].x = xx
            fig.data[0].y = yy
            fig.data[1].x = xPoints
            fig.data[1].y = yPoints
            fig.data[2].x = xInterp
            fig.data[2].y = yInterp
        return fig

def GetCurvePlotWidgets():
    """ Returns the widgets needed for the Curve Plot
    An Oranization method to help declutter
    """
    tStepsize = 1/32
    stepsize = 5/32
    tWidget = widgets.FloatSlider(min = 0, max = 1, value = 0.5, step = tStepsize, description = "t")
    xWidget = widgets.FloatSlider(min = 0, max = 5, value = 0, step = stepsize, readout = False, description = "x")
    yWidget = widgets.FloatSlider(min = 0, max = 5, value = 0, step = stepsize, readout = False, description = "y")
    xWidget.style.handle_color = "#db4a40" #red
    yWidget.style.handle_color = "#a5db40" #Green (lime)
    tWidget.style.handle_color = "#c134d1" #Purple
    return xWidget, yWidget, tWidget