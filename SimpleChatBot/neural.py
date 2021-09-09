import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import convolve2d as conv2D 
import sys
import json
"""
Building a simple Convolutional Neural Network
1 Layer -- Conv
2 Layer -- MaxPool
3 Layer -- Flatten
4 Layer -- FCC + Softmax
"""

"""
Activation functions to be used
"""
def linear(x,diff=False):
	if diff:
		return np.ones(x.shape)
	return x
 
def sigmoid(x,diff=False):
	if diff:
		return x*(1-x)
	return 1/(1 + np.exp(-x))

def tanh(x,diff=False):
	if diff:
		return (1-x**2)/2
	return (1 - np.exp(-x))/(1 + np.exp(-x))

def relu(x,diff=False):
	out = np.zeros(x.shape)
	if diff:
		out[np.where(x>0)] = 1
		return out
	out[np.where(x>0)] = x[np.where(x>0)]
	return out

def leaky_relu(x,diff=False):
	out = None
	if diff:
		out = 0.1 * np.ones(x.shape)
		out[np.where(x>0)] = 1
		return out
	out = x.copy() * 0.1
	out[np.where(x>0)] = x[np.where(x>0)]
	return out

"""
Activation Function class
"""
class act_fun():
	def __init__(self,fun_type = "sigmoid"):
		if fun_type == "sigmoid":
			self.exec = sigmoid
		elif fun_type == "tanh":
			self.exec = tanh
		elif fun_type == "relu":
			self.exec = relu
		elif fun_type == "leaky_relu":
			self.exec = leaky_relu

def generate_regions(img,fsize,ssize):
	fx, fy = fsize
	sx, sy = ssize
	rows , cols = img.shape
	for i in range(0,rows - fx + 1,sx):
		for j in range(0,cols - fy + 1,sy):
			yield img[i:i+fx,j:j+fy], i//sx ,j//sy


"""
Batch Size
"""
batch_size = 0

