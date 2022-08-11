import numpy as np

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
    
    #Mathematically the cross product alread has the trapezoids scale in the magnitude
    
    return [x,y,z]



def GenerateVectorList(X, Y, Z):
    """returns [z position, z normal] and total area.

    An X, Y and Z surface. In the form of:
    X = [[#, #, #, #], [#, # ,# ,#]]
    where i and j incremints form our surface (X[i][j], Y[i][j], Z[i][j])
    all inputs should have the same size (we can adjust in the future for more adjustability)
    """
    N = len(X)
    area = 0; #To divide by when calulcating force.
    heightNormal = [[0] * 2  for i in range(N*N)]; #[z position, z normal]
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
            area += (np.sqrt(n1[0]**2 + n1[1]**2 + n1[2]**2) + np.sqrt(n2[0]**2 + n2[1]**2 + n2[2]**2))/2
            
            heightNormal[i*N + j][0] = (A[2] + B[2] + C[2] + D[2]) /4.0 #Z position of the center ABCD 
            heightNormal[i*N + j][1] = (n1[2] + n2[2])/2
            
    return heightNormal, area



def RemapPressure(depth, startDepth):
    """returns the depth pressure pascals (kg/(m * s^2))
    Takes a depth value and startDepth where the water level starts. 

    """
    remappedDepth = np.max(depth - startDepth, 0); #clamps so only values greater than zero are calculated
    
    #Hydro static pressure = fluid density(kg / m^3) * gravity(m/s^2) * fluid depth(m)
    return (997) * (9.80665) * remappedDepth



def CalculatePressure(heightNormal, depthLevel):
    """returns the total pressure sum over all heightNormal points, (kg/(m * s^2))
    Takes the heightNormal list [depth, z_normal], and a depthLevel where the water starts

    we do need to convert our z positions into a depth range which should be positive the deeper you. 
    Maybe in the future unify it all to avoid these conversions
    """
    N = len(heightNormal); 
    pressure = 0
    for i in range(0, N):
        pressure += heightNormal[i][1] * RemapPressure(-1*heightNormal[i][0], depthLevel) #kg/(m*s^2)
        
    return pressure



def BinarySearch(heightNormal, area, weight, binarySearchMax = 16):
    """returns the equilibrium depth (m)
    takes the heightNormal list [depth, z_normal], surface area, a defined weight, and how deep in the binary search to look

    Performs a binary search to find the equilibrium depth dependent on the weight
    """
    #should implement an automatic min max for the search
    searchMin = 0
    searchMax = 1
    # ---searchMin ---
    #       |
    #       |
    #  searchLevel
    #       |
    #       |
    #---searchMax ---
    for d in range(0, binarySearchMax):
        searchLevel = (searchMax + searchMin)/2.0
        pressure = CalculatePressure(heightNormal, searchLevel)
        
        #Pascals to Newtons, based on area
        force = pressure * area   #kg/(m* s^2) * m^2 = kg m/ s^2 = (N)
        
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
    heightNormal, area = GenerateVectorList(X, Y, Z) 
    
    return BinarySearch(heightNormal, area, weight, binarySearchMax)
    
    