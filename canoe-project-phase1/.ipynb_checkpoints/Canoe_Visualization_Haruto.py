#!/usr/bin/env python
# coding: utf-8

# In[29]:


import numpy as np
import plotly.graph_objs as go

def type_one(r1, r2, r3):
    eta, theta = np.meshgrid(np.linspace(0.0, 2 * np.pi, 50), np.linspace(np.pi / 2, 3 * np.pi / 2, 50))
    X = r3 * np.cos(eta)
    Y = r1 * np.sin(eta) * np.sin(theta)
    Z = r2 * np.cos(theta)
    return X, Y, Z


def type_two(r1, r2, r3):
    eta, theta = np.meshgrid(np.linspace(0.0, 2 * np.pi, 50), np.linspace(np.pi / 2, 3 * np.pi / 2, 50))
    X = r3 * np.cos(eta)
    Y = r1 * np.sin(eta) * np.sin(theta)
    Z = r2 * np.abs(np.sin(eta)) * np.cos(theta)

    return X, Y, Z


def type_three(r1, r2, r3, ia):
    eta, theta = np.meshgrid(np.linspace(0.01, np.pi - 0.01, 50), np.linspace(np.pi / 2, 3 * np.pi / 2, 50))
    X = r3 * np.cos(eta)
    Y = r1 * np.sin(eta) * np.abs(np.sin(theta)) ** (ia / (r1 * np.sin(eta))) * np.sign(np.sin(theta))
    Z = r2 * np.abs(np.sin(eta)) * np.abs(np.cos(theta)) ** (ia / (r2 * np.abs(np.sin(eta)))) *         np.sign(np.cos(theta))

    return X, Y, Z


def plot_canoe(Width, Height, Length, Corner_radius, type):
    # can show slider for only one parameter at a time
    
    #first, find which parameter is the changing parameter, 
    #and put that paraneter name into 'label'
    which_R_max = np.argmax([len(Width), len(Height), len(Length), len(Corner_radius)])
    if which_R_max == 0:
        R_selected = Width
        label = 'Width: '
    elif which_R_max == 1:
        R_selected = Height
        label = 'Height: '
    elif which_R_max == 2:
        R_selected = Length
        label = 'Length: '
    else:
        R_selected = Corner_radius
        label = 'Corner_radius: '
    
    #Then, get the min and max range of the 3D figure of the canoe we will be making
    max_range = 1.5 * max([max(Width), max(Height), max(Length)])
    min_range = - max_range

    fig = go.Figure()

    for w in Width:
            for h in Height:
                for l in Length:
                    for c in Corner_radius:
                        #Do calculations to get the parameters to make the 
                        #3D figure according to the type of Canoe we have.
                        if type == 1:
                            X, Y, Z = type_one(w, h, l)
                        elif type == 2:
                            X, Y, Z = type_two(w, h, l)
                        else:
                            X, Y, Z = type_three(w, h, l, c)
                        
                        #Get outside of for loop, and make the 3D figure
                        fig.add_trace(go.Surface(x=X, y=Y, z=Z, visible=False))
                        fig.layout = go.Layout(
                            title='Type ' + str(type) + ' canoe visualization',
                            scene=dict(
                                xaxis=dict(
                                    gridcolor='rgb(255, 255, 255)',
                                    zerolinecolor='rgb(255, 255, 255)',
                                    showbackground=True,
                                    backgroundcolor='rgb(230, 230,230)',
                                    range=[min_range, max_range]),
                                yaxis=dict(
                                    gridcolor='rgb(255, 255, 255)',
                                    zerolinecolor='rgb(255, 255, 255)',
                                    showbackground=True,
                                    backgroundcolor='rgb(230, 230,230)',
                                    range=[min_range, max_range],
                                    ),
                                zaxis=dict(
                                    gridcolor='rgb(255, 255, 255)',
                                    zerolinecolor='rgb(255, 255, 255)',
                                    showbackground=True,
                                    backgroundcolor='rgb(230, 230,230)',
                                    range=[min_range, max_range])))
    
    fig.update_yaxes(
    scaleanchor = "x",
    scaleratio = 1,
  )
    fig.data[0].visible = True

    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            label="{:.2f}".format(R_selected[i]),
            args=[{"visible": [False] * len(fig.data)}]
        )
        step["args"][0]["visible"][i] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": label},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
    )
    return fig


# In[30]:


import numpy as np
Width = np.arange(0.3, 1.5, 0.1)
Height = [1.0]
Length = [3.0]
Corner_radius=[0.0]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=1)
fig.show()


# In[21]:


Width = [0.6]
Height = np.arange(0.6, 1.1, 0.1)
Length = [3.0]
Corner_radius=[0.0]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=1)
fig.show()


# In[22]:


Width = [0.6]
Height = [1.0]
Length = np.arange(1.0, 2.1, 0.1)
Corner_radius=[0.2]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=1)
fig.show()


# In[23]:


Width = np.arange(0.3, 1.5, 0.1)
Height = [1.0]
Length = [3.0]
Corner_radius=[0.0]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=2)
fig.show()


# In[24]:


Width = [0.6]
Height = np.arange(0.6, 1.1, 0.1)
Length = [3.0]
Corner_radius=[0.0]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=2)
fig.show()


# In[25]:


Width = [0.6]
Height = [1.0]
Length = np.arange(1.0, 2.1, 0.1)
Corner_radius=[0.0]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=2)
fig.show()


# In[26]:


Width = np.arange(0.3, 1.5, 0.1)
Height = [1.0]
Length = [3.0]
Corner_radius=[0.2]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=3)
fig.show()


# In[27]:


Width = [0.6]
Height = np.arange(0.6, 1.1, 0.1)
Length = [3.0]
Corner_radius=[0.2]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=3)
fig.show()


# In[31]:


Width = [0.6]
Height = [1.0]
Length = np.arange(1.0, 2.1, 0.1)
Corner_radius=[0.2]
fig = plot_canoe(Width, Height, Length, Corner_radius, type=3)
fig.show()


# In[32]:


Width = [0.6]
Height = [1.0]
Length = [3.0]
Corner_radius = np.arange(0.1, 0.3, 0.05)
fig = plot_canoe(Width, Height, Length, Corner_radius, type=3)
fig.show()


# In[ ]:




