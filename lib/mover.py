"""Dynamics of imaginary system

Rules of the fake simulation are as follows:
1) Particles of same sort are attracted to each other according to a square law rule
2) Particles of are atracted to stronger sort according to a square law rule
3) Particles of are repelled to weaker sort according to a square law rule
4) On top of that, there is a random movement with uniform distribution in x,y
"""
import time
import numpy as np
import threading
from typing import Tuple
from settings import SIZE_BOX, THRESHOLD_CHANGE_SORT, NR_ELEMENTS, SEED, SLEEPTIME_THREAD

np.random.seed(SEED)

class Dynamics(threading.Thread):
    def __init__(self,particles,queue,stop_event):
        self.min_distance = SIZE_BOX
        self.index_min = 0
        self.particles = particles
        self.queue = queue
        self.stop_event = stop_event
        
        self.cntr=0
        threading.Thread.__init__(self, name="mover_thread")

    def get_min_distance(self, index:int):
        self.min_distance = SIZE_BOX
        self.index_min = index
        self.change_sort = False
        for i in range(len(self.particles)):
            if i == index:
                continue
            distance = self.individual_distance(self.particles[index],self.particles[i])
            
            if self.min_distance > distance and distance > THRESHOLD_CHANGE_SORT:
                if self.weakness(self.particles[index],self.particles[i]):
                    self.change_sort = True                
                else:
                    self.change_sort = False
                        
    def individual_distance(self,part1,part2):
        return np.sqrt((part1._x-part2._x)**2+(part1._y-part2._y)**2)

    def weakness(self,part1,part2):
        # Defines if the sort of part1 is weak to the sort of part2
        if (part1.sort == "r" and part2.sort == "p") or \
            (part1.sort == "p" and part2.sort == "s") or \
            (part1.sort == "s" and part2.sort == "r"):
            return True
        else:
            return False
                
    def modify_sort(self,part):
        if (part.sort == "r"):
            part.sort = "p"
            
        elif (part.sort == "p"):
            part.sort = "s"
            
        elif (part.sort == "s"):
            part.sort = "r"
        
    def move_particle(self,part):
        while True:
            Dx = 1-2*np.random.rand()
            new_x = Dx+part._x
            if new_x > 0 and new_x < SIZE_BOX:          
                part._x = new_x
                break
            
        while True:
            Dy = 1-2*np.random.rand()
            new_y = Dy+part._y
            if new_y > 0 and new_y < SIZE_BOX:          
                part._y = new_y
                break
    
    def run(self):
        #select random particle by its index
        #calculate distances 
        # see if sort is changed
        #move particle
        #send index and particle object to queue
        while not self.stop_event.is_set():
            time.sleep(SLEEPTIME_THREAD)
            self.cntr=self.cntr+1
            index = int(np.floor((NR_ELEMENTS)*np.random.rand()))
            self.get_min_distance(index)
            
            if self.change_sort:
                self.modify_sort(self.particles[index])
            
            self.move_particle(self.particles[index])
            
            self.queue.put((index,self.particles[index]))
    
    def join(self):
        threading.Thread.join(self)
        
    
    
    
    