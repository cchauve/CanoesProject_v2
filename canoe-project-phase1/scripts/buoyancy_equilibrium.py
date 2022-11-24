"""
This script is for calculating the equilibrium float line of 3d surfaces stored in the form
X = N by N list of points
Y = N by N list of points
Z = N by N list of points

This is done through an approximation method that does the equivalent calculation to matching the volume displaced with the weight of the boat.
Here we implement an approaximation of the Divergence Theorem. We make an assumption that the boat is symmetrical so all the forces cancel out except for the verticle ones.
We save the normals, height, and the area it represents into a list named heightNormalArea.
Then sum over every element, by linearly increasing the force of a given normal based on its height to water level. 

Best use is to get your X Y Z lists then call
EquilibriumSearch(X, Y, Z, weight, binarySearchMax = 16)
Put in the weight (in Newtons, mass times gravity) of your canoe then it will output the equilibrium level in terms of depth (distance from surface)
"""
#from numpy import sqrt
from math import sqrt, isnan
GLOBAL_WaterDensity = 997 #(kg / m^3)
GLOBAL_Gravity      = 9.80665 #(m/s^2)

def Cross(A , B, C):
    """returns a perpendicular vector with magnitude equal to the trapezoid defined by ABC
    A = [x,y,z]
    B ..
    C ..
    right hand rule ABC
    """
    U = [B[0]-A[0], B[1] - A[1], B[2] - A[2]]
    V = [C[0]-A[0], C[1] - A[1], C[2] - A[2]]
    
    x =  U[1]*V[2] - U[2]*V[1]
    y = -U[0]*V[2] + U[2]*V[0]
    z =  U[0]*V[1] - U[1]*V[0]
    #Mathematically the cross product already has the trapezoids area of the trapezoid defined by UV 
    return [x,y,z]


def GetArea(heightNormalArea):
    """Returns the total surface area of the surface
    Takes a heightNormalArea list
    
    Should update in the future so there's less unused data being passed around
    """
    area = 0
    for i in range(0, len(heightNormalArea)):
        area = heightNormalArea[i][2]
    return area


def GetMinMaxHeight(heightNormalArea):
    """Returns the minumum and maximum height from heightNormalArea"""
    minimum = heightNormalArea[0][0]
    maximum = heightNormalArea[0][0]
    N = len(heightNormalArea)
    for i in range(0,N):
        value = heightNormalArea[i][0]
        if (value < minimum): minimum = value
        if (value > maximum): maximum = value
        
    return minimum, maximum


def GenerateVectorList(X, Y, Z):
    """returns [z position, z normal] and total area.

    An X, Y and Z surface. In the form of:
    X = [[#, #, #, #], [#, # ,# ,#]]
    where i and j incremints form our surface (X[i][j], Y[i][j], Z[i][j])
    all inputs should have the same size (we can adjust in the future for more adjustability)
    """
    N = len(X)   #number of rows    X[N][ ]
    M = len(X[0])#number of columns X[ ][M]
    
    area = 0; #To divide by when calulcating force.
    heightNormalArea = [[0] * 3  for i in range((N-1)*(M-1))]; #[z position, z normal]
    listPos = 0
    for i in range(0, N-1):
        for j in range(0, M-1):
            # A ---- B
            # | \    |
            # |  \   |
            # |    \ |
            # D ---- C
            A = [X[i  ][j  ], Y[i  ][j  ], Z[i  ][j  ]]
            B = [X[i+1][j  ], Y[i+1][j  ], Z[i+1][j  ]]
            C = [X[i+1][j+1], Y[i+1][j+1], Z[i+1][j+1]]
            D = [X[i  ][j+1], Y[i  ][j+1], Z[i  ][j+1]]
            
            n1 = Cross(A, D, C)
            n2 = Cross(A, C, B)
            
            #adding the two trapezoids and dividing by 2 is the same as adding the two triangles together
            deltaArea = (sqrt(n1[0]**2 + n1[1]**2 + n1[2]**2) + sqrt(n2[0]**2 + n2[1]**2 + n2[2]**2))/2.0
           
            heightNormalArea[listPos][0] = (A[2] + B[2] + C[2] + D[2]) /4.0  #Z position of the center ABCD 
            heightNormalArea[listPos][1] = ((n1[2] + n2[2])/2.0) / deltaArea #Normalize the normals (save the z direction)
            heightNormalArea[listPos][2] = deltaArea
            
            listPos = listPos + 1 #order doesnt matter for the list   
    return heightNormalArea


def CalculateForce(heightNormalArea, waterLevel):
    """returns the total Force over all heightNormalArea points, (kg * m/ s^2)
    Takes the HNA list [depth, z_normal, area], and a waterLevel where the water starts (anything below is underwater)
    """
    N = len(heightNormalArea); 
    force = 0
    RemapPressure = lambda a: max(waterLevel - a,0) * GLOBAL_WaterDensity * GLOBAL_Gravity
    
    for i in range(0, N):
        newForce = -heightNormalArea[i][1] * RemapPressure(heightNormalArea[i][0]) * heightNormalArea[i][2]
        if (not isnan(newForce)): 
            force += newForce #( kg/(m*s^2) ) * delta(m^2)

    return force #kg * m / s^2

def BinarySearch(heightNormalArea, weight, binarySearchMax = 16, symmetryMultiplier = 1):
    """returns the equilibrium depth (m)
    takes the heightNormal list [depth, z_normal, area], surface area, a defined weight, and how deep in the binary search to look
    Also a symmetry if you only put in a symmetric half, quarter, etc of your object into the search
    
    Performs a binary search to find the equilibrium depth dependent on the weight
    """
    searchMax, searchMin = GetMinMaxHeight(heightNormalArea) #reverse order so it would be in depth form.
    
    searchDistance = abs(searchMax - searchMin)
    searchMin -= searchDistance * 0.1
    searchMax += searchDistance * 0.1
    
    # ---searchMax ---
    #       |
    #       |
    #  searchLevel
    #       |
    #       |
    #---searchMin ---
    for d in range(0, binarySearchMax):
        searchLevel = (searchMax + searchMin)/2.0
        force = CalculateForce(heightNormalArea, searchLevel) * symmetryMultiplier
        #Pascals to Newtons, based on area
        #kg/(m* s^2) * m^2 = kg m/ s^2 = (N)
        
        if (force == weight):
            return searchLevel
        
        #something is wonky with the math below, need to investigate however this is working.
        #the force of water is less than our boats weight
        #Clearly we can raise the water level and search higher
        if (force < weight): 
            searchMax = searchLevel
            
        #the force of water is more than our boats weight
        #Clearly we can lower the water level and search lower
        if (force > weight):
            searchMin = searchLevel
                 
    return searchLevel


def EquilibriumSearch(X, Y, Z, weight, binarySearchMax = 16, symmetryMultiplier = 1):
    """returns the equilibrium depth.

    Like binary search but takes the X, Y, Z array of points defining the boat, 
    a defined weight, and binary search limit.
    Calculates the heightNormal list [depth, z_normal] and surface area.
    Also a symmetry if you only put in a symmetric half, quarter, etc of your object into the search
    
    Mainly for condensing the amount of code needed in the final notebook (possibly)
    """
    heightNormalArea = GenerateVectorList(X, Y, Z) 
    
    return BinarySearch(heightNormalArea, weight, binarySearchMax, symmetryMultiplier = 1)