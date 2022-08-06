import numpy as np
# A = [x,y,z]
# B ..
# C ..
# right hand rule ABC
# returns a vector proportional to the area of the triangle ABC
def CustomNormal(A , B, C):
    U = [B[0]-A[0], B[1] - A[1], B[2] - A[2]]
    V = [C[0]-A[0], C[1] - A[1], C[2] - A[2]]
    
    x =  U[1]*V[2] - U[2]*V[1]
    y = -U[0]*V[2] + U[2]*V[0]
    z =  U[0]*V[1] - U[1]*V[0]
    
    #s = np.sqrt(x*x + y*y + z*z) #magnitude of the vector
    #Mathematically we would divide x, y, z by our scale, but we also want to factor in the size of the triangle, so we need to multiply by scale/2.
    #scale cancels out and we just divide by 2.
    
    x /= 2.0
    y /= 2.0
    z /= 2.0
    
    return [x,y,z] #we can output the lenght hear too if necessary. For less output clutter I am not

# An X, Y and Z surface. in the form of:
# X = [[#, #, #, #], [#, # ,# ,#]]
# where i and j incremints form our surface (X[i][j], Y[i][j], Z[i][j])
# all inputs should have the same size (we can adjust in the future for more adjustability)
# returns [z position, z normal] and total area.
def GenerateVectorList(X, Y, Z):
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
            
            n1 = CustomNormal(A, D, C)
            n2 = CustomNormal(A, C, B)
            
            area += np.sqrt(n1[0]**2 + n1[1]**2 + n1[2]**2) + np.sqrt(n2[0]**2 + n2[1]**2 + n2[2]**2)
            
            heightNormal[i*N + j][0] = (A[2] + B[2] + C[2] + D[2]) /4.0 #Z position of the center of A
            heightNormal[i*N + j][1] = n1[2] + n2[2] 
            
            #We dont average the normal because we want the normal of square in proportion to its area. 
    
    return [heightNormal, area]

# returns the depth pressure amount, based on depth and the startDepth (where water actually starts.)
def RemapPressure(depth, startDepth):
    remappedDepth = np.max(depth - startDepth, 0); #clamps so only values greater than zero are calculated
    #return remappedDepth * (997)*(9.80665) #density of water (kg/m^3) * gravity (m/s^2)
    #Hydro static pressure = fluid density(kg / m^3) * gravity(m/s^2) * fluid depth(m)
    return remappedDepth * (100.0) * (9.80665) #was 1000, might be off by a factor of 10? 

def EquilibriumSearch(X, Y, Z, weight, binarySearchMax):
    [heightNormal, area] = GenerateVectorList(X, Y, Z) #[z position, z normal]
    N = len(heightNormal);
    
    print("AREA: ")
    print(area)
    
    searchMin = 0
    searchMax = 1
    searchLevel = 0.5
    # ---searchMin ---
    #       |
    #       |
    #  searchLevel
    #       |
    #       |
    #---searchMax ---
    
    for d in range(0, binarySearchMax):
        
        pressure = 0
        for i in range(0, N):
            pressure += heightNormal[i][1] * RemapPressure(-1*heightNormal[i][0], searchLevel) #kg/(m*s^2)
            
        force = pressure * area   #kg/(m* s^2) * m^2 = kg m/ s^2
        #print("\n\nForce, then searchLevel")
        print(force)
        #print(searchLevel)
        
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
            
        searchLevel = (searchMax + searchMin)/2.0   
    
        
    return searchLevel
    