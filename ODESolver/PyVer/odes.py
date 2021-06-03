import numpy as np 
import matplotlib.pyplot as plt 
from emath import *
from eparse import *

"""
class:		ODE solver
"""
class OdeSolver:
	def __init__(self,str_eq,initial,tdom):
		self.parse_eq = ParseEq(str_eq)
		self.initial = initial
		self.tdom = tdom
	def solve(self):
		funf = lambda u,t :np.array([u[i] for i in range(1,len(u))] + [self.parse_eq.eval(u,t)])
		self.u_solve, self.t_solve = runge_kutta(funf,self.initial,self.tdom)
		return self.u_solve, self.t_solve
	def plot_solution(self):
		for i in range(self.parse_eq.eq_degree):
			plt.plot(self.t_solve,self.u_solve[:,i],label="u"+str(i))
		plt.legend()
		plt.show()
if __name__=="__main__":
        #Test OdeSolver
        testeq = "d2x/dt2 + 2*dx/dt + x = fun_cos(x)"
        os = OdeSolver(testeq,np.array([0,5]),[0,8])
        u,t = os.solve()
        os.plot_solution()

        
