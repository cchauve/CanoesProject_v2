import bpy
#https://docs.blender.org/api/current/bpy.types.BezierSplinePoint.html
#splines[#].bezier_points.-- 
#- co            for control point
#- handle_left   for the first handle
#- handle_right  for the second handle
"""
Initializes the curves data into lists
then Sorts it, by ascending order in x and z
"""
def InitializeCurves(curvesV, curvesU):
    splineV = curvesV.splines
    splineU = curvesU.splines

    num_v = len(splineV)
    num_u = len(splineU)
    #We set up 3 vectors 
    #[0] for left handle vector
    #[1] for originm
    #[2] for right handle vector
    listV = [[[[0,0,0],[0,0,0],[0,0,0]] for i in range(num_u)] for j in range(num_v)]
    listU = [[[[0,0,0],[0,0,0],[0,0,0]] for i in range(num_u)] for j in range(num_v)]
    for i in range(num_v):
        for j in range(num_u):
            #To shorten and limit the calls to memeory
            pointV = splineV[i].bezier_points[j]
            pointU = splineU[j].bezier_points[i]

            listV[i][j][1] = pointV.co
            listU[i][j][1] = pointU.co
            #loops through each list value, for vector subtraction.
            for l in range(3):
                listV[i][j][0][l] = pointV.handle_left[l]  - pointV.co[l]
                listV[i][j][2][l] = pointV.handle_right[l] - pointV.co[l] 
                
                listU[i][j][0][l] = pointU.handle_left[l]  - pointU.co[l]
                listU[i][j][2][l] = pointU.handle_right[l] - pointU.co[l] 
    
    #listV[i][j] i cycles through the bezier_points, j cycles through the splines
    #listU[i][j] i cycles through the splines, j cycles through the bezier_points
    #we want to sort V by average z, in increasing form
    #we want to sort U by average x, in increasing form
    listV = specialBubbleSort(listV, 2, True)
    listU = specialBubbleSort(listU, 0, False)
    return listV, listU

"""
Returns a sorted spline, organized by increasing average x,y,z value

size          number of elements in spline
secondarySize number of elements within spline
element       = 0 -> x
              = 1 -> y
              = 2 -> z
"""
def specialBubbleSort(spline, element, state):
    if (state):
        size = len(spline)
        secondarySize = len(spline[0])
    else:
        size = len(spline[0])
        secondarySize = len(spline)
    
    if state:
        for sort_itr in range(size):
            for spline_itr in range(0, size - sort_itr - 1):
                this_points = spline[spline_itr    ]
                next_points = spline[spline_itr + 1]
                thisAverage = 0
                nextAverage = 0
                for point_itr in range(0, secondarySize):
                    thisAverage += this_points[point_itr][1][element]
                    nextAverage += next_points[point_itr][1][element]

                #perform the bubble sort and swap!
                if (thisAverage > nextAverage):
                    spline[spline_itr  ] = next_points
                    spline[spline_itr+1] = this_points
    else:
        for sort_itr in range(size):
            for spline_itr in range(0, size- sort_itr - 1):
                thisAverage = 0
                nextAverage = 0
                for point_itr in range(0, secondarySize):
                    thisAverage += spline[point_itr][spline_itr][1][element]
                    nextAverage += spline[point_itr][spline_itr+1][1][element]
                
                if (thisAverage > nextAverage):
                    for point_itr in range(0, secondarySize):
                        spline[point_itr][spline_itr], spline[point_itr][spline_itr+1] = spline[point_itr][spline_itr+1], spline[point_itr][spline_itr]
    return spline
"""
Parses all the curve data into a string for export.
"""
def ParseString(curvesDataV, curvesDataU):
    VectorToString = lambda vector: "["+"{:.3f}".format(vector[0])+","+"{:.3f}".format(vector[1])+","+"{:.3f}".format(vector[2])+"]"
    GetLength = lambda vector: vector[0]
    GetWidth  = lambda vector: abs(vector[1])
    GetHeight = lambda vector: vector[2]
    num_v = len(curvesDataV)
    num_u = len(curvesDataV[0])
    
    max_length = 0
    max_width = 0
    max_height = 0

    P = "P =\t["
    V = "V =\t["
    U = "U =\t["

    for i in range(num_v):
        P += "\n\t["
        V += "\n\t["
        if (i < num_v-1):
            U += "\n\t["
        
        for j in range(num_u):
            P += VectorToString(curvesDataV[i][j][1]) + ","
            if (GetLength(curvesDataV[i][j][1]) > max_length):
                max_length = GetLength(curvesDataV[i][j][1])
                
            if (GetWidth (curvesDataV[i][j][1]) > max_width):
                max_width  = GetWidth (curvesDataV[i][j][1])
            
            if (GetHeight(curvesDataV[i][j][1]) > max_height):
                max_height = GetHeight(curvesDataV[i][j][1])
            
            if (j < num_u-1):
                #Get the vectors, else you are just collecting the last point.
                V += "[" + VectorToString(curvesDataV[i][j  ][2]) + "," 
                V +=       VectorToString(curvesDataV[i][j+1][0]) + "],"

            if (i < num_v-1):
                U += "[" + VectorToString(curvesDataU[i  ][j][2]) + "," 
                U +=       VectorToString(curvesDataU[i+1][j][0]) + "],"    
        #Backspace the last comma
        P = P[:len(P)-1] + "],"
        V = V[:len(V)-1] + "],"

        if (i!= num_v-1):
            U = U[:len(U)-1] + "],"
    
    #Backspace the last comma then close it up
    P = P[:len(P)-1] + "\n\t]"
    V = V[:len(V)-1] + "\n\t]"
    U = U[:len(U)-1] + "\n\t]"
    #width * 2 since the canoe/vessel is two times as long.
    properties   = "length = "+"{:.3f}".format(max_length) + "\nwidth = "+"{:.3f}".format(max_width*2) + "\nheight = "+"{:.3f}".format(max_height)
    length_scale = "ideal_length / length"
    width_scale  = "ideal_width  / width"
    height_scale = "ideal_height / height"
    properties  += "\nif(onlyDimensions):\n\treturn [length,width,height]"
    properties  += "\nscale = [" + length_scale + ", " + width_scale + ", " + height_scale + "]"
    
    functionCall = "P = ScaleArray(P, scale)\nV = ScaleSpecialArray(V, scale)\nU = ScaleSpecialArray(U, scale)"
    return "#units in metric\n" + properties + "\n\n" + P + "\n\n" + V + "\n\n" + U + "\n\n" + functionCall



curveName = "Nootkan"
curvesV = bpy.data.curves[curveName + " V"]
curvesU = bpy.data.curves[curveName + " U"]
curvesDataV, curvesDataU = InitializeCurves(curvesV, curvesU)


bpy.data.texts["Data"].write(ParseString(curvesDataV, curvesDataU))

    
    

