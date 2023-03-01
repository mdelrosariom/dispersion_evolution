#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 00:24:47 2022

@author: rosario miranda

This function will create a landscape defined by a mainland with 1/4 of the total
size of the landscape and one island that is always separated from the mainland by sea.
The size of the island can be small, medium, or large. The shape of the island 
can be a square or a rectangle (x<y). 

arguments: 
nrow = number of rows (y size of the landscape).
ncol = number of columns (x size of the landscape).
size = size of the island: 1/8 of mainland, 1/4 of mainland ,1/8 of mainland....
shape = 0 (square), 1 (rectangle where x = 1/2 y)



"""

import random as rn
import math 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def simple_landscape(nrow,ncol,size,shape):
    
    #we create the sea (no land still)
    landscape = np.zeros((nrow, ncol))
    
    #we create the mainland (size fix)
    ##first the dimentions of the mainland
    main = ncol//4
    
    #we append it into the sea
    landscape[:,0:main] =1  
    
    #we create the dimentions of the island        
    
    dim = math.floor(ncol*size)   
        
    if shape == 0:                
       
       posy = rn.randint(main+2, ncol-dim) #position in y
        
       posx = rn.randint(0,nrow-dim) #position in x
    
        #now we append the island to the lanscape   
        
       landscape[posx:posx+dim, posy:posy+dim] = 2  
            
    else: 
            
        dimx = dim 
            
        dimy = dim//2
            
        posy = rn.randint(main+2, ncol-dimy) #position in y
        
        posx = rn.randint(0,nrow-dimx)
            
        landscape[posx:posx+dimx, posy:posy+dimy] = 2  
    
    
    
    return landscape
    
    
    
