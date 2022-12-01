import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import scripts.BezierCurve as bc

from ipywidgets import interact, fixed, interact_manual 
import ipywidgets as widgets
from IPython.display import display

def GetCurvePlotWidgets():
    tStepsize = 1/32
    stepsize = 5/32
    tWidget = widgets.FloatSlider(min = 0, max = 1, value = 0.5, step = tStepsize, description = "t")
    xWidget = widgets.FloatSlider(min = 0, max = 5, value = 0, step = stepsize, readout = False, description = "x")
    yWidget = widgets.FloatSlider(min = 0, max = 5, value = 0, step = stepsize, readout = False, description = "y")
    xWidget.style.handle_color = "red"
    yWidget.style.handle_color = "green"
    tWidget.style.handle_color = "blue"
    return xWidget, yWidget, tWidget
    
def CurvePlot():
    resolution = 40
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

    for i in range(0, resolution):
        xx[i], yy[i] = bc.CurvePoint(points, i/(resolution-1))
    
    pointPlot = go.Scatter(
        visible = True,
        mode = "markers+lines+text",
        line = dict(color = "#2eb089", width = 3),
        marker = dict(color = "#2eb089", size = 7),
        text = ["P1", "P2", "P3"],
        textposition = "bottom center",
        name = "1st Interpolation",
        x = xPoints,
        y = yPoints
    )
    curvePlot = go.Scatter(
        visible = True,
        line = dict(color = "#141414", width = 5),
        mode = "lines",
        name = "Bézier Curve",
        x = xx,
        y = yy
    )
    interpolatedPlot = go.Scatter(
        visible = True,
        line = dict(color = "#20808c", width = 3),
        marker = dict(color = "#ad2a13", size = 7),
        mode = "markers+lines",
        name = "2nd Interpolation",
        x = xInterp,
        y = yInterp
    )
    
    fig = go.Figure()
    fig.add_trace(curvePlot)
    fig.add_trace(pointPlot)
    fig.add_trace(interpolatedPlot)
    fig.update_layout(width = 500, height = 500)
    standard = dict(range = [-1,6], zeroline = False, showgrid = False, visible = False, scaleratio = 1)
    fig.update_xaxes(standard)
    fig.update_yaxes(standard, scaleanchor = "x", )
    
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