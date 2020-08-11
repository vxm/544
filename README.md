 Imagine a grid of 8x8, where each cell has one of two colours, black and white, and each cell is of different colour to the cells sharing the same edge. You are now seeing a Chess board. 

 And there are 2 possible boards with these conditions. Without rotations.

 With the same rules, but the dimensions of the grid, being 3x2 and 7 different colours, we would get 40362 possible boards.

 I have added to this repository the python script that creates in blender the geometry representing all these possibilities. It translates colours to rotations and eliminates the broken hierarchies.
 
 The script needs to be executed inside Blender and it will delete the current scene.
 
About the geometry:

 Each cube represents one possible board. All of them can be seen in the image plot added to this repo.

 This geometry is full of symmetries, obviously the Number of colours final rotation, and interestingly each of the colour "Wedges" is simetrical to a rotated plane. And more could be found on the exploration of the Y (horizontal) axis. Such as; the tree is equal every two vertical (now to the grid) rows. I will try to show this property later on.
 
  IMPORTANT NOTES:

 If you execute the script inside Blender, please reduce the amount of rows and columns as it can take a while to calculate.
 Even if the calculation is finished, probably your OpenGL scene is going to be slow and problematic.
 This script starts removing the objects on the scene, so, save before you run it.
