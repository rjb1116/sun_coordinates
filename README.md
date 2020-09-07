# sun_coordinates
Get the spherical coordinates of the sun in the sky from any location on earth at any time

## Quick Summary
The sun.py script can take in any location in the world, and any time, and output the spherical coordinates of the sun from the perpective of a person standing on the earth's surface at that location. This is done using vector addition and coordinate transformations (elaborated on later).

The location of the sun is given by two angles:
* Theta_from_North - angle measured clockwise from due north to the point on the horizon underneath the sun
* Phi_from_Horizon: - angle from the horizon up to the sun

A 3D visualization using Matplotlib of the sun's location in the sky is also outputted by the model:
![Figure1](Figures/figure1.png)

## How to run the code
The code takes three inputs: time, location, and save figure boolean

These inputs can be given in the command line, or by modifying the get_inputs(args) method within the script directly.

Command Line Instructions:
* -d: Date and time string of form 'YYYY-MM-DD HH:MM:SS'
* -c: String containing the city. This input is relatively versatile since multiple city structures are accepted (for example: San Francisco or San Francisco, CA)
* -p: Write True if you want a png image of the 3D visualization to be stored locally with the title 'out.png'

## Math behind calculations

The key calculation is getting the vector that points from the person on the surface of the earth, to the sun (Vector A in the figure below). This can be calculated simply be adding two vectors: a vector pointing from the center of the sun to the center of the earth (Vector A) and a vector pointing from the center of the earth to the surface of the sun (Vector B).

\overrightarrow{A}  
