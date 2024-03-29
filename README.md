# GR Ray Tracing

# Introduction
In Einstein's theory of general relativity (GR), light doesn't necessarily travel in straight lines. This leads to all sorts of weird and interesting visual phenomena. For example, in the vicinity of a black hole light can be deflected so strongly that you can actually see behind it. This project uses the equations of GR to simulate the path of light rays, and thus generate images.

# Usage

The default setup is a Schwazschild black hole with a simple accretion disk. To run, simply execute the python file GR_RayTracer.py, it will compile and run the C++ code. To modify the geometry of the scene simply edit the metric ($g$) and its inverse in GR_RayTracer.py. Modifying the scene is slightly more involved, currently the accretion disk is implemented via an if statement in testGR.cpp
```C 
if (abs(theta - M_PI/2)<0.01 && rr > 1.02*R && rr < 10*R)
```
This isn't very generalizable, so I'd recommend implementing a function that checks for ray collisions which could be used to specify all the objects in the scene.

# Theory

Below is a brief review of the math/physics behind this project. If that's not your cup of tea, you can skip to either the implementation or results sections.

## Ray Tracing

Before getting to GR, a review the basics of ray tracing is in order.

![Ray Tracing Cartoon](ray-tracing-image.jpg)

To generate an image, light rays are sent out of the camera (the reason they aren't sent out of a light source is that the vast majority of them won't reach the camera). Each ray is sent out at a different angle such that it intersects with a single pixel in the image plane. The ray then reflects (and refracts) off objects in the scene until either it reaches a light source, or a maximum number of reflections is reached. If a ray reaches a light source, the corresponding pixel (i.e. the one it initially intersected in the image plane) is colored accordingly. The exact details of how a pixel is colored can get complicated, it depends on the properties of every object it interacted with as well as the light source it hit. However, these details are not relevant for this project, as there is only one object (the accretion disk) which also acts as the light source. It is clear to see from the figure above how this procedure will result in an image similar to one taken with a real camera.

Note: This is a very simplified description of ray tracing, but it suffices here.

## Geodesic Equation

The geodesic equation in general relativity is analogous to $\vec{F}=m\vec{a}$ in classical mechanics. It is typically written (in the case of no external forces) as:

$$
\frac{d^2x^{\mu}}{d\tau^2} = -\Gamma^\mu_{\alpha\beta}\frac{dx^{\alpha}}{d\tau}\frac{dx^{\beta}}{d\tau}
$$

Here $x^\mu$ is the 4-vector representing the position of the particle in question, $\tau$ is the proper time of the particle, and $\Gamma^\mu_{\alpha\beta}$ represents the Christoffel symbols (additionally note that the RHS is using Einstein summation notation). 


> Christoffel symbols quantify how the coordinates we are using change relative to free-falling (inertial) coordinates. These changes manifest as inertial “forces” when we observe from our non-inertial coordinates. An analogy from classical mechanics is the centrifugal and Coriolis force terms that arise in a polar coordinate system. This is more than just an analogy though, by comparing the known equations of motion for a free moving particle to the geodesic equation, we can actually read off the Christoffel symbols for the polar coordinates: $\ddot{r}=r\dot{\theta}^2\rightarrow\Gamma^r_{\theta\theta}=-r$ and $\ddot{\theta}=-\frac{2}{r}\dot{r}\dot{\theta}\rightarrow \Gamma^\theta_{r\theta}=\Gamma^\theta_{\theta r}=\frac{1}{r}$. The punchline of GR is that gravity is just an inertial force, and the reason that "normal" coordinates are non-inertial is because the geometry of spacetime is curved.


This ray tracer uses the geodesic equation to solve for the path that photons take in the vicinity of a black hole (since they are not simply straight lines), and then finds those that intersect with an accretion disk to generate an image.

## Schwarzschild Metric

The typical way to obtain the Christoffel symbols necessary to apply the geodesic equation is via the metric. 


