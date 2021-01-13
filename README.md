Imagine a grid of 8x8, each cell has one of two colours, black and white, and each cell is of different colour to the cells sharing the same edge. If you did, you would be imagining a chess board. 

 And there are 2 possible boards with these conditions.

 Following these rules with different dimensions of the grid; 3x2 and instead of 2 colours we use 7, then we would find 40362 possible boards instead of 2. You can calculate it using the script I wrote and added to this repo.

 I have added to this repository the python script that creates in Blender the geometry for all the boards with any dimension and colour set. It translates colours to rotations and eliminates the invalid hierarchies.
 

About the geometry:

 Each cube represents one possible board. All of them can be seen in the image plot added to this repo.

 This geometry is full of symmetries, obviously the Number of colours final rotation, and interestingly each of the colour "Wedges" is symmetrical to a rotated plane. And more could be found on the exploration of the Y (horizontal) axis. Such as; the tree is equal every two vertical (now to the grid) rows. I will try to show this property later on.
 
 
 ![3x3x7](3x3x7.png)
 
 
  
  IMPORTANT NOTES:

 If you execute the script inside Blender, please reduce the amount of rows and columns as it can take a while to calculate.
 Even if the calculation is finished, probably your OpenGL scene is going to be slow and problematic.
 This script starts removing the objects on the scene, so, save before you run it.