"""
1 Layer -- Conv
"""
class conv():
	def __init__(self,filter_size,strider_size=(1,1)):
		#num, r, c = filter_size
		#self.num_filters = num
		self.fsize = filter_size #(r,c)
		self.ssize = strider_size
		self.filters = np.random.random(filter_size)
	def forward(self, in_data):
		num_i, i_rows, i_cols = in_data.shape
		num_f, f_rows, f_cols = self.fsize 
		s_rows, s_cols = self.ssize
		self.i = in_data
		self.conv_o = np.zeros((num_i*num_f,(i_rows - f_rows)//s_rows + 1,(i_cols - f_cols )//s_cols + 1))
		for k in range(num_i*num_f):
			for reg,i,j in generate_regions(in_data[k//num_f],(f_rows,f_cols),self.ssize):
				self.conv_o[k][i][j] = np.sum(self.filters[k%num_f] * reg)
		return self.conv_o
	def backward(self,err_data):
		self.delta = err_data
		num_e, e_rows, e_cols = err_data.shape
		num_f, f_rows, f_cols = self.fsize 
		out = np.zeros(self.i.shape)
		for i in range(num_e):
			out[i//num_f] += conv2D(err_data[i],self.filters[i%num_f])
		return out
	def update(self, alpha=1):
		num_i, i_rows, i_cols = self.i.shape
		num_f, f_rows, f_cols = self.fsize
		num_d, d_rows, d_cols = self.delta.shape
		for i in range(num_i):
			for j in range(num_f):
				for reg,k,l in generate_regions(self.i[i],(d_rows,d_cols),self.ssize):
					self.filters[j][k][l] -= alpha*np.sum(self.delta[i*num_f + j]*reg)
"""
2 Layer -- Max Pool
"""
class max_pool():
	def __init__(self,pool_size):
		self.pool_size = pool_size
	def forward(self,in_data):
		self.i = in_data
		self.in_shape = in_data.shape
		num, rows, cols = in_data.shape
		self.max_pool_o = np.zeros((num,rows//self.pool_size[0],cols//self.pool_size[1]))
		for k in range(len(in_data)):
			for reg, i, j in generate_regions(in_data[k],self.pool_size,self.pool_size):
				self.max_pool_o[k][i][j] = np.max(reg)
		return self.max_pool_o
	def backward(self,err_data):
		out = np.zeros(self.in_shape)
		for k in range(len(self.i)):
			for reg, i, j in generate_regions(self.i[k],self.pool_size,self.pool_size):
				ix, iy = np.where(reg == self.max_pool_o[k][i][j])
				out[k][i*self.pool_size[0] + ix[0]][j*self.pool_size[1] + iy[0]] = err_data[k][i][j]
		return out
	def update(self,alpha=1):
		pass				
"""
3 Layer -- Flatten
"""
class flatten():
	def __init__(self):
		self.in_shape = None
		self.out_shape = None
	def forward(self,in_data):
		num,rows,cols = in_data.shape
		self.in_shape = (num, rows,cols)
		self.out_shape = (batch_size, rows * cols * (num//batch_size))
		return in_data.reshape(self.out_shape)
	def backward(self,err_data):
		return err_data.reshape(self.in_shape)
	def update(self,alpha=1):
		pass

"""
4 Layer -- FCC + Softmax (Cross Entropy Loss)
"""
class fcc_softmax():
	def __init__(self,inputs,outputs,fun_type="sigmoid"):
		self.type = "fcc_softmax"
		self.inputs = inputs
		self.outputs = outputs
		self.w = np.random.random([inputs,outputs])
		self.bias = np.random.random(outputs)
		self.act_fun = act_fun(fun_type=fun_type)
		self.delta = None
	def forward(self,in_data):
		# Storing input data 
		self.i = in_data
		# Calculate output of the fully connected layer
		self.fcc_o = self.act_fun.exec(np.dot(in_data,self.w) + self.bias)
		# Calculate output of the softmax layer
		self.softmax_o = np.exp(self.fcc_o)
		tmp = np.sum(self.softmax_o,axis=1).reshape(len(self.softmax_o),1)
		self.softmax_o = self.softmax_o / tmp
		return self.softmax_o
	def backward(self,target_data):
		# Gradient of the Cross Entroyp loss
		# Calculate error for the FCC layer output
		e1 = self.softmax_o - target_data
		# Calculate Delta (update factor)
		self.delta = e1*self.act_fun.exec(self.fcc_o,diff=True)
		# Backpropagete Error
		err = np.dot(self.delta,self.w.T)
		return err
	def update(self,alpha=1):
		self.w -= alpha*self.i.T.dot(self.delta)
		self.bias -= alpha*np.sum(self.delta,axis=0)
"""
Extra Layers for other testings
"""

# Extra Layer -- Simple FCC layer
class fcc():
	def __init__(self,inputs,outputs,fun_type="sigmoid"):
		self.type = "fcc"
		self.inputs = inputs
		self.outputs = outputs
		self.w = np.random.random([inputs,outputs])
		self.bias = np.random.random(outputs)
		self.act_fun = act_fun(fun_type=fun_type)
		self.delta = None
	def forward(self,in_data):
		# Storing input data
		self.i = in_data
		# Calculate output of the fully connected layer
		self.fcc_o = self.act_fun.exec(np.dot(in_data,self.w) + self.bias)
		return self.fcc_o
	def backward(self,err_data):
		# Calculate Delta (update factor)
		self.delta = err_data*self.act_fun.exec(self.fcc_o,diff=True)
		# Backpropagete Error
		err = np.dot(self.delta,self.w.T)
		return err
	def update(self,alpha=1):
		self.w -= alpha*self.i.T.dot(self.delta)
		self.bias -= alpha*np.sum(self.delta,axis=0)

# Extra Layer -- Simple FCC layer + Mean Square Error
class fcc_mse():
	def __init__(self,inputs,outputs,fun_type="sigmoid"):
		self.type = "fcc_mse";
		self.inputs = inputs
		self.outputs = outputs
		self.w = np.random.random([inputs,outputs]) 
		self.bias = np.random.random(outputs) 
		self.act_fun = act_fun(fun_type=fun_type)
		self.delta = None
	def forward(self,in_data):
		# Storing input data
		self.i = in_data
		# Calculate output of the fully connected layer
		self.fcc_o = self.act_fun.exec(np.dot(in_data,self.w) + self.bias)
		return self.fcc_o
	def backward(self,target_data):
		#Calculate error - gradient of the Mean Square Loss 
		err_data = self.fcc_o - target_data
		# Calculate Delta (update factor)
		self.delta = err_data*self.act_fun.exec(self.fcc_o,diff=True)
		# Backpropagete Error
		err = np.dot(self.delta,self.w.T)
		return err
	def update(self,alpha=1):
		self.w -= alpha*self.i.T.dot(self.delta)
		self.bias -= alpha*np.sum(self.delta,axis=0)


def forward(model,in_data):
	global batch_size
	batch_size = len(in_data)
	o = in_data
	for l in model:
		o = l.forward(o)
	return o
def backward(model,target_data):
	o = target_data
	for l in reversed(model):
		o = l.backward(o)
	return o
def update(model,alpha=1):
	for l in model:
		l.update(alpha=alpha)
def train(model,in_data,target_data,alpha=1,numIt=500):
	for i in range(numIt):
		forward(model,in_data)
		backward(model,target_data)
		update(model,alpha=alpha)

def save_model(model,dir_path):
	out = {"layers":[]}
	for l in model:
		tmp = {}
		tmp["type"] = l.type
		tmp["weights"] = l.w.tolist()
		tmp["bias"] = l.bias.tolist()
		out["layers"].append(tmp)
	with open(dir_path,"w") as file:
		json.dump(out,file)
	return out

def load_model(model,dir_path):
	with open(dir_path,"r") as file:
		data = json.load(file)
		for i in range(len(model)):
			model[i].w = np.array(data["layers"][i]["weights"]) 
			model[i].bias = np.array(data["layers"][i]["bias"])