import numpy as np
import plotly.graph_objs as go

def type_one(r1, r2, r3, eta, theta):
    X = r3 * np.cos(eta)
    Y = r1 * np.sin(eta) * np.sin(theta)
    Z = r2 * np.cos(theta)

    return X, Y, Z


def type_two(r1, r2, r3, eta, theta):
    X = r3 * np.cos(eta)
    Y = r1 * np.sin(eta) * np.sin(theta)
    Z = r2 * np.abs(np.sin(eta)) * np.cos(theta)

    return X, Y, Z


def type_three(r1, r2, r3, ia, eta, theta):
    X = r3 * np.cos(eta)
    Y = r1 * np.sin(eta) * np.abs(np.sin(theta)) ** (ia / (r1 * np.sin(eta))) * np.sign(np.sin(theta))
    Z = r2 * np.abs(np.sin(eta)) * np.abs(np.cos(theta)) ** (ia / (r2 * np.abs(np.sin(eta)))) * \
        np.sign(np.cos(theta))

    return X, Y, Z


def plot_canoe(R1, R2, R3, a, eta, theta, type):
    # can show slider for only one parameter at a time

    which_R_max = np.argmax([len(R1), len(R2), len(R3), len(a)])
    if which_R_max == 0:
        R_selected = R1
        label = 'R1: '
    elif which_R_max == 1:
        R_selected = R2
        label = 'R2: '
    elif which_R_max == 2:
        R_selected = R3
        label = 'R3: '
    else:
        R_selected = a
        label = 'a: '
    
    max_range = 1.5 * max([max(R1), max(R2), max(R3)])
    min_range = - max_range

    fig = go.Figure()

    for r1 in R1:
            for r2 in R2:
                for r3 in R3:
                    for ia in a:

                        if type == 1:
                            X, Y, Z = type_one(r1, r2, r3, eta, theta)
                        elif type == 2:
                            X, Y, Z = type_two(r1, r2, r3, eta, theta)
                        else:
                            X, Y, Z = type_three(r1, r2, r3, ia, eta, theta)
        
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
