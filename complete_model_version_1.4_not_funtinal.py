#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:55:04 2023

@author: rosario
THE UPDATED VERSION CONTAINS THE FOLLOWING MODIFICATIONS: 
1. Now I used the updated version of simple landscape (not the old one as in the previous version). 
2. main, for the size of the mainland, is defined as a global variable. 
3. simple_landscape now its a matrix with three values 0: sea, 1: mainland and 2 island (so its easy to indentify where is the individual)
4. I fixed the dispersal of individuals (wrong in old version) and now individuals can move backwars or forward
5. Now world is (supposedly) a torus or a round world (i.e. individuals that reach the limit of one side appear on the other side). 
6. I changed the initial definition of dispersal capacity. Now is more flexible and less strict
7. Now competitive ability and dispersal capacity are not linked and can be codominant (i.e. each trait can be obtained from a different parent or 
the descendant can inherit a propiety that is the mean of the parents. 
8. 


"""

import random as rnd
import math 
import numpy as np
from numpy import random
import statistics as s
sp_1 = rnd.choices(["A", "T", "C", "G"], k= 100) 
sp_2 = rnd.choices(["A", "T", "C", "G"], k= 100) 
sp_3 = rnd.choices(["A", "T", "C", "G"], k= 100) 
#sp_4 = rnd.choices(["A", "T", "C", "G"], k= 100) 

ncol = 40 
nrow = 40
size = 1/4
shape = 0 
#global function mainland (main)
#main = ncol//4
main = ncol//2
#LANDSCAPE 
def simple_landscape(nrow,ncol,size,shape):
    
    #we create the sea (no land still)
    landscape = np.zeros((nrow, ncol))
    landscape[:,0:main] =1  
    
    #we create the dimentions of the island        
    
    dim = math.floor(ncol*size)   
        
    if shape == 0:         
       print(" aaaaaaaaaaaaaaaaaaaaaaah", ncol,nrow,main+2, ncol-dim )
       
       #modification 9/4/23, all dimentions/positions being positive
       posy = abs(rnd.randint(main+2, ncol-dim)) #position in y
       
       posx = abs(rnd.randint(0,nrow-dim)) #position in x
    
        #now we append the island to the lanscape   
        
       landscape[posx:posx+dim, posy:posy+dim] = 2  
            
    else: 
            
        dimx = dim 
            
        dimy = dim//2
            
        posy = abs(rnd.randint(main+2, ncol-dimy)) #position in y
        
        posx = abs(rnd.randint(0,nrow-dimx))
            
        landscape[posx:posx+dimx, posy:posy+dimy] = 2  
    return landscape
mainland_island = simple_landscape(40, 40, 1/4, 0)    

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
        startpop = 100
        for n in range(startpop):
            #this is to get inizializated in mainland (not islands)
            #abs just in case because it must be positive 
            x_ini= abs(rnd.randint(0, main)) #needs to be between the limits of the world ncol  
            #initial because its not for the seeds
            y_ini= abs(rnd.randint(0, nrow)) #needs to be between the limits of the world nrow 
            #initial because is not for the seeds 
            disp_cap_ini = rnd.randint(min(nrow,ncol)/4, min(nrow,ncol)/2)  #change for gauss if necessary. this is lamnda that will be on the poisson distr
            comp_ab_ini =  rnd.randint(0,10)  #provisionary
            mainland_island = simple_landscape(nrow, ncol, 1/2, 0)
            spe_cho = 0#rnd.choice(range(0))
            if spe_cho == 0 :
                genome_ini = sp_1[:]
            #if spe_cho == 1:
             #   genome_ini = sp_2[:]
            #if spe_cho == 2: 
             #   genome_ini = sp_3[:]
            #if spe_cho == 3 :
             #   genome_ini = sp_4[:]
            for mutation in range(10):    
                genome_ini[rnd.randint(0,99)] = rnd.choice(["T","A", "C", "G"])
            
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
        for now it prints who is the mainland and who in island, but is pretty fleible and we can 
        get the genome and / or the dispersal ability of the organism
        '''             
        rnd.shuffle(self.population) #shuffle population so that individuals in the beginning of the list
        #don't get an advantage        
        oldpop = self.population[:]
       
        for plan in oldpop: 
             if plan.x != 0 and plan.y != 0: 
                 if mainland_island[plan.x-1, plan.y-1] == 0:  #All the individuals that fall into the sea end up dead.
                     plan.state = "dead"                 
             if plan.age >2:
                 print("it is")
                 plan.state = "dead"
            #of Plant, but it created problems. anual plants die after 1 year              
                
        oldpop = [org_alive for org_alive in oldpop if org_alive.state != "dead"] 
        offspring = [] #FOR MODIFICATION OF COMPETENCE SEE 236
        del self.population[:]
        list_nei = []
        for plant in oldpop: 
            plant.get_older()            
            plant_obj = plant.pos
            rest_plants = [pla for pla in oldpop if pla != plant]  
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
                        chose = rnd.randint(0,1)
                        if chose ==1:
                            new_genome = genome_org_1[:50] + genome_org_2[51:]
                        else: 
                            new_genome = genome_org_2[:50] + genome_org_1[51:]
                        chose2 = rnd.randint(0,2)
                        if chose2 == 0: 
                            new_comp_ab = plant.comp_ab
                        elif chose2 == 1:
                            new_comp_ab = other.comp_ab                        
                        else : 
                            new_comp_ab = s.mean([plant.comp_ab, other.comp_ab]) #codominance
                        chose3 = rnd.randint(0,2)
                        if chose3== 0: 
                            new_disp_cap =  plant.disp_cap 
                        elif chose3==1 : 
                            new_disp_cap = other.disp_cap
                        else: 
                            new_disp_cap = s.mean([plant.disp_cap, other.disp_cap]) #codominance
                                                   
                        x_pos_parent = rnd.choice([plant.x, other.x])    
                        y_pos_parent = rnd.choice([plant.y, other.y])
                            
                        dir_mov_x =rnd.randint(0,1)
                        dir_mov_y = rnd.randint(0,1)
                        if dir_mov_x == 0:
                            new_x =  x_pos_parent + int(random.poisson(new_disp_cap,1))
                        else: 
                            new_x =  x_pos_parent - int(random.poisson(new_disp_cap,1))
                        if dir_mov_y ==0: 
                            new_y =  y_pos_parent + int(random.poisson(new_disp_cap,1))
                        else: 
                            new_y =  y_pos_parent - int(random.poisson(new_disp_cap,1))
                       #round world     
                        if new_x> ncol: 
                            new_x = new_x - ncol #fixed 09/04
                        if new_y > nrow: 
                            new_y = new_y - nrow #fixed
                            
                        #modif 09/4
                        if new_x<0: #negative, out of the limits of the word with x = range(0,ncol)
                            new_x = ncol-(abs(new_x))
                        if new_y <0: 
                            new_y = nrow-(abs(new_y))
                            
                        plant = Plant(new_x, new_y, new_genome,new_comp_ab, new_disp_cap)
                        if not any(plant.pos in sublist for sublist in offspring): 
                            offspring.append([plant.pos, plant])                           
                        else: 
                            comp_ab_new = plant.comp_ab #COMPETITIVE ABILITY OF THE NEW PLANT (THAT JUST ARRIVED AT THE POSITION)                                
                            for i in offspring :
                                    if plant.pos in i:                                         
                                        comp_ab_ori = i[1].comp_ab                                                   
                                        if comp_ab_ori > comp_ab_new: 
                                            pass 
                                        if comp_ab_ori < comp_ab_new: 
                                             offspring[offspring.index(i)] = [plant.pos, plant]
                                        if comp_ab_ori == comp_ab_new: 
                                            j = [plant.pos,plant]
                                            winner = rnd.choice([i,j])                                             
                                            offspring[offspring.index(i)] = winner
                              
        offspring = [x[1] for x in offspring] #WE CLEAN OFFSPRING NOW IT IS JUST A LIST OF PLANTS (NOT POSITIONS)
        self.population.append(offspring) #AND NOW WE APPEND ALL THE NEW OFFSPRING TO THE POPULATION
        self.population = [item for sublist in self.population for item in sublist]
               
                       
        print(len(oldpop)) 
        return oldpop

meta = Metapopulation(40,40)             
            
for timer in range(3):
   a = meta.a_day_in_the_life()
   print(a)
    
   
