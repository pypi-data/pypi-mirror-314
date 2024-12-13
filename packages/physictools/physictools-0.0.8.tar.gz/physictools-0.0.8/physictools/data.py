import scipy.optimize as sp
import scipy.stats as st
from typing import List,Callable
import types
import numpy as np

def fit_curve(func: Callable,x_vals: List[float],y_vals: List[float],startx:float=0,endx:float=None,starty:float=0,endy:float=None,guess:List[float]=None,maxfev:int=10000)->tuple[Callable,List[float],List[float]]:
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
    if endx == None: endx = max(x_vals)
    if endy == None: endy = max(y_vals)   
    x_fit,y_fit=[],[]
    for i in range(0,len(x_vals)):
        x = x_vals[i]
        y = y_vals[i]
        if (startx <= x <= endx and starty <= y <= endy):
            x_fit.append((x-startx))
            y_fit.append((y-starty))
    
    if (len(x_fit)<2): raise Exception("wrong bounds")
    if (guess==None): popt,pcov=sp.curve_fit(func,x_fit,y_fit,maxfev=maxfev)
    else: popt,pcov=sp.curve_fit(func,x_fit,y_fit,p0=guess,maxfev=maxfev)
    return (lambda x: (func((np.array(x)-startx),*popt)+starty) if (isinstance(x,(list,np.ndarray))) else (func((x-startx), *popt))+starty),(popt),(pcov)

def get_data(fileloc: str, sep: str=",", comma: str=".", cols:str="1/2",breaker: str = "\n",skip:int=0) -> List[float]:
    datalines = []
    values = []
    xs = []
    i=0
    for col in cols.lower().split("/"):
        if (col != ""):xs.append([i,int(col)-1])
        i += 1
    i=0
    string = ""
    for i in range(0,len(xs)):
        values.append([])
    with open(fileloc, 'r') as file:
        datalines = file.read().split(breaker)
    for i in range(skip,len(datalines)-1):
        for j in range(0,len(xs)):
            val = datalines[i].split(sep)[xs[j][0]].replace(comma,".")
            if (val != ""):values[xs[j][1]].append(float(val))
            else:
                values[xs[j][1]].append(None)
                string += "Empty or incomplete row found at:"+str(i+1)+"(Appending none)\n"
    i = len(datalines)-1
    if (datalines[i] != ""): 
        for j in range(0,len(xs)):
            values[xs[j][1]].append(float(datalines[i].split(sep)[xs[j][0]].replace(comma,".")))
    if string != "": print(string)
    return values

def fit_and_confidence(func_1:Callable, x_vals:list,y_vals:list,confidence: float = .95,startx:float=0,endx:float=None,starty:float=0,endy:float=None,guess:List[float]=None,maxfev:int=10000) -> tuple[Callable,list,list,list]:
    func, popt,pcov = fit_curve(func_1,x_vals,y_vals,startx=startx,endx=endx,starty=starty,endy=endy,maxfev=maxfev,guess=guess)
    if endx == None: endx = max(x_vals)
    if endy == None: endy = max(y_vals)   
    x_fit, y_fit = [],[]
    for i in range(0,len(x_vals)):
        x = x_vals[i]
        y = y_vals[i]
        if (startx <= x <= endx and starty <= y <= endy):
            x_fit.append((x))
            y_fit.append((y))
    x_vals,y_vals = x_fit,y_fit
    if (isinstance(func,(list,np.ndarray))): y_err = (np.array(y_vals)-np.array(func)).std() * np.sqrt(1/len(x_vals) + (x_vals - x_vals.mean())**2 / np.sum((x_vals - x_vals.mean())**2))
    else: y_err = (np.array(y_vals)-func(np.array(x_vals))).std() * np.sqrt(1/len(x_vals) + (x_vals - np.mean(x_vals))**2 / np.sum((x_vals - np.mean(x_vals))**2))
    y_err *= st.t.ppf((1+confidence)/2,len(x_vals)-len(popt))
    return func,x_vals,func(np.array(x_vals))+y_err,func(np.array(x_vals))-y_err,[popt,pcov]
    
def author():
    print("Thank you for downloading physictools ~ Pulok00")
