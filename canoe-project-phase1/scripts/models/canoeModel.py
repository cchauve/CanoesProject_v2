import scripts.BezierSurface as bs

def GetCanoe(ideal_length, ideal_width, ideal_height, canoe_type, resolution):
    inputArgs = {"ideal_length":ideal_length, "ideal_width":ideal_width, "ideal_height":ideal_height, "onlyDimensions":False}

    if   (canoe_type == 1):
        P, V, U = GetCanoeNootkan(**inputArgs)
    elif (canoe_type == 2):
        P, V, U = GetCanoeHaida(**inputArgs)
    elif (canoe_type == 3):
        P, V, U = GetCanoeKutenai(**inputArgs)
    else:
        P, V, U = GetCanoeNootkan(**inputArgs)

    XX, YY, ZZ = bs.GetSurface(P,U,V, resolution)
    return XX, YY, ZZ   

def ScaleArray(A, scale):
    num_rows = len(A)
    num_cols = len(A[0])
    for i in range(num_rows):
        for j in range(num_cols):
            A[i][j][0] *= scale[0]
            A[i][j][1] *= scale[1]
            A[i][j][2] *= scale[2]
    return A

def ScaleSpecialArray(A, scale):
    num_rows = len(A)
    num_cols = len(A[0])
    num_inner = len(A[0][0])
    for i in range(num_rows):
        for j in range(num_cols):
            for k in range(num_inner):
                A[i][j][k][0] *= scale[0]
                A[i][j][k][1] *= scale[1]
                A[i][j][k][2] *= scale[2]
    return A

def GetCanoeNootkan(ideal_length, ideal_width, ideal_height, onlyDimensions):
    """
    Nootkan Style Canoe
    
    returns the P, U, V arrays for the bs.GetSurface method
    """
    #units in metric
    length = 7.687
    width = 1.249
    height = 1.135
    if(onlyDimensions):
        return [length,width,height]
    scale = [ideal_length / length, ideal_width  / width, ideal_height / height]

    P =	[
        [[0.031,0.000,0.048],[0.031,0.000,0.048],[0.795,0.000,0.003],[3.648,0.000,0.003],[6.581,-0.000,0.031],[7.217,-0.000,0.387],[7.687,-0.000,0.898]],
        [[-0.011,0.000,0.558],[-0.011,-0.070,0.558],[0.811,-0.292,0.440],[3.623,-0.625,0.438],[5.786,-0.450,0.522],[7.041,-0.185,0.717],[7.666,-0.087,1.135]]
        ]

    V =	[
        [[[-0.000,0.000,0.000],[0.000,0.000,0.000]],[[0.274,0.000,-0.033],[-0.210,0.000,0.000]],[[0.193,0.000,-0.000],[-1.365,0.000,0.003]],[[1.259,0.000,-0.002],[-0.584,0.000,-0.017]],[[0.539,-0.000,0.015],[-0.208,0.000,-0.316]],[[0.192,-0.000,0.291],[-0.135,0.000,-0.098]]],
        [[[-0.003,-0.029,0.000],[-0.001,0.039,0.001]],[[0.379,0.023,-0.057],[-0.520,0.113,0.023]],[[0.588,-0.128,-0.026],[-1.153,-0.004,-0.021]],[[0.787,0.003,0.014],[-0.832,-0.135,-0.066]],[[0.928,0.150,0.073],[-0.177,-0.049,-0.060]],[[0.331,0.091,0.112],[-0.104,0.000,-0.162]]]
        ]

    U =	[
        [[[-0.019,-0.034,0.142],[-0.013,-0.002,-0.161]],[[0.000,0.000,0.131],[-0.018,0.002,-0.174]],[[0.003,-0.114,0.000],[0.000,0.206,-0.274]],[[-0.016,-0.393,0.000],[0.010,0.332,-0.432]],[[-0.440,-0.176,0.204],[0.056,0.109,-0.093]],[[-0.039,-0.029,0.061],[0.047,0.086,-0.071]],[[-0.005,-0.020,0.087],[0.007,0.024,-0.069]]]
        ]

    P = ScaleArray(P, scale)
    V = ScaleSpecialArray(V, scale)
    U = ScaleSpecialArray(U, scale)
    return P, V, U

def GetCanoeKutenai(ideal_length, ideal_width, ideal_height, onlyDimensions):
    """
    Kutenai Style Canoe
    
    returns the P, U, V arrays for the bs.GetSurface method
    """
    #units in metric
    length = 4.672
    width = 0.628
    height = 0.376
    if(onlyDimensions):
        return [length,width,height]
    scale = [ideal_length / length, ideal_width  / width, ideal_height / height]

    P =	[
        [[0.001,0.000,0.013],[1.231,0.000,0.027],[2.337,0.000,0.022],[3.442,0.000,0.027],[4.672,0.000,0.013]],
        [[0.446,0.000,0.192],[1.143,-0.174,0.151],[2.337,-0.272,0.148],[3.530,-0.174,0.151],[4.228,0.000,0.192]],
        [[0.814,0.000,0.376],[1.447,-0.216,0.335],[2.336,-0.314,0.332],[3.227,-0.216,0.335],[3.859,0.000,0.376]]
        ]

    V =	[
        [[[0.430,-0.000,-0.021],[-0.265,-0.000,-0.002]],[[0.265,0.000,0.002],[-0.433,0.000,0.000]],[[0.433,0.000,0.000],[-0.265,0.000,0.002]],[[0.265,-0.000,-0.002],[-0.430,-0.000,-0.021]]],
        [[[0.251,-0.072,-0.016],[-0.257,0.046,0.008]],[[0.251,-0.045,-0.008],[-0.263,0.000,0.000]],[[0.263,0.000,0.000],[-0.251,-0.045,-0.008]],[[0.257,0.046,0.008],[-0.251,-0.072,-0.016]]],
        [[[0.243,-0.094,-0.016],[-0.255,0.057,0.008]],[[0.248,-0.055,-0.008],[-0.263,0.000,0.000]],[[0.263,0.000,0.000],[-0.248,-0.055,-0.008]],[[0.255,0.057,0.008],[-0.243,-0.094,-0.016]]]
        ]

    U =	[
        [[[0.193,-0.000,0.073],[-0.108,0.000,-0.045]],[[-0.045,-0.088,0.001],[-0.021,0.011,-0.058]],[[0.000,-0.170,0.000],[0.007,0.023,-0.053]],[[0.045,-0.088,0.001],[0.021,0.011,-0.058]],[[-0.193,-0.000,0.073],[0.108,0.000,-0.045]]],
        [[[0.108,0.000,0.045],[-0.131,0.000,-0.076]],[[0.021,-0.011,0.056],[-0.117,-0.026,-0.050]],[[-0.007,-0.023,0.053],[0.000,0.006,-0.073]],[[-0.021,-0.011,0.056],[0.117,-0.026,-0.050]],[[-0.108,0.000,0.045],[0.131,0.000,-0.076]]]
        ]

    P = ScaleArray(P, scale)
    V = ScaleSpecialArray(V, scale)
    U = ScaleSpecialArray(U, scale)
        
    return P, V, U

