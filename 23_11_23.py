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
4. now just one plant per square, the one standing is chosed randomly (still not competitive ability, nor any other attribute). competence is added see 13 and 14

5. plants inizialize with red color
6. plants only do offspring after they turn 1 year. 

7. plants dont move anymore
8. plants have a dispersal capacity (given by normal distribution) and they produce offspring which new position is determined 
by this dispersal ability (see dispersal function and update function). at the same time, the offspring inherates this 
capacity of one of the parents (no codominance for the moment) 

9. different species (at the moment only two) with different genomes (for the moment it can reproduce independently of this)
10. different species have different color. 

11. individuals now reproduce if they belong to the same species

12. parents can produce more than 1 seed, line 208 onwards.

13. plants have as an atribute competitive ability, line 114. 
REDEFINED IN THIS CODE TO BE BETWEEN 0 AND 1 (DECIMAL)
14. plant win place accordingly to competitive ability, plant that stay in place is the 
one how has more competitive ability, others get deleted from population. 243-258
REDEFINED IN THIS VERSION. plant assigned a probability (a value between 0 and 1)
loop that last until a winner is found. iteration over the plants that are on the same position
checking for each if their comp ab (prob) is bigger than a value that gets renew in each 
iteration 

15. some chunks made functions

16. 12-11-23 there is another matrix "environmental niche" that describes the niche of the environment
the complete niche is just a list of numbers between 1 and 12. the complete niche is associated with
the mainland (in the mainland there are all the niches), then in the island, there is a subset of 
the niches of the mainland, a list of 4 numbers in ascending order that are taked randomply from
the entire niche of the mainland. the species will have an atribute of the niche of a list of 3.
17. now each species has a characteristic niche a list between 1-10 with a len of 3. 
imp note: for now, the niche of the different species can overlap (i can solve this if necessary)

18. 19/11/23. now there is an adaptation process in which the niche of the individual shift 
to be similar to the niche of the environment. it changes one step at the time. occurs 
if the current_time_step is multiple of the time_of adaptation. Ej. each 5 time steps 
if the time_of_adaptation in 5, etc., in this way, we can modify the timing of adatation
and its easy to make it dependent of the type of specie. thought the niche of the species 
change over time to be each and each time more similar to the environmental niche, this 
not gives a competitive adventage (it will come soon). 

other details: 
    adaptation in condition if mainland_island[plant.x][plant.y] == 2: but change
    if other islands have other number (not 2)
CORRECTION OF 18. adaptation occur in the offspring, not in the plants, in all the offspring. 

19. 21/11/23 individuals get eliminated on islands if their niche does not overlap (at least in one element)
i.e. if the individual is not adapted to the island, then it can't stay there. This condition applies 
only to islands (not mainland), but mathematically there is not a problem with that. 

20. 23/11/23 if there is multiple individuals in island, then the selection for which one 
stays depends on how well are adapted to the environment, i.e. if the can use more resourses 
of the environment or not (i.e. environmental niche of island [1234] and options ind1 niche [012], ind2 [123], ind3 [456]
                           ind2>ind1>ind3 so ind2 will gain the place) in case of equally adapted individuals in the same 
place, after checking apply the same condition as in continent (with winner based on best competitive ability)
a new attribute of plant (niche_width) is defined for this but only in individuals that are in islands 

    
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
time_of_adaptation =5 #the adaptation will occur if the time step is multiple of this number
current_time_step = 0
niche_mainland = [1,2,3,4,5,6,7,8,9,10,11,12]
sp_1 = ['sp_1']+ rnd.choices(["A", "T", "C", "G"], k= 100) 
niche_of_sp1 =  rnd.randint(1,10)
niche_sp_1 =  list(range(niche_of_sp1, niche_of_sp1+3))

sp_2 = ['sp_2']+ rnd.choices(["A", "T", "C", "G"], k= 100) 
niche_of_sp2 =  rnd.randint(1,10)
niche_sp_2 =  list(range(niche_of_sp2, niche_of_sp2+3))

