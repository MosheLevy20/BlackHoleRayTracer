from sympy import *
import matplotlib.pyplot as plt
import numpy as np
from sympy.printing import cxxcode
import subprocess
import time
t, r, theta, phi = symbols("t r theta phi")
s = symbols("s")
coords = [t,r,theta, phi]
G = 1 
#TODO runge kutta, redshift
#Schwartzschild Metric
M = 1.5
rS = 2*G*M
g00 = -(1-rS/r)
g11 = 1/(1-rS/r)
g22 = r**2
g33 = r**2*sin(theta)**2
dTau = 50

g = [[g00,0,0,0],
	 [0,g11,0,0],
	 [0,0,g22,0],
	 [0,0,0,g33]]

ginv = [[1/g00,0,0,0],
		[0,1/g11,0,0],	
		[0,0,1/g22,0],
		[0,0,0,1/g33]]

def chris(g,k,i,j):
	total = 0
	for m in range(4):
		total += 0.5*ginv[k][m]*(diff(g[m][i],coords[j])+diff(g[m][j],coords[i])-diff(g[i][j],coords[m]))
	return total

chrisC = []
for x in range(4):
	row = []
	for y in range(4):
		column = []
		for z in range(4):
			c = chris(g,x,y,z)
			column.append(c)
		row.append(column)

	chrisC.append(row)

# t, r, theta, phi = symbols("t r theta phi", cls=Function)
# coords_s = [t(s), r(s), theta(s), phi(s)]


# def solveGeodesicEq():
	
# 	eqs = []
# 	for mu in range(4):
# 		#second diff of coords[mu] with respect to s
# 		LHS = diff(coords_s[mu],s,2)
# 		RHS = 0
# 		#print("RHS: ", RHS)
# 		for alpha in range(4):
# 			for beta in range(4):
# 				RHS += chrisC[mu][alpha][beta]*diff(coords_s[alpha], s)*diff(coords_s[beta], s)
# 		#replace coords with their expressions in terms of s
# 		for i in range(4):
# 			RHS = RHS.subs(coords[i], coords_s[i])

# 		#solve RHS = 0 for coords[mu](s)
# 		#print(RHS)
# 		eqs.append(Eq(RHS,LHS))
# 	#solve the system of equations
# 	print(eqs)
# 	sol = dsolve(eqs, coords_s)
# 	return sol
# sol = solveGeodesicEq()
# #sols = [(t(s), (-sqrt((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2))) + diff(t(s), (s, 2)))/diff(t(s), (s, 2)), 2.0*atan((-sqrt((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))*diff(phi(s), (s, 2)) - 1.4142135623731*sqrt((-((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), s)**2*diff(theta(s), s)**2 - 2.0*((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), s)*diff(phi(s), (s, 2))*diff(r(s), s) - ((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), (s, 2))**2 + 2.0*diff(phi(s), s)**2*diff(r(s), s)**2*diff(t(s), (s, 2)) - diff(phi(s), s)**2*diff(r(s), s)*diff(t(s), s)*diff(theta(s), s)**2 + diff(phi(s), s)**2*diff(t(s), (s, 2))*diff(theta(s), s)**2 + 2.0*diff(phi(s), s)*diff(phi(s), (s, 2))*diff(r(s), s)*diff(t(s), (s, 2)) - diff(phi(s), (s, 2))**2*diff(r(s), s)*diff(t(s), s) + diff(phi(s), (s, 2))**2*diff(t(s), (s, 2)))*diff(t(s), (s, 2))) + 2.0*diff(phi(s), s)*diff(r(s), s)*diff(t(s), (s, 2)) + diff(phi(s), (s, 2))*diff(t(s), (s, 2)))/((-((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5 + diff(t(s), (s, 2)))*diff(phi(s), s)*diff(theta(s), s))), phi(s)), (t(s), (-sqrt((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2))) + diff(t(s), (s, 2)))/diff(t(s), (s, 2)), 2.0*atan((-sqrt((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))*diff(phi(s), (s, 2)) + 1.4142135623731*sqrt((-((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), s)**2*diff(theta(s), s)**2 - 2.0*((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), s)*diff(phi(s), (s, 2))*diff(r(s), s) - ((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), (s, 2))**2 + 2.0*diff(phi(s), s)**2*diff(r(s), s)**2*diff(t(s), (s, 2)) - diff(phi(s), s)**2*diff(r(s), s)*diff(t(s), s)*diff(theta(s), s)**2 + diff(phi(s), s)**2*diff(t(s), (s, 2))*diff(theta(s), s)**2 + 2.0*diff(phi(s), s)*diff(phi(s), (s, 2))*diff(r(s), s)*diff(t(s), (s, 2)) - diff(phi(s), (s, 2))**2*diff(r(s), s)*diff(t(s), s) + diff(phi(s), (s, 2))**2*diff(t(s), (s, 2)))*diff(t(s), (s, 2))) + 2.0*diff(phi(s), s)*diff(r(s), s)*diff(t(s), (s, 2)) + diff(phi(s), (s, 2))*diff(t(s), (s, 2)))/((-((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5 + diff(t(s), (s, 2)))*diff(phi(s), s)*diff(theta(s), s))), phi(s)), (t(s), (sqrt((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2))) + diff(t(s), (s, 2)))/diff(t(s), (s, 2)), 2.0*atan((sqrt((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))*diff(phi(s), (s, 2)) - 1.4142135623731*sqrt((((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), s)**2*diff(theta(s), s)**2 + 2.0*((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), s)*diff(phi(s), (s, 2))*diff(r(s), s) + ((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), (s, 2))**2 + 2.0*diff(phi(s), s)**2*diff(r(s), s)**2*diff(t(s), (s, 2)) - diff(phi(s), s)**2*diff(r(s), s)*diff(t(s), s)*diff(theta(s), s)**2 + diff(phi(s), s)**2*diff(t(s), (s, 2))*diff(theta(s), s)**2 + 2.0*diff(phi(s), s)*diff(phi(s), (s, 2))*diff(r(s), s)*diff(t(s), (s, 2)) - diff(phi(s), (s, 2))**2*diff(r(s), s)*diff(t(s), s) + diff(phi(s), (s, 2))**2*diff(t(s), (s, 2)))*diff(t(s), (s, 2))) + 2.0*diff(phi(s), s)*diff(r(s), s)*diff(t(s), (s, 2)) + diff(phi(s), (s, 2))*diff(t(s), (s, 2)))/((((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5 + diff(t(s), (s, 2)))*diff(phi(s), s)*diff(theta(s), s))), phi(s)), (t(s), (sqrt((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2))) + diff(t(s), (s, 2)))/diff(t(s), (s, 2)), 2.0*atan((sqrt((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))*diff(phi(s), (s, 2)) + 1.4142135623731*sqrt((((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), s)**2*diff(theta(s), s)**2 + 2.0*((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), s)*diff(phi(s), (s, 2))*diff(r(s), s) + ((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5*diff(phi(s), (s, 2))**2 + 2.0*diff(phi(s), s)**2*diff(r(s), s)**2*diff(t(s), (s, 2)) - diff(phi(s), s)**2*diff(r(s), s)*diff(t(s), s)*diff(theta(s), s)**2 + diff(phi(s), s)**2*diff(t(s), (s, 2))*diff(theta(s), s)**2 + 2.0*diff(phi(s), s)*diff(phi(s), (s, 2))*diff(r(s), s)*diff(t(s), (s, 2)) - diff(phi(s), (s, 2))**2*diff(r(s), s)*diff(t(s), s) + diff(phi(s), (s, 2))**2*diff(t(s), (s, 2)))*diff(t(s), (s, 2))) + 2.0*diff(phi(s), s)*diff(r(s), s)*diff(t(s), (s, 2)) + diff(phi(s), (s, 2))*diff(t(s), (s, 2)))/((((-2.0*diff(r(s), s)*diff(t(s), s) + diff(t(s), (s, 2)))*diff(t(s), (s, 2)))**0.5 + diff(t(s), (s, 2)))*diff(phi(s), s)*diff(theta(s), s))), phi(s))]
# print(len(sol))
# print(sol)
# quit()
def ricci(g,i,j):
	total = 0
	
	for k in range(4):
		total += diff(chrisC[k][i][j],coords[k])
	for k in range(4):
		total -= diff(chrisC[k][i][k],coords[j])
	for m in range(4):
		for k in range(4):
			total += chrisC[k][i][j]*chrisC[m][k][m]
	for m in range(4):
		for k in range(4):
			total -= chrisC[k][i][m]*chrisC[m][j][k]
	total = simplify(total)
	return total





#print(chrisC)
#how to include braces in python fstring? 
#
#

cppFile = "#include <cmath>\n#include \"chrisC.h\"\nvoid calcChrisC(double r, double theta, double phi, double t, double chrisC1[4][4][4]){\n"
for index, row in enumerate(chrisC):
	for index2, column in enumerate(row):
		for index3, value in enumerate(column):
			#print(index,index2,index3,value)
			cppCode = cxxcode(value)
			#remove std:: from cxxcode
			#cppCode = cppCode.replace("std::","")
			cppFile += f"chrisC1[{index}][{index2}][{index3}] = {cppCode};\n"
cppFile += "return;}"
#print(cppFile)

#write chrisC to txt file
with open('chrisC.cpp', 'w') as f:
	f.write(cppFile)

#run the following: g++ -fopenmp -o testGR testGR.cpp chrisC.cpp Ray.cpp Vector3.cpp -std=c++11 using subprocess
subprocess.run(["/opt/homebrew/Cellar/gcc/12.2.0/bin/aarch64-apple-darwin21-g++-12", "-fopenmp", "-o", "testGR", "testGR.cpp", "chrisC.cpp", "Ray.cpp", "Vector3.cpp", "-std=c++11"])
#time the next line
start = time.time()
subprocess.run(["./testGR"])
end = time.time()
print(end - start,"time to run")
subprocess.run(["python3", "reconstructParallel.py"])


def cartesian(pos):
	radius = pos[1]
	theta = pos[2]
	phi = pos[3]
	x = radius*sin(theta)*cos(phi)
	y = radius*sin(theta)*sin(phi)
	z = radius*cos(theta)
	return [x,y,z]




# def polar(x,y):
# 	return [math.sqrt(x**2+y**2),math.atan2(y,x)]

# class ray(object):
# 	"""docstring for ray"""
# 	def __init__(self, pos, vel):
# 		self.pos = pos
# 		self.vel = vel
# 		self.worldLine = []
# 	def geodesic(self):
# 		self.worldLine.append(cartesian(self.pos))
		
# 		dim = len(self.pos)
# 		newVel = []
# 		for lamda, l in enumerate(self.vel):
# 			a = 0
# 			for mu in range(dim):
# 				for nu in range(dim):
# 					cVal = chrisC[lamda][mu][nu].subs(r, self.pos[1])
# 					a -= cVal*self.vel[mu]*self.vel[nu]
# 					#print(chrisC[0][0][1].subs(r, 3.5),'this')
# 			newVel.append(l+a*dTau)
# 		self.vel = newVel

# 		for lamda, l in enumerate(self.pos):
# 			self.pos[lamda] += self.vel[lamda]*dTau



# lines = []
# for i in range(1,2):
# 	print(i)
# 	#r0,theta0 = polar(5,1.45+i*0.02)
# 	r0, theta0 = [100*rs, 0]
# 	#vr0,vtheta0 = polar(-0.1*i,0)
	
# 	ray1 = ray([0,r0,theta0], [1,0,0.00041])
# 	for j in range(3000):
# 		ray1.geodesic()
# 		if abs(ray1.pos[1]) <= 1.1*rs:
# 			break;
# 	lines.append(ray1.worldLine)
# print(2*G*M)
# #print(lines[1])
# for i in lines:
# 	X = [j[0] for j in i]
# 	Y = [j[1] for j in i]
# 	#plt.plot(np.cumsum(X), np.cumsum(Y))
# 	#for j in i:
# 	plt.scatter(X,Y)
# 	plt.plot(X,Y)
	
# plt.show()










		