def GetCanoeHaida(ideal_length, ideal_width, ideal_height, onlyDimensions):
    """
    Haida Style Canoe

    returns the P, U, V arrays for the bs.GetSurface method
    """
    #units in metric
    length = 6.379
    width = 1.005
    height = 0.811
    if(onlyDimensions):
        return [length,width,height]
    scale = [ideal_length / length, ideal_width  / width, ideal_height / height]

    P =	[
        [[0.034,0.000,0.561],[0.468,0.000,0.152],[1.007,-0.000,-0.016],[2.897,0.000,-0.018],[5.191,0.000,-0.003],[5.225,0.000,0.254],[6.204,-0.000,0.539],[6.379,0.000,0.597]],
        [[0.017,0.000,0.649],[0.246,0.042,0.446],[1.080,0.255,0.177],[2.865,0.393,0.060],[4.830,0.181,0.148],[5.192,0.154,0.365],[6.292,0.047,0.666],[6.374,0.000,0.704]],
        [[-0.001,0.000,0.737],[0.000,0.045,0.737],[1.155,0.418,0.472],[2.857,0.503,0.420],[4.475,0.476,0.480],[5.201,0.357,0.580],[6.370,0.048,0.811],[6.370,0.000,0.811]]
        ]

    V =	[
        [[[0.169,0.000,-0.160],[-0.177,-0.000,0.152]],[[0.169,0.000,-0.145],[-0.348,0.000,0.014]],[[0.630,0.000,-0.001],[-0.823,-0.000,0.000]],[[0.626,0.000,0.000],[-1.008,-0.000,0.000]],[[0.008,-0.000,0.093],[-0.015,0.000,-0.094]],[[0.376,0.000,0.091],[-0.342,-0.000,-0.107]],[[0.068,0.000,0.021],[-0.068,-0.000,-0.023]]],
        [[[0.000,0.046,0.000],[-0.155,-0.012,0.104]],[[0.411,0.020,-0.099],[-0.326,-0.070,0.087]],[[0.638,0.137,-0.169],[-0.700,0.006,-0.016]],[[1.307,-0.012,0.029],[-0.443,0.223,-0.115]],[[0.146,-0.011,0.076],[-0.147,0.021,-0.071]],[[0.400,-0.056,0.192],[-0.192,0.026,-0.042]],[[0.038,-0.005,0.008],[0.000,0.039,0.000]]],
        [[[0.000,0.017,0.000],[0.000,-0.014,0.000]],[[0.447,0.143,-0.122],[-0.253,-0.047,0.031]],[[0.355,0.066,-0.043],[-0.977,-0.016,0.000]],[[0.928,0.016,0.000],[-0.635,0.057,-0.044]],[[0.288,-0.026,0.020],[-0.273,0.075,-0.050]],[[0.447,-0.123,0.082],[-0.388,0.104,-0.074]],[[0.000,-0.015,0.000],[0.000,0.020,0.000]]]
        ]

    U =	[
        [[[-0.007,0.000,0.034],[0.007,0.000,-0.034]],[[-0.091,0.019,0.113],[0.074,-0.009,-0.089]],[[0.025,0.079,0.012],[-0.012,-0.081,-0.073]],[[-0.015,0.196,-0.007],[0.006,-0.075,-0.066]],[[0.011,0.088,-0.000],[0.192,-0.171,-0.064]],[[0.000,0.080,0.000],[0.001,-0.067,-0.062]],[[0.033,0.028,0.045],[-0.027,-0.006,-0.042]],[[-0.002,-0.000,0.042],[0.002,0.000,-0.042]]],
        [[[-0.007,0.000,0.034],[0.007,0.000,-0.034]],[[-0.074,0.009,0.089],[0.079,0.008,-0.116]],[[0.012,0.081,0.073],[-0.049,0.006,-0.132]],[[-0.006,0.075,0.066],[-0.001,-0.007,-0.181]],[[-0.113,0.183,0.079],[0.087,0.001,-0.172]],[[-0.001,0.067,0.062],[0.023,-0.049,-0.142]],[[0.027,0.006,0.042],[-0.026,0.003,-0.057]],[[-0.002,-0.000,0.042],[0.002,0.000,-0.042]]]
        ]

    P = ScaleArray(P, scale)
    V = ScaleSpecialArray(V, scale)
    U = ScaleSpecialArray(U, scale)
    return P, V, U