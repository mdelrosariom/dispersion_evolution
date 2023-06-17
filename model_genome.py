#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:17:54 2023

@author: rosario
"""

import random as rnd
import tkinter as tk
import numpy as np
import math as math
import statistics as s
from numpy import random
sp_1 = rnd.choices(["A", "T", "C", "G"], k= 100) 
sp_2 = rnd.choices(["A", "T", "C", "G"], k= 100) 
sp_3 = rnd.choices(["A", "T", "C", "G"], k= 100) 
sp_4 = rnd.choices(["A", "T", "C", "G"], k= 100) 
species = [sp_1, sp_2, sp_3, sp_4]

nrow = 20 
ncol = 20 
size = 1/4 
shape = 0 
main = ncol//2

def simple_landscape(nrow,ncol,size,shape):    
    main = ncol//2    
    landscape = np.zeros((nrow, ncol))
    landscape[:,0:main] = 1            
    dim = math.floor(ncol*size)   
    if shape == 0:                       
       posy = abs(rnd.randint(main+2, ncol-dim)) #position in y       
       posx = abs(rnd.randint(0,nrow-dim)) #position in x        
       landscape[posx:posx+dim, posy:posy+dim] = 2  
            
    else:             
        dimx = dim             
        dimy = dim//2            
        posy = abs(rnd.randint(main+2, ncol-dimy)) #position in y        
        posx = abs(rnd.randint(0,nrow-dimx))            
        landscape[posx:posx+dimx, posy:posy+dimy] = 2  
    return landscape
mainland_island = simple_landscape(nrow, ncol, size, shape) 


class Visual:
    '''This class arranges the visual output.'''
    def __init__(self, ncol, nrow):
        '''Initialize the visual class'''
        self.zoom = 15
        self.ncol = ncol
        self.nrow = nrow
        self.main = ncol//2
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, 
                                width =  self.ncol * self.zoom, 
                                height = self.nrow * self.zoom) #create window
        self.canvas.pack()
        self.canvas.config(background = 'royalblue')
        self.coord = 0, 0, main*self.zoom, nrow*self.zoom #x1,y1, x2,y2, x1==y1 == 0 in mainland
        self.mainland = self.canvas.create_rectangle(self.coord, fill="saddlebrown")
        is_coor = np.where(mainland_island==2) 
        is_coor = tuple(zip(*is_coor))       
        is_coor = is_coor[0][1]*self.zoom, is_coor[0][0]*self.zoom, is_coor[-1][1]*self.zoom, is_coor[-1][0]*self.zoom       
        self.island = self.canvas.create_rectangle(is_coor, fill ="saddlebrown" )     
        self.squares = np.empty((self.ncol, self.nrow),dtype=object)
        self.initialize_squares()
     
    def create_plant(self,x,y, id):       
        '''Create circle for individual'''
        if id == "specie_1":
            radius = 0.5
            return self.canvas.create_oval((x - radius) * self.zoom,
                                       (y - radius) * self.zoom,
                                       (x + radius) * self.zoom,
                                       (y + radius) * self.zoom,
                                       outline='black', 
                                       fill='forestgreen')
        if id == "specie_2":
            radius = 0.5
            return self.canvas.create_oval((x - radius) * self.zoom,
                                      (y - radius) * self.zoom,
                                      (x + radius) * self.zoom,
                                      (y + radius) * self.zoom,
                                      outline='black', 
                                      fill='blue')
        if id == "specie_3":
            radius = 0.5
            return self.canvas.create_oval((x - radius) * self.zoom,
                                     (y - radius) * self.zoom,
                                     (x + radius) * self.zoom,
                                     (y + radius) * self.zoom,
                                     outline='black', 
                                     fill='purple')
        if id == "specie_4":
            radius = 0.5
            return self.canvas.create_oval((x - radius) * self.zoom,
                                     (y - radius) * self.zoom,
                                     (x + radius) * self.zoom,
                                     (y + radius) * self.zoom,
                                     outline='black', 
                                     fill='pink')                               
    def initialize_squares(self):
        '''returns a square (drawing object)'''
        for x in range(self.ncol):
            for y in range(self.nrow):
                self.squares[x, y] = self.canvas.create_rectangle(self.zoom * x,
                                                      self.zoom * y, 
                                                      self.zoom * x + self.zoom,
                                                      self.zoom * y + self.zoom,
                                                      outline = 'black', 
                                                      fill = '')


### ok check 
class Plant:
    '''Class that regulates individuals and their properties'''
    def __init__(self,
                 x,
                 y,                
                 drawing, 
                 genome,
                 disp_cap, 
                 comp_ab,specie):
        '''Initialization'''
        self.x = x
        self.y = y
        self.pos = [self.x, self.y]       
        self.drawing = drawing 
        self.age = 0
        self.genome = genome
        self.specie = "specie_"+str(specie+1)
        self.disp_cap = disp_cap
        self.comp_ab = comp_ab
        self.state = "alive"        
        self.id = rnd.randint(1,2000)

    
class Metapopulation:
    '''Contains the whole population, regulates daily affairs'''
    def __init__(self, 
                 ncol, 
                 nrow):
        '''Initialization'''           
        self.main = ncol//2	
        self.ncol = ncol	
        self.nrow = nrow
        self.visual = Visual(self.ncol, self.nrow)       
        self.population = []
        self.initialize_pop()
        
    def initialize_pop(self):
        '''Initialize individuals'''
        startpop = 50
        
        for n in range(startpop):            
            x_ini = int(rnd.uniform(0,self.main))           
            y_ini = int(rnd.uniform(0,self.nrow))            
            spe = rnd.randint(0,3)
            genome_ini = species[spe]
            drawing = self.visual.create_plant(x_ini, y_ini, "specie_"+(str(spe+1))) ###! !!!           
            disp_cap_ini = rnd.randint(min(nrow,ncol)/4, min(nrow,ncol)/2) 
            comp_ab_ini = rnd.randint(0,10)
            plant = Plant( x_ini,
             y_ini,                
             drawing, 
             genome_ini,
             disp_cap_ini, 
             comp_ab_ini,spe)
            self.population.append(plant)
                                      

    def a_day_in_the_life(self):
        list_nei = []             
        oldpop = self.population[:]
        del self.population[:]      
         #I will delete every individual once I find the neighbours, so I will do another list
        for p in oldpop:
            print(mainland_island[p.y-1, p.x-1])

            if p.age < 2: 
                
                self.population.append(p)
            else: 
               # self.population.remove(p)
                self.visual.canvas.delete(p.drawing)

            #if p.x != 0 and p.y != 0: 
#                 
            if mainland_island[p.y-1, p.x-1] != 0.0:
#                    s
                self.population.append(p)
            else: 
                     #self.population.remove(p)
                self.visual.canvas.delete(p.drawing)
# =============================================================================
                    
        oldpop = self.population[:]          
        oldpop2 = oldpop[:]        
        for ind in range(len(oldpop2)):
            plant_obj = oldpop2[0]            
           
            plant_comp = [plant for plant in oldpop2 if plant != plant_obj]
            for PLANT in range(len(plant_comp)): 
                
                pos1 = plant_obj.pos
                plant_com = plant_comp[PLANT]
                pos2 = plant_com.pos                
                vx = pos1[0]
                vy = pos1[1]
                nx = pos2[0]
                ny = pos2[1]
                if vx == nx-1 and vy == ny-1 or vx == nx-1 and vy ==ny or vx == nx-1 and vy == ny+1 \
                or vx == nx and vy == ny-1 or vx == nx and vy == ny+1 or vx == nx +1 and vy == ny-1 \
                or vx == nx+1 and vy == ny   or vx == nx+1 and vy == ny+1 :
                   # print("nei")
                    #I think that for now its easier if we make them reproduce if the two 
                    #individuals are of the same specie, without compare the genome, after 
                    #we can change to compare the genome, the code is below and it should work
                    if plant_obj.specie == plant_com.specie: 
                        genome_org_1 = plant_obj.genome                             
                        genome_org_2 = plant_com.genome  
# ============================================================================= For reproduction comparing genome and no species
#                         match = 0
#                         for i in range(len(genome_org_1)): 
#                         if genome_org_1[i] == genome_org_2[i]:
#                             match = match +1                     
#                         if match/len(genome_org_1) >= 0.7 :
# =============================================================================
                        #NEW GENOME OF THE SON

                        chose = rnd.randint(0,1)
                        if chose ==1:
                            new_genome = genome_org_1[:50] + genome_org_2[51:]
                        else: 
                            new_genome = genome_org_2[:50] + genome_org_1[51:]
                            
                        chose2 = rnd.randint(0,2)
                        if chose2 == 0: 
                            new_comp_ab = plant_obj.comp_ab
                        elif chose2 == 1:
                            new_comp_ab =plant_com.comp_ab                        
                        else : 
                            new_comp_ab = s.mean([plant_obj.comp_ab, plant_com.comp_ab])    #codominance
                        ########## ############# ######
                        chose3 = rnd.randint(0,2)
                        if chose3== 0: 
                            new_disp_cap =  plant_obj.disp_cap 
                        elif chose3==1 : 
                            new_disp_cap = plant_com.disp_cap
                        else: 
                            new_disp_cap = s.mean([plant_obj.disp_cap, plant_com.disp_cap]) #codominance
                        ######
                        

                        x_pos_parent = rnd.choice([plant_obj.x, plant_com.x])    
                        y_pos_parent = rnd.choice([plant_obj.y, plant_com.y])
                            
                        dir_mov_x =rnd.randint(0,1)
                        dir_mov_y = rnd.randint(0,1)
                        if dir_mov_x == 0:
                            #inherits the same dispersive capacity with which it disperses
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

                        drawing = self.visual.create_plant(new_x, new_y, plant_obj.specie)
                        self.population.append(Plant(new_x,
                          new_y,                
                          drawing, 
                          new_genome,
                          new_disp_cap, 
                          new_comp_ab,int(plant_obj.specie[-1])))#it will be of the species of the parents
                        #the above line is kind of messy for the specie, but we need the number 
                        

                        
            oldpop2.remove(plant_obj)
        for plant in oldpop:
            plant.age +=1
            
#                     #neig_of_indiv.append(other)
#        
#                 #oldpop2.remove(ind)
# =============================================================================
            
          
        print(len(self.population))
        self.visual.canvas.update()
             
        
meta = Metapopulation(20,20)
for timer in range(3):
   # initialize_pop()
    meta.a_day_in_the_life()
tk.mainloop()
