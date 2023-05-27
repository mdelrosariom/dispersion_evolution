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
        startpop = 10
        
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
        oldpop2 = oldpop[:] #I will delete every individual once I find the neighbours, so I will do another list
        for indiv in oldpop:   
            if indiv.age < 2 and mainland_island[indiv.y, indiv.x] != 0: 
                self.population.append(indiv)
                
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
                    print("nei")
                
            oldpop2.remove(plant_obj)
                
#                     #neig_of_indiv.append(other)
#        
#                 #oldpop2.remove(ind)
# =============================================================================
            
          
        print(len(self.population))
        self.visual.canvas.update()
             
        
meta = Metapopulation(20,20)
for timer in range(2):
   # initialize_pop()
    meta.a_day_in_the_life()
tk.mainloop()