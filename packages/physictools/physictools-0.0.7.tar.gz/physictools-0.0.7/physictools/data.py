import scipy.optimize as sp
from typing import List,Callable
import types
import numpy as np

def fit_curve(func: Callable,x_vals: List[float],y_vals: List[float],startx:float=None,endx:float=None,starty:float=None,endy:float=None,guess:List[float]=None,maxfev:int=10000)->tuple[Callable,List[float],List[float]]:
    if not isinstance(func, (types.FunctionType)): raise Exception("Bad parameter 'func'")  
    if not isinstance(x_vals, (list,np.ndarray)): raise Exception("Bad parameter 'x_vals'")    
    if not isinstance(y_vals, (list,np.ndarray)): raise Exception("Bad parameter 'y_vals'")        
    if not isinstance(startx, (float,int,types.NoneType)): raise Exception("Bad parameter 'startx'")    
    if not isinstance(endx, (float,int,types.NoneType)): raise Exception("Bad parameter 'endx'")    
    if not isinstance(starty, (float,int,types.NoneType)): raise Exception("Bad parameter 'starty'")    
    if not isinstance(endy, (float,int,types.NoneType)): raise Exception("Bad parameter 'endy'")    
    if not isinstance(guess, (list,types.NoneType,np.ndarray)): raise Exception("Bad parameter 'guess'")    
    if not isinstance(maxfev, (int)): raise Exception("Bad parameter 'maxfev'") 
    if (len(x_vals) < 2): raise Exception("'x_vals' too small")
    if (len(x_vals) != len(y_vals)): raise Exception("Size of 'x_vals' does not match size of 'y_vals'")
    if startx == None: startx = min(x_vals)
    if endx == None: endx = max(x_vals)
    if starty == None: starty = min(y_vals)
    if endy == None: endy = max(y_vals)   
    x_fit,y_fit = [],[]
    for i in range(0,len(x_vals)):
        x = x_vals[i]
        y = y_vals[i]
        if (startx <= x <= endx and starty <= y <= endy):
            x_fit.append((x-startx))
            y_fit.append((y-starty))
    if (len(x_fit)<2): raise Exception("wrong bounds")
    if (guess==None): popt,pcov=sp.curve_fit(func,x_fit,y_fit,maxfev=maxfev)
    else: popt,pcov=sp.curve_fit(func,x_fit,y_fit,p0=guess,maxfev=maxfev)
    return lambda x: (func((x-startx), *popt))+starty,popt,pcov

def get_data(fileloc: str, sep: str=",", comma: str=".", cols:str="x1/y1",breaker: str = "\n",skip:int=0):
    datalines = []
    values = []
    xs = []
    ys = []
    i=0
    for col in cols.lower().split("/"):
        if (col.startswith("x")):xs.append([i,int(col.replace("x",""))-1])
        if (col.startswith("y")):ys.append([i,int(col.replace("y",""))-1])
        i += 1
    i=0
    for i in range(0,len(xs)):
        values.append([[],[]])
    with open(fileloc, 'r') as file:
        datalines = file.read().split(breaker)
    for i in range(skip,len(datalines)-1):
        for j in range(0,len(xs)):
            val = datalines[i].split(sep)[xs[j][0]].replace(comma,".")
            if (val != ""):values[xs[j][1]][0].append(float(val))
            else:
                values[xs[j][1]][0].append(None)
                print("Empty or incomplete row found at:"+str(i+1)+"(Appending none)")
        for j in range(0,len(ys)):
            val = datalines[i].split(sep)[ys[j][0]].replace(comma,".")
            if (val != ""):values[ys[j][1]][1].append(float(val))
            else:
                values[ys[j][1]][1].append(None)
                print("Empty or incomplete row found at:"+str(i+1)+"(Appending none)")
    i = len(datalines)-1
    if (datalines[i] != ""): 
        for j in range(0,len(xs)):
            print(datalines[i].split(sep))
            values[xs[j][1]][0].append(float(datalines[i].split(sep)[xs[j][0]].replace(comma,".")))
        for j in range(0,len(ys)):
            values[ys[j][1]][1].append(float(datalines[i].split(sep)[ys[j][0]].replace(comma,".")))
    return values

def author():
    print("Thank you for downloading physicstools ~ Pulok00")
