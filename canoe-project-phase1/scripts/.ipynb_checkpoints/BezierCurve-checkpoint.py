def Curve(points, t):
    """ Takes in points and a time t from 0 to 1, outputs a vector in the same dimension as the individual points.
    points = [[P0],[P1],...[P(n-1)]]
    """
    n = len(points)
    d = len(points[0])
    finalPos = [0]*d
    
    for i in range(0,n): #0,1,2,...,n-1
        multiplier = factorial(n)/(factorial(i)*factorial(n-i))*((1-t)**(n-i) t**i)
        for j in range(0,d):
            finalPos[j] +=  multiplier * points[i][j]
    return finalPos
    
def factorial(x):
    f = 1
    for i in range(2, x + 1):
        f *= i
    return fact