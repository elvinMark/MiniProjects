import numpy as np
from emath import *
"""
Parsing equation expression
"""
"""
global variables used in parsing equations and evaluating them
"""
_index = 0
_str = ""
_eq_degree = 0
_VAR = ["x","t"]
_NUM = "0123456789"
_OP1 = "/*^"
_OP2 = "+-"
_CONS = ["e","pi"]
_LETTER = "abcdefghijklmnopqrstuvwxyz"
_FUN = ["sin","cos","tan","log","sinh","cosh","tanh","csc","sec","cot","csch","sech","coth","arcsin","arccos","arctan"]

_CONS_VALUES = {"e":np.e,"pi":np.pi}
_FUN_DEF = {"sin":lambda x: np.sin(x),"cos":lambda x:np.cos(x),"tan":lambda x:np.tan(x),"log":lambda x:np.log(x),\
			"sinh":lambda x:(np.exp(x) - np.exp(-x))/2,"cosh":lambda x:(np.exp(x) + np.exp(-x))/2,\
			"tanh":lambda x :(np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x)), "csc":lambda x:1/np.sin(x),\
			"sec":lambda x:1/np.cos(x),"cot":lambda x:1/np.tan(x),"csch":lambda x:2/(np.exp(x) - np.exp(-x)),\
			"sech":lambda x:2/(np.exp(x) + np.exp(-x)),"coth":lambda x:(np.exp(x) + np.exp(-x))/(np.exp(x) - np.exp(-x)),\
			"arcsin":lambda x:np.arcsin(x),"arccos":lambda x:np.arccos(x),"arctan":lambda x:np.arctan(x)}
_VAR_DEF = {"u0":1,"t":2}
_DERIV_DEF = {"u1":3,"u2":4,"u3":0,"u4":0,"u5":0}

"""
classes:
			PNode
			ParseEq

parsing functions:
			parse_variable
			parse_constant
			parse derivative
			parse_number
			parse_fun
			parse_term
			parse_exp
			is_tem
evaluate parsed nodes:
			eval_constant
			eval_num
			eval_variable
			eval_derivative
			eval_operation
			eval_function
			eval_node

"""
class PNode:
	def __init__(self,ptype,stem=None):
		self.child = []
		self.ptype = ptype
		self.stem = stem
	def add_child(self,child):
		self.child.append(child)
	def remove_child(self):
		return self.child.pop()
	def num_child(self):
		return len(self.child)
	def print_tree(self,depth):
		print(" "*depth,end="")
		print(self.ptype)
		for c in self.child:
			c.print_tree(depth+1)

def parse_variable():
	global _index
	node = PNode("variable")
	if _str[_index] == "x":
		tmp = PNode("u0")
		node.add_child(tmp)
		_index += 1
	elif _str[_index] == "t":
		tmp = PNode("t")
		node.add_child(tmp)
		_index += 1
	else:
		print("Error parsing: Variable expected")
		print("at index %d character %s"%(_index,_str[_index]))
		exit()
	return node
def parse_constant():
	global _index
	node = PNode("constant") #const_(name)
	s = ""
	_index += 6
	while _str[_index] in _LETTER:
		s += _str[_index]
		_index += 1
		if _index == len(_str):
			break
	if not s in _CONS:
		print("Error parsing: constand not defined")
		exit()
	tmp = PNode(s)
	node.add_child(tmp)
	return node
def parse_derivative():
	global _index
	global _eq_degree
	node = PNode("derivative")
	_index += 1
	if _str[_index] == "x": #dx/dt
		tmp = PNode("u1")
		node.add_child(tmp)
		_index += 4
		if _eq_degree < 1:
			_eq_degree = 1
	elif _str[_index] in _NUM: #dkx/dtk
		k = int(_str[_index])
		tmp = PNode("u"+_str[_index])
		node.add_child(tmp)
		_index += 6
		if _eq_degree < k:
			_eq_degree = k
	else:
		print("Error parsing: Derivative expected")
		print("at index %d character %s"%(_index,_str[_index]))
		exit()
	return node

def parse_number():
	global _index
	node = PNode("number")
	s = ""
	while _str[_index] in _NUM or _str[_index]==".":
		s += _str[_index]
		_index += 1
		if _index == len(_str):
			break
	tmp = PNode(s)
	node.add_child(tmp)
	return node

def parse_fun():
	global _index
	node = PNode("function")
	s = ""
	_index += 4#fun_(name)
	while _str[_index] in _LETTER and _str[_index]!="(":
		s += _str[_index]
		_index += 1
		if _index == len(_str):
			break
	if _str[_index] != "(":
		print("Error parsing function: ( expected")
		exit()
	_index += 1
	if not s in _FUN:
		print("Error parsing function: Function not found")
		exit()
	tmp = PNode(s)
	tmp1 = parse_exp()
	tmp.add_child(tmp1)
	node.add_child(tmp)
	_index += 1
	return node
def parse_term():
	global _index
	node = PNode("term")
	while not _str[_index] in _OP2 and _str[_index]!=")":
		if _str[_index] in _VAR:
			tmp = parse_variable()
			node.add_child(tmp)
		elif _str[_index] == "c":
			tmp = parse_constant()
			node.add_child(tmp)
		elif _str[_index] == "d":
			tmp = parse_derivative()
			node.add_child(tmp)
		elif _str[_index] == "(":
			_index += 1
			tmp = parse_exp()
			node.add_child(tmp)
			if _str[_index] == ")":
				_index += 1
			else:
				print("Error parsing: ) expected")
				exit()	
		elif _str[_index] in _NUM:
			tmp = parse_number()
			node.add_child(tmp)
		elif _str[_index] in _OP1 :
			tmp = PNode("operation")
			tmp1 = PNode(_str[_index])
			tmp1.add_child(node.remove_child())
			_index += 1
			tmp1.add_child(parse_term())
			tmp.add_child(tmp1)
			node.add_child(tmp)
		elif _str[_index] == "f":
			tmp = parse_fun()
			node.add_child(tmp)
		else:
			print("Error parsing: Term expected")
			print("at index %d character %s"%(_index,_str[_index]))
			exit()
		if _index == len(_str):
			break
	return node

