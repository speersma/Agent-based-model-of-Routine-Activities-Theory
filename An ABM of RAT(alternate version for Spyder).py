#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 19:49:53 2022

@author: markspeers
"""

#%% import commands 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
import time
from IPython.display import display, clear_output


#%% Functions
# define size of city, number of citizens in it, number of offenders within number of citizens, 
#and number of capable guardians

def make_city_v2(rows, columns, number_citizens, number_offenders, number_guardians):
    # create city_array of designated size full of zeros
    city = np.zeros((rows, columns))
    
    # define percentage of city that is filled with citizens
    citizen_percent = number_citizens/city.size
    
    # define percentage of citizens that are offenders
    offender_percent = number_offenders/number_citizens
    
    # define percentage of citizens that are capable guardians
    guardian_percent = number_guardians/number_citizens
    
# CITIZEN ASSIGNMENT LOOP 

    # loop through each row
    for i in range(city.shape[0]):
    
        # loop through each column
        for j in range(city.shape[1]):
            
            # assign current index to random value b/w 0 and 1
            city[i,j] = np.random.uniform(0,1)
            
            # if the assigned value is <= % of city that is filled with citizens, assign 1 (citizen)
            if city[i,j] <= citizen_percent:
                city[i,j] = 1 
            
            # else assign 0 (empty space)
            else:
                city[i,j] = 0 
    
# OFFENDER ASSIGNMENT LOOP 
    
    # loop through each row
    for i in range(city.shape[0]):
        
        # loop through each column
        for j in range(city.shape[1]):
            
            # if the value at index [i,j] is 1: (if there is a citizen in the cell)
            if city[i,j] == 1:
            
                # set index[i,j] = np.random.uniform(0,1) (randomizing cell value)
                city[i,j] = np.random.uniform(0,1)
            
                # if index[i,j] <= percentage of citizens that are offenders: 
                if city[i,j] <= offender_percent:
            
                    # index[i,j] = 2 (assigning the value cell as an offender)
                    city[i,j] = 2
            
                # else:
                    # index[i,j] = 1 (leaving as citizen)
                else:
                    city[i,j] = 1
            
            # else:
                # pass - we leave the 0 as a 0 
            else:
                pass
                    
# CAPABLE GUARDIAN ASSIGNMENT LOOP
    
    # loop through each row 
    for i in range(city.shape[0]):
        
        # loop through each column 
        for j in range(city.shape[1]):
            
            # if the value at index [i,j] is 1: (if there is a citizen in the cell)
            if city[i,j] == 1:
                
                # use np.random.uniform(0,1) to assign a new cell value
                city[i,j] = np.random.uniform(0,1)
                
                # if the new cell value is <= the percentage of capable guardians 
                if city[i,j] <= guardian_percent:
                    # assign a cell value of 3 (capable guardian) 
                    city[i,j] = 3
                    
                # else:
                    # assign a cell value of 1 (citizen) 
                else:
                    city[i,j] = 1
                    
            # if the original cell value is not 1, then leave as is
                # pass
            else:
                pass
            
    # return city
    return city


### FUNCTION TO PLOT 
def cityplot(cityarray):
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111)
    ax.set_title('City Plot')
    plt.imshow(cityarray, cmap = 'Accent')
    
    
## FUNCTION TO PLOT ROBBERY RECORD ARRAY
def heatmapplot(robbery_record_array):
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111)
    ax.set_title("Robbery Heat Map")
    plt.imshow(robbery_record_array, cmap = "Reds")
    

## FUNCTINO TO CHECK IF POINT IS WITHIN BOUNDS OF ARRAY
def onBoard(i,j,image):
    if i <= image.shape[0]-1 and i >= 0 and j <= image.shape[1]-1 and j >= 0:
        return True
    else:
        return False
    


## FIXED SIZE SUBSET FUNCTION TO PULL NEIGHBOR VALUES OUT OF ARRAY
def fixed_size_subset(a, x, y, size):
    '''
    Gets a subset of 2D array given a x and y coordinates
    and an output size. If the slices exceed the bounds 
    of the input array, the non overlapping values
    are filled with NaNs
    ----
    a: np.array
        2D array from which to take a subset
    x, y: int. Coordinates of the center of the subset
    size: int. Size of the output array
    ----       
    Returns:
        np.array
        Subset of the input array
    '''
    o, r = np.divmod(size, 2)
    l = (x-(o+r-1)).clip(0)
    u = (y-(o+r-1)).clip(0)
    a_ = a[l: x+o+1, u:y+o+1]
    out = np.full((size, size), np.nan, dtype=a.dtype)
    out[:a_.shape[0], :a_.shape[1]] = a_
    return out


robbery_record = np.arange(0,10, dtype=int)
## FUNCTION TO MOVE OFFENDERS ----
def advance_city_v2(city, previous_city):
    
    # defining new city
    new_city = city.copy()
    
    # defining city_copy to use as neighbor check and later as previous_city
    city_copy = city.copy()

    for i in range(city.shape[0]):
        for j in range(city.shape[1]):

            # if cell in city is empty space:
                # it stays empty in new_city
            if city[i,j] == 0:
                new_city[i,j] = 0

            # if cell in city is a citizen 
                # it stays a citizen in new_city and doesn't move (booooo)
            elif city[i,j] == 1:
                new_city[i,j] = 1

            # if cell in city is capable guardian
                # it stays a guardian in new_city and doesn't move (boooo)
            elif city[i,j] == 3:
                new_city[i,j] = 3

            # if cell in city is the location of a new offender, then do not alter it
            elif city[i,j] == 4:
                continue

                # if cell in city is offender 
            elif city[i,j] == 2:

                ##-- FINDING NEW POINT FOR OFFENDER TO MOVE TO --##

                found_point = False
                while found_point == False:

                    # select distance (6-8 cells) to be travelled 
                    distance = np.random.randint(6,9) 

                    # select direction to travel (north = 1, east = 2, south = 3, west = 4)
                    direction = np.random.randint(1,5)

                    # identify new_point based on distance and direction
                    if direction == 1: # if new direction is north 
                        #new_point = city[i-distance,j]
                        new_point_i = i - distance
                        new_point_j = j
                        if onBoard(new_point_i, new_point_j, city) == True and city[new_point_i, new_point_j] != 2 and city[new_point_i, new_point_j] != 4 and city[new_point_i, new_point_j] !=3:
                            found_point = True
                            #print(new_point_i, new_point_j)
                            new_city[new_point_i, new_point_j] = 2
                            city[new_point_i, new_point_j] = 4

                    elif direction == 2: # if new direction is east
                        #new_point = city[i,j+distance]
                        new_point_i = i
                        new_point_j = j + distance
                        if onBoard(new_point_i, new_point_j, city) == True and city[new_point_i, new_point_j] != 2 and city[new_point_i, new_point_j] != 4 and city[new_point_i, new_point_j] !=3:
                            found_point = True
                            #print(new_point_i, new_point_j)
                            new_city[new_point_i, new_point_j] = 2
                            city[new_point_i, new_point_j] = 4

                    elif direction == 3: # if direction is south 
                        #new_point = city[i+distance,j]
                        new_point_i = i + distance
                        new_point_j = j
                        if onBoard(new_point_i, new_point_j, city) == True and city[new_point_i, new_point_j] != 2 and city[new_point_i, new_point_j] != 4 and city[new_point_i, new_point_j] !=3:
                            found_point = True
                            #print(new_point_i, new_point_j)
                            new_city[new_point_i, new_point_j] = 2
                            city[new_point_i, new_point_j] = 4

                    elif direction == 4: # if direction is west 
                        #new_point = city[i,j-distance]
                        new_point_i = i
                        new_point_j = j - distance
                        if onBoard(new_point_i, new_point_j, city) == True and city[new_point_i, new_point_j] != 2 and city[new_point_i, new_point_j] != 4 and city[new_point_i, new_point_j] !=3:
                            found_point = True
                            #print(new_point_i, new_point_j)
                            new_city[new_point_i, new_point_j] = 2
                            city[new_point_i, new_point_j] = 4

                ##-- FILLING IN OFFENDER'S OLD LOCATION WITH PREVIOUS_CITY VALUE --## 

                ###-- checking value of offender's old location in previous_city --###

                # if value of offender's old location in previous_city was empty
                    # set the cell's value in new_city to empty
                if previous_city[i,j] == 0:
                    new_city[i,j] = 0

                # if value of offender's old location in previous_city was citizen
                    # set the cell's value in new_city to a citizen
                if previous_city[i,j] == 1:
                    new_city[i,j] = 1

                # if value of offender's old location in previous_city was capable guardian
                    # set the cell's value in new_city to a capable guardian
                    #  I DON'T THINK THIS IS NECESSARY ANYMORE BECAUSE OFFENDERS AREN'T ABLE TO MOVE ONTO A SPACE THAT ==3
                if previous_city[i,j] == 3:
                    new_city[i,j] = 3

                # if value of offender's location in previous_city was offender
                    # set the value in new_city to empty 
                if previous_city[i,j] == 2:
                    new_city[i,j] = 0


                ##-- CHECKING IF OFFENDER IS ON SAME CELL AS CITIZEN --##

                # if offender's new location had a citizen on it in city:
                    # check neighbor values of that offender's new_point index in city 
                if city_copy[new_point_i, new_point_j] == 1:

                    ##-- CHECKING THE NEIGHBORS FOR A CAPABLE GUARDIAN --##

                    # if there is a capable guardian in the neighborhood values of city[new_point]:
                    if 3 in fixed_size_subset(city_copy, new_point_i, new_point_j, 15):

                        # no robbery is recorded 

                        # set the cell's value in new_city = to offender (2)
                        new_city[new_point_i, new_point_j] = 2

                    # if there is NOT a capable guardian in the neighborhood values:
                    elif 3 not in fixed_size_subset(city_copy, new_point_i, new_point_j, 15):

                        # set the cell at robbery_record[i,j] += 1 
                        robbery_record[new_point_i, new_point_j] += 1

                        # set the cell's value in new_city = to offender (2) 
                        new_city[new_point_i, new_point_j] = 2

                # if offender's new location did not have a citizen on it:
                    # no robbery is recorded, continue looping through the array
                else:
                    continue

    previous_city = city_copy.copy()
    
    return new_city, previous_city


#%% MODEL 1 - 20,000 PEOPLE, 1800 OFFENDERS, 30 CAPABLE GUARDIANS
# creating city, initial previous_city and robbery_record
city = make_city_v2(200, 200, 20000, 1800, 30)
previous_city = city.copy()
robbery_record = np.zeros_like(city)

fig = plt.figure(figsize=(20,20))

#plotting the original city
cityplot(city)

for i in range(100):
    
    city, previous_city = advance_city_v2(city, previous_city)
    
    cityplot(city)
    time.sleep(0.01)  # 
    clear_output(wait=True)
    display(fig)
    plt.show()
    plt.clf()
    
    
plt.close()

heatmapplot(robbery_record)

robbery_record.sum()
# sum amount of robberies == 70728

#%% MODEL 2 - 20,000 PEOPLE, 1800 OFFENDERS, 60 CAPABLE GUARDIANS
city = make_city_v2(200, 200, 20000, 1800, 60)
previous_city = city.copy()
robbery_record = np.zeros_like(city)

fig = plt.figure(figsize=(20,20))

#plotting the original city
cityplot(city)

for i in range(100):
    
    city, previous_city = advance_city_v2(city, previous_city)
    
    cityplot(city)
    time.sleep(0.01)  # 
    clear_output(wait=True)
    display(fig)
    plt.show()
    plt.clf()
    
    
plt.close()

heatmapplot(robbery_record)

robbery_record.sum()
# sum amount of robberies == 60198


#%% MODEL 3 - (BIRKS ET AL., 2014) - SMALLER CITY 
city = make_city_v2(100, 100, 2500, 225, 5)
previous_city = city.copy()
robbery_record = np.zeros_like(city)

fig = plt.figure(figsize=(20,20))

#plotting the original city
cityplot(city)

for i in range(100):
    
    city, previous_city = advance_city_v2(city, previous_city)
    
    cityplot(city)
    time.sleep(0.01)  # 
    clear_output(wait=True)
    display(fig)
    plt.show()
    plt.clf()
    
    
plt.close()

heatmapplot(robbery_record)

robbery_record.sum()
# sum amount of robberies == 4315



#%% MODEL 4 - (BIRKS ET AL., 2014) - SMALLER CITY - HIGH GUARDIAN PRESENCE
city = make_city_v2(100, 100, 2500, 225, 15)
previous_city = city.copy()
robbery_record = np.zeros_like(city)

fig = plt.figure(figsize=(20,20))

#plotting the original city
cityplot(city)

for i in range(100):
    
    city, previous_city = advance_city_v2(city, previous_city)
    
    cityplot(city)
    time.sleep(0.01)  # 
    clear_output(wait=True)
    display(fig)
    plt.show()
    plt.clf()
    
    
plt.close()

heatmapplot(robbery_record)


robbery_record.sum()
# sum amount of robberies == 4680
