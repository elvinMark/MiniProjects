package com.test;

import com.parse.*;
import com.math.*;

public class eTest{
	public static void main(String args[]){
		eODE ode = new eODE("y'' = -y");
		double[] init = {0,1};
		double[] tdom = {0,5};
		int N = 50;
		ode.solve(init,tdom,N);
		ode.print();
		for(int i = 0;i<N;i++){
			System.out.println(ode.t[i] + " " + ode.u[i][0] + " " + ode.u[i][1]);
		}
	}
}