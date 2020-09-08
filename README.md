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

Example Command Line Input:

```
python sun.py -d '2020-09-07 13:54:00' -c 'San Francisco' -p True
```

## Math behind calculations

The key calculation is getting the vector that points from the person on the surface of the earth, to the sun (Vector C in the figure below). 

![Figure2](Figures/figure2.png)

This can be calculated simply by adding two vectors: a vector pointing from the center of the sun to the center of the earth (Vector A) and a vector pointing from the center of the earth to the surface of the earth (Vector B).

_**A**_ + _**B**_ = -_**C**_ 

The tricky part of this math is the reference frame (ie coordinate system) of the vectors. Ultimately, we want vector C in the reference frame of a person standing on the surface of the earth. In other words, the origin should be at the person's feet, with x pointing east, y pointing north, and z pointing straight up. The reason we want this is that Theta_from_North and Phi_from_Horizon pop out super easily from those x, y, and z coordinates. Unfortunately, representing vectors _**A**_ and _**B**_ in the earth's surface coordinate system is difficult. However, _**A**_ and _**B**_ can be represented easily in different coordinate systems: _**A**_ can be represented easily in a coordinate system with the origin at the sun, and _**B**_ can be represented easily with an origin at the center of the earth.

To reconcile this challenge, the key is to use coordinate transformations! The basic idea here is that we start with a vector in one coordinate system, transform it to the coordinate system of the vector we want to add it to, and then add that vector without too much trouble since the 2nd vector can be represented easily in the new coordinate system. The workflow is broken down as follows:

1. Write vector _**A**_<sup>s</sup>, which goes from the center of the sun to the center of the earth, in the sun's coordinate system (origin at center of the sun).
2. Transform _**A**_<sup>s</sup> to _**A**_<sup>e</sup> so that it's in the coordinate system of the earth (origin is at the center of the earth)
3. Write vector _**B**_<sup>e</sup>, which goes from the center of the earth to the earth's surface, in earth's coordinate system.
4. Add _**A**_<sup>e</sup> and _**B**_<sup>e</sup> to get _**C**_<sup>e</sup>, which is the vector we ultimately want, but is currently in the wrong coordinate system.
5. Transform _**C**_<sup>e</sup> to _**C**_<sup>es</sup> so that it's in the coordinate system of the earth's surface (origin centered at a person's feet on the surface)

Useful guide about coordinate transformations can be found here:
(https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-07-dynamics-fall-2009/lecture-notes/MIT16_07F09_Lec03.pdf)

### Step 1. Write _**A**_<sup>s</sup> in the sun's coordinate system

![Figure 3](Figures/figure3.png)

From the above figure, it's pretty straightforward to see that vector _**A**_<sup>s</sup>, in the coordinate system of the sun (superscript s), can be written as:
![Figure 4](Figures/figure4.png)

### Step 2. Transforming _**A**_<sup>s</sup> to _**A**_<sup>e</sup> so that it's in earth's coodinate system

We now have to transform _**A**_<sup>s</sup> to _**A**_<sup>e</sup> (coordinate system of the earth). Fun fact: If it were not for the fact that the earth rotated around a tilted axis, the earth and the sun would share the same coordinate system! This difference is the key to coming up with the basis vectors for the earth's coordinate system. The figure below will help illustrate visually how the sun's basis vectors and the earth's basis vectors differ.

![Figure 5](Figures/figure5.png)

From the figure, we see that y and z are shifted by the tilt of the earth. Luckily, we can define the new coordinate system where the tilt only occurs in the yz plane such that x is preserved! The basis vectors for earth's coordinate system are as follows:
![Figure 6](Figures/figure6.png)

To transform _**A**_<sup>s</sup>, we use the following formulas, which can be found in the MIT lecture notes I linked above.
![Figure 7](Figures/figure7.png)

After wading through the tedious algebra, we get the following for _**A**_<sup>e</sup>:
![Figure 8](Figures/figure8.png)

### Step 3. Write _**B**_<sup>e</sup> in the earth's coordinate system

_**B**_<sup>e</sup> is the vector that goes from the center of the earth to the earth's surface at the location we're interested in. Any location on the surface of the earth can be represented by two angles, &theta;<sub>LL</sub> and &phi;<sub>LL</sub>, as shown in the figure below. 

![Figure 9](Figures/figure9.png)

From the above figure, and using the definition of spherical coordinates, _**B**_<sup>e</sup> can be derived as:
![Figure 10](Figures/figure10.png)

### Step 4. Add _**A**_<sup>e</sup> and _**B**_<sup>e</sup> to get _**C**_<sup>e</sup>

To get _**C**_<sup>e</sup>, we need to add _**A**_<sup>e</sup> and _**B**_<sup>e</sup> and then flip the direction so that _**C**_<sup>e</sup> is pointing towards the sun:
![Figure 11](Figures/figure11.png)










These two angles are akin to longitude and latitude (hence the subscript LL), but there are a few key differences. The "longitude" (&theta;<sub>LL</sub>) also depends on the rotation of the earth (ie what time it is!). The "latitude" is defined to have a different zero point. I defined &phi;<sub>LL</sub> to be zero at the poles, but latitude is zero at the equator. Taking these corrections into account, we get the following formulas for &theta;<sub>LL</sub> and &phi;<sub>LL</sub>:












