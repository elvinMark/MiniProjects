package com.parse;

import java.util.*;
import com.parse.*;

public class eParse{
	String expr;
	int len;
	int curr_index;
	ArrayList<String> constants;
	ArrayList<String> variables;
	String[] functions = {"sin","cos","tan","csc","sec","cot","log","asin","acos","atan","exp","sinh","cosh","tanh","csch","sech","coth"};
	int degree;

	public eParse(){
		expr = "";
		degree = 0;
	}

	public void setExpr(String s){
		expr = "";
		for(int i = 0; i<s.length();i++){
			if(s.charAt(i) != ' ')
				expr += s.charAt(i);
		}
		len = expr.length();
		curr_index = 0;
	}

	public void setConstants(){
		constants = new ArrayList<String>();
		constants.add("pi");
		constants.add("e");
	}

	public void setVariables(){
		variables = new ArrayList<String>();
		variables.add("x");
	}

	public int getDegree(){
		return degree;
	}

	public boolean isConstant(String s){
		for(String tmp : constants){
			if(tmp.equals(s))
				return true;
		}
		return false;
	}

	public boolean isVariable(String s){
		for(String tmp : variables){
			if(tmp.equals(s))
				return true;
		}
		return false;	
	}

	public boolean isFunction(String s){
		for(String tmp : functions){
			if(tmp.equals(s))
				return true;
		}
		return false;	
	}

	public boolean isDerivative(String s){
		if(s.charAt(0)!='y')
			return false;
		for(int i = 1;i<s.length();i++)
			if(s.charAt(i)!='\'')
				return false;
		return true;
	}

	public boolean isTerm(){
		char c = expr.charAt(curr_index);
		return eUtils.isNumber(c) || eUtils.isLetter(c) || c=='(';	
	}

	public String lookahead(){
		String s = "";
		int index = curr_index;
		char c = expr.charAt(index);
		while(eUtils.isLetter(c) || eUtils.isNumber(c) || c=='\''){
			s += c;
			index++;
			if(index == len)
				break;
			c = expr.charAt(index);
		}
		return s;
	}

	public eNode parseConstant(){
		String s = "";
		eNode node = new eNode("Constant");
		char c = expr.charAt(curr_index);
		while(eUtils.isLetter(c) || eUtils.isNumber(c)){
			s += c;
			curr_index++;
			if(curr_index == len)
				break;
			c = expr.charAt(curr_index);
		}
		node.addChild(new eNode(s));
		return node;
	}

	public eNode parseVariable(){
		String s = "";
		eNode node = new eNode("Variable");
		char c = expr.charAt(curr_index);
		while(eUtils.isLetter(c) || eUtils.isNumber(c)){
			s += c;
			curr_index++;
			if(curr_index == len)
				break;
			c = expr.charAt(curr_index);
		}
		node.addChild(new eNode(s));
		return node;
	}

	public eNode parseNumber(){
		String s = "";
		eNode node = new eNode("Number");
		while(eUtils.isNumber(expr.charAt(curr_index))){
			s += expr.charAt(curr_index);
			curr_index++;
			if(curr_index == len)
				break;
		}
		node.addChild(new eNode(s));
		return node;
	}

	public eNode parseFunction(){
		String s = "";
		eNode node = new eNode("Function");
		eNode tmp,tmp1;
		char c = expr.charAt(curr_index);
		while(eUtils.isLetter(c)){
			s += c;
			curr_index++;
			if(curr_index == len)
				break;
			c = expr.charAt(curr_index);
		}
		if(c != '(')
			System.exit(0);
		curr_index++;
		tmp = parseExpression();
		tmp1 = new eNode(s);
		tmp1.addChild(tmp);
		node.addChild(tmp1);
		c = expr.charAt(curr_index);
		if(c!=')')
			System.exit(0);
		curr_index++;
		return node;
	}

	public eNode parseDerivative(){
		String s = "y";
		int i = 0;
		char c;
		eNode node = new eNode("Derivative");
		curr_index++;
		c = expr.charAt(curr_index);
		while(c=='\''){
			curr_index++;
			i++;
			if(curr_index == len)
				break;
			c = expr.charAt(curr_index);
		}
		s += i;
		if(degree<i)
			degree = i;
		node.addChild(new eNode(s));
		return node;
	}

	public eNode parseSimpleTerm(){
		eNode node = new eNode("Term");
		eNode tmp;
		String str;
		char c = expr.charAt(curr_index);
		if(eUtils.isNumber(c)){
			tmp = parseNumber();
			node.addChild(tmp);
		}
		else if(eUtils.isLetter(c)){
			str = lookahead();
			if(isConstant(str)){
				tmp = parseConstant();
				node.addChild(tmp);
			}
			else if(isVariable(str)){
				tmp = parseVariable();
				node.addChild(tmp);
			}
			else if(isFunction(str)){
				tmp = parseFunction();
				node.addChild(tmp);
			}
			else if(isDerivative(str)){
				tmp = parseDerivative();
				node.addChild(tmp);
			}
		}
		else if(c == '('){
			curr_index++;
			tmp = parseExpression();
			node.addChild(tmp);
			if(expr.charAt(curr_index)!=')')
				System.exit(0);
			curr_index++;
		}
		return node;
	}

	public eNode parseTerm(){
		eNode node = new eNode("Term");
		eNode tmp, tmp1, tmp2;
		String str;
		char c = expr.charAt(curr_index);
		while(!eUtils.isFirstOperation(c) && c!=')'){
			if(eUtils.isNumber(c) || eUtils.isLetter(c) || c == '('){
				tmp = parseSimpleTerm();
				node.addChild(tmp);
			}
			else if(eUtils.isSecondOperation(c)){
				tmp1 = new eNode("Operation");
				tmp2 = new eNode(c+"");
				if(node.getNumChild()==0)
					System.exit(0);
				tmp2.addChild(node.popChild());
				curr_index++;
				tmp = parseSimpleTerm();
				tmp2.addChild(tmp);
				tmp1.addChild(tmp2);
				tmp2 = new eNode("Term");
				tmp2.addChild(tmp1);
				node.addChild(tmp2);
			}
			else{
				System.exit(0);
			}
			if(curr_index == len)
				break;
			c = expr.charAt(curr_index);
		}
		return node;
	}

	public eNode parseExpression(){
		eNode node = new eNode("Expression");
		eNode tmp, tmp1, tmp2,tmp3;
		while(curr_index<len){
			if(eUtils.isFirstOperation(expr.charAt(curr_index))){
				tmp1 = new eNode("Operation");
				tmp2 = new eNode(""+expr.charAt(curr_index));
				if(node.getNumChild() == 0){
					tmp3 = new eNode("Number");
					tmp3.addChild(new eNode("0"));
					tmp = new eNode("Term");
					tmp.addChild(tmp3);
					node.addChild(tmp);
				}
				tmp2.addChild(node.popChild());
				curr_index++;
				tmp3 = parseTerm();
				tmp2.addChild(tmp3);
				tmp1.addChild(tmp2);
				tmp3 = new eNode("Term");
				tmp3.addChild(tmp1);
				node.addChild(tmp3);
			}
			else if(isTerm()){
				tmp = parseTerm();
				node.addChild(tmp);
			}
			else
				break;
		}
		return node;
	}

	public eNode parse(){
		return parseExpression();
	}
}