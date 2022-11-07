from sympy import *
#change maximum recursion depth
import sys
sys.setrecursionlimit(10000)
u = symbols("u", cls=Function)
phi = symbols("phi")
u = u(phi)
#solve diff(u(phi), phi, 2) = 3/2*u(phi)**2 -u(phi), u(phi)
#second derivative of u(phi) with respect to phi
LHS = diff(u, (phi, 2))
RHS = 3/2*u**2 - u
print(dsolve(Eq(LHS, RHS), u))
