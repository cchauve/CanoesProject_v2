import plotly.graph_objects as go
GLOBAL_WaterDensity = 997     #(kg / m^3)
GLOBAL_Gravity      = 9.80665 #(m/s^2)

"""
For handling all the inputs and outputs of the simple cube model
"""

def CalcEquilibrium(height, density, waterDensity, gravity):
    """
    Takes a height, density of object, waterDensity, and gravity to calculate the equilibrium.
    Length and depth of object arent neccesary and get cancelled out.
    """
    return height*density*gravity / waterDensity
    
def CalcBouyancy(length, depth, height, waterLevel, waterDensity = GLOBAL_WaterDensity, gravity = GLOBAL_Gravity):
    """
    Calculates the current bouyancy force given the current length, depth, height, waterLevel.
    WaterDensity and gravity have a constant global value unless told otherwise. Still trying to find 
    a nice way around it.
    """
    
    #max and min to clamp waterLevel to be no less than 0, and no bigger than height. 
    return max(min(height, waterLevel), 0) * depth * length * waterDensity * gravity

def CalcWeight(length, depth, height, density, gravity = GLOBAL_Gravity):
    """
    Takes length, depth, height, density and gravity which has a default value unless stated otherwise.
    """
    return length * depth * height * density * gravity


"""
Graphing tools are past this point
"""

def GetWaterDiagram(length, waterLevel):
    """
    The polygon line drawing of what the box looks like
    """
    X = [-length, 2*length, None, 0,  0         ,  length    , length]
    Y = [ 0     , 0       , None, 0, -waterLevel, -waterLevel, 0     ]
    return X, Y

def GetCubeDiagram(length, height, waterLevel):
    """
    The polygon line drawing of what the water + box looks like
    """
    X = [0, length , length             , 0                  , 0]
    Y = [0, 0      , height - waterLevel, height - waterLevel, 0]
    return X, Y

def GetWaterTrace(length, waterLevel):
    """
    The graph for our water, including the cube thats under it. 
    Takes the length of the 
    """
    X , Y = GetWaterDiagram(length, waterLevel)
    scatter = go.Scatter(
        visible = False,
        line = dict(color = "#1991df", width = 3),
        name = "w = " + str(waterLevel),
        x = X,
        y = Y
    )
    return scatter

def GetCubeTrace(length, height, waterLevel):
    """
    The graph for our cube thats out of the water. 
    """
    X,Y = GetCubeDiagram(length, height, waterLevel) 
    traceCube = go.Scatter(
                    visible = False,
                    line = dict(color = "#141414", width = 3),
                    name = "v = " + str(waterLevel),
                    x = X, 
                    y = Y,
                )
    return traceCube

def GetSliders(steps, resolution, prefixText):
    """
    Sets up the slider ui, inserts what the steps look like, the resolution (how many steps)
    Aswell as some prefix text for the slider.
    """
    sliderList = [dict(
        active = int(resolution/2),
        currentvalue = {"prefix":  prefixText},
        pad = {"t": resolution},
        steps = steps,
    )]
    
    return sliderList

def GenerateSteps(length, depth, height, density, N, TitleText):
    """
    What each slice of the slider will look like, as well as what the title will look like
    Takes in a length, depth, height, and density to calculate force total.
    Height is disjoint, and preset need to fix for the future.
    """
    steps = []
    for i in range(0, N, 2):
        waterLevel = i/2 * height/(N/2 - 1)
        waterLevelStr = "{:.4f}".format(waterLevel)
        
        buoyancyForce = CalcBouyancy(length, depth, height, waterLevel)
        weightForce = CalcWeight(length, depth, height, density)
        totalForce = "{:.4f}".format(buoyancyForce - weightForce)
        
        step = dict(
            method = "update",
            args = [{"visible": [False]*N},
                    {"title": TitleText[0] + waterLevelStr + TitleText[1] + totalForce}],
        )
        step["args"][0]["visible"][i  ] = True
        step["args"][0]["visible"][i+1] = True
        steps.append(step)
    return steps