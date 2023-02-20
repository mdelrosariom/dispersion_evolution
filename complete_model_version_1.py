#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:55:04 2023

@author: rosario
"""

import random as rnd
import math 
import numpy as np
from numpy import random


ncol = 20 
nrow = 20

#LANDSCAPE 
def simple_landscape(nrow,ncol,size,shape):    
    '''
    Create a landscape = matrix of 0,1,2. 0 = sea, 1 = mainland (always in the left side) and always 
    1//4 of the total. 2 = island (this can have advantages after). The integers can be changed by gradients
    and be related to resourses for example. Only ONE ISLAND is formed by the moment. 
    One can modify the shape and size of the island. 
    Size: 0 = small, 1 = medium, 2 (or other) = big.
    shape = 0  square
    shape = other rectangle perpendicular to the mainland
    '''    
    #we create the sea (no land still)
    landscape = np.zeros((nrow, ncol))
    
    #we create the mainland (size fix)
    ##first the dimentions of the mainland
    main = ncol//4    
    #we append it into the sea
    landscape[:,0:main] =1      
    #we create the dimentions of the island    
    if size == 0: #small         
        dim = math.floor(ncol*1/8)           
        if shape == 0:                     
            posy = rnd.randint(main+2, ncol-dim) #position in y        
            posx = rnd.randint(0,nrow-dim) #position in x    
        #now we append the island to the lanscape   
            ##landscape[posx:posx+dim, posy:posy+dim] = 1 #20/feb modification, change island for 2 
            ## to identify which organisms are in the island 
            landscape[posx:posx+dim, posy:posy+dim] = 2  
            
        else: 
            
            dimx = dim             
            dimy = dim//2            
            posy = rnd.randint(main+2, ncol-dimy) #position in y        
            posx = rnd.randint(0,nrow-dimx)            
            landscape[posx:posx+dimx, posy:posy+dimy] = 1  
    
    elif size == 1: #medium     
        dim = math.floor(ncol*1/4)            
        if shape == 0:        
            posy = rnd.randint(main+2, ncol-dim) #position in y        
            posx = rnd.randint(0,nrow-dim) #position in x    
        #now we append the island to the lanscape    
            landscape[posx:posx+dim, posy:posy+dim] = 1 
        
        else:             
            dimx = dim             
            dimy = dim//2            
            posy = rnd.randint(main+2, ncol-dimy) #position in y        
            posx = rnd.randint(0,nrow-dimx)            
            landscape[posx:posx+dimx, posy:posy+dimy] = 1        
     
    else: #large 
        dim = math.floor(ncol*1/2)            
        if shape == 0:     
            posy = rnd.randint(main+2, ncol-dim) #position in y        
            posx = rnd.randint(0,nrow-dim) #positi    
        #now we append the island to the lanscape        
            landscape[posx:posx+dim, posy:posy+dim] = 1 
            
        else:             
            dimx = dim             
            dimy = (dim//2)            
            posy = rnd.randint(main+2, ncol-dimy) #position in y        
            posx = rnd.randint(0,nrow-dimx)            
            landscape[posx:posx+dimx, posy:posy+dimy] = 1  
     
    return landscape
mainland_island = simple_landscape(20, 20, 2, 0)    

#################################### SPECIE PLANT 

class Plant():
    ''' 
    Definition of our specie= plant. It has coordinates that can be separated (x,y) or together on a list
    age (just annual plants so it can be 0 and 1 and after it dies). genome, combination of 100 nucleotides 
    (A,T,C,G), competitive ability (comp_ab) and dispersal capacity (disp_cap) that is the lambda of 
    a poisson distribtion. 
    '''
    
    def __init__(self,x,y, genome, comp_ab, disp_cap ): #competentitive ability
        self.x = x
        self.y = y
       ###### if mainland_island[self.x-1, self.y-1] == 1:   #-1 because if self.x/self.y == max(colnum)/max(rownum) = problems
        self.pos = [self.x, self.y]
        self.age = 0
            #for now its haploid. can be easily a diploid (;)
        self.genome = genome
        self.disp_cap = disp_cap
        self.comp_ab = comp_ab
        self.state = "alive"
    def get_older(self): 
        self.age += 1
        #else:
            
         #   self.state = "dead" #it falls in sea then just dead but i think is not necessary
          #  self.pos = [self.x, self.y]
            
################################### METAPOPULATION, INIZIALIZE POPULATION, DAY IN THE LIFE

class Metapopulation:
    '''Contains the whole population, regulates daily affairs'''
    def __init__(self, 
                 ncol, 
                 nrow):
        '''
        Initialization defined by the limits of the landscape 
        '''           
        self.max_x = ncol
        self.max_y = nrow
        self.population = []
        self.initialize_pop()
        
    def initialize_pop(self):
        '''
        Initialize individuals. We want to inizialize individuals in the mainland, not in islands.
        For the way in which the mainland_island landscape is defined, we can define that the plants 
        are inizialized in the mianland that is 1/4 of the max number of columns from left to right
        '''
        startpop = 300
        for n in range(startpop):
            #this is to get inizializated in mainland (not islands)
            x_ini= rnd.randint(0, ncol//4) #needs to be between the limits of the world ncol  
            #initial because its not for the seeds
            y_ini= rnd.randint(0, nrow) #needs to be between the limits of the world nrow 
            #initial because is not for the seeds 
            genome_ini = rnd.choices(["A", "T", "C", "G"], k= 100)  #the length of the genome is 100 and is conformed by nucleotides
            disp_cap_ini = int(random.poisson(int((min(nrow,ncol)/4)), 1))  #change for gauss if necessary 
            comp_ab_ini =  [rnd.randint(0,10)]  #provisionary
            mainland_island = simple_landscape(nrow, ncol, 2, 0)
            self.population.append(Plant(x_ini, y_ini, genome_ini, comp_ab_ini, disp_cap_ini))
            
    def a_day_in_the_life(self):
        '''
        Here we can define which plant is dead and which not. So we change the state of the 
        plant to dead and then expulse from the population (delete). Any plant is consider dead 
        when is older than 1 or it falls in the sea. 
        For each plant, we check neighbours in a circle concentrical with the organism. if there is another
        plant, then we check the genome, if the genome coincide >= than 70% there is reproduction and 
        the genome of the descendant is 50% of each parent (from which parent is which half is random). 
        each descendant also inherits the competitive ability and the dispersal capacity of each parent 
        (randomly, but can be even more random). 
        Two plants cant be in the same coordinates at the same time, if there are 2 plants in the same 
        coordinates then we check the competitive ability and the one who has the biggest competitive ability 
        conserve the place and the other is removed. If they have the same ability the one who is removed is 
        chosed randomly
        for now it prints who is the mainland and who in island, but is pretty flexible and we can 
        get the genome and / or the dispersal ability of the organism
        '''             
        rnd.shuffle(self.population) #shuffle population so that individuals in the beginning of the list
        #don't get an advantage        
        oldpop = self.population[:]
        
        for plan in oldpop: 
            if mainland_island[plan.x-1, plan.y-1] == 0 or  plan.age >1: #All the individuals that fall into the sea end up dead. this was before in the definition
            #of Plant, but it created problems. anual plants die after 1 year
                
                plan.state = "dead"
                
        oldpop = [org_alive for org_alive in oldpop if org_alive.state != "dead"] 
        # we just need the list of all all individuals that are alive         
        
        del self.population[:]
        list_nei = []
        for plant in oldpop: 
            plant.get_older()
            plant_obj = plant.pos
            rest_plants = [pla for pla in oldpop if pla != plant] 
            
            for p in rest_plants:
                plant_comp = p.pos                
                if plant_comp == plant_obj: 
                    comp_ab_1 = p.comp_ab
                   
                    comp_ab_2 = plant.comp_ab 
                    if comp_ab_1 > comp_ab_2 :
                        
                        if plant in oldpop:
                            oldpop.remove(plant)
                        
                    elif comp_ab_1 < comp_ab_2:
                        oldpop.remove(p)
                    else: 
                        if p and plant in oldpop:
                            a = rnd.choice([p,plant]) 
                            oldpop.remove(a)
                       
                        else: 
                            pass
                                          
            for other in rest_plants:                 
                plant_comp = other.pos                
                pair = [plant_obj, plant_comp]
                done = (list_nei.count([plant_obj,plant_comp]) + list_nei.count([plant_comp,plant_obj]))
                vx = plant_obj[0]
                vy = plant_obj[1]
                nx = plant_comp[0]
                ny = plant_comp[1]
                
                if done==0:   
                    list_nei.append(pair)
                    if vx == nx-1 and vy == ny-1 or vx == nx-1 and vy ==ny or vx == nx-1 and vy == ny+1 \
                    or vx == nx and vy == ny-1 or vx == nx and vy == ny+1 or vx == nx +1 and vy == ny-1 \
                    or vx == nx+1 and vy == ny   or vx == nx+1 and vy == ny+1 :
                        genome_org_1 = plant.genome                             
                        genome_org_2 = other.genome  
                        match = 0
                        for i in range(len(genome_org_1)): 
                            if genome_org_1[i] == genome_org_2[i]:
                                    
                                match = match +1 
                        if match/len(genome_org_1) >= 0.7 :
                           # print("REPRODUCTION")
                            chose = rnd.randint(0,1)
                            if chose ==1:
                                new_genome = genome_org_1[:50] + genome_org_2[51:]
                                new_comp_ab = plant.comp_ab
                                new_disp_cap =  plant.disp_cap                                
                            else: 
                                new_genome = genome_org_2[:50] + genome_org_1[51:]
                                new_comp_ab = other.comp_ab
                                new_disp_cap = other.disp_cap
                                
                            new_x = int(random.poisson(new_disp_cap,1))
                            new_y = int(random.poisson(new_disp_cap,1))
                            self.population.append(Plant(new_x,
                                                              new_y,
                                                              new_genome,
                                                              new_comp_ab, new_disp_cap))
        
        for plant_final in oldpop: 
            if mainland_island[plant_final.x-1, plant_final.y-1] == 1 : 
                print("plant in mainland")
            elif mainland_island[plant_final.x-1, plant_final.y-1] == 2 : 
                print("plant in island")
                                  
               
meta = Metapopulation(40,40)             
            
for timer in range(4000):
    meta.a_day_in_the_life()