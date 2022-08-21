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
from numpy import sqrt


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
    N = len(X)
    area = 0; #To divide by when calulcating force.
    heightNormalArea = [[0] * 3  for i in range((N-1)**2)]; #[z position, z normal]
    for i in range(0, N-1):
        for j in range(0, N-1):
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
           
            heightNormalArea[i*(N-1) + j][0] = (A[2] + B[2] + C[2] + D[2]) /4.0  #Z position of the center ABCD 
            heightNormalArea[i*(N-1) + j][1] = ((n1[2] + n2[2])/2.0) / deltaArea #Normalize the normals (save the z direction)
            heightNormalArea[i*(N-1) + j][2] = deltaArea
            
            
    return heightNormalArea


def RemapPressure(depth, startDepth):
    """returns the depth pressure pascals (kg/(m * s^2))
    Takes a depth value and startDepth where the water level starts. 
    """
    remappedDepth = max(depth - startDepth, 0) #clamps so only values greater than zero are calculated
    #if (remappedDepth < 0) remappedDepth = 0 
    #Hydro static pressure = fluid density(kg / m^3) * gravity(m/s^2) * fluid depth(m)
    return (997) * (9.80665) * remappedDepth #(kg / m * s^2)


def CalculateForce(heightNormalArea, depthLevel):
    """returns the total Force over all heightNormalArea points, (kg * m/ s^2)
    Takes the HNA list [depth, z_normal, area], and a depthLevel where the water starts

    We do need to convert our z positions into a depth range which should be positive the deeper you. 
    Maybe in the future unify it all to avoid these conversions
    """
    
    N = len(heightNormalArea); 
    force = 0
    
    for i in range(0, N):
        force += (heightNormalArea[i][1] * RemapPressure(-1*heightNormalArea[i][0], depthLevel)) * heightNormalArea[i][2] #( kg/(m*s^2) ) * delta(m^2)
    return force #kg * m / s^2


def BinarySearch(heightNormalArea, weight, binarySearchMax = 16):
    """returns the equilibrium depth (m)
    takes the heightNormal list [depth, z_normal, area], surface area, a defined weight, and how deep in the binary search to look

    Performs a binary search to find the equilibrium depth dependent on the weight
    """
    searchMax, searchMin  = GetMinMaxHeight(heightNormalArea) #reverse order so it would be in depth form.
    searchMin *= -1
    searchMax *= -1
    
    # ---searchMin ---
    #       |
    #       |
    #  searchLevel
    #       |
    #       |
    #---searchMax ---
    
    for d in range(0, binarySearchMax):
        searchLevel = (searchMax + searchMin)/2.0
        force = CalculateForce(heightNormalArea, searchLevel)
        
        #Pascals to Newtons, based on area
       #kg/(m* s^2) * m^2 = kg m/ s^2 = (N)
        
        if (force == weight):
            return searchLevel
        
        #the force of water is greater than our boats weight, float level must have less depth
        #should lower the force
        if (force > weight): 
            searchMin = searchLevel
            
        #the force of water is less than our boats weight, float level must have more depth
        #should raise the force
        if (force < weight):
            searchMax = searchLevel
            
    return searchLevel


def EquilibriumSearch(X, Y, Z, weight, binarySearchMax = 16):
    """returns the equilibrium depth.

    Like binary search but takes the X, Y, Z array of points defining the boat, a defined weight, and binary search limit.
    Calculates the heightNormal list [depth, z_normal] and surface area.
    Mainly for condensing the amount of code needed in the final notebook (possibly)
    """
    heightNormalArea = GenerateVectorList(X, Y, Z) 
    
    return BinarySearch(heightNormalArea, weight, binarySearchMax)