import numpy as np
from scripts.plot_functions_Haruto import plot_canoe 
from scripts.plot_functions_Haruto import coordinates

"""
in order to create a canoe, we will need to get 5 variables
first, we specify which type of canoe we are making. This must be a single integer
then we decide on the width, height, length, and corner radius of the canoe
any one of the 4 variables above could be a changing variable, and we could put multiple numbers as an input
the numbers for 4 variables are put into an array
"""

print("What is the type of the canoe we want to make?: ")
type=int(input())
print("What is the width of the canoe we want to make?: ")
width=list(map(float, input().split()))
print("What is the height of the canoe we want to make?: ")
height=list(map(float, input().split()))
print("What is the length of the canoe we want to make?: ")
length=list(map(float, input().split()))
print("What is the corner radius of the canoe we want to make?: ")
corner_radius=list(map(float, input().split()))

"""
make the 3D figure of the canoe, and show it.
"""
fig = plot_canoe(width, height, length, corner_radius, type)
fig.show()