species_list = [sp_1, sp_2]

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
    def __init__(self, x, y, drawing, specie):
        self.x = x
        self.y = y
        self.drawing = drawing
        self.age = 0
        self.pos = [x,y]
        self.disp_cap = rnd.randint(2,19) #for now random, after we can define diferent species based on this
        self.specie = specie
        if specie == "sp_1": 
            self.color = 'forestgreen'
            self.niche = niche_sp_1
        if specie == "sp_2": 
            self.color = 'blue'
            self.niche = niche_sp_2
        self.comp_ab = rnd.random()
        

def create_plant(x, y,initial_color):
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

def niche(mainland_island):
    '''
  this will create other matrix that contains the values of the niche of all
  the landscape. the niche is simply a list of numbers from 0 to 10 (for now)
  the mainland contains all the niches (from 1 to 12). island will contain a subset 
  of this niche. a list of lists with 2 or 2 subsets of the mainland. a species 
  will have a "species niche" that is simply a list of 3 numbers (ascending order,
  e.g [1 2 3]) if at least one of the numbers of the species niche is in the sequence 
  of the island niche, then the specie can live there, otherwise, it cant  '''    

    en_niche = np.zeros(mainland_island.shape)
# Transform it into a list so you can replace the elements
    en_niche = [[[item] for item in row] for row in en_niche] # need to transform it in lists because its 
    niche_of_island =  rnd.randint(1,9)  #we need to define this now because if now it will produce 
#one each time (in every coordinate of the island and we want the same )
    for i in range(len(en_niche)):
    
        for j in range(len(en_niche)): 
            if mainland_island[i][j] == 1:
                en_niche[i][j] = niche_mainland #complete niches only 4 availables
            if mainland_island[i][j] == 2:            
                en_niche[i][j] = list(range(niche_of_island, niche_of_island+4)) # i am thinking of 
  #larger than the niche i am thinking for species (len = 3)
    return en_niche
            
environmental_niche = niche(mainland_island)   

def adapt(environmental_niche, plant_niche):
    '''
    this function takes the environmental_nichevironmenvironmental_nichetal niche and the niche of each plant_nicheividual
    and shift the niche of the plant_nicheividual to be more simmilar to the niche of the
    environmental_nichevironmenvironmental_nichet, i.e. adapts plant_nicheividuals to the environmental_nichevironmenvironmental_nichet. this function does 
    not work if the niche of the plant_nicheividual is totally inside in the environmental_nichevironmenvironmental_nichetal
    niche. plant_nicheividuals do not adapt to mainlands (because there is a total coincidenvironmental_nichece)
    '''
   
   # if set(environmental_niche) & set(plant_niche): #not empty, check overlap 
    ## 23 11 FIX THIS SO IT CAN ADAPT TO THE ISLAND!!! 
    
    niche_over = list(set(environmental_niche) & set(plant_niche))
    
    
    #width_niche = len(niche_over)        
    #if len(niche_over) > 0 and niche_over[-1] in environmental_niche[0:3]:#we need to know if the niche of the plant_nicheividual is at the left or at 
    #the right so  if this condition is true, and taking into account that at least for now the 
    #lenvironmental_niche(niche) is 3, thenvironmental_niche the niche of the plant_nicheividual will be at the left*
    #and we need to know that to know if we need to subtracr (shit to left) or add 
    #shift to right, this will solve the problem of superposition WE NEED TO ADD THAT CONDI OF OVER >0 
    #BECAUSE WE STILL DONT PUT THE CONDITION OF THE OVERLAPING BETWEEN PLANT AND NICHE TO STABLISH
    #modification for if the niche of the plant is larger than 3
    if len(niche_over) > 0 and niche_over[-1] in environmental_niche[0:len(plant.niche)]:
    
        if not (all(elemenvironmental_nichet in plant_niche for elemenvironmental_nichet in environmental_niche)): 
            plant_niche = [i+1 for i in plant_niche]
                     
    else: # *else will be at the right of the environmental_nichevironmenvironmental_nichet
         if not (all(elemenvironmental_nichet in plant_niche for elemenvironmental_nichet in environmental_niche)): 
            plant_niche = [i-1 for i in plant_niche]
    return plant_niche

