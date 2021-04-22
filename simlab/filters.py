import io
from flask import Response, request
from matplotlib.backends.backend_svg import FigureCanvasSVG

from matplotlib.figure import Figure
import numpy as np

def low_pass_tf(w,R,C):
    
    wc = 1/(R*C)
    
    return 1.0/(1.0 + 1j*(w/wc))

def high_pass_tf(w,R,C):
    wc = 1/(R*C)
    
    return (1j*w/wc)/(1.0 + 1j*w/wc)
def low_pass_filter(R,C):
    # R is input
    # C is input
    
    f = np.logspace(1,5)  # from 10e1 to 10e5 frequencies check if you want to get a variable range according to you
    
    
    Gain = 20*np.log(abs(low_pass_tf(2*np.pi*f,R,C)))
    phase = np.angle(low_pass_tf(2*np.pi*f,R,C))   
    # Commented code for Vout corresponding to Vin which maybe used if want to find the value 
    # Vout = Vin*(low_pass_tf(2*np.pi*f,R,C))
    return f,Gain,phase

def high_pass_filter(R,C):
    # R is input
    # C is input
    
    f = np.logspace(1,5) # Check if the range required is correct or not
    
    Gain = 20*np.log(abs(high_pass_tf(2*np.pi*f,R,C)))
    
    phase = np.angle(high_pass_tf(2*np.pi*f,R,C))
    
    # Commented code for Vout corresponding to Vin which maybe used if want to find the value 
    # Vout = Vin*(high_pass_tf(2*np.pi*f,R,C))
    
    return f,Gain,phase
