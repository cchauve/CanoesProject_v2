import numpy as np
import plotly.graph_objs as go

def coordinates(w, h, l, c, type):
    """
    Get the 3D coordinates of the canoe
    input: 5 integer values for width, height, length, corner radius, and canoe type
    output: list of x-coordinates of the canoe, named X
    output: list of y-coordinates of the canoe, named Y
    output: list of z-coordinates of the canoe, named Z
    """
    
    """
    get two arrays of numbers a and b for each canoe type to do the calculation
    calculate x-coordinates, y-coordinates, z-coordinates of the canoe
    """
    if  type == 1:
        a, b = np.meshgrid(np.linspace(0.0, 2*np.pi, 50), np.linspace(np.pi/2, (3/2)*np.pi, 50))
        X = l*np.cos(a)
        Y = w*np.sin(a)*np.sin(b)
        Z = h*np.cos(b)
        return X, Y, Z
    if type==2:
        a, b = np.meshgrid(np.linspace(0.0, 2*np.pi, 50), np.linspace(np.pi/2, (3/2)*np.pi, 50))
        X = l*np.cos(a)
        Y = w*np.sin(a)*np.sin(b)
        Z = h*np.abs(np.sin(a))*np.cos(b)
        return X, Y, Z
    if type==3:
        a, b = np.meshgrid(np.linspace(0.01, np.pi-0.01, 50), np.linspace(np.pi/2, (3/2)*np.pi, 50))
        X = l*np.cos(a)
        Y = w*np.sin(a)*np.abs(np.sin(b))**(c/(w*np.sin(a)))*np.sign(np.sin(b))
        Z = h*np.abs(np.sin(a))*np.abs(np.cos(b))**(c/(h*np.abs(np.sin(a))))*np.sign(np.cos(b))
        return X, Y, Z

def plot_canoe(width, height, length, corner_radius, type):
    """
    make a 3D figure of a canoe. The figure can only show one slider, and accepts only one changing variable
    input: 4 arrays for width, height, length, and corner radius of the canoe
    input: 1 integer for canoe type
    output: 3D plot of the canoe with a changing variable
    """
    
    """
    first, find which parameter is the changing variable
    so we could use that variable name in the figure
    """
    which_R_max = np.argmax([len(width), len(height), len(length), len(corner_radius)])
    if which_R_max == 0:
        R_selected = width
        label = 'width: '
    elif which_R_max == 1:
        R_selected = height
        label = 'height: '
    elif which_R_max == 2:
        R_selected = length
        label = 'length: '
    else:
        R_selected = corner_radius
        label = 'corner radius: '
    
    """
    then, get the min and max range of the 3D figure of the canoe we will be making
    """
    max_range = 1.5 * max([max(width), max(height), max(length)])
    min_range = - max_range

    fig = go.Figure()

    """
    since we want to make a canoe with a changing variable
    we will be making a canoe for all the cases value changes
    and switch which canoe to show as we decide on which value to show
    """
    
    for w in width:
            for h in height:
                for l in length:
                    for c in corner_radius:
                        """
                        make the 3D figure for each values in changing variable.
                        """
                        X, Y, Z = coordinates(w, h, l, c, type)
                        fig.add_trace(go.Surface(x=X, y=Y, z=Z, visible=False))
                        fig.layout = go.Layout(title='Type '+str(type)+' canoe visualization',
                            scene=dict(
                                xaxis=dict(range=[min_range, max_range]),
                                yaxis=dict(range=[min_range, max_range]),
                                zaxis=dict(range=[min_range, max_range])))
    
    fig.update_yaxes(scaleanchor = "x", scaleratio = 1)
    fig.data[0].visible = True

    """
    make a slider for the changing variable
    """
    steps = []
    for i in range(len(fig.data)):
        step = dict(method="update", label="{:.2f}".format(R_selected[i]), args=[{"visible": [False] * len(fig.data)}])
        step["args"][0]["visible"][i] = True
        steps.append(step)

    sliders = [dict(active=0, currentvalue={"prefix": label}, pad={"t": 50},
    steps=steps)]

    fig.update_layout(sliders=sliders)
    return fig
