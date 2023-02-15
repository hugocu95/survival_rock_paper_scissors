""" Class rock-paper-scizors
"""

import numpy as np
from typing import Tuple
from settings import SIZE_BOX

class RPS():
    def __init__(self,position:Tuple=None,sort:str=None):        
        self.position = position
        # Select sort (rock paper or scissor)
        self.sort = sort   
    
    @property
    def position(self):
        return self._x, self._y
    
    @position.setter
    def position(self,vals):
        try: 
            x,y = vals 
        except TypeError:
            self._x = SIZE_BOX*np.random.rand()
            self._y = SIZE_BOX*np.random.rand()
        else:
            self._x = x
            self._y = y
    
    @position.deleter
    def position(self):
        print("Deleting position")
        del self._x
        del self._y
            
    @property 
    def sort(self):
        return self._sort
        
    @sort.setter
    def sort(self,val):
        if val is None:
            rnd = np.random.rand()
            if rnd<0.33:
                val1 = "r"
            elif rnd>0.33 and rnd<0.66:
                val1 = "p"
            else:
                val1 = "s"
            self._sort = val1
        elif val in ["r","p","s"]:
            self._sort = val
        else:
            raise ValueError("Value must be one of the following: r, p or s")
        
    @sort.deleter
    def sort(self):
        del self._sort
