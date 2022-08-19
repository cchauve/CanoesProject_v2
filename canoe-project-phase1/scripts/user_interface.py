import numpy as np
#from scripts.plot_funcs import plot_canoe 
#from scripts.plot_funcs import coordinates

"""
in order to create a canoe, we will need to get 5 variables
first, we specify which type of canoe we are making. This must be a single integer
then we decide on the width, height, length, and corner radius of the canoe
any one of the 4 variables above could be a changing variable, and we could put multiple numbers as an input
the numbers for 4 variables are put into an array
"""

type=int(input("canoe type is: "))
min_width, max_width=input("width range is: ").split()
width=np.arange(float(min_width), float(max_width)+0.001, 0.1).tolist()
min_height, max_height=input("height range is: ").split()
height=np.arange(float(min_height), float(max_height)+0.001, 0.1).tolist()
min_length, max_length=input("length range is: ").split()
length=np.arange(float(min_length), float(max_length)+0.001, 0.1).tolist()
min_corner_radius, max_corner_radius=input("corner radius range is: ").split()
corner_radius=np.arange(float(min_corner_radius), float(max_corner_radius)+0.001, 0.1).tolist()

"""
make the 3D figure of the canoe, and show it.
"""
fig=plot_canoe(width, height, length, corner_radius, type)
fig.show()
