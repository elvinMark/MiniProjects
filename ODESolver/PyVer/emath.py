import numpy as np 
"""
Function Name:	Runge-Kutta (RK4)
Input:			Diff Function (from differential equation)
				Initial conditions
				Time domain as an array of 2 elements
				Number of time steps
Output:			Time array
				Solution array
"""
def runge_kutta(funf,u0,tdom,steps=50):
	t = np.linspace(tdom[0],tdom[1],steps)
	u = []
	u.append(u0)
	h = (tdom[1]-tdom[0])/(steps-1)
	for i in range(1,steps):
		utmp = u[i-1]
		ttmp = t[i-1]
		k1 = funf(utmp,ttmp)
		k2 = funf(utmp + k1*h/2, ttmp + h/2)
		k3 = funf(utmp + k2*h/2, ttmp + h/2)
		k4 = funf(utmp + k3*h, ttmp + h)
		utmp = utmp + (k1 + 2*k2 + 2*k3 + k4)*h/6
		u.append(np.array(utmp))
	u = np.array(u)
	return u,t
"""
#Test runge_kutta function
u0 = np.array([0,1])
tdom = [0,5]

def testf(u,t):
	return np.array([u[1],-u[0]])

u,t = runge_kutta(testf,u0,tdom)
plt.plot(t,u[:,0])
plt.show()
"""

"""
Function Name:		Newton Method
Input:				Function f(x) (f(x) = 0)
					Derivative of function f(x)
					Initial Point 
					Maximum number of iterations
					Maximum error in the approximation

"""
def newton_method(funf,dfunf,x0,maxIt=20,error=1e-2):
	for i in range(maxIt):
		x = x0 - funf(x0)/dfunf(x0)
		if x0 > 0:
			if np.abs((x-x0)/x0)<error:
				break
		x0 = x
	return x
"""
#Test netwon_method function
def funf(x):
	return x**3 - 11
def dfunf(x):
	return 3*x**2
print(newton_method(funf,dfunf,5))
"""