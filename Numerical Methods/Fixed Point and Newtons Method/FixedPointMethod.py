# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 14:55:14 2022

@author: Ammar
"""

import matplotlib.pyplot as plt
import math
import time
import sympy as sm
from tabulate import *


# for evaluating function
def g(x):
    val = sm.simplify(gx).subs({"x":x})
    return val

# for receiving derivative function
def Dg(x):
    return sm.diff(gx, x)

# checks if the derivative is less than 1 for convergence
def validityCheck(p0):
    if(Dg("x").subs({"x": p0}) < 1):
        return True
    print("Result is not convergent, please provide a different value")
    print("Point value at derivative: ", Dg("x").subs({"x": p0, "e": math.exp(1)}))
    return False

# writing results to a file
def fileWrite(c, p0, error, asym, t):
    global fx
    iteration = []
    i = 1
    while(i <= c):
        iteration.append(i)
        i+=1
    file = open("FixedPoint.txt", "w", encoding="utf-8")
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

def AsympConvergence(fx, p0):
    asym = []
    for i in range(len(fx)):
        if(i > 0):
            asym.append(abs(fx[i] - p0)/abs(fx[i-1] -p0))
        else:
            asym.append(" ")
    return asym
            
    
def ModifiedFixedPoint(p0, e):
     err = 1000
     fx = []
     error = []
     if(Dfunc(p0) < 1):
         start = time.time_ns()
         count = 0
         while(err >= e):
             if(count > 30):
                 print("Convergence is taking too much time")
                 break       #important in cases of slow convergence
             try:
                 fx.append(p0)
                 prev = p0
                 p0 = func(p0)
                 err = abs(prev - p0)
                 error.append(err)
                 count +=1
                 print(count ,"  ", p0, "         ", err)
             except:
                 print("Overflow error, rerun or reconsider fixed point method for this equation.")
                 break
                
         end = time.time_ns()
         print("TIME TAKEN: ", end - start)
         asym = AsympConvergence(fx, p0)
         fileWrite(count, fx, error, asym, end - start)
         plotmygraph(fx, count)
         return p0
     else:
         p0 = float(input("Provide another root guess, the current does not converge: "))
         FixedPoint(p0, e)
             
     end = time.time_ns()
     print("TIME TAKEN: ", end - start, "ns")
     return p0
def func(x):
    return sm.simplify("15*(1 - E**(-x/10))").subs({"x": x}) #modified version of g(x)
def Dfunc(x):
    eq = sm.simplify("15*(1 - E**(-x/10))")
    return sm.diff(eq, "x").subs({"x": x})
def ApplicationExample():
    C = 10
    vy = vx = 160
    global fx
    fx = "y(t) = (C*vy + 32*C**2)(1 − e**(−t/C)) − 32*C*t"
    print("y(t) = (C*vy + 32*C**2)(1 − e**(−t/C)) − 32*C*t")
    print("x(t) = Cvx(1 − e**(−t/C))")
    e = 0.001
    p0 = 5.5
    p0 = ModifiedFixedPoint(p0, e)
    xt = "({}*{})*(1-E**(-x/10))".format(C, vx)
    print("x = ", sm.simplify(xt).subs({"x": p0}))   
    return p0
                                                                                                                                                                                                                                                                                                        #group 5: author (Ammar)
def writeX(p0):
    C = 10
    vx = 160
    file = open("FixedPoint.txt", "a", encoding="utf-8")
    file.write("X = {}".format(sm.simplify("({}*{})*(1-E**(-x/10))".format(C, vx)).subs({"x": p0})))
    file.close()

def plotmygraph(fx, i):
    x = []
    count = 1
    while(count <= i):
        x.append(count)
        count+=1
    plt.plot(x, fx)
    plt.title("Fixed point convergence chart")
    plt.xlabel("Iteration")
    plt.ylabel("p0 (value of x)")
    plt.show()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     #group 5: author (Ammar)
def FixedPoint(p0, e):
    err = 1000
    fx = []
    error = []
    #check for code validity
    if(validityCheck(p0)):
        start = time.time_ns()
        count = 0
        while(err >= e):
            if(count > 30):
                print("Convergence is taking too much time")
                break       #important in cases of slow convergence
            try:
                fx.append(p0)
                prev = p0
                p0 = g(p0)
                err = abs(prev - p0)
                error.append(err)
                count +=1
                print(count ,"  ", p0, "         ", err)
            except:
                print("Overflow error, rerun or reconsider fixed point method for this equation.")
                break
        end = time.time_ns()
        print("TIME TAKEN: ", end - start)
        asym = AsympConvergence(fx, p0)
        fileWrite(count, fx, error, asym)
        plotmygraph(fx, count)
        return p0
    else:
        p0 = float(input("Provide another root guess, the current does not converge: "))
        FixedPoint(p0, e)
    
def main():
    global gx
    global fx
    decision = input("Do you want to run application example? (y/N) ")
    if (decision != "y"):
        fx = str(input("Enter function in terms of x: "))
        gx = fx + "+ x"
        p0 = eval(input("Input initial guess: "))
        e = float(input("Input tolerance level: "))
        print(g(p0))
        print(Dg("x"))
        FixedPoint(p0, e)
    else:
        p0 = ApplicationExample()
        writeX(p0)

if __name__ == "__main__":
    main()