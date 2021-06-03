from pydub import AudioSegment
from proc_graph import *
import numpy as np
import matplotlib.pyplot as plt
import sys

def proc_audio(dir):
    s = AudioSegment.from_file(dir)
    ss = s.get_array_of_samples()

    f = np.fft.fft(ss)
    fa = np.abs(f)
    m = max(fa)

    #apply log
    #fa = np.log(fa)

    #normalization
    fa = fa/max(fa)

    #find coeff
    n = 18 #Aproximated Function degree
    f = np.linspace(-1,1,len(fa))
    c = find_coeff(f,fa,n)

    return c
"""
if __name__ == "__main__":
    s = AudioSegment.from_file(sys.argv[1])
    ss = s.get_array_of_samples()

    f = np.fft.fft(ss)
    fa = np.abs(f)
    m = max(fa)

    #apply log
    #fa = np.log(fa)#np.array([0 if i<0.1*m else i for i in fa])
    #normalization
    fa = fa/float(m)

    #find coeff
    n = 30 #Aproximated Function degree
    f = np.linspace(-1,1,len(fa))
    c = find_coeff(f,fa,n)
    
    if sys.argv[2] == "-show":
        plt.plot(fa)
        plt.show()
    elif sys.argv[2] == "-save":
        plt.plot(fa)
        plt.savefig(sys.argv[1].split(".")[0]+".png")
    elif sys.argv[2] == "-aprox":
        x = f
        y = eval_poly(c,f)
        print(c)
        plt.grid()
        plt.plot(x,y)
        plt.show()
    elif sys.argv[2] == "-aproxsave":
        x = f
        y = eval_poly(c,f)
        plt.plot(x,y)
        plt.grid()
        plt.savefig("img/"+sys.argv[1].split(".")[0]+"-1.png")
"""
