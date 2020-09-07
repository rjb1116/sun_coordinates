# sun_coordinates
Get the spherical coordinates of the sun in the sky from any location on earth at any time

## Quick Summary
The sun.py script can take in any location in the world, and any time, and output the spherical coordinates of the sun from the perpective of a person standing on the earth's surface at that location. This is done using vector addition and coordinate transformations elaborated on below.

For example, if you were to stand at Longitude 0, Latitude 0, at noon on the spring equinox, this model would output that the sun is pretty close to direclty overhead.

The location of the sun is given by two angles:
- Theta_from_North - angle measured clockwise from due north to the point on the horizon underneath the sun
- Phi_from_Horizon: - angle from the horizon up to the sun

A 3D visualization using Matplotlib of the sun's location in the sky is also outputted by the model. 


![Figure1](Figures/figure1.png)
