package com.parse;

import java.util.*;

public class eNode{
	public String type;
	public ArrayList<eNode> child;

	public eNode(String s){
		this.type = s;
		this.child = new ArrayList<eNode>();
	}

	public void addChild(eNode child){
		this.child.add(child);
	}

	public eNode popChild(){
		return this.child.remove(this.child.size()-1);
	}

	public int getNumChild(){
		return this.child.size();
	}

	public void print(int depth){
		for(int i = 0;i<depth;i++)
			System.out.print(" ");
		System.out.println(type);
		for(eNode tmp : child)
			tmp.print(depth + 1);
	}
}