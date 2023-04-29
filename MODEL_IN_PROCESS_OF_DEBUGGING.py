#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 13:55:04 2023

@author: rosario
visuals
"""

import random as rnd
import math 
import numpy as np
import tkinter as tk #for visual 
from numpy import random

sp_1 = rnd.choices(["A", "T", "C", "G"], k= 100) 
sp_2 = rnd.choices(["A", "T", "C", "G"], k= 100) 
sp_3 = rnd.choices(["A", "T", "C", "G"], k= 100) 
#sp_4 = rnd.choices(["A", "T", "C", "G"], k= 100) 

ncol = 500
nrow = 500
size = 1/4
shape = 0 

main = ncol//2
 
def simple_landscape(nrow,ncol,size,shape):    
    
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


#### DEBUG 29-APR. OK. FUNCION SIMPLE_LANDSCAPE FUNCTIONS OK. 

class Plant():        
    def __init__(self,x,y, genome, comp_ab, disp_cap, drawing): #FOR VISIUAL OUTPUT. MODIFICATION.
        self.x = x
        self.y = y
        self.pos = [self.x, self.y]
        self.age = 0
        self.genome = genome
        self.disp_cap = disp_cap
        self.comp_ab = comp_ab
        self.state = "alive"
        self.drawing = drawing #FOR VISIUAL OUTPUT. MODIFICATION.
        
    def get_older(self): 
        self.age += 1

#### DEBUG 29-APR. OK. CLASS PLANT AND FUNCTION GET_OLDER OK. 

#29- APR additioin of block to create visual output 

class Visual:
    '''This class arranges the visual output.'''
    def __init__(self, ncol, nrow, mainland_island, main): # modif: original def __init__(self, max_x, max_y):
        '''Initialize the visual class'''
        self.zoom = 15
        self.max_x = ncol #max_x
        self.max_y = nrow #max_y
        self.top = tk.Tk()
        self.top.geometry("500x500") #????? 29 ABRIL I DONT KNOW HOW TO CHANGE THIS SO I CAN USE VARIABLES

        self.Landscape = tk.Canvas(self.top, bg="royalblue", height=nrow, width=ncol)

        self.coord = 0, 0, main, nrow #x1,y1, x2,y2, x1==y1 == 0 in mainland
        self.mainland = self.Landscape.create_rectangle(self.coord, fill="saddlebrown")

        #now we need to find the coordinates of the island in the landscape (matrix)
        self.mainland_island = simple_landscape(nrow, ncol, 1/4,0)
        
        self.coor_island = np.where(mainland_island==2) 
        self.coor_island = tuple(zip(*self.coor_island))
        
        self.coord2 = self.coor_island[0][1], self.coor_island[0][0],self.coor_island[-1][1], self.coor_island[-1][0]
        self.mainland = self.Landscape.create_rectangle(self.coord2, fill="saddlebrown")

        self.Landscape.pack()
        self.top.mainloop()
             
        
        # self.squares = np.empty((self.max_x, self.max_y),dtype=object)
        self.initialize_squares()
        
    def create_individual(self,x,y):       
        '''Create circle for individual'''
        radius = 0.1
        return self.canvas.create_oval((x - radius) * self.zoom,
                                       (y - radius) * self.zoom,
                                       (x + radius) * self.zoom,
                                       (y + radius) * self.zoom,
                                       outline='black', 
                                       fill='black')
    
    # I DONT THINK THE FOLLOWING IS NECESSARY BECAUSE MY SPECIE DOES NOT MOVE (PLANT)                                   
# =============================================================================
#     def move_drawing(self,drawing, x, y):
#         radius= 0.1
#         self.canvas.coords(drawing,(x - radius) * self.zoom,
#                                    (y - radius) * self.zoom,
#                                    (x + radius) * self.zoom,
#                                    (y + radius) * self.zoom)                                       
#         
# =============================================================================
#NOT NECESSARY, MY COMMUNITY DOES NOT INCLUDE RESOURSES 
# =============================================================================
#     def color_square(self, resources, x, y):
#         '''Changes the color of the square (according to resourses, so its not needed)'''        
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
# =============================================================================
# =============================================================================
#         
#     def initialize_squares(self):
#         '''returns a square (drawing object)'''
#         for x in range(self.max_x):
#             for y in range(self.max_y):
#                 self.squares[x, y] = self.canvas.create_rectangle(self.zoom * x,
#                                                      self.zoom * y, 
#                                                      self.zoom * x + self.zoom,
#                                                      self.zoom * y + self.zoom,
#                                                      outline = 'black', 
#                                                      fill = 'black')
# 
# 
# 
# 
# =============================================================================