def is_term(s):
	return s in _NUM or s in _VAR or s == "d" or s=="(" or s=="c" or s=="f"
def parse_exp():
	global _index
	node = PNode("expression")
	while _index < len(_str):
		if _str[_index] in _OP2:
			tmp0 = PNode("operation")
			if _str[_index] == "-":
				tmp = PNode("-")
				_index += 1
				if node.num_child() == 0:
					tmp2 = PNode("number")
					tmp1 = PNode("0")
					tmp2.add_child(tmp1)
					tmp.add_child(tmp2)
				else:
					tmp.add_child(node.remove_child())
				tmp1 = parse_term()
				tmp.add_child(tmp1)
				tmp0.add_child(tmp)
				node.add_child(tmp0)
			elif _str[_index] == "+":
				tmp = PNode("+")
				_index += 1
				if node.num_child == 0:
					tmp1 = PNode("0")
					tmp.add_child(tmp1)
				else:
					tmp.add_child(node.remove_child())
				tmp1 = parse_term()
				tmp.add_child(tmp1)
				tmp0.add_child(tmp)
				node.add_child(tmp0)
		elif is_term(_str[_index]):
			tmp = parse_term()
			node.add_child(tmp)
		else:
			break
	return node
def eval_constant(node):
	return _CONS_VALUES[node.ptype]
def eval_num(node):
	return float(node.ptype)
def eval_variable(node):
	return _VAR_DEF[node.ptype]
def eval_derivative(node):
	return _DERIV_DEF[node.ptype]
def eval_operation(node):
	tmp1 = node.child[0]
	tmp2 = node.child[1]
	if node.ptype == "+":
		return eval_node(tmp1) + eval_node(tmp2)
	elif node.ptype == "-":
		return eval_node(tmp1) - eval_node(tmp2)
	elif node.ptype == "*":
		return eval_node(tmp1) * eval_node(tmp2)
	elif node.ptype == "/":
		return eval_node(tmp1) / eval_node(tmp2)
	elif node.ptype == "^":
		return eval_node(tmp1) ** eval_node(tmp2)
def eval_function(node):
	tmp = node.child[0]
	return _FUN_DEF[node.ptype](eval_node(tmp))

def eval_node(node):
	if node.ptype == "expression":
		return eval_node(node.child[0])
	elif node.ptype == "constant":
		return eval_constant(node.child[0])
	elif node.ptype == "number":
		return eval_num(node.child[0])
	elif node.ptype == "variable":
		return eval_variable(node.child[0])
	elif node.ptype == "derivative":
		return eval_derivative(node.child[0])
	elif node.ptype == "operation":
		return eval_operation(node.child[0])
	elif node.ptype == "term":
		return eval_node(node.child[0])
	elif node.ptype == "function":
		return eval_function(node.child[0])

class ParseEq:
	def __init__(self,str_eq):
		global _index
		global _str
		global _eq_degree
		tmp = str_eq.split("=")
		if len(tmp) != 2:
			self.right_side = None
			self.left_side = None
			print("Error: Input Equation not well defined")
			exit()
		self.left_side = tmp[0].replace(" ","")
		self.right_side = tmp[1].replace(" ","")
		_index = 0
		_str = self.left_side
		_eq_degree = 0
		self.left_exp = parse_exp()
		_index = 0
		_str = self.right_side
		self.right_exp = parse_exp()
		self.one_side_exp = PNode("expression")
		tmp = PNode("operation")
		tmp1 = PNode("-")
		tmp1.add_child(self.left_exp)
		tmp1.add_child(self.right_exp)
		tmp.add_child(tmp1)
		self.one_side_exp.add_child(tmp)
		self.eq_degree = _eq_degree
	def __str__(self):
		tmp = ""
		tmp += "Left Side: "+ self.left_side + "\n"
		tmp += "Right Side: "+ self.right_side + "\n"
		return tmp
	def print_nodes(self):
		print("Left Side:")
		self.left_exp.print_tree(0)
		print("Right Side:")
		self.right_exp.print_tree(0)
		print("One Sided expression")
		self.one_side_exp.print_tree(0)
	def print_details(self):
		print(self)
		print("Equation Degree: %d"%(self.eq_degree))
		print("Parse:")
		self.one_side_exp.print_tree(0)
	def funf(self,y):
		global _DERIV_DEF
		_DERIV_DEF["u" + str(self.eq_degree)] = y
		return eval_node(self.one_side_exp)
	def eval(self,u,t):
		global _VAR_DEF
		global _DERIV_DEF
		_VAR_DEF["u0"] = u[0]
		_VAR_DEF["t"] = t
		for i in range(1,len(u)):
			_DERIV_DEF["u"+str(i)] = u[i]
		h = 0.001
		funf = lambda y: self.funf(y)
		dfunf = lambda y: (funf(y+h)-funf(y))/h
		x0 = u[0]
		return newton_method(funf,dfunf,x0)

"""
#Test parsing
testeq = "d2x/dt2 + x + fun_cos(x*t) = 0"
pe = ParseEq(testeq)
pe.print_details()
"""