def dispersal(indiv):
       
 #I will use the gaussian for dispersal because its simple and commonly used in dispersal 
 #studies 
    dispersal_x = np.random.normal(indiv.disp_cap, 1) #standar derivation common 1 
    dispersal_y = np.random.normal(indiv.disp_cap, 1)    
    #a chunck so the seed can be dispersed also to left and down
    direction = rnd.choice([-1, 1])
    dx = dispersal_x*direction
    direction = rnd.choice([-1, 1])
    dy = dispersal_y*direction    
    x_new = int((indiv.x + dx) % nrow) #%nrow module to wrap up the world 
    y_new = int((indiv.y + dy) % ncol) #%nrow module to wrap up the world 

    if mainland_island[int(y_new), int(x_new)] != 0:
        canvas.coords(indiv.drawing, (x_new - 0.5) * visual.zoom, (y_new - 0.5) * visual.zoom,
                      (x_new + 0.5) * visual.zoom, (y_new + 0.5) * visual.zoom)
        indiv.x = x_new
        indiv.y = y_new       

        return ([indiv.x, indiv.y])
    else: 
        pass

visual = Visual(ncol, nrow)
canvas = visual.canvas
population = []

# Create individuals only on the mainland
for _ in range(50):
    for specie in species_list: 
        x = int(rnd.uniform(0, main)) #discrete mov
        y = int(rnd.uniform(0, nrow)) #discrete mov
        drawing = create_plant(x, y, initial_color='red')       
        specie = species_list[species_list.index(specie)][0]
        plant = Plant(x, y, drawing, specie)
        
        population.append(plant)

def update():
    global current_time_step
    global population  # Declare population as a global variable
    neighbors = population[:]
    plants_to_remove = []    
        #offspring 
    pop_nei = population[:] #we made this list to find neighbors of plants

    for x in range(len(population)): 
        plant_obj = population[x]
        if plant_obj.age > 1:  
            wo_pl_ob = [x for x in pop_nei if x != plant_obj]
            
            for plant_com in wo_pl_ob:
                if plant_com.specie == plant_obj.specie:
                    
                    pos1 = plant_obj.pos
                       
                    pos2 = plant_com.pos
                    
                    vx = pos1[0]
                    vy = pos1[1]
                    nx = pos2[0]
                    ny = pos2[1]
                    if vx == nx-1 and vy == ny-1 or vx == nx-1 and vy ==ny or vx == nx-1 and vy == ny+1 \
                    or vx == nx and vy == ny-1 or vx == nx and vy == ny+1 or vx == nx +1 and vy == ny-1 \
                    or vx == nx+1 and vy == ny   or vx == nx+1 and vy == ny+1 :
                        #parents can produce more than 1 seed
                        num_offspring = rnd.randint(1,4) #now the plant could produce more than 1 seed/ offspring, randomly 
                        for seed in range(num_offspring):
                        
                            parent_disp = rnd.choice([plant_obj,plant_com])
                            position = dispersal(parent_disp) #for now its that parent
                            if position != None: #this means, the seed did not end on the sea
                                x_off = position[0]
                                y_off =position[1]                            
                            
                            #position_off = dispersal(parent_pos)
                            
                            #if mainland_island[int(y_off), int(x_off)] != 0: #we already have that condition inside dispersal function
                            
                                drawing_off = create_plant(x_off, y_off, plant_obj.color)
                                offspring = Plant(x_off, y_off, drawing_off, plant_obj.specie)
                                parent_disp_cap =rnd.choice([plant_obj, plant_com]) #for now we chose one at random, after we can think on codominance
                                offspring.disp_cap = parent_disp_cap.disp_cap
                                if current_time_step%time_of_adaptation: #only adapt (shift its niche one place) each 100 time steps 
                                    if mainland_island[offspring.x][offspring.y] >1: #23 11 23 correction so occurs in future islands #== 2: #adaptation occur in islands
                                        offspring.niche = adapt(environmental_niche[offspring.x][offspring.y],offspring.niche)
                                population.append(offspring)     
                          
            pop_nei.remove(plant_obj)  
            
        #plants die after 1 years
    for plant in population:
        if plant.age >= 3:
            canvas.delete(plant.drawing)
            plants_to_remove.append(plant)     
            
     
    #to kill of the islands all the plants that dont have a compatible niche
    for plant in population: 
        if mainland_island[plant.x][plant.y] > 1:  # Only consider islands #this is in the case we build multiple islands in the future
            if not set(environmental_niche[plant.x][plant.y]) & set(plant.niche):
                canvas.delete(plant.drawing)
                plants_to_remove.append(plant)
            
            
