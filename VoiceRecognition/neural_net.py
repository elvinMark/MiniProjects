import numpy as np
from numpy import *
import json
#Simple perceptron with 3 layers
def sigmoid(x):
    return 1/(1 + np.exp(-x))

class perceptron():
    def __init__(self,n_i,n_h,n_o):
        self.n_i = n_i
        self.n_h = n_h
        self.n_o = n_o
        self.w1 = np.random.random([n_i,n_h])
        self.w2 = np.random.random([n_h,n_o])
    def forward(self,in_data):
        self.i = in_data
        self.o1 = sigmoid(in_data.dot(self.w1))
        self.o2 = sigmoid(self.o1.dot(self.w2))
    def backward(self,err_data):
        self.delta2 = self.o2*(1 - self.o2)*err_data
        err = self.delta2.dot(self.w2.T)
        self.delta1 = self.o1*(1 - self.o1)*err
    def update(self):
        self.w1 = self.w1 - 0.5*self.i.T.dot(self.delta1)
        self.w2 = self.w2 - 0.5*self.o1.T.dot(self.delta2)
    def train(self,in_data,out_data,N):
        for i in range(N):
            self.forward(in_data)
            self.backward(self.o2 - out_data)
            self.update()
    def get_output(self):
        return self.o2

    def load_weight(self,dirw):
        d = json.load(open(dirw))
        self.w1 = np.array(eval(d["w1"]))
        self.w2 = np.array(eval(d["w2"]))
    def save_weight(self,dirw):
        a = {"w1":str(list(self.w1)).replace("\n ",""),"w2":str(list(self.w2)).replace("\n ","")};
        json.dump(a,open(dirw,"w"))
    
