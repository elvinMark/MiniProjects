import numpy as np
from neural_net import *
from proc_audio import *

af = ["arriba1","arriba2","arriba3","abajo1","abajo2","abajo3","derecha1","derecha2","derecha3","izquierda1","izquierda2","izquierda3"]
o = np.array([[1,0,0,0],[1,0,0,0],[1,0,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,1],[0,0,0,1],[0,0,0,1]])
i = np.array([proc_audio(i+".m4a") for i in af])

print(i)
print(o)
p = perceptron(19,12,4)
p.train(i,o,5000)
p.forward(i)
print(p.get_output())
p.save_weight("my_weight.json")
