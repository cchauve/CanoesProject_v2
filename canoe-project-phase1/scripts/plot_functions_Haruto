#import numpy, which is useful to plot functions
#import plotly.graph_objs, which is used to make 3D graphs
import numpy as np
import plotly.graph_objs as go
def coordinates(w, h, l, c, type):
    #This is to calculate the 3D coordinates of the Canoe
    #it returns 2D list of numbers X, Y, Z that stores 3D coordinates.
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
    #For the input, we have 4 array input for 'width, height, length, and corner_radius'
    #and 1 integer input for 'type'.
    
    #make a figure of a canoe we want to make, and returns the figure we made.
    #the figure can only show one changing parameter for the slider.
    
    #first, find which parameter is the changing parameter, 
    #and put that paraneter name into 'label'
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
    
    #Then, get the min and max range of the 3D figure of the canoe we will be making
    max_range = 1.5 * max([max(width), max(height), max(length)])
    min_range = - max_range

    fig = go.Figure()

    #Since we want to make a canoe with a changing parameter
    #we will be making a canoe for all the cases parameter changes
    #and switch which canoe to show as we decide on which parameter to show. 
    
    for w in width:
            for h in height:
                for l in length:
                    for c in corner_radius:
                        #Do calculations to get the coordinates to make the 
                        #3D figure according to the type of Canoe we have.
                        #X is the list of X coordinates of the canoe we are making
                        #Y is the list of Y coordinates of the canoe we are making
                        #Z is the list of Z coordinates of the canoe we are making
                        X, Y, Z = coordinates(w, h, l, c, type)
                        
                        #make the 3D figure
                        fig.add_trace(go.Surface(x=X, y=Y, z=Z, visible=False))
                        fig.layout = go.Layout(title='Type '+str(type)+' canoe visualization',
                            scene=dict(
                                xaxis=dict(range=[min_range, max_range]),
                                yaxis=dict(range=[min_range, max_range]),
                                zaxis=dict(range=[min_range, max_range])))
    
    fig.update_yaxes(scaleanchor = "x", scaleratio = 1)
    fig.data[0].visible = True

#Make a slider for the changing parameter
    steps = []
    for i in range(len(fig.data)):
        step = dict(method="update", label="{:.2f}".format(R_selected[i]),
                    args=[{"visible": [False] * len(fig.data)}])
        step["args"][0]["visible"][i] = True
        steps.append(step)

    sliders = [dict(active=0, currentvalue={"prefix": label}, pad={"t": 50},
    steps=steps)]

    fig.update_layout(sliders=sliders)
    return fig
