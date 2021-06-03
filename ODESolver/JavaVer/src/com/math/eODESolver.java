package com.math;

import com.math.*;

public class eODESolver{
	public static double newtonMethod(eFunction funf, double x0, int maxIt, double prec){
		double h=0.001;
		double x,f0,f1,df;
		x = 0;
		for(int i = 0;i<maxIt;i++){
			funf.setDiffValue(funf.getDegree(), x0);
			f0 = funf.eval();
			funf.setDiffValue(funf.getDegree(), x0 + h);
			f1 = funf.eval();
			df = (f1 - f0)/h;
			x = x0 - (f0/df);
			if(Math.abs(x - x0) <= prec * Math.abs(x))
				break;
			x0 = x;
		}
		return x;
	}

	public static double[] fun_f(eFunction funf, double[] u, double t){
		double[] out;
		int len = u.length;
		out = new double[len];
		funf.setVariableValue(t);
		for(int i = 0;i<len;i++)
			funf.setDiffValue(i,u[i]);
		for(int i = 1;i<len;i++)
			out[i-1] = u[i];
		out[len-1] = newtonMethod(funf,u[0],20,0.00001);
		return out;
	}

	public static double[] addVec(double[] v1, double[] v2){
		double[] out = new double[v1.length];
		for(int i = 0;i<v1.length ;i++)
			out[i] = v1[i] + v2[i];
		return out;
	}

	public static double[] scaleVec(double[] v1, double num){
		double[] out = new double[v1.length];
		for(int i = 0;i<v1.length ;i++)
			out[i] = v1[i] * num;
		return out;
	}

	public static double[] linspace(double t0, double tf, int N){
		double[] out = new double[N];
		double h = (tf - t0)/(N-1);
		out[0] = t0;
		for(int i = 1;i<N;i++)
			out[i] = out[i-1] + h;
		return out;
	}
	
	public static double[][] rungeKutta(eFunction funf, double[] init, double[] time){
		double h;
		double[][] out;
		double[] k1,k2,k3,k4;
		int N = time.length;
		
		out = new double[N][];
		out[0] = init;

		for(int i = 1; i<N;i++){
			h = time[i] - time[i-1];
			k1 = fun_f(funf,out[i-1],time[i-1]);
			k2 = fun_f(funf,addVec(out[i-1],scaleVec(k1,h/2)),time[i-1] + h/2);
			k3 = addVec(out[i-1],scaleVec(k1,h/2));
			k3 = fun_f(funf,addVec(out[i-1],scaleVec(k2,h/2)),time[i-1] + h/2);
			k4 = fun_f(funf,addVec(out[i-1],scaleVec(k3,h)),time[i-1] + h);
			k1 = scaleVec(k1,h/6);
			k2 = scaleVec(k2,h/3);
			k3 = scaleVec(k3,h/3);
			k4 = scaleVec(k4,h/6);
			out[i] = addVec(out[i-1],addVec(addVec(addVec(k1,k2),k3),k4));
		}
		return out;
	}
}