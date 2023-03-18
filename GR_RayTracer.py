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
subprocess.run(["g++", "-fopenmp", "-o", "testGR", "testGR.cpp", "chrisC.cpp", "Ray.cpp", "Vector3.cpp", "-std=c++11"])
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








		
