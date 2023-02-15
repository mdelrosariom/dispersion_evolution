#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:09:41 2023

@author: rosario
"""
'''
this program produce the specie "Plant" with all the characteristics, now they are all together under 
the characteristic information (easy accessible list of lists -each list is a characteristic). Furthermore, 
this program only accept the stablishment of organisms if the initially "fall" under the land of the landscape
(coordenates x,y == 1 land). If the organism fall into land is considered "alive" (state.alive), and if it falls
into sea (mainland coordenates x,y= 0) it is considered  dead (state = dead).

'''


ncols = 20
nrows = 20

import random as rnd
class Plant():
    
    def __init__(self): #competentitive ability
        
        self.x = rnd.randint(0, ncols) #needs to be between the limits of the world ncol  
        self.y = rnd.randint(0, nrows) #needs to be between the limits of the world nrow 
        
        if mainland_island[self.x, self.y] == 1:   
            self.pos = [self.x, self.y]
            self.age = 0
            #the length of the genome is 100 and is conformed by nucleotides
            #for now its haploid. can be easily a diploid (;)
            self.genome = rnd.choices(["A", "T", "C", "G"], k= 100) #needs to be k= something. random choice for repetitions
            
            #this will be one (annual plants) 
            #self.reproductive_age = rnd.randint(10, 15)
            self.disp_cap = [int((min(nrows,ncols)/4))]#int(np.random.poisson(lambda, 1)) #first term is lambda of poisson... we can 
            #change for gauss (or other
            #biologically it makes sense that the plant move 1/4 of the size of the world (can be changed)
            self.comp_ab = [rnd.randint(0,10)] 
            self.information = [self.pos, self.age, self.genome, self.disp_cap, self.comp_ab]
            self.state = "alive"
        else: 
            self.state = "dead"