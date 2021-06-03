from emath import *
from math import *
import numpy as np 
import matplotlib.pyplot as plt 

streq = "d2y/dx2 + 2*dy/dx + y = atan(y)"
ls,rs = streq.split("=")

# Clean spaces
ls = ls.replace(" ","")
rs = rs.replace(" ","")

# Rename derivatives and function x(t) in both sides
ls = ls.replace("d2y/dx2","u2")
ls = ls.replace("dy/dx","u1")
ls = ls.replace("y","u0")

rs = rs.replace("d2y/dx2","u2")
rs = rs.replace("dy/dx","u1")
rs = rs.replace("y","u0")

# Put everything in one side
eq = ls + "-" + rs

# Initial conditions and time domain
initial = np.array([0,5])
tdom = [0,5]

def _funf(s,y):
	s = s.replace("y",str(y))
	return eval(s)

def eval_fun(u,t):
	tmp = eq
	for i in range(len(u)):
		tmp = tmp.replace("u"+str(i),str(u[i]))
	tmp = tmp.replace("x",str(t))
	k = i+1
	tmp = tmp.replace("u" + str(k),"y")
	h = 0.001
	funf = lambda y: _funf(tmp,y)
	dfunf = lambda y: (funf(y+h) - funf(y))/h
	ulast = newton_method(funf,dfunf,u[0])
	out = []
	for i in range(k-1):
		out.append(u[i+1])
	out.append(ulast)
	return np.array(out)

u,t = runge_kutta(eval_fun,initial,tdom)
k = len(u[0])
for i in range(k):
	plt.plot(t,u[:,i],label="u"+str(i))
plt.legend()
plt.show()