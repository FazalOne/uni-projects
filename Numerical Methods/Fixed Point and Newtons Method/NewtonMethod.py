# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 18:59:57 2022

@author: Ammar
"""
import math
import time
import sympy as sm
import matplotlib.pyplot as plt
from tabulate import *

def f(x):
    val = sm.simplify(fx).subs({"x": x})
    return val

def Df(x):
    return sm.diff(fx, x)

def validityCheck(p0):
    return sm.diff(fx, "x").subs({"x": p0}) != 0

def fileWrite(c, p0, error, asym, t):
    global fx
    iteration = []
    i = 1
    while(i <= c):
        iteration.append(i)
        i+=1
    file = open("NewtonMethod.txt", "w", encoding="utf-8")
    file.write("{} \n".format(fx))
    data = {"i": iteration, "p0": p0, "error": error, "|Pn+1 - P| / |Pn - P|": asym}
    frame = tabulate(data, headers=dict.keys(data))
    file.write(frame)
    file.write(" \n")
    if(round(asym[-2] / asym[-1]) != 1):
        file.write("Asymptotic convergence constant moves non linearly \n")
    else:
        file.write("Asymptotic convergence constant moves sublinearly \n")
    file.write("Convergence constant = {} \n".format(asym[-2] /asym[-1]))
    file.write("Time Taken: {} ns \n".format(t))
    file.close()
    return;
    
def NewtonMethod(p0, e):
    err = 1000
    fx = []
    error = []
    #check for code validity
    if(validityCheck(p0)):
        start = time.time_ns()
        count = 0
        while(err >= e):
            try:
                fx.append(p0)
                prev = p0
                p0 = p0 - f(p0) / Df("x").subs({"x": p0})
                err = abs(prev - p0)
                error.append(err)
                count +=1
                print(count ,"  ", p0, "         ", err)
            except:
                print("Overflow error, rerun or reconsider fixed point method for this equation.")
                break
                
        end = time.time_ns()
        print("TIME TAKEN: ", end - start, "ns")
        asym = AsympConvergence(fx, p0)
        fileWrite(count, fx, error, asym, end - start)
        plotmygraph(fx, count)
        plotmygraph(fx, count)
        return p0
    else:
        p0 = float(input("Provide another root guess, the current does not converge: "))
        NewtonMethod(p0, e)
        
def AsympConvergence(fx, p0):
    asym = []
    for i in range(len(fx)):
        if(i > 0):
            asym.append(abs(fx[i] - p0)/abs(fx[i-1] -p0))
        else:
            asym.append(" ")
    return asym

def ApplicationExample():
    global fx
    C = 10
    vy = vx = 160
    print("y(t) = (C*vy + 32*C**2)(1 − e**(−t/C)) − 32*C*t")
    print("x(t) = C*vx*(1 − e**(−t/C))")
    fx= "({}*{} + 32*{}**2)*(1 - E**(-x/{})) - 32*{}*x".format(C,vy, C,C, C)
    print("Dy(x) where x is t: ", sm.diff(sm.simplify(fx), "x"))
    e = 0.001
    p0 = NewtonMethod(5.5, e)
    xt = "({}*{})*(1-E**(-x/10))".format(C, vx)
    print("x = ", sm.simplify(xt).subs({"x": p0}))
    return p0

def writeX(p0):
    C = 10
    vx = 160
    file = open("NewtonMethod.txt", "a", encoding="utf-8")
    file.write("X = {}".format(sm.simplify("({}*{})*(1-E**(-x/10))".format(C, vx)).subs({"x": p0})))
    file.close()

def plotmygraph(fx, i):
    x = []
    count = 1
    while(count <= i):
        x.append(count)
        count+=1
    plt.plot(x, fx)
    plt.title("Newton Raphson convergence chart")
    plt.xlabel("Iteration")
    plt.ylabel("p0 (value of x)")
    plt.show
    
def main():
    global fx
    global xt
    decision = input("Do you want to print out the example equation's solution?(y/N) ")
    if(decision != "y"):
        fx = str(input("Enter function in terms of x: "))
        p0 = eval(input("Input initial guess: "))
        e = float(input("Input tolerance level: "))
        print("Equation: ", fx)
        print( "Differential equation: ", Df("x"))
        NewtonMethod(p0, e)
    else:
        p0 = ApplicationExample()
        writeX(p0)
    
if __name__ == "__main__":
    main()