package com.parse;

public class eUtils{
	public static boolean isNumber(char c){
		return c>='0' && c<='9' || c=='.';
	}
	public static boolean isLetter(char c){
		return c>='a' && c<='z';
	}
	public static boolean isFirstOperation(char c){
		return c=='+' || c=='-';
	}
	public static boolean isSecondOperation(char c){
		return  c=='*' || c=='/' || c=='^';
	}
}