# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:15:58 2023

@author: mdrmi
for now creates a mainland island landscape, individuals of the same species only with 
position as an atribute. the indivuals die if the fall into the sea. the individuals die after 
2 years. the individuals have a change of 50% of having offspring. the simulation can be seen in
a graphical window. 
new: 
1. control number of time steps (apart from the duration). 
2. offspring now can be created anywhere (before error, only in mainland).
3. offspring creating if neighbours in one of the 8 adjacent squares of girds. 
4. now just one plant per square, the one standing is chosed randomly (still not competitive ability, nor any other attribute)

5. plants inizialize with red color
6. plants only do offspring after they turn 1 year. 
"""
import random as rnd
import tkinter as tk
import numpy as np
import math as math

nrow = 20
ncol = 20
size = 1/4
main = ncol // 2
shape = 0

current_time_step = 0

# time steps of the simulation
max_time_steps = 10  # 


def simple_landscape(nrow, ncol, size, shape):
    landscape = np.zeros((nrow, ncol))
    landscape[:, 0:main] = 1
    if shape == 0: #island is a square 
        dim = math.floor(ncol * size)
        posx = rnd.randint(0, nrow - dim)
        posy = rnd.randint(main + 2, ncol - dim)
        landscape[posx:posx+dim, posy:posy+dim] = 2
    else: #island is a rectangle #24-9 im not sure this part works because i didnt try it. 
        dimx = dim             	
        dimy = dim//2            	
        posx = abs(rnd.randint(main+2, ncol-dimy)) #position in y        	
        posy = abs(rnd.randint(0,nrow-dimx))            	
        landscape[posx:posx+dimx, posy:posy+dimy] = 2 
    return landscape

mainland_island = simple_landscape(nrow, ncol, size, shape)

class Visual:
    def __init__(self, max_x, max_y):
        self.zoom = 15
        self.max_x = max_x
        self.max_y = max_y
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=max_x * self.zoom, height=max_y * self.zoom)
        self.canvas.pack()
        self.canvas.config(background='royalblue')
        self.squares = np.empty((self.max_x, self.max_y), dtype=object)
        self.initialize_squares()

    def initialize_squares(self):
        '''
        create the land (island and mainland as brown) and the squares that represent each coordinate

        '''
        for x in range(self.max_x):
            for y in range(self.max_y):
                fill_color = 'saddlebrown' if mainland_island[y, x] != 0 else ''
                self.squares[x, y] = self.canvas.create_rectangle(
                    x * self.zoom, y * self.zoom, (x + 1) * self.zoom, (y + 1) * self.zoom,
                    outline='black', fill=fill_color )

class Plant:
    def __init__(self, x, y, drawing):
        self.x = x
        self.y = y
        self.drawing = drawing
        self.age = 0
        self.pos = [x,y]

def create_plant(x, y,initial_color='forestgreen'):
    '''
    the plant is created on the windowa in a different function
    '''
    radius = 0.5
    return canvas.create_oval(
        (x - radius) * visual.zoom, (y - radius) * visual.zoom,
        (x + radius) * visual.zoom, (y + radius) * visual.zoom,
        outline='black', 
        fill = initial_color
        #fill='forestgreen'
    )

def move_plant(indiv):
    dx = rnd.uniform(-0.5, 0.5)
    dy = rnd.uniform(-0.5, 0.5)
    x_new = (indiv.x + dx) % nrow
    y_new = (indiv.y + dy) % ncol

    if mainland_island[int(y_new), int(x_new)] != 0:
        canvas.coords(indiv.drawing, (x_new - 0.5) * visual.zoom, (y_new - 0.5) * visual.zoom,
                      (x_new + 0.5) * visual.zoom, (y_new + 0.5) * visual.zoom)
        indiv.x = x_new
        indiv.y = y_new

    else:
         canvas.delete(indiv.drawing)
         population.remove(indiv)


visual = Visual(ncol, nrow)
canvas = visual.canvas
population = []

# Create individuals only on the mainland
for _ in range(100):
    x = int(rnd.uniform(0, main)) #discrete mov
    y = int(rnd.uniform(0, nrow)) #discrete mov
    drawing = create_plant(x, y,initial_color='red')
    plant = Plant(x, y, drawing)
    
    population.append(plant)

def update():
    global current_time_step
    global population  # Declare population as a global variable
    neighbors = population[:]
    plants_to_remove = []
    
        #offspring 
    pop_nei = population[:] #we made this list to find neighbors of plants

# =============================================================================
    for x in range(len(population)): 
        
# =============================================================================
        plant_obj = population[x]
        if plant_obj.age > 1:  
            wo_pl_ob = [x for x in pop_nei if x != plant_obj]
            for plant_com in wo_pl_ob:
                    
                pos1 = plant_obj.pos
                   
                pos2 = plant_com.pos
                
                vx = pos1[0]
                vy = pos1[1]
                nx = pos2[0]
                ny = pos2[1]
                if vx == nx-1 and vy == ny-1 or vx == nx-1 and vy ==ny or vx == nx-1 and vy == ny+1 \
                or vx == nx and vy == ny-1 or vx == nx and vy == ny+1 or vx == nx +1 and vy == ny-1 \
                or vx == nx+1 and vy == ny   or vx == nx+1 and vy == ny+1 :
                    
                    x_off = int(rnd.uniform(0, ncol))
                    y_off = int(rnd.uniform(0, nrow))
                    
                    if mainland_island[int(y_off), int(x_off)] != 0:
                    
                        drawing_off = create_plant(x_off, y_off)
                        offspring = Plant(x_off, y_off, drawing_off)
                        population.append(offspring)         
                
            pop_nei.remove(plant_obj)  
            
        #plants die after 1 years
    for plant in population:
        if plant.age >= 3:
            canvas.delete(plant.drawing)
            plants_to_remove.append(plant)        

    
    
    
    for plant_1 in population: 
        same_place =[]
        same_place.append(plant_1)
        rest = [x for x in population if x != plant_1]
        for plant_2 in rest: 
            if plant_1.pos == plant_2.pos:
                same_place.append(plant_2)
        winner= rnd.choice(same_place)
        losers = [x for x in same_place if x !=winner]
        for los in losers: 
            plants_to_remove.append(los)            
        
        
        
            
    population = [plant for plant in population if plant not in plants_to_remove]

    for plant in plants_to_remove:
        canvas.delete(plant.drawing)

    for plant in population:
        move_plant(plant)
        plant.age += 1
        print(plant.age)  

    print(len(population))
    current_time_step += 1
    if current_time_step < max_time_steps:
        # Schedule the next update with an interval
        visual.root.after(200, update)
    else:
        # Stop the simulation when we reach the maximum time steps
        print("Simulation finished.")

    
    

update()
visual.root.mainloop()