"""
functions to compute the coordinates of a canoe given its parameters and visualize a canoe
"""
import numpy as np
import plotly.graph_objects as go
from ipywidgets import *

def get_coordinates(w, h, l, c, a, b, canoe_type):
    """
    get the 3D coordinates of the canoe
    input: 4 floating point numbers for width, height, length, and corner radius of the canoe
    input: 2 list of floating point numbers for eta, and theta
    input: 1 integer for canoe type
    output: list of x-coordinates of the canoe, named X
    output: list of y-coordinates of the canoe, named Y
    output: list of z-coordinates of the canoe, named Z
    """
    X=x_coordinates(l, a)
    Y=y_coordinates(w, c, a, b, canoe_type)
    Z=z_coordinates(h, c, a, b, canoe_type)
    return X, Y, Z

def x_coordinates(l, a):
    """
    input: length of canoe, and eta
    output: list of x-coordinates of the canoe
    """
    return l*np.cos(a)

def y_coordinates(w, c, a, b, canoe_type):
    """
    input: width of canoe, corner radius of canoe, eta, theta, and canoe type
    output: list of y-coordinates of the canoe
    """
    if canoe_type==3:
        return w*np.sin(a)*np.abs(np.sin(b))**(c/(w*np.sin(a)))*np.sign(np.sin(b))
    else:
        return w*np.sin(a)*np.sin(b)

def z_coordinates(h, c, a, b, canoe_type):
    """
    input: height of canoe, corner radius of canoe, eta, theta, canoe type
    output: list of z-coordinates of the canoe
    """
    if canoe_type==1:
        return h*np.cos(b)
    if canoe_type==2:
        return h*np.abs(np.sin(a))*np.cos(b)
    else:
        return h*np.abs(np.sin(a))*np.abs(np.cos(b))**(c/(h*np.abs(np.sin(a))))*np.sign(np.cos(b))
    
def get_eta_theta(canoe_type):
    """
    input: canoe type
    output: list of angles in radians called eta and theta
    """
    if canoe_type==3:
        a, b=np.meshgrid(np.linspace(0.01, np.pi-0.01, 50), np.linspace(np.pi/2, (3/2)*np.pi, 50))
    else:
        a, b=np.meshgrid(np.linspace(0.0, 2*np.pi, 50), np.linspace(np.pi/2, (3/2)*np.pi, 50))
    return a, b

def plot_canoe(width, height, length, corner_radius, canoe_type):
    """
    make a 3D figure of a canoe. 
    input: 1 integer for canoe type
    input: 4 lists of floating point numbers showing ranges of width, 
        ranges of height, ranges of length, and ranges of corner radius for the canoe
    output: 3D figure of the canoe with 4 sliders for width, height, length, corner radius
    """

    eta, theta=get_eta_theta(canoe_type)
    X, Y, Z=get_coordinates(width[0], height[0], length[0], corner_radius[0], eta, theta, canoe_type)
    fig=go.Figure()
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, visible=False))
    """
    make the title, define range of x,y,z axis, define name of x,y,z axis,
    bound y-axis by x-axis, make sure that figure of canoe always show up in the center
    """
    max_range=max(width[1], height[1], length[1])
    min_range=(-max_range)
    fig.layout=go.Layout(title='Type '+str(canoe_type)+' canoe visualization',
        scene=dict(
        xaxis=dict(range=[min_range, max_range]), xaxis_title='Length(m)',
        yaxis=dict(range=[min_range, max_range]), yaxis_title='Width(m)',
        zaxis=dict(range=[min_range, max_range]), zaxis_title='Height(m)'))
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.data[0].visible=True
    """
    make a slider for width, height, length, and corner radius. Each slider slides by 0.1. 
    calculate coordinates for new figure as slider slides, and show that figure
    """
    @interact(width=(width[0], width[1], 0.1), height=(height[0], height[1], 0.1), 
              length=(length[0], length[1], 0.1), corner_radius=(corner_radius[0], corner_radius[1], 0.1))
    def update(width=width[1], height=height[1], length=length[1], corner_radius=corner_radius[1]):
        with fig.batch_update():
            X, Y, Z=get_coordinates(width, height, length, corner_radius, eta, theta, canoe_type)
            fig.data[0].x=X
            fig.data[0].y=Y
            fig.data[0].z=Z
        return fig
