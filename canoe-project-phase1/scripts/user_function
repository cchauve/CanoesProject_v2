#import numpy, which is useful for ploting graphs, and call it np
#import python files for functions
import numpy as np
from scripts.plot_functions_Haruto import plot_canoe import coordinates

#get the type of canoe we want to make.
type=int(input("What type of canoe are we want to make?: "))
#get the width of the canoe we want to make.
print("What is the width of the canoe we want to make?: ")
width =list(map(float, input().split()))
#get the height of the canoe we want to make.
print("What is the height of the canoe we want to make?: ")
height =list(map(float, input().split()))
#get the length of the canoe we want to make.
print("What is the length of the canoe we want to make?: ")
length =list(map(float, input().split()))
#get the corner radius of the canoe we want to make.
print("What is the corner radius of the canoe we want to make?: ")
corner_radius =list(map(float, input().split()))

#make the 3D figure of the canoe, and show it.
fig = plot_canoe(width, height, length, corner_radius, type)
fig.show()

