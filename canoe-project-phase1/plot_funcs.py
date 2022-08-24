import numpy as np
import plotly.graph_objs as go
import ipywidgets as widgets
from ipywidgets import *
import decimal

def get_coordinates(w, h, l, c, a, b, type):
    """
    Get the 3D coordinates of the canoe
    input: 6 integer values for width, height, length, corner radius, eta, theta
    input: 1 integer for canoe type
    output: list of x-coordinates of the canoe, named X
    output: list of y-coordinates of the canoe, named Y
    output: list of z-coordinates of the canoe, named Z
    """
    X=x_coordinates(l, a)
    Y=y_coordinates(w, c, a, b, type)
    Z=z_coordinates(h, c, a, b, type)
    return X, Y, Z

def x_coordinates(l, a):
    """
    input: length of canoe and eta
    output: list of x-coordinates of the canoe
    """
    return l*np.cos(a)

def y_coordinates(w, c, a, b, type):
    """
    input: width of canoe, corner radius of canoe, eta, theta, canoe type
    output: list of y-coordinates of the canoe
    """
    if type==3:
        return w*np.sin(a)*np.abs(np.sin(b))**(c/(w*np.sin(a)))*np.sign(np.sin(b))
    else:
        return w*np.sin(a)*np.sin(b)

def z_coordinates(h, c, a, b, type):
    """
    input: height of canoe, corner radius of canoe, eta, theta, canoe type
    output: list of z-coordinates of the canoe
    """
    if type==1:
        return h*np.cos(b)
    if type==2:
        return h*np.abs(np.sin(a))*np.cos(b)
    else:
        return h*np.abs(np.sin(a))*np.abs(np.cos(b))**(c/(h*np.abs(np.sin(a))))*np.sign(np.cos(b))

def get_eta_theta(type):
    """
    input: canoe type
    output: list of angles in radians called eta and theta
    """
    if type==3:
        a, b=np.meshgrid(np.linspace(0.01, np.pi-0.01, 50), np.linspace(np.pi/2, (3/2)*np.pi, 50))
    else:
        a, b=np.meshgrid(np.linspace(0.0, 2*np.pi, 50), np.linspace(np.pi/2, (3/2)*np.pi, 50))
    return a, b

def check(width, height, length, corner_radius, type):
    """
    checks if the input of plot_canoe() is acceptable, and has no errors.
    checks if canoe range is too large, canoe range input is not set to 1 decimal place,
    and if canoe type is 1 or 2 or 3
    
    input: all the input of plot_canoe()
    output: 1 if there was an error, 0 if there was no error
    """
    temp=[width, height, length, corner_radius]
    label=['width', 'height', 'length', 'corner radius']
    for i in range(4):
        if temp[i][1]-temp[i][0]>=10:
            print(label[i], "range is too large and such canoe does not exist. Make the range smaller.")            
            return 1
        if (decimal.Decimal(str(temp[i][0]))%decimal.Decimal("0.1")!=0 or
            decimal.Decimal(str(temp[i][1]))%decimal.Decimal("0.1")!=0):
            print("input for range should be a multiple of 0.1.", label[i],
                 "range does not satisfy this")
            return 1
    if type<=0 or type>=4:
        print("there is no such canoe type")
        return 1
    return 0

def plot_canoe(width, height, length, corner_radius, type):
    """
    make a 3D figure of a canoe. 
    input: 4 arrays showing ranges of width, height, length, and corner radius of the canoe
    input: 1 integer for canoe type
    output: 3D figure of the canoe with 4 sliders for width, height, length, corner radius
    """

    wrong=check(width, height, length, corner_radius, type)
    if wrong==1:
        return None
    """
    first, calculate the maximum number used to make the canoe. This will be
    used to define the range of x,y,z axis 
    """
    max_range=max(width[1], height[1], length[1])
    min_range=(-max_range)
    eta, theta=get_eta_theta(type)
    fig=go.Figure()
    X, Y, Z=get_coordinates(width[0], height[0], length[0], corner_radius[0], eta, theta, type)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, visible=False))
    """
    make the layout of the figure. We added the title, range of x,y,z axis, 
    bounded y-axis by x-axis, made sure that figure of canoe always show up in the center
    """
    fig.layout = go.Layout(title='Type '+str(type)+' canoe visualization',
        scene=dict(
        xaxis=dict(range=[min_range, max_range]),
        yaxis=dict(range=[min_range, max_range]),
        zaxis=dict(range=[min_range, max_range])))
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.data[0].visible=True
 
    @interact(width=(width[0], width[1], 0.1), height=(height[0], height[1], 0.1), 
              length=(length[0], length[1], 0.1), corner_radius=(corner_radius[0], corner_radius[1], 0.1))
    def update(width, height, length, corner_radius):
        with fig.batch_update():
            X, Y, Z=get_coordinates(width, height, length, corner_radius, eta, theta, type)
            fig.data[0].x=X
            fig.data[0].y=Y
            fig.data[0].z=Z
        return fig