>The metric $g_{\mu \nu}$ is a tensor that allows us to calculate distances in spacetime (essentially generalizing the pythagorean theorem). The "spacetime interval" analogous to distance is given by $ds^2=g_{\mu \nu}dx^\mu dx^\nu$. We recover the pythagorean theorem by using the "flat metric" where all the diagonal elements of $g$ are 1, and all the off diagonals are 0. The metric alone is enough to fully determine the geometry of spacetime.

The equation relating the Christoffel symbols to the metric is
$$\Gamma^\mu_{\rho \sigma}=\frac{1}{2} g^{\mu \alpha}(g_{\alpha \rho, \sigma} + g_{\alpha \sigma, \rho } - g_{\rho \sigma, \alpha})$$

Here $g^{\mu \nu}$ is the inverse of $g_{\mu \nu}$, and the commas indicate differentiation WRT whichever variable follows. 

The metric used to generate the image in the results section is the Schwarzschild metric. The Schwarzschild metric describes spacetime in the vicinity of a non-rotating uncharged black hole. It is given (in spherical coordinates centered on the black hole) by
```math
g_{\mu \nu} = \begin{pmatrix}-\left( 1-\frac{r_s}{r}\right) & 0 & 0 & 0\\ 0 & \left( 1-\frac{r_s}{r}\right)^{-1} & 0 & 0\\ 0 & 0 & r^2 & 0\\ 0 & 0 & 0 & r^2 sin^2(\theta)\\\end{pmatrix}
```
Here $r_s$ is the Schwarzschild radius (A.K.A the radius of no return). Past this radius nothing, not even light, can escape the black hole.

# Implementation

To generate images there is a four step process:
* Calculate the Christoffel symbols from the metric
* Initialize the light ray positions and momenta (i.e. directions), with one for each pixel in the camera
* Using the Christoffel symbols previously calculated, integrate the geodesic equation to find the path that each light ray takes
* Determine which light rays intersect with the accretion disk, and color the corresponding pixel in the ouput image accordingly


## Sympy (GR_RayTracer.py)
Calculating the Christoffel symbols from the metric is done via the equation from the theory section, using the python SymPy library. The Christoffel symbols are then written to a C++ file (chrisC.cpp), where they can be accessed for the time integration. 

## Ray Initialization (testGR.cpp)
As described in the theory section, a light ray is sent out of the camera at a slightly different angle for each pixel. To acheive this, a ray object is created which has a 4-position and 4-momentum. The postions are all initialized to the same point, but the momenta vary depending on the pixel in order to send them in the right direction.


## C++ with OpenMPI for Time Integration (testGR.cpp)
For each ray the class method ```Ray::geodesic()``` (which uses the euler method to integrate the geodesic equation) is repeatedly called until the ray either hits the accretion disk, hits the black hole, or goes far enough away from the black hole that we can confidently say it is never coming back. If a ray hits the accretion disk, the corresponding pixel color is colored red (with brightness varying as $1/r$ for visualization purposes) To speed up this process OpenMPI is used to calculate the paths of many rays in parallel, this can be done since the rays don't interact with each other. The file reconstructParallel.py creates the final image from the raw output.

# Results
Below is the final result!

![Schwarzschild Black Hole](Schwarzschild.png)
### Explanation of what you are seeing
When light gets emitted from the accretion disk, its path is not a straight line (from the perspective of a distant observer). Instead it follows a warped path, as illustrated by the figure below. The figure shows the path of a small sample of rays originating from the camera.

![Ray Path Around Black Hole](lightBending2D2.png)


So light emitted from the far side of the black hole can actually bend around it and reach the camera. The interpretation of the image is now apparent. At the center of the image, the black region represents the black hole itself (though technically it is empty space, since all the mass is in the singularity at the center). The red regions around the black hole show a warped view of the accretion disk (without the deflection of light the accretion disk would look similar to the rings of Saturn). Both the top and bottom of the far side (i.e. beyond the black hole) of the accretion disk are visible. See the figure below.

![Schwarzschild Black Hole](SchwarzschildExplained.jpg)




## Next Steps

- Switch time integration to Runge Kutta
- Add frequency redshift