# This forms a list with all the plants in the same place (lists called same_place)
    for plant_1 in population: 
        same_place = []
        comp_ab_values = []  # Make a list for later
       # winner = None  # Initialize winner

        same_place.append(plant_1)
        rest = [x for x in population if x != plant_1]
    
        for plant_2 in rest: 
            if plant_1.pos == plant_2.pos:
                same_place.append(plant_2)
            
                # To here ok, now we need to pick the one in that list who has better competitive ability
        if len(same_place) > 1: # Step 1: Make a list with all the values of competitive ability of the plants in that position  
        #####FIRST WE WILL CHECK BEST ADAPTED !!!!! NEWWW
           
            #adaptation.append()
    #BEST ADAPTED FIRST IN ISLANDS BECAUSE ITS SUPPOSE THAT ALL EQUALLY ADAPTED TO MAINLAND. 
            if mainland_island[same_place[0].x][same_place[0].y] > 1: #to check if individuals are in islands
                winner = []
                best_adapted = []
                for veg in same_place:    
                    niche_width = len(set(environmental_niche[veg.x][veg.y]) & set(veg.niche))        
                    veg.niche_width = niche_width
                
                max_niche_width = max(same_place, key=lambda x: x.niche_width) #this magical thing let you choose from which attribute you want the maximum
                #in our case is niche_width
                for iv in same_place: 
                    
                    if iv.niche_width == max_niche_width.niche_width: 
                        best_adapted.append(iv)
                if len(best_adapted) ==1: 
                    winnner = best_adapted[0]
                    losers = [x for x in same_place if x !=winner]
                    
                else: #if there is multiple individuals best adapted. Ww apply the other criteria of best competitive ability 
                    rnd.shuffle(same_place) #just in case, so we don't give advantages
                    
                    while len(winner) < 1: #process continue until there is a winner
                        for competitor in same_place:  #we try every plant in the space
                            chances_of_win = rnd.random() #and compare the value with a random number who gets reassigned each time, 
                            #for me this is more fair
                            if chances_of_win < competitor.comp_ab: #check chances
                                winner.append(competitor) # we win a competitor!
                            losers = [x for x in same_place if x !=winner]
                    for los in losers: 
                        plants_to_remove.append(los)       
                        
                    
                    
                for los in losers: 
                    plants_to_remove.append(los) 
                    
                    
            
           
            else: # selection of best competitor in island
            
        
        
        
                winner = [] #where the winner will be 
                rnd.shuffle(same_place) #just in case, so we don't give advantages
                
                while len(winner) < 1: #process continue until there is a winner
                    for competitor in same_place:  #we try every plant in the space
                        chances_of_win = rnd.random() #and compare the value with a random number who gets reassigned each time, 
                        #for me this is more fair
                        if chances_of_win < competitor.comp_ab: #check chances
                            winner.append(competitor) # we win a competitor!
                        losers = [x for x in same_place if x !=winner]
                for los in losers: 
                    plants_to_remove.append(los)    
  
                    
    population = [plant for plant in population if plant not in plants_to_remove]

    for plant in plants_to_remove:
        canvas.delete(plant.drawing)

    for plant in population:
       
        plant.age += 1
     
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


