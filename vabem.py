# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:15:58 2023

@author: mdrmi
for now creates a mainland island landscape, individuals of the same species only with 
position as an atribute. the indivuals die if the fall into the sea. the individuals die after 
2 years. the individuals have a change of 50% of having offspring. the simulation can be seen in
a graphical window. 

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

def create_plant(x, y):
    '''
    the plant is created on the windowa in a different function
    '''
    radius = 0.5
    return canvas.create_oval(
        (x - radius) * visual.zoom, (y - radius) * visual.zoom,
        (x + radius) * visual.zoom, (y + radius) * visual.zoom,
        outline='black', fill='forestgreen'
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
    drawing = create_plant(x, y)
    plant = Plant(x, y, drawing)
    
    population.append(plant)

def update():
    global population  # Declare population as a global variable

    plants_to_remove = []
    for plant in population:
        move_plant(plant)
        plant.age += 1
        #offspring 
        posibilitie_off = rnd.randint(0,1)
        if posibilitie_off ==1: 
            x_off = rnd.uniform(0, main)
            y_off = rnd.uniform(0, nrow)
            drawing_off = create_plant(x_off, y_off)
            offspring = Plant(x_off, y_off, drawing_off)
            population.append(offspring)
        
        #plants die after 2 years
        
        if plant.age >= 2:
            canvas.delete(plant.drawing)
            plants_to_remove.append(plant)
        

        
        
            
    population = [plant for plant in population if plant not in plants_to_remove]

    for plant in plants_to_remove:
        canvas.delete(plant.drawing)

    visual.root.after(200, update) #time steps 

    print(len(population))

    
    

update()
visual.root.mainloop()
