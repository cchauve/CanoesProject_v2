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
    listV = [[[[0,0,0],[0,0,0],[0,0,0]] for i in range(num_u)] for j in range(num_v)]
    listU = [[[[0,0,0],[0,0,0],[0,0,0]] for i in range(num_u)] for j in range(num_v)]
    for i in range(num_v):
        for j in range(num_u):
            listV[i][j][1] = splineV[i].bezier_points[j].co
            listU[i][j][1] = splineU[j].bezier_points[i].co
            for l in range(3):
                listV[i][j][0][l] = splineV[i].bezier_points[j].handle_left[l] - splineV[i].bezier_points[j].co[l]
                listV[i][j][2][l] = splineV[i].bezier_points[j].handle_right[l] - splineV[i].bezier_points[j].co[l] 
                
                listU[i][j][0][l] = splineU[j].bezier_points[i].handle_left[l] - splineU[j].bezier_points[i].co[l]
                listU[i][j][2][l] = splineU[j].bezier_points[i].handle_right[l] - splineU[j].bezier_points[i].co[l] 
            
    #we want to sort V by average z, in increasing form
    #we want to sort U by average x, in increasing form
    listV = specialBubbleSort(listV, 2)
    listU = specialBubbleSort(listU, 0)
    return listV, listU

"""
Returns a sorted spline, organized by increasing average x,y,z value

size          number of elements in spline
secondarySize number of elements within spline
element       = 0 -> x
              = 1 -> y
              = 2 -> z
"""
def specialBubbleSort(spline, element):
    size = len(spline)
    secondarySize = len(spline[0])
    for sort_itr in range(1, size - 1):
        for spline_itr in range(0, (size - 1) - sort_itr):
            bpy.data.texts["myFile.txt"].write(str(spline_itr) + " ")
            this_points = spline[spline_itr    ]
            next_points = spline[spline_itr + 1]
            thisAverage = 0
            nextAverage = 0
            for point_itr in range(0, secondarySize):
                thisAverage += this_points[point_itr][1][element]
                nextAverage += next_points[point_itr][1][element]

            #perform the bubble sort
            if (thisAverage > nextAverage):
                spline[spline_itr  ] = next_points
                spline[spline_itr+1] = this_points
    return spline
"""
Parses all the curve data into a string for export.
"""
def ParseString(curvesDataV, curvesDataU):
    VectorToString = lambda vector: "["+"{:.5f}".format(vector[0])+","+"{:.5f}".format(vector[1])+","+"{:.5f}".format(vector[2])+"]"
    num_v = len(curvesDataV)
    num_u = len(curvesDataV[0])

    P = "P=["
    V = "V=["
    U = "U=["

    for i in range(num_v-1):
        P += "\n  ["
        V += "\n  ["
        U += "\n  ["
        for j in range(num_u-1):
            P += VectorToString(curvesDataV[i][j][1]) + ","
            V += VectorToString(curvesDataV[i][j][2]) + ","
            U += VectorToString(curvesDataU[i][j][2]) + ","
        #Catch the last indexs, and get the last row of V
        P += VectorToString(curvesDataV[i][num_u-1][1]) + "]," #comma to start the next list
        V += VectorToString(curvesDataV[i][num_u-1][2]) + "]\n  ["
        U += VectorToString(curvesDataU[i][num_u-1][2]) + "]\n  ["

        for j in range(num_u-1):
            V += VectorToString(curvesDataV[i+1][j][0]) + ","
            U += VectorToString(curvesDataU[i+1][j][0]) + ","
        V += VectorToString(curvesDataV[i+1][num_u-1][0]) + "]"
        U += VectorToString(curvesDataU[i+1][num_u-1][0]) + "]"
        if (i < num_v-2): 
            V+= "," #else we've hit the end of V
            U+= ","
    P += "\n  ["
    for j in range(num_u-1):
        P += VectorToString(curvesDataV[num_v-1][j][1]) + ","
    P += VectorToString(curvesDataV[num_v-1][num_u-1][1]) + "]\n  ]" #no comma as this is the end
    V+="\n  ]"
    U+="\n  ]"

    return P + "\n\n" + V + "\n\n" + U

curveName = "Nootkan"
curvesV = bpy.data.curves[curveName + " V"]
curvesU = bpy.data.curves[curveName + " U"]
curvesDataV, curvesDataU = InitializeCurves(curvesV, curvesU)
#P,V,U = Parse(curvesDataV, curvesDataU)

bpy.data.texts[curveName].write(ParseString(curvesDataV, curvesDataU))

    
    

