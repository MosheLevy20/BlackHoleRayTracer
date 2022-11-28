# GR Ray Tracing

# Geodesic Equation

The geodesic equation in general relativity is analogous to $\vec{F}=m\vec{a}$ in classical mechanics. It is typically written as:

$$
\frac{d^2x^{\mu}}{d\tau^2} = -\Gamma^\mu_{\alpha\beta}\frac{dx^{\alpha}}{d\tau}\frac{dx^{\beta}}{d\tau}
$$

Here $x^\mu$ is the 4-vector representing the position of the particle in question, $\tau$ is the proper time of the particle, and $\Gamma^\mu_{\alpha\beta}$ represents the Christoffel symbols (additionally note that the RHS is using Einstein summation notation). 


Christoffel symbols quantify how the coordinates we are using change relative to free-falling (inertial) coordinates. These changes manifest as inertial “forces” when we observe from our non-inertial coordinates. An analogy from classical mechanics is the centrifugal and Coriolis force terms that arise in a polar coordinate system. This is more than just an analogy, by comparing the known equations of motion for a free moving particle to the geodesic equation, we can actually read off the Christoffel symbols for the polar coordinates: $\ddot{r}=r\dot{\theta}^2\rightarrow\Gamma^r_{\theta\theta}=-r$ and $\ddot{\theta}=-\frac{2}{r}\dot{r}\dot{\theta}\rightarrow \Gamma^\theta_{r\theta}=\Gamma^\theta_{\theta r}=\frac{1}{r}$.




For this ray tracer we’ll use the geodesic equation to solve for the path that photons take in the vicinity of a black hole, and then find those that intersect with an accretion disk.

# Schwarzschild Metric

The typical way we obtain the Christoffel symbols is via the metric. 

TODO

# Implementation

## Sympy

TODO

## Ray Initialization (Camera)

TODO

## C++ with OpenMPI for Time Integration

TODO

## Next Steps

- Switch time integration to Runge Kutta
- Add frequency redshift
