# Codes to visualize the canoe in 3D
plot_canoe() is a function that makes 3D figure of a canoe according to the input.
The inputs are width range, height range, length range, corner radius range, and canoe type.

Suppose the user gives 1 and 3 as an input for width range. The numbers will be stored as a 2 element list [1, 3].
There are 3 types of canoe, and they are type 1, type 2, type 3.

Below are functions used in plot_canoe().

### check()
check funciton, first used in the plot_canoe(), checks if there is something
strange about the input. First, it checks if the given range is too large.
Second, it checks if the input can be expressed in first decimal place. Thirdly, it checks if the type is given an input of 1 or 2 or 3.

### get_eta_theta()
eta and theta are list of angles in radians used to make 3D figure of the canoe

### get_coordinates()
function to calculate the x-coordinate, y-coordinate, z-coordinate of the canoe. To get the coordinates, function uses x_coordinates(), y_coordinates(), and z_coordinates()

### @interact()
Makes a slider that the user can use in real time. As the number used in the slider changes, the function will show new figure with matching inputs.  
