"""Dynamics of imaginary system

Rules of the fake simulation are as follows:
1) Particles move randomly with uniform distribution in x,y
2) If the distance of the moving particle to another particle is smaller than the 
    THRESHOLD_CHANGE_SORT and there is a type weakness, the particle will change of type
"""
import time
import threading
import numpy as np
from settings import SIZE_BOX, THRESHOLD_CHANGE_SORT, NR_ELEMENTS, SEED, SLEEPTIME_THREAD, MAX_STEP_SIZE

np.random.seed(SEED)

class Dynamics(threading.Thread):
    def __init__(self,particles,queue,stop_event):
        self.min_distance = SIZE_BOX
        self.index_min = 0
        self.change_sort = False

        self.particles = particles
        self.queue = queue
        self.stop_event = stop_event
        
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
                self.min_distance = distance
                if self.weakness(self.particles[index],self.particles[i]):
                    self.change_sort = True                
                else:
                    self.change_sort = False
                        
    def individual_distance(self,part1,part2):
        return np.sqrt((part1._x-part2._x)**2+(part1._y-part2._y)**2)

    def weakness(self,part1,part2):
        # Defines if the sort of part1 is weak to the sort of part2
        return (part1.sort == "r" and part2.sort == "p") or \
            (part1.sort == "p" and part2.sort == "s") or \
            (part1.sort == "s" and part2.sort == "r")
             
    def modify_sort(self,part):
        if part.sort == "r":
            part.sort = "p"
            
        elif part.sort == "p":
            part.sort = "s"
            
        elif part.sort == "s":
            part.sort = "r"
        
    def move_particle(self,part):
        while True:
            dx = MAX_STEP_SIZE*(1-2*np.random.rand())
            new_x = dx+part._x
            if 0 < new_x < SIZE_BOX:          
                part._x = new_x
                break
            
        while True:
            dy = MAX_STEP_SIZE*(1-2*np.random.rand())
            new_y = dy+part._y
            if 0 < new_y < SIZE_BOX:          
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

            index = int(np.floor((NR_ELEMENTS)*np.random.rand()))
            self.get_min_distance(index)
            
            if self.change_sort:
                self.modify_sort(self.particles[index])
            
            self.move_particle(self.particles[index])
            
            self.queue.put(item=(index,self.particles[index]))
    
    def join(self):
        threading.Thread.join(self)
        
    
    
    
    