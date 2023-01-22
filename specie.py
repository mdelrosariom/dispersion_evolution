#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 18:24:17 2023

@author: rosario
"""
'''
This function creates an individual plant.
x,y are the positions of the individual, the position should (maybe) be: 0<x<cols, and 0<y<nrows. 
The individual does not move but only occupies that position for one time step (if the time step is 1 year).
because it's an annual plant.
The genome is composed of a single string (vector) of length 100 nucleotides (A, T, C, G).
the idea for reproduction (not done yet): Each individual checks if there is another individual in the 
neighbouring cells. If there is an individual, then the genome is checked to see if the percentage of the same nucleotides 
in the same position is 70% or more, then the individuals produce seeds (or one seed). 
Idea for dispersal (not done yet): each plant has "disp_cap" i.e., dispersal capacity; disp_cap = lambda of Poisson
distribution. When parents produce a seed, the seed will be positioned in a coordenate (x,y) where x and y 
are values taken from the Poisson distribution with the lambda of the parents. 
each individual has a comp_ab i.e. competitive ability (just a number between 0 and 10). Since only can be one 
individual per cell (per x,y coordinate in the world), if an individual is dispersed to an occupied cell or 
Two individuals are initially in the same cell, then the individual with the biggest competitive ability 
can stay there, and the other dies. 
If an individual is dispersed or initialised in the sea (cell with a zero value), then it dies.

'''
import random 
import numpy as np
#we will need to define ncol, nrow as global variables

class Plant:
    
    def __init__(self,
                 x, # position in x of world SO X, Y CANT BE BIGGER THAN THE LIMITS OF THE WORLD
                 #ncol,nrow, respectively
                 y, #position in y of the world 
                 genome, 
                 disp_cap #dispersal capacity will be lambda in the poisson distrb.  
                 comp_ab): #competentitive ability
        
        self.x = x #needs to be between the limits of the world ncol  
        self.y = y  #needs to be between the limits of the world nrow 
        self.age = 0
        #the length of the genome is 100 and is conformed by nucleotides
        #for now its haploid. can be easily a diploid (;)
        self.genome = random.choices(["A", "T", "C", "G"], k= 100) #needs to be k= something. random choice for repetitions
        #this will be one (annual plants) 
        #self.reproductive_age = rnd.randint(10, 15)
        self.disp_cap = int((min(nrow,ncol)/4))#int(np.random.poisson(lambda, 1)) #first term is lambda of poisson... we can 
        #change for gauss (or other)
        #biologically it makes sense that the plant move 1/4 of the size of the world (can be changed)
        self.comp_ab = random.randint(0,10) #
        
        
    
