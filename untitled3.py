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
nrow= 20 
ncol = 20 
size = 1/4 
shape = 0 
main = ncol//2
def simple_landscape(nrow,ncol,size,shape):    
    main = ncol//2    
    landscape = np.zeros((nrow, ncol))
    landscape[:,0:main] =1            
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
        self.coord = 0, 0, self.main*self.zoom, nrow*self.zoom #x1,y1, x2,y2, x1==y1 == 0 in mainland
        self.mainland = self.canvas.create_rectangle(self.coord, fill="saddlebrown")
        is_coor= np.where(mainland_island==2) 
        is_coor = tuple(zip(*is_coor))       
        is_coor = is_coor[0][1]*self.zoom, is_coor[0][0]*self.zoom,is_coor[-1][1]*self.zoom, is_coor[-1][0]*self.zoom
       
        self.island = self.canvas.create_rectangle(is_coor, fill ="saddlebrown" )     
        
        
    def create_individual(self,x,y):       
        '''Create circle for individual'''
        radius = 0.1
        return self.canvas.create_oval((x - radius) * self.zoom,
                                       (y - radius) * self.zoom,
                                       (x + radius) * self.zoom,
                                       (y + radius) * self.zoom,
                                       outline='black', 
                                       fill='forestgreen')
                                       

    def move_drawing(self,drawing, x, y):
        radius= 0.1
        self.canvas.coords(drawing,(x - radius) * self.zoom,
                                    (y - radius) * self.zoom,
                                    (x + radius) * self.zoom,
                                    (y + radius) * self.zoom)                                       
        


# =============================================================================
#     def color_square(self, resources, x, y):
#         '''Changes the color of the square'''        
#         color = (resources)/float(100)
#         if color < 0:
#             color = 0
#         elif color > 1:
#             color = 1  
#         green = int(255 * color)
#         red = 255 - green        
#         blue = 0
#         rgb = red, green, blue     
#         hex_code = '#%02x%02x%02x' % rgb        
#         self.canvas.itemconfigure(self.squares[x, y],fill=str(hex_code))
#         
# =============================================================================
# =============================================================================
#     def initialize_squares(self):
#         '''returns a square (drawing object)'''
#         for x in range(self.ncol):
#             for y in range(self.nrow):
#                 self.squares[x, y] = self.canvas.create_rectangle(self.zoom * x,
#                                                      self.zoom * y, 
#                                                      self.zoom * x + self.zoom,
#                                                      self.zoom * y + self.zoom,
#                                                      outline = 'black', 
#                                                      fill = 'black')
# 
# 
# =============================================================================
class Individual:
    '''Class that regulates individuals and their properties'''
    def __init__(self,
                 x,
                 y,
                 resources,
                 drawing, 
                 genome,
                 disp_cap, 
                 comp_ab):
        '''Initialization'''
        self.x = x
        self.y = y
        self.pos = [self.x, self.y]
        self.angle = rnd.uniform(0, 2 * math.pi)
        self.resources = resources
        self.drawing = drawing 
        self.age = 0
        self.reproductive_age = rnd.randint(10, 15)
        self.genome = genome
        self.disp_cap = disp_cap
        self.comp_ab = comp_ab
        self.state = "dead"
        

    def move(self, ncol, nrow):
        '''Calculates movement'''
        speed = 1
        diversion = math.pi / 3.0
        self.resources -= 1
        self.angle += rnd.uniform(-diversion,diversion)
        dx = speed * math.cos(self.angle)
        dy = speed * math.sin(self.angle)        
        self.x = int((self.x + dx) % ncol)
        self.y = int((self.y + dy) % nrow)
  
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
        initial_resources = 70
        self.environment = np.zeros((self.ncol,self.nrow)) + initial_resources
        self.population = []
        self.initialize_pop()
        
    def initialize_pop(self):
        '''Initialize individuals'''
        startpop = 100        
        start_resources = 10
        for n in range(startpop):
            
            x = int(rnd.uniform(0,self.main))
           # print("x", x)
            y = int(rnd.uniform(0,self.nrow))
            drawing = self.visual.create_individual(x, y)
            genome_ini = ["A", "T", "A"]
            disp_cap_ini = rnd.randint(min(nrow,ncol)/4, min(nrow,ncol)/2) 
            comp_ab_ini = rnd.randint(0,10)
            self.population.append(Individual(x, y, 
                                              start_resources,
                                              drawing, genome_ini, 
                                              disp_cap_ini, 
                                              comp_ab_ini))
                                      
    def a_day_in_the_life(self):
        '''Replenish patches and draw visual'''             
        rnd.shuffle(self.population)
        cost_of_offspring = 10           
        #shuffle population so that individuals in the beginning of the list
        #don't get an advantage        
        oldpop = self.population[:]
        del self.population[:]
        
        for indiv in oldpop:   
            print("posicion", indiv.x, indiv.y)
            if indiv.x != 0 and indiv.y != 0: 
                if mainland_island[indiv.x-1, indiv.y-1] == 0:  #All the individuals that fall into the sea end up dead.
                    indiv.state = "dead"    
            if indiv.state == "dead": 
                self.visual.canvas.delete(indiv.drawing)
                
            oldpop = [org_alive for org_alive in oldpop if org_alive.state != "dead"] 
                    
# =============================================================================
#             if plan.age >2:
#                 print("it is")
#                 plan.state = "dead" lets do it after
#             
# =============================================================================

            if indiv.age>=indiv.reproductive_age:
                n_offspring = int(indiv.resources) // cost_of_offspring
                for n in range(n_offspring):
                    drawing = self.visual.create_individual(indiv.x, indiv.y)
                    disp_cap = rnd.randint(min(nrow,ncol)/4, min(nrow,ncol)/2) 
                    comp_ab = rnd.randint(0,10)
                    self.population.append(Individual(indiv.x,
                                                      indiv.y,
                                                      cost_of_offspring,
                                                      drawing, 
                                                      ["A", "T", "A"],disp_cap, 
                                                      comp_ab
                                                      )) 
                #parents die after reproducing 
                self.visual.canvas.delete(indiv.drawing)
            else:
                if indiv.resources >= 0:
                    indiv.move(self.ncol, self.nrow)
                    self.visual.move_drawing(indiv.drawing, 
                                             indiv.x, 
                                             indiv.y)
                    if self.environment[int(indiv.x), int(indiv.y)]>0:
                        if self.environment[int(indiv.x), int(indiv.y)] > 5:
                            self.environment[int(indiv.x), int(indiv.y)] -= 5
                            indiv.resources += 5
                        else:
                            indiv.resources += self.environment[int(indiv.x), int(indiv.y)]
                            self.environment[int(indiv.x), int(indiv.y)] = 0
                    indiv.age += 1
                    self.population.append(indiv)
                else:
                    self.visual.canvas.delete(indiv.drawing)
            
# =============================================================================
#         for x in range(self.ncol):
#             for y in range(self.nrow):
#               #  self.visual.color_square(self.environment[x,y], x, y)   
# =============================================================================
        self.environment += .3 #replenish resources in patches
        np.clip(self.environment, 0, 100, out = self.environment)
        # amount of resources has to stay between 0 and 100
        print (len(self.population))
        self.visual.canvas.update()
        
        
meta = Metapopulation(20,20)
for timer in range(100):
    meta.a_day_in_the_life()
tk.mainloop()