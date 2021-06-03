package com.math;

import java.util.*;
import com.parse.*;
import com.math.*;

public class eODE{
	public eFunction fun;
	public double[] t;
	public double[][] u;
	public int num_points;

	public eODE(String expr){
		StringTokenizer st = new StringTokenizer(expr,"=");
		String s1,s2;
		eParse parser = new eParse();
		eNode node;
		double[][] u;
		double[] t;
		s1 = st.nextToken();
		s2 = st.nextToken();
		parser.setConstants();
		parser.setVariables();
		parser.setExpr(s1 + "-" + "(" + s2 + ")");
		node = parser.parse();
		fun = new eFunction(node,parser.getDegree());
		num_points = 0;
	}

	public void solve(double[] init, double[] tdom, int N){
		t = eODESolver.linspace(tdom[0],tdom[1],N);
		u = eODESolver.rungeKutta(fun,init,t);
		num_points = N;
	}

	public void print(){
		fun.print();
	}
}