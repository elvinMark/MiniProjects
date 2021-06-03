package com.math;

import java.util.*;
import com.math.*;
import com.parse.*;

public class eDiffEq{
	public eNode expr;
	public int degree;
	public HashMap<String,Double> var_values;
	public HashMap<String,Double> diff_values;

	public eDiffEq(eNode node,int degree){
		this.expr = node;
		this.degree = degree;
		var_values = new HashMap<String,Double>();
		diff_values = new HashMap<String,Double>();
		var_values.put("x",0.0);
		for(int i = 0;i<=degree;i++)
			diff_values.put(("y" + i),0.0);
	}

	public void setVariableValue(double x){
		var_values.replace("x",x);
	}

	public void setDiffValue(int i, double y){
		diff_values.replace(("y"+i),y);
	}

	public int getDegree(){
		return degree;
	}

	public double evalNumber(eNode node){
		return Double.parseDouble(node.type);
	}

	public double evalVariable(eNode node){
		return var_values.get(node.type);
	}

	public double evalConstant(eNode node){
		return eConstants.values.get(node.type);
	}

	public double evalDerivative(eNode node){
		return diff_values.get(node.type);
	}

	public double evalFunction(eNode node){
		double s;
		s = evalExpression(node.child.get(0));
		if(node.type.equals("sin"))
			return Math.sin(s);
		else if(node.type.equals("cos"))
			return Math.cos(s);
		else if(node.type.equals("tan"))
			return Math.tan(s);
		else if(node.type.equals("sec"))
			return 1/Math.cos(s);
		else if(node.type.equals("csc"))
			return 1/Math.sin(s);
		else if(node.type.equals("cot"))
			return 1/Math.tan(s);
		else if(node.type.equals("log"))
			return Math.log(s);
		else if(node.type.equals("asin"))
			return Math.asin(s);
		else if(node.type.equals("acos"))
			return Math.acos(s);
		else if(node.type.equals("atan"))
			return Math.atan(s);
		else if(node.type.equals("exp"))
			return Math.exp(s);
		else if(node.type.equals("sinh"))
			return (Math.exp(s) - Math.exp(-s))/2;
		else if(node.type.equals("cosh"))
			return (Math.exp(s) + Math.exp(-s))/2;
		else if(node.type.equals("tanh"))
			return (Math.exp(s) - Math.exp(-s))/(Math.exp(s) + Math.exp(-s));
		else if(node.type.equals("csch"))
			return 2/(Math.exp(s) - Math.exp(-s));
		else if(node.type.equals("sech"))
			return 2/(Math.exp(s) + Math.exp(-s));
		else if(node.type.equals("coth"))
			return (Math.exp(s) + Math.exp(-s))/(Math.exp(s) - Math.exp(-s));
		else
			return 0;
	}

	public double evalOperation(eNode node){
		double s1,s2;
		s1 = evalTerm(node.child.get(0));
		s2 = evalTerm(node.child.get(1));
		if(node.type.equals("+"))
			return s1+s2;
		else if(node.type.equals("-"))
			return s1-s2;
		else if(node.type.equals("*"))
			return s1*s2;
		else if(node.type.equals("/"))
			return s1/s2;
		else if(node.type.equals("^"))
			return Math.pow(s1,s2);
		else
			return 0;
	}

	public double evalTerm(eNode node){
		if(node.type.equals("Term"))
			return evalTerm(node.child.get(0));
		else if(node.type.equals("Operation"))
			return evalOperation(node.child.get(0));
		else if(node.type.equals("Number"))
			return evalNumber(node.child.get(0));
		else if(node.type.equals("Variable"))
			return evalVariable(node.child.get(0));
		else if(node.type.equals("Derivative"))
			return evalDerivative(node.child.get(0));
		else if(node.type.equals("Function"))
			return evalFunction(node.child.get(0));
		else if(node.type.equals("Expression"))
			return evalExpression(node.child.get(0));
		else
			return 0;
	}

	public double evalExpression(eNode node){
		if(node.type.equals("Term"))
			return evalTerm(node.child.get(0));
		else if(node.type.equals("Expression"))
			return evalExpression(node.child.get(0));
		else
			return 0;
	}

	public double eval(){
		return evalExpression(expr.child.get(0));
	}

	public void print(){
		expr.print(0);
	}
}