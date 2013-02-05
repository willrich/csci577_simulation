# -*- coding: utf-8 -*-
"""
Created on Fri Feb 01 15:49:39 2013

@author: Nathan Sponberg, Kevin Joyce, Patrick Funk
"""

from scipy import *
from numpy import *
import pylab as pl
from IPython.core.debugger import Tracer
from matplotlib.pyplot import *
from matplotlib.mlab import find
debug_here = Tracer()

# Function performs eulers method on another passed to it
def euler(x, f, dt):
    return x+f(x,dt)*dt

# Function simulates falling object, x is a vector contain
# position and velocity data, outputs velocity and acceleration
# dt is the time step
def FallingBody(x,dt):
    return array([x[1], -9.8])

# Function simulates simple harmonic oscillation, x is a vector contain
# position and velocity data, outputs velocity and acceleration
# dt is the time step
def Oscillator(x,dt):
    k=1
    return array([x[1], -k*x[0]])

# Analytic solution for a falling body
def FallingAnalytic(t,y0):
  yprime0 = 0 # hack for now
  #  return array([-1./2. * 9.8 * t**2 + y0,-9.8*t+y'0])
  return -1./2. * 9.8 * t**2 + y0

# Analyitic solution for Oscillation

def OscilAnalytic(k, m, x0, dt, numPoints):
    result = []    
    for i in range(numPoints):
        result.append([x0*math.cos(math.sqrt(k/m)*(i*dt))])
    return result


def OneDMotionSim(f, startState, resolution, dt):
    states = startState
    for i in range(resolution):
        states.append(euler(states[-1], f, dt))
    return states

################# Begin Simulations ######################
# 1 Falling object 
#initial state for falling object
resolution = 1000
stateFalling = [array([10.0,0.0])]
(a,b) = (0.,2.)
t = linspace(a,b,resolution)
x_exact = FallingAnalytic(t,stateFalling[0][0])
numeric_states = OneDMotionSim(FallingBody,stateFalling,resolution-1,(b-a)/resolution)
numeric_solution = array(numeric_states)

figure(1)
clf()
# obtain only positive values
idx = find( x_exact >= 0 )
plot(t[idx],x_exact[idx])
#debug_here()
plot(t[idx],numeric_solution.T[0][idx])
legend(("Analytic Solution","Numeric Solution"))

#initial state for Oscillation
startOscil = [array([1.0,0.0])]

# 2 Simple Harmonic Motion
#runs simulation for oscillator, time interval is 40000*0.001 = 40 secs
oscilStates = OneDMotionSim(Oscillator, startOscil, 40000, 0.001)
num_oscil_solution = array(oscilStates)

figure(2)
#plots the oscillation with position and velocity
pl.plot(oscilStates)

#plots the analytic solution for the oscillation
#note: dt and numPoints should match dt and resolution
#from the simulation
pl.plot(OscilAnalytic(1,1,1,0.001,40000))

pl.show()

#####   Energy    ##########

# Total Energy for Falling object

E_fall_total = 9.8*10

# Total Energy for simulation

E_fall_simulation = 9.8*numeric_solution[:,0] + .5*numeric_solution[:,1]**2

# plot of result
figure(1)
pl.plot(E_fall_simulation)
axhline(y=98)

# Percent difference
E_fall_change = abs(E_fall_total-E_fall_simulation[-1])/(E_fall_total)

# Total Energy for spring

E_spring_total = 1./2.

# Total Energy for simulation

E_spring_simulation = 1./2.*array(num_oscil_solution[:,0])**2 + 1./2.*array(num_oscil_solution[:,1])

# plot of result
figure(2)
pl.plot(E_spring_simulation)
axhline(y=1/2)

# percent difference

E_spring_change = abs(E_spring_total-E_spring_simulation[-1])/(E_spring_total)